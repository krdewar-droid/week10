Task: Week 10 – Task 1A Page Setup & API Connection

Prompt: "Help me implement Part A of the Week 10 assignment. The Streamlit app should use st.set_page_config(page_title='My AI Chat', layout='wide'), load the Hugging Face token from st.secrets['HF_TOKEN'], send a test message like 'Hello!' to the Hugging Face chat completions API using the model meta-llama/Llama-3.2-1B-Instruct, display the response in the main area, and show a clear error message if the token is missing or if the API request fails."

AI Suggestion:
The AI suggested adding the Streamlit page configuration, loading the Hugging Face token securely using st.secrets, sending a test request to the Hugging Face API with a hardcoded message, displaying the model response in the app, and handling missing tokens or API errors with clear user-visible messages.

My Modifications & Reflections:
I used the suggested structure for the API request and token loading. I ran the app with streamlit run app.py and verified that the AI response appears when the token is present and that a clear error message appears if the token is missing.




Task: Week 10 – Task 1B Multi-Turn Conversation UI

Prompt: "Extend my Streamlit chat app to support a multi-turn conversation. Replace the hardcoded test message with a real chat interface using st.chat_message and st.chat_input. Store the conversation history in st.session_state and send the full message history to the Hugging Face API so the model keeps context."

AI Suggestion:
The AI suggested implementing Streamlit’s native chat UI using st.chat_message to display messages and st.chat_input for user input. It recommended storing the full conversation history in st.session_state.messages and sending the entire message list with each API request so the model maintains context between messages.

My Modifications & Reflections:
I followed the suggested approach and tested the app with streamlit run app.py. I verified that multiple messages can be sent, previous messages remain visible, and the model responds with context-aware replies (e.g., remembering earlier information).



Task: Week 10 – Task 1C Chat Management

Prompt: "Extend my Streamlit chat app to support chat management. Add a sidebar with a New Chat button, show a list of chats with titles and timestamps, allow switching between chats without losing history, highlight the active chat, and add a delete (✕) button to remove chats."

AI Suggestion:
The AI suggested using st.sidebar to create a chat navigation panel, storing multiple chats in st.session_state, displaying each chat with a title and timestamp, highlighting the active chat, enabling switching between chats, and adding a delete button that removes the selected chat and updates the active state.

My Modifications & Reflections:
I implemented the sidebar chat system and tested it with streamlit run app.py. I verified that I can create multiple chats, switch between them without losing messages, and delete chats correctly with the active chat updating as expected.




Task: Week 10 – Task 1D Chat Persistence

Prompt: "Extend my Streamlit chat app so that each chat is saved as a JSON file in a chats/ directory. The file should include a chat ID, title or timestamp, and full message history. The app should load all chats from the folder on startup, allow continuing conversations, and delete the JSON file when a chat is removed."

AI Suggestion:
The AI suggested saving each chat as a separate JSON file inside the chats folder containing the chat ID, title, timestamp, and message history. It recommended automatically loading these files when the app starts, updating the files after each message, generating titles from the first user message, and deleting the file when the chat is removed.

My Modifications & Reflections:
I implemented the JSON storage and loading logic and tested the app with streamlit run app.py. I verified that chats remain in the sidebar after restarting the app, conversations can continue normally, and deleting a chat also removes its JSON file.




Task: Week 10 – Task 2 Response Streaming

Prompt: "Modify my Streamlit chat app so that the Hugging Face API response streams token-by-token instead of waiting for the full response. Use stream=True in the API request, parse the server-sent event stream, and display the output incrementally in the UI."

AI Suggestion:
The AI suggested enabling streaming by adding stream=True to the request and handling the server-sent event format returned by the Hugging Face API. It recommended updating the response display incrementally using a Streamlit placeholder (such as st.empty()) and optionally adding a small delay so the streaming effect is visible.

My Modifications & Reflections:
I implemented streaming and tested the app using streamlit run app.py. I verified that the assistant response appears progressively in the chat interface and that the final full response is saved correctly to the conversation history.




Task: Week 10 – Task 3 User Memory

Prompt: "Add a user memory system to my Streamlit chat app. After each assistant response, make a second API call that extracts any personal traits or preferences from the user message and store them in memory.json. Display the stored memory in a sidebar panel and use it to personalize future responses."

AI Suggestion:
The AI suggested making a second API call after each message to extract personal information from the user text and return it as JSON. It recommended storing this information in memory.json, displaying it in a sidebar expander, adding a button to clear/reset memory, and including the stored memory as a system prompt in future API requests so responses can be personalized.

My Modifications & Reflections:
I implemented the memory extraction and storage system and tested the app using streamlit run app.py. I verified that personal details mentioned in messages are saved to memory.json, appear in the sidebar panel, persist after restarting the app, and influence future responses from the model.
