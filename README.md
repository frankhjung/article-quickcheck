# Thoughts on Random Number Generators

This is part 2 in the series on Random numbers. The series contains:

1. [Random Number Generators in bash scripts](https://gitlab.com/theMarloGroup/articles/random)
2. [Random Number Generators to test code](https://gitlab.com/theMarloGroup/articles/quickcheck)
3. [Random Number Generators in simulation](https://gitlab.com/theMarloGroup/articles/simulation)


## Render to HTML

To render a HTML or PDF version of this article, run

```bash
make quickcheck.html
make quickcheck.pdf
```

This will generate documents into the `public` directory.

## GitHub

The rendered version is also available online at:

* [GitHub](https://frankhjung.github.io/article-quickcheck/)

See pipeline configuration:

* [.github/workflows/main.yml](.github/workflows/main.yml)

## GitLab

The rendered version is also available online at:

* [GitLab](https://themarlogroup.gitlab.io/articles/quickcheck/)

See pipeline configuration:

* [.gitlab-ci.yml](.gitlab-ci.yml)

## Python Hypothesis Examples

Some examples using [Hypothesis](https://hypothesis.readthedocs.io/en/latest/).

To use strategies try:

```python
from hypothesis.strategies import lists, integers

integers().example()
Out[2]: 8448

lists(integers(), min_size=5, max_size=10).example()
Out[3]: [22, -108, 6137, -15222, -6307496272059922727, -125, -4, -30, 20459]
```

The `example` method should only be used interactively.

### Initialise Virtual Environment and Packages

Activate virtual environment (venv) with:

```bash
pip3 install virtualenv ; python3 -m virtualenv venv
```

Start virtual environment (venv) with:

```bash
source venv/bin/activate
```

Install dependent packages:

```bash
pip3 install -r requirements.txt
```

Deactivate with:

```bash
deactivate
```

### Validate Code

Format and line code:

```bash
yapf --style google --parallel -i src/*.py
pylint src/*.py
```

### Run Test Code

```bash
pytest -v src/test_example.py
```

To get runtime statistics:

```bash
pytest -v --hypothesis-show-statistics src/test_example.py
```

#### Results

We have forced an error, so you can see what it produces.

```text
$ pytest -v --hypothesis-show-statistics src/test_example.py

============================= test session starts ==============================
platform linux -- Python 3.7.5rc1, pytest-5.0.0, py-1.8.0, pluggy-0.13.0 -- /home/frank/documents/articles/quickcheck/venv/bin/python3
cachedir: .pytest_cache
hypothesis profile 'default' -> database=DirectoryBasedExampleDatabase('/home/frank/documents/articles/quickcheck/.hypothesis/examples')
metadata: {'Python': '3.7.5rc1', 'Platform': 'Linux-5.2.0-3-amd64-x86_64-with-debian-bullseye-sid', 'Packages': {'pytest': '5.0.0', 'py': '1.8.0', 'pluggy': '0.13.0'}, 'Plugins': {'hypothesis': '4.40.1', 'metadata': '1.8.0', 'cov': '2.7.1', 'html': '1.21.1'}, 'JAVA_HOME': '/usr/lib/jvm/default-java'}
rootdir: /home/frank/documents/articles/quickcheck
plugins: hypothesis-4.40.1, metadata-1.8.0, cov-2.7.1, html-1.21.1
collecting ... collected 4 items

src/test_example.py::test_email PASSED                                   [ 25%]
src/test_example.py::test_sorting_list_of_integers PASSED                [ 50%]
src/test_example.py::test_shuffle_is_noop FAILED                         [ 75%]
src/test_example.py::test_alphanumeric PASSED                            [100%]

=================================== FAILURES ===================================
_____________________________ test_shuffle_is_noop _____________________________

    @given(lists(integers()), randoms())
>   def test_shuffle_is_noop(a_list, _random):
        """
        Show intermediate steps in test using `note`.

src/test_example.py:39: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

a_list = [0, 1], _random = RandomWithSeed(1)

    @given(lists(integers()), randoms())
    def test_shuffle_is_noop(a_list, _random):
        """
        Show intermediate steps in test using `note`.
        """
        b_list = list(a_list)
        _random.shuffle(b_list)
        note("Shuffle: %r" % (b_list))
>       assert a_list == b_list
E       assert [0, 1] == [1, 0]
E         At index 0 diff: 0 != 1
E         Full diff:
E         - [0, 1]
E         + [1, 0]

src/test_example.py:46: AssertionError
---------------------------------- Hypothesis ----------------------------------
Falsifying example: test_shuffle_is_noop(a_list=[0, 1], _random=RandomWithSeed(1))
Shuffle: [1, 0]
============================ Hypothesis Statistics =============================
src/test_example.py::test_email:

  - 100 passing examples, 0 failing examples, 0 invalid examples
  - Typical runtimes: 1-26 ms
  - Fraction of time spent in data generation: ~ 97%
  - Stopped because settings.max_examples=100

src/test_example.py::test_sorting_list_of_integers:

  - 100 passing examples, 0 failing examples, 0 invalid examples
  - Typical runtimes: 0-1 ms
  - Fraction of time spent in data generation: ~ 70%
  - Stopped because settings.max_examples=100

src/test_example.py::test_shuffle_is_noop:

  - 20 passing examples, 11 failing examples, 3 invalid examples
  - Typical runtimes: 0-1 ms
  - Fraction of time spent in data generation: ~ 21%
  - Stopped because nothing left to do

src/test_example.py::test_alphanumeric:

  - 100 passing examples, 0 failing examples, 0 invalid examples
  - Typical runtimes: 1-4 ms
  - Fraction of time spent in data generation: ~ 89%
  - Stopped because settings.max_examples=100

====================== 1 failed, 3 passed in 2.11 seconds ======================
```
