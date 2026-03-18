import streamlit as st
import requests
from datetime import datetime
import uuid
import json
import os

# Page setup
st.set_page_config(page_title="My AI Chat", layout="wide")

# Load Hugging Face token
try:
    hf_token = st.secrets["HF_TOKEN"]
    if not hf_token:
        raise ValueError("Token is empty")
except (KeyError, ValueError):
    st.error("Hugging Face token not found or empty. Please add HF_TOKEN to .streamlit/secrets.toml")
    st.stop()

# API details
API_URL = "https://router.huggingface.co/v1/chat/completions"
MODEL = "meta-llama/Llama-3.2-1B-Instruct"

# Memory file
MEMORY_FILE = "memory.json"

# Load memory
def load_memory():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

# Save memory
def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

# Extract memory from user message
def extract_memory(user_message):
    prompt = f"Given this user message, extract any personal facts or preferences as a JSON object. If none, return {{}}. Message: {user_message}"
    headers = {"Authorization": f"Bearer {hf_token}"}
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 200
    }
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        extracted = data["choices"][0]["message"]["content"]
        # Try to parse as JSON
        try:
            return json.loads(extracted)
        except:
            return {}
    except:
        return {}

# Chats directory
CHATS_DIR = "chats"
os.makedirs(CHATS_DIR, exist_ok=True)

# Initialize session state
if "chats" not in st.session_state:
    st.session_state.chats = []
if "active_chat_id" not in st.session_state:
    st.session_state.active_chat_id = None
if "memory" not in st.session_state:
    st.session_state.memory = load_memory()

# Function to load chats from files
def load_chats():
    chats = []
    if os.path.exists(CHATS_DIR):
        for filename in os.listdir(CHATS_DIR):
            if filename.endswith(".json"):
                filepath = os.path.join(CHATS_DIR, filename)
                try:
                    with open(filepath, "r") as f:
                        chat = json.load(f)
                        chats.append(chat)
                except:
                    pass  # Skip corrupted files
    return chats

# Function to save chat to file
def save_chat(chat):
    filename = f"{chat['id']}.json"
    filepath = os.path.join(CHATS_DIR, filename)
    with open(filepath, "w") as f:
        json.dump(chat, f, indent=2)

# Function to delete chat file
def delete_chat_file(chat_id):
    filename = f"{chat_id}.json"
    filepath = os.path.join(CHATS_DIR, filename)
    if os.path.exists(filepath):
        os.remove(filepath)

# Load chats on startup
if not st.session_state.chats:
    st.session_state.chats = load_chats()
    if st.session_state.chats:
        st.session_state.active_chat_id = st.session_state.chats[0]["id"]

# Function to create new chat
def create_new_chat():
    chat_id = str(uuid.uuid4())
    chat = {
        "id": chat_id,
        "title": f"Chat {len(st.session_state.chats) + 1}",
        "timestamp": datetime.now().isoformat(),
        "messages": []
    }
    st.session_state.chats.append(chat)
    st.session_state.active_chat_id = chat_id
    save_chat(chat)
    return chat

# Function to get active chat
def get_active_chat():
    if st.session_state.active_chat_id:
        for chat in st.session_state.chats:
            if chat["id"] == st.session_state.active_chat_id:
                return chat
    return None

# Function to update chat title based on first message
def update_chat_title(chat):
    if chat["messages"]:
        first_user_msg = next((msg["content"] for msg in chat["messages"] if msg["role"] == "user"), "")
        chat["title"] = first_user_msg[:20] + "..." if len(first_user_msg) > 20 else first_user_msg or f"Chat {len(st.session_state.chats)}"
        save_chat(chat)

# Function to delete chat
def delete_chat(chat_id):
    st.session_state.chats = [c for c in st.session_state.chats if c["id"] != chat_id]
    delete_chat_file(chat_id)
    if st.session_state.active_chat_id == chat_id:
        if st.session_state.chats:
            st.session_state.active_chat_id = st.session_state.chats[-1]["id"]
        else:
            st.session_state.active_chat_id = None

# Sidebar
with st.sidebar:
    st.title("Chats")
    
    if st.button("New Chat"):
        create_new_chat()
        st.rerun()
    
    for chat in st.session_state.chats:
        col1, col2 = st.columns([4, 1])
        is_active = chat["id"] == st.session_state.active_chat_id
        with col1:
            if st.button(chat["title"], key=f"select_{chat['id']}", use_container_width=True, type="primary" if is_active else "secondary"):
                st.session_state.active_chat_id = chat["id"]
                st.rerun()
        with col2:
            if st.button("✕", key=f"delete_{chat['id']}"):
                delete_chat(chat["id"])
                st.rerun()
    
    # User Memory
    with st.expander("User Memory"):
        st.json(st.session_state.memory)
        if st.button("Clear Memory"):
            st.session_state.memory = {}
            save_memory({})
            st.rerun()

# Main area
active_chat = get_active_chat()
if active_chat:
    # Display chat history
    for message in active_chat["messages"]:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Type your message..."):
        # Add user message
        active_chat["messages"].append({"role": "user", "content": prompt})
        
        # Update title if first message
        if len(active_chat["messages"]) == 1:
            update_chat_title(active_chat)
        
        # Extract memory from user message
        extracted = extract_memory(prompt)
        if extracted:
            st.session_state.memory.update(extracted)
            save_memory(st.session_state.memory)
        
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)
        
        # Prepare messages for API with memory
        system_prompt = f"User preferences: {json.dumps(st.session_state.memory)}" if st.session_state.memory else ""
        api_messages = [{"role": "system", "content": system_prompt}] if system_prompt else []
        api_messages += [{"role": msg["role"], "content": msg["content"]} for msg in active_chat["messages"]]
        
        # Send to API
        headers = {"Authorization": f"Bearer {hf_token}"}
        payload = {
            "model": MODEL,
            "messages": api_messages,
            "max_tokens": 512,
            "stream": True
        }
        
        try:
            response = requests.post(API_URL, headers=headers, json=payload, stream=True)
            response.raise_for_status()
            
            # Stream the response
            ai_response = ""
            placeholder = st.empty()
            with st.chat_message("assistant"):
                for line in response.iter_lines():
                    if line:
                        line = line.decode('utf-8')
                        if line.startswith('data: '):
                            data = line[6:]
                            if data == '[DONE]':
                                break
                            try:
                                import time
                                chunk = json.loads(data)
                                if 'choices' in chunk and chunk['choices']:
                                    delta = chunk['choices'][0].get('delta', {})
                                    if 'content' in delta:
                                        ai_response += delta['content']
                                        placeholder.write(ai_response)
                                        time.sleep(0.05)  # Small delay for visibility
                            except json.JSONDecodeError:
                                continue
            
            # Add AI response to chat
            active_chat["messages"].append({"role": "assistant", "content": ai_response})
            
            # Save chat
            save_chat(active_chat)
                
        except requests.exceptions.RequestException as e:
            st.error(f"API Error: {str(e)}")
        except KeyError:
            st.error("Unexpected API response format")
else:
    st.write("No active chat. Create a new chat from the sidebar.")

