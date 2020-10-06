---
title: 'Using Randomness to Test Code'
author: '[frank.jung@marlo.com.au](mailto:frank.jung@marlo.com.au)'
geometry: margin=25mm
header-includes:
  - \usepackage{fancyhdr}
  - \usepackage{graphicx}
  - \pagestyle{fancy}
  - \fancyhead[L]{\includegraphics[height=7.5mm]{images/themarlogroup.png}}
  - \fancyfoot[L]{© Marlo 2020}
date: '13 February 2020'

---

![Photo by Mika Baumeister on Unsplash](images/banner.png)

# Using Randomness to Test Code

In [part 1](https://marlo.com.au/some-thoughts-on-random-number-generators/) of
this series, we explored how to generate and test (pseudo) random values. In
this article we will explore how random values can be used in testing. You may
already be familiar with randomness in test invocation. For instance
[JUnit5](https://junit.org/) provides an annotation to [randomise the order of
test
execution](https://junit.org/junit5/docs/current/user-guide/#writing-tests-test-execution-order).
Here, however, we are looking at a style of testing that uses randomly generated
input values that tests _properties_ of your code. This is known as "Property
Based Testing".

You may be asking is: *Why would you use random values in testing? Doesn't that
defeat the whole purpose of unit testing, where known values are tested to known
responses?* Well, no. Often it is hard to think of suitable positive and
negative test cases that exercise your code. In addition: what if many randomly
selected tests can be automatically run? And what if these tests cover many
different input values? And what if instances where tests fail are automatically
recorded so they can be reported and replayed later? These are just some of the
benefits to this approach to testing.

Property based testing seeks to verify a large range of applicable input values
with your program code. It does this by generating a random sample of valid
input values. Perhaps an example may help. Given a utility method to convert a
string field into uppercase text, then a unit test would use some suggestive
values. In pseudo code this may look like:

```text
Given "abc123" then expect "ABC123"
Given "ABC" then expect "ABC"
Given "123" then expect "123"
```

In comparison, property based tests we are looking at the behaviour of any field
that matches the input type. In pseudo code this looks like:

```text
For any lowercase alphanumeric string then expect the same string but in uppercase.
For any uppercase alphanumeric string then expect the same string, unchanged.
For any non-alphabetic string then expect the same string, unchanged.
```

The "for any" is where the randomness comes in.

This article is organised as follows: First we will [review](#history) where
these ideas came from, then do a short [introduction to property based
testing](#introducing-property-based-testing). This will introduce
[Generators](#generators). Next, we will briefly discuss
[Shrinkage](#shrinkage), and reproducing tests before [finishing](#summary)
with some final observations.


## History

These concepts aren't new. Tools like [Lorem Ipsum](https://www.lipsum.com/)
have been around since the 1960`s to model text.

Kent Beck provided a unit testing framework for
[Smalltalk](https://en.wikipedia.org/wiki/Smalltalk) in 1989. Those tests had to
be hand crafted. This introduced a number of key concepts that we now take for
granted. It provided an organisation and recipes for unit tests. For each test
case, the test data was created then thrown away at the end. Tests cases were
aggregated into a test suite. The test suite is part of a framework that also
produced a report, which is an example of what is known as [literate
programming](https://en.wikipedia.org/wiki/Literate_programming).

In 1994, Richard Hamlet wrote about Random Testing. Not the "random" as in the
slang definition, meaning haphazard. Instead what Hamlet was suggesting is that
computers could efficiently test a "vast number" of random test points. A second
benefit he identified was that random testing provided a "statistical prediction
of significance in the observed results". This last point is somewhat technical.
In essence it describes the ability to quantify the significance of a test that
does *not* fail. In other words: is this just testing trivial cases?

A few years later, in 1999, the influential paper by
[Claessen](http://www.cse.chalmers.se/~koen/) and
[Hughes](https://en.wikipedia.org/wiki/John_Hughes_(computer_scientist)) called,
[QuickCheck: A Lightweight Tool for Random Testing of Haskell
Programs](https://www.researchgate.net/publication/2449938_QuickCheck_A_Lightweight_Tool_for_Random_Testing_of_Haskell_Programs),
provided a whole new way to run tests using randomised values. Their paper was
written for the functional programming language,
[Haskell](https://www.haskell.org/). It proved influential and quickly inspired
a suite of property based testing tools for many other languages. A useful list
of current implementations appears on the
[QuickCheck](https://en.wikipedia.org/wiki/QuickCheck) Wikipedia page.

So, that is a bit of background. We will now look at the features of Property
Based Testing.


## Introducing Property Based Testing

With property based testing the idea is that for a function or method, any
valid input should yield a valid response. Likewise, any input outside this
range should return an appropriate failure. Compare this to how systematic
tests are normally written: Given a *specific* input, check the program's
return value. And that highlights the problem: you need to be sure you have
chosen correct and *sufficient* input values to test your code. The tools we
use to check test coverage do not check the *adequacy* of your tests. Just
that you have a test for a control flow path. So the quality of a test is
dependent upon the quality of the inputs. Property based testing provides
tools to test using randomly generated values selected over the range of input.
This changes the focus of our tests. We concentrate on the properties of
functions under test. That is it focuses on what the inputs are and what the
outputs are expected to be. With systematic testing (unit tests) we are
selecting only a few inputs. Assumptions made on these selections could lead to
failures. Testing the properties of an input over a large range of values can
help to find bugs otherwise ignored in specific unit tests. We have experienced
this first hand. It is a true "aha" moment when the tests uncover a use case
whose input we hadn't thought of.

In summary:

* With Unit Testing we provide fixed inputs (e.g. 0,1,2,…) and get a fixed
  result (e.g. 1,2,4,…).

* With Property Based Testing we provide a declaration of inputs (e.g. All
  non-negative `int`s) and declaration of conditions that must be held (e.g.
  Result is an `int`).

At its core, Property Based Testing is the production of randomised input test
values. These test values are produced using *generators*.


## Generators

Random values are produced using *generators*. These are specific functions used
to provide a random value. Some common generators are used to manufacture
Booleans, numeric types (e.g. floats, ranges of integers), characters and
strings. Both [QuickCheck](http://hackage.haskell.org/package/QuickCheck) and
[JUnit-QuickCheck](https://pholser.github.io/junit-quickcheck/) have many
generators. And once you have a primitive generator, you can then compose these
into more elaborate generators and structures like lists and maps, or other
bespoke structures.

Apart from custom values, you may also want a custom distribution. Random
testing is most effective when the values being tested closely match the
distribution of the actual data. As the provided generators know nothing of your
data so will typically use a uniform distribution. If however, something else
is required then you will need to provide your own generator. Luckily, these are
not difficult to write. The test tools we have used
([Haskell:QuickCheck](http://hackage.haskell.org/package/QuickCheck),
[Java:JUnit-QuickCheck](https://github.com/pholser/junit-quickcheck) and
[Python:Hypothesis](https://hypothesis.works/)) have rich libraries of
generators which can be easily extended.


## Shrinkage

On failure, QuickCheck then reduces the selection to the minimum set. So, from
a large distribution of values, QuickCheck finds the minimal case that fails
the test. In practice, what this does is concentrate tests to the extremes of
an input value. However, this behaviour can be modified using a *Generator*.

Shrinkage is an important feature to property based testing. Having an example
of failure is good. Having a minimal example of failure is better. With a
minimal example you are more likely to understand the reasons for the failure.


## Test Reproduction

Random testing is useful, but once a failure has been identified, then we would
like to repeat these failed tests to ensure they have been fixed. Tools such as
Python's Hypothesis record all failed tests. On future runs those specific
failed tests are automatically included in any re-runs.

Other tools such as Java's
[JUnit-QuickCheck](https://github.com/pholser/junit-quickcheck) allow the
repetition of tests by specifying a random seed. When a test fails, the random
seed used to generate that test is reported, and can then be used to reproduce
the tests.


## Code Examples

So, what does this look like? Marlo uses Java for development of integration
solutions. So the first examples shown here will use the above Java
JUnit-QuickCheck package.

The following generator will create a alphanumeric word with a length of between
1 and 12 characters.

```java
/** Alphanumeric characters: "0-9A-Za-z". */
private static final String ALPHANUMERICS =
    "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";

/** Generate a word. Do not create null words. */
@Override
public String generate(final SourceOfRandomness randomness, final GenerationStatus status) {
  final int stringSize = randomness.nextInt(11) + 1; // only non-null words
  final StringBuilder randomString = new StringBuilder(stringSize);
  IntStream.range(0, stringSize)
      .forEach(
          ignored -> {
            final int randomIndex = randomness.nextInt(ALPHANUMERICS.length());
            randomString.append(ALPHANUMERICS.charAt(randomIndex));
          });
  return randomString.toString();
}
```

[(source)](https://github.com/frankhjung/java-quickcheck/blob/master/src/test/java/com/marlo/quickcheck/AlphaNumericGenerator.java)

To use this generator in a unit test:

```java
/**
  * Test alphanumeric word is same for stream as scanner using Alphanumeric generator. Trials
  * increased from the default of 100 to 1000.
  *
  * @param word a random alphanumeric word
  */
@Property(trials = 1000)
public void testAlphanumericWord(final @From(AlphaNumericGenerator.class) String word) {
  assertEquals(1, WordCountUtils.count(new Scanner(word)));
  assertEquals(1, WordCountUtils.count(Stream.of(word)));
}
```

[(source)](https://github.com/frankhjung/java-quickcheck/blob/master/src/test/java/com/marlo/quickcheck/WordCountTests.java)

Here we are using our custom generator, and have increased the trials to 1000
from the default of 100. The expected property of our word count utility is that
given this input string, we would have just one word.

Once we have a custom generator, we can orchestrate it for use in more elaborate
tests. For example, from our random word generator, lets create a random
sentence:

```java
/**
  * Test a sentence of alphanumeric words. A sentence is a list of words separated by a space.
  *
  * @param words build a sentence from a word stream
  */
@Property
public void testAlphanumericSentence(
    final List<@From(AlphaNumericGenerator.class) String> words) {
  final String sentence = String.join(" ", words);
  assertEquals(
      WordCountUtils.count(new Scanner(sentence)), WordCountUtils.count(Stream.of(sentence)));
}
```
[(source)](https://github.com/frankhjung/java-quickcheck/blob/master/src/test/java/com/marlo/quickcheck/WordCountTests.java)

At Marlo we also use Ansible for automation. Ansible is Python based. An
excellent QuickCheck library for Python is
[Hypothesis](https://hypothesis.readthedocs.io/en/latest/index.html). An
equivalent generator to the Java example above is the
[text](https://hypothesis.readthedocs.io/en/data.html?highlight=text#hypothesis.strategies.text)
strategy. Used in a test, it looks like:

```python
@given(text(min_size=1, max_size=12, alphabet=ascii_letters + digits))
def test_alphanumeric(a_string):
    """
    Generate alphanumeric sized strings like:
        'LbkNCS4xl2Xl'
        'z3M4jc1J'
        'x'
    """
    assert a_string.isalnum()
    a_length = len(a_string)
    assert a_length >= 1 and a_length <= 12
```

[(source)](src/test_example.py)

While the above are only trivial examples, it does demonstrate how this style of
testing is a valuable alternative to systematic tests. A larger number of test
cases can be run against your code. The style of tests are different, in that
they focus on the generalised behaviour of code rather than specific use cases.


## Summary

In this article we took a brief look at the features of using random values
for tests. Randomness is intrinsic to Property Based Testing tools like
QuickCheck. Using generators you can not only shape the distribution of test
values but also customise the value types. Recording the random seed enables
you to repeat specific test runs. And having a minimal failed test case helps
diagnose problems.

Property based tests don't replace unit tests. Instead they augment your
existing tests with values that you may not have thought about.

Generating a large number of tests may, however, give a false sense of
security if most of these test cases are trivial. So, choosing the correct
inputs, whether randomly generated or systematically selected is important.

Overall, writing property based tests was not hard and uncovered areas of
weakness I had not considered. So, why not get better quality results using
randomness to your advantage!?


## Resources

* [Beyond Unit Tests](https://www.hillelwayne.com/talks/beyond-unit-tests/)
* [JUnit5](https://junit.org/junit5/)
* [JUnit-QuickCheck](https://pholser.github.io/junit-quickcheck/) a Java QuickCheck style tool (GitHub)
* [Lorem Ipsum](https://www.lipsum.com/)
* [Property Testing](https://en.wikipedia.org/wiki/Property_testing)
* [Python Hypothesis](https://hypothesis.readthedocs.io/en/latest/index.html)
* [QuickCheck: A Lightweight Tool for Random Testing of Haskell Programs by Koen Claessen & John Hughes (1999)](https://www.researchgate.net/publication/2449938_QuickCheck_A_Lightweight_Tool_for_Random_Testing_of_Haskell_Programs) (PDF)
* [QuickCheck: As a test set generator](https://wiki.haskell.org/QuickCheck_as_a_test_set_generator)
* [QuickCheck: A tutorial on generators](https://www.stackbuilders.com/news/a-quickcheck-tutorial-generators)
* [QuickCheck: Automatic testing of Haskell programs](http://hackage.haskell.org/package/QuickCheck)
* [QuickCheck](https://en.wikipedia.org/wiki/QuickCheck)
* [Random Testing by Richard Hamlet (1994)](https://pdfs.semanticscholar.org/b02a/67acd634cf04a1c7ca3fa58975c3d6ff1c4b.pdf) (PDF)
* [Simple Smalltalk Testing: With Patterns by Kent Beck (1989)](https://web.archive.org/web/20150315073817/http://www.xprogramming.com/testfram.htm)
* [Source for this article](https://github.com/frankhjung/article-quickcheck) (GitHub)

