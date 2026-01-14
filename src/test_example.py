#!/usr/bin/env python
"""
Hypothesis test examples.

More examples at

https://www.programcreek.com/python/example/102260/hypothesis.strategies.text

"""

from collections import Counter
from random import Random
from string import ascii_letters, digits

import pytest
from hypothesis import given, note
from hypothesis.strategies import (
    emails,
    integers,
    lists,
    randoms,
    text,
)


@given(text(min_size=12, max_size=64, alphabet=ascii_letters + digits))
def test_alphanumeric(alphanumeric_string: str) -> None:
    """Test that generated strings contain only alphanumeric characters.

    Args:
        alphanumeric_string: A randomly generated string of alphanumeric
            characters between 12 and 64 characters in length.

    Examples:
        Generated strings like 'LbkNCS4xl2XlEtu',
        'z3M4jc1JxXQokvmUeAr6YpgT', 'vxDKNjBPHzxqD7egsD'
    """
    assert alphanumeric_string.isalnum()
    string_length = len(alphanumeric_string)
    assert 12 <= string_length <= 64


@given(lists(emails(), min_size=1, max_size=10))
def test_email(email_list: list[str]) -> None:
    """Test that generated email addresses conform to RFC 5322.

    Args:
        email_list: A list of 1 to 10 randomly generated email addresses
            following RFC 5322, section-3.4.1 format.
    """
    assert all(email.count("@") == 1 for email in email_list)


@pytest.mark.xfail(
    reason="Intentional failure to demonstrate hypothesis note usage"
)
@given(lists(integers()), randoms())
def test_shuffle_is_noop(original_list: list[int], random_gen: Random) -> None:
    """Demonstrate test failure with intermediate step logging.

    This test intentionally fails to show how `note` can be used to
    log intermediate values during property-based testing.

    Args:
        original_list: A randomly generated list of integers.
        random_gen: A Random instance for shuffling operations.
    """
    shuffled_list = list(original_list)
    random_gen.shuffle(shuffled_list)
    note(f"Shuffle: {shuffled_list!r}")
    assert original_list == shuffled_list


@given(lists(integers()))
def test_sorting_list_of_integers(int_list: list[int]) -> None:
    """Test that sorting preserves elements and maintains order.

    Verifies three properties of the sorted() function:
    1. Returns a list
    2. Contains same elements as input (no loss or addition)
    3. Elements are in non-decreasing order

    Args:
        int_list: A randomly generated list of integers.
    """
    sorted_list = sorted(int_list)
    assert isinstance(sorted_list, list)
    assert Counter(sorted_list) == Counter(int_list)
    assert all(x <= y for x, y in zip(sorted_list, sorted_list[1:]))
