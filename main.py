import os
from dotenv import load_dotenv
from chatgpt_tool.chat_session import ChatSession

def main():
    load_dotenv()
    session_token = os.getenv("session_token")
    initial_prompt = os.getenv("initial_prompt")

    chat_session = ChatSession(session_token, initial_prompt)
    chat_session.start()


if __name__ == "__main__":
    main()
