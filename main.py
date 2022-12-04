import os
from dotenv import load_dotenv
from chatgpt_tool.chat_session import ChatSession

def main():
    load_dotenv()
    access_token = os.getenv("access_token")
    initial_prompt = os.getenv("initial_prompt")

    chat_session = ChatSession(access_token, initial_prompt)
    chat_session.start()


if __name__ == "__main__":
    main()
