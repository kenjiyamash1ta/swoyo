import argparse
import re


def is_russian_phone_number(phone: str) -> bool:
    """
    Проверяет, является ли номер российским.
    Российские номера начинаются с +7 или 8 и имеют 10 цифр после этого.
    """
    pattern = r"^(\+7|8)\d{10}$"
    return re.match(pattern, phone) is not None


def parse() -> tuple[str, str, str]:
    argparser = argparse.ArgumentParser(description="Send SMS")
    argparser.add_argument(
        "-s",
        type=str,
        required=True,
        help="Sender num (Russian phone number)"
    )
    argparser.add_argument(
        "-r",
        type=str,
        required=True,
        help="Recipient num (Russian phone number)"
    )
    argparser.add_argument(
        "-m",
        type=str,
        required=True,
        help="Text SMS (max 500 chars)"
    )
    args = argparser.parse_args()

    if not is_russian_phone_number(args.s):
        raise ValueError("Номер отправителя должен быть российским")
    if not is_russian_phone_number(args.r):
        raise ValueError("Номер получателя должен быть российским")

    if len(args.m) > 500:
        raise ValueError(
            "Сообщение слишком длинное. Максимальная длина: 500 символов."
        )

    return (args.s, args.r, args.m)
