import os
from dotenv import load_dotenv
from chatgpt_repl.chat_session import ChatSession


def main():
    load_dotenv()
    session_token = os.getenv("session_token")
    initial_prompt = os.getenv("initial_prompt")
    assert session_token is not None
    assert initial_prompt is not None

    session_name = input("Enter session name: ")
    chat_session = ChatSession(session_name, session_token, initial_prompt)
    chat_session.chatbot.refresh_session()
    chat_session.start()


if __name__ == "__main__":
    main()
