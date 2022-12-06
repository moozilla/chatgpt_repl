import pytest
from unittest.mock import MagicMock
from chatgpt_repl.chat_session import ChatSession

mock_session_token = "1234567890"
mock_conversation_id = "1234567890"
mock_parent_id = "1234567890"


@pytest.fixture
def mock_chatbot_message():
    return {
        "message": "test response",
        "conversation_id": mock_conversation_id,
        "parent_id": mock_parent_id,
    }


@pytest.fixture
def mock_chatbot(mock_chatbot_message):
    chatbot_mock = MagicMock()
    chatbot_mock.get_chat_response.return_value = mock_chatbot_message
    chatbot_mock.refresh_session.return_value = None
    return chatbot_mock


@pytest.fixture
def chat_session(mock_chatbot):
    session_name = "pytest"
    initial_prompt = "How are you?"

    chat_session = ChatSession(session_name, mock_session_token, initial_prompt)
    chat_session.chatbot = mock_chatbot
    return chat_session


def test_create_config(chat_session):
    expected_result = {
        "Authorization": "",
        "session_token": mock_session_token,
    }

    result = chat_session.create_config(mock_session_token)
    assert expected_result == result


def test_create_chatbot(chat_session):
    mock_config = {"Authorization": ""}

    chatbot = chat_session.create_chatbot(mock_config, mock_conversation_id)

    assert chatbot.config == mock_config
    assert chatbot.conversation_id == mock_conversation_id


def test_get_chat_response(chat_session, mock_chatbot_message):
    chatbot_mock = chat_session.chatbot

    # Happy path
    result = chat_session.get_chat_response("Test prompt")
    assert mock_chatbot_message == result
    assert chatbot_mock.refresh_session.call_count == 0

    # Simulate an expired token
    chatbot_mock.get_chat_response.return_value = ValueError("Expired token")
    result = chat_session.get_chat_response("Test prompt")
    assert result == None
    assert chatbot_mock.refresh_session.call_count == 1


def test_run_prompt_loop(chat_session):
    # Not sure how to test this method
    pass


def test_start(chat_session, mocker, capsys):
    # Create a mock for run_prompt_loop
    mock_run_prompt_loop = mocker.patch.object(chat_session, "run_prompt_loop")

    # Capture the print output
    chat_session.start()
    captured = capsys.readouterr()

    # Check the print output
    assert (
        captured.out
        == "Sending initial prompt to ChatGPT\n> How are you?\n...\n\ntest response\n\n"
    )

    # Check that run_prompt_loop was called
    mock_run_prompt_loop.assert_called_once()
