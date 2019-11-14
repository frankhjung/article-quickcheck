#!/usr/bin/env python
# coding: utf-8
"""
Hypothesis test examples.

More examples at

https://www.programcreek.com/python/example/102260/hypothesis.strategies.text

"""

from collections import Counter
from string import ascii_letters, digits

from hypothesis import given, note
from hypothesis.strategies import lists, emails, integers, text, randoms


@given(text(min_size=12, max_size=64, alphabet=ascii_letters + digits))
def test_alphanumeric(a_string):
    """
    Generate alphanumeric sized strings like:
        'LbkNCS4xl2XlEtu'
        'z3M4jc1JxXQokvmUeAr6YpgT'
        'vxDKNjBPHzxqD7egsD'
    """
    assert a_string.isalnum()
    a_length = len(a_string)
    assert a_length >= 12 and a_length <= 64


@given(lists(emails(), min_size=1, max_size=10))
def test_email(email_list):
    """
    Email addresses as per RFC 5322, section-3.4.1
    """
    assert all(x.count('@') == 1 for x in email_list)


@given(lists(integers()), randoms())
def test_shuffle_is_noop(a_list, _random):
    """
    Show intermediate steps in test using `note`.
    """
    b_list = list(a_list)
    _random.shuffle(b_list)
    note("Shuffle: %r" % (b_list))
    assert a_list == b_list


@given(lists(integers()))
def test_sorting_list_of_integers(int_list):
    """
    Test sorting a list of integers.
    """
    sorted_list = sorted(int_list)
    assert isinstance(sorted_list, list)
    assert Counter(sorted_list) == Counter(int_list)
    assert all(x <= y for x, y in zip(sorted_list, sorted_list[1:]))
