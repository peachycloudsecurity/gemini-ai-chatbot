import streamlit as ui
import os
import google.generativeai as ai_framework
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
# Configure the AI framework with API key
ai_framework.configure(api_key=os.getenv("GOOGLE_API_KEY"))
security_model=ai_framework.GenerativeModel('gemini-pro')

# Function to map internal roles to UI roles
def map_role_for_ui(internal_role):
  if internal_role == "model":
    return "assistant"
  else:
    return internal_role

# Initialize the chat history in the UI's session state if not present
if "security_chat_history" not in ui.session_state:
    ui.session_state.security_chat_history = security_model.start_chat(history = [])

# Set the window title for the security chatbot
ui.title("GCP Cloud Security Assistant!")

# Display existing chat messages
for chat_entry in ui.session_state.security_chat_history.history:
    with ui.chat_message(map_role_for_ui(chat_entry.role)):
        ui.markdown(chat_entry.parts[0].text)

# Custom prompt for GCP Cloud Security inquiries
security_prompt = "Hello! I'm here to help you with GCP Cloud Security. What security concerns do you have?"

# Detailed prompt template for GCP Cloud Security Response 
input_prompt = """
    Provide a comprehensive response based on the input provided below for Google cloud security. Please provide a detailed report and answer the question as detailed as possible from the provided context. 
    If any other questions is added or asked apart from GCP cloud security then say this is beyond my scope !.
    """

# Handle new user messages
if user_input := ui.chat_input(security_prompt):
    # Append the custom prompt to the user's input
    full_input = f"{input_prompt} {user_input}"

    # Show user's last message
    ui.chat_message("user").markdown(user_input)
    
    # Send the combined input to the security model and get a assistant's response
    security_response = ui.session_state.security_chat_history.send_message(full_input)
    with ui.chat_message("assistant"):
        ui.markdown(security_response.text)
