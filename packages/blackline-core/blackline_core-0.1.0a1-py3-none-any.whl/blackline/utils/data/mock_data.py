from datetime import datetime
from typing import List


def user_data() -> List:
    return [
        (
            datetime(2021, 1, 1),
            "Dave",
            "dave@example.com",
            "12345",
            True,
            "127.0.0.1",
        ),
        (
            datetime(2021, 6, 1),
            "Alison",
            "alison@example.com",
            "23456",
            True,
            "127.0.0.2",
        ),
        (
            datetime(2022, 3, 1),
            "Chris",
            "chris@example.com",
            "34567",
            False,
            "127.0.0.3",
        ),
        (
            datetime(2022, 4, 1),
            "Megan",
            "megan@example.com",
            "45678",
            True,
            "127.0.0.4",
        ),
    ]


def user_data_deidentified() -> List:
    return [
        (
            datetime(2022, 4, 1, 0, 0),
            "Megan",
            "megan@example.com",
            "45678",
            True,
            "127.0.0.4",
        ),
        (
            datetime(2022, 3, 1, 0, 0),
            "Chris",
            "chris@example.com",
            "34567",
            False,
            "###.#.#.#",
        ),
        (
            datetime(2021, 1, 1, 0, 0),
            None,
            "fake@email.com",
            "12345",
            True,
            "###.#.#.#",
        ),
        (
            datetime(2021, 6, 1, 0, 0),
            None,
            "fake@email.com",
            "23456",
            True,
            "###.#.#.#",
        ),
    ]
