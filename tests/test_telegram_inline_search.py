from telegram_inline_search import main
import pytest


def test_token_file_notexist():
    with pytest.raises(Exception) as e_info:
        main.load_telegram_bot_token("")
