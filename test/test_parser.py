import pytest
from unittest.mock import patch
import sys
from src.parser import parse

def test_valid_input():
    # Валидные данные
    test_args = ["program_name", "-s", "+79123456789", "-r", "89123456789", "-m", "Hello"]
    with patch.object(sys, "argv", test_args):
        sender, recipient, message = parse()
        assert sender == "+79123456789"
        assert recipient == "89123456789"
        assert message == "Hello"

def test_invalid_sender():
    # Невалидный номер отправителя
    test_args = ["program_name", "-s", "123456789", "-r", "89123456789", "-m", "Hello"]
    with patch.object(sys, "argv", test_args):
        with pytest.raises(ValueError, match="Номер отправителя должен быть российским"):
            parse()

def test_invalid_recipient():
    # Невалидный номер получателя
    test_args = ["program_name", "-s", "+79123456789", "-r", "123456789", "-m", "Hello"]
    with patch.object(sys, "argv", test_args):
        with pytest.raises(ValueError, match="Номер получателя должен быть российским"):
            parse()

def test_message_too_long():
    # Сообщение слишком длинное
    long_message = "A" * 501  
    test_args = ["program_name", "-s", "+79123456789", "-r", "89123456789", "-m", long_message]
    with patch.object(sys, "argv", test_args):
        with pytest.raises(ValueError, match="Сообщение слишком длинное"):
            parse()