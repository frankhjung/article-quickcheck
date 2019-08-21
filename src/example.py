#!/usr/bin/env python
# coding: utf-8
"""
Test examples using
[Hypothesis](https://hypothesis.readthedocs.io/en/latest/).

Activate virtual environment (venv) with:

    pip3 install virtualenv
    python3 -m virtualenv venv
    source venv/bin/activate
    pip3 install -r requirements.txt

Start virtual environment (venv) with:

    source venv/bin/activate

Deactivate with:

    deactivate

Format code with:

    yapf --style google --parallel -i src/example.py
    pylint src/example.py
    pytest -v src/example.py

"""

from collections import Counter

from hypothesis import given
from hypothesis.strategies import lists, emails, integers


@given(lists(emails(), min_size=1, max_size=10))
def test_email(email_list):
    """
    Email addresses as per RFC 5322, section-3.4.1
    """
    assert all('@' in x for x in email_list)


@given(lists(integers()))
def test_sorting_list_of_integers(int_list):
    """
    Test sorting a list of integers.
    """
    sorted_list = sorted(int_list)
    assert isinstance(sorted_list, list)
    assert Counter(sorted_list) == Counter(int_list)
    assert all(x <= y for x, y in zip(sorted_list, sorted_list[1:]))
