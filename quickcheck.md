---
title: 'Using Randomness to Test Code'
author: '[frank.jung@marlo.com.au](mailto:frank.jung@marlo.com.au)'
header-includes:
  - \usepackage{fancyhdr}
  - \usepackage{graphicx}
  - \pagestyle{fancy}
  - \fancyhead[L]{\includegraphics[height=7.5mm]{images/themarlogroup.png}}
  - \fancyfoot[L]{© The Marlo Group 2019}
date: '11 October 2019'

---

![Photo by Mika Baumeister on Unsplash](images/banner.png)

# Using Randomness to Test Code

In [part 1](https://marlo.com.au/some-thoughts-on-random-number-generators/) of
this series, we explored how to generate and test (pseudo) random values. In
this article we will explore how random values can be used in testing. This is
also known as property based testing.

The first question you may be asking is: why would you use random values in
testing? Doesn't that defeat the whole purpose of unit testing, where known
values are tested to known responses? Well, no. Not if you think of testing the
properties of your code. Property based testing seeks to verify a large range of
applicable input values with your program code. It does this by generating a
random sample of valid input values. When generating property values, the choice
of probability distribution for random samples can be chosen to suit your use
case. If you wanted representative data then perhaps a normal distribution
suffices. Perhaps you want an even spread using a uniform distribution. Or maybe
you are testing the edges of property values then a custom distribution can be
employed.

Are you delivering solutions using micro-service or lambda functions? If so,
then property testing may well be suited to your needs.

The article is organised as follows: First we will [review](#history) where
these ideas came from, then do a short [introduction to property based
testing](#introducing-property-based-testing). This will introduce
[Generators](#generators). Next, we will briefly discuss
[Shrinkage](#shrinkage), and reproducing tests before [finishing](#summary) with
some final observations.


## History

These concepts aren't new. Tools like [Lorem Ipsum](https://www.lipsum.com/)
have been around since the 1960's to model text.

Kent Beck provided a unit testing framework for
[Smalltalk](https://en.wikipedia.org/wiki/Smalltalk) in 1989. Initially, tests
had to be hand crafted. It did describes a philosophy of writing and running
tests embodied by a [literate
program](https://en.wikipedia.org/wiki/Literate_programming) test framework.

In 1994, Richard Hamlet wrote about Random Testing. Not the "random" as in the
slang definition, meaning haphazard. Instead, Hamlet suggested that computers
could efficiently test a "vast number" of random test points. A second benefit
he identified was that random testing provided "statistical prediction of
significance in the observed results".

A few years later, in 1999, the influential paper by
[Claessen](http://www.cse.chalmers.se/~koen/) and
[Hughes](https://en.wikipedia.org/wiki/John_Hughes_(computer_scientist)) called,
[QuickCheck: A Lightweight Tool for Random Testing of Haskell
Programs](https://www.researchgate.net/publication/2449938_QuickCheck_A_Lightweight_Tool_for_Random_Testing_of_Haskell_Programs),
provided a whole new tool kit to run tests with randomised values. Their paper
was written for the functional programming language,
[Haskell](https://www.haskell.org/), but it quickly inspired a suite of property
based testing tools in many other languages. A useful list of current
implementations appears on the
[QuickCheck](https://en.wikipedia.org/wiki/QuickCheck) Wikipedia page.


## Introducing Property Based Testing

With property based testing the idea is that for a function or method, any valid
input should yield a valid response. Likewise, any input outside this range
should return an appropriate failure. Compare this to how systematic tests are
normally written: Given a *specific* input, check the programs return value. And
that highlights the problem: you need to be sure you have chosen correct and
*sufficient* input values to test your code. The tools we use to check test
coverage do not check the *adequacy* of your tests. Just that you have a test
for a control flow path. So the quality of a test is dependent upon the quality
of the inputs. Property based testing provides tools to test over randomly
values selected over the range of input. This changes the focus of our tests. We
concentrate on the properties of functions under test. What the inputs are and
what the outputs are expected to be. With systematic testing (unit tests) we are
selecting only a few inputs. Assumptions made on these selections could lead
to failures. Testing the properties of an input over a large range of values can
help to find bugs otherwise ignored in specific unit tests. We have experienced
this first hand. It is a true "aha" moment when the tests uncover a use case
whose input we hadn't thought of!

With Unit Testing we provide fixed inputs (e.g. 0,1,2,…) and get a fixed result
(e.g. 1, 2, 4, …).

With Property Based Testing we provide a declaration of inputs (e.g. All `int`s)
and declaration of conditions that must be held (e.g. Result is an `int`).

At the core of Property Based Testing is the production randomised input test
values. These test values are produced using *generators*.


## Generators

Random values are produced using *generators*. These are specific functions used
to provide a random value. Some common generators are used to manufacture
Booleans, numeric types (e.g. floats, ranges of integers), characters and
strings. Both [QuickCheck](http://hackage.haskell.org/package/QuickCheck) and
[QuickTheories](https://github.com/quicktheories/QuickTheories) have many
generators. And once you have a primitive generator, you can then compose these
into more elaborate generators and structures, including lists and maps. Or you
can build your own!

Apart from custom values, you may also want a custom distribution. Random
testing is most effective when the values being tested closely match the
distribution of the actual data. As the provided generators know nothing of your
data, they typically will use a uniform distribution. If however, something else
is required then you will need to provide your own generator. Luckily, these are
not difficult to write. The test tools we have used (Haskell:QuickCheck,
Java:QuickTheories and Python:Hypothesis) have rich libraries of generators but
can also be easily extended.


## Shrinkage

On failure, QuickCheck then reduces the selection to the minimum set. So, from a
large distribution of values, QuickCheck finds the minimal case that fails the
test. In practice, what this does is concentrate tests to the extremes of an
input value. However, this behaviour can be modified using a *Generator*.

Shrinkage is an important feature to property based testing. Having an example
of failure is good. Having a minimal example of failure is better. With a
minimal example you are more likely to understand the reasons for the failure.


## Test Reproduction

Random testing is useful, but once a failure has been identified, then we would
like to repeat these failed tests to ensure they have been fixed. Tools such as
Python's Hypothesis record all failed tests so on future runs those tests are
automatically included in any re-runs.

Other tools such as Java's QuickTheories allow the repetition of tests by
specifying a random seed. When a test fails, the random seed used to generate
that test is reported, and can then be used to reproduce the tests.

## Summary

In this article we took a brief look at the features of using random values for
tests. Randomness is intrinsic to Property Based Testing tools like QuickCheck.
Using generators you can not only shape the distribution of test values but also
customise the value types. Recording the random seed enables you to repeat
specific test runs. And having a minimal failed test case helps diagnose
problems.

Generating a large number of tests may, however, give a false sense of security
if most of these test cases are trivial. So, choosing the correct inputs,
whether randomly generated or systematically selected is important.

QuickCheck style test tools don't replace unit tests, rather they augment
existing test cases. By thinking on the properties of your code, then the test
cases can become more general and cover a greater parameter range.

## Resources

* [Beyond Unit Tests](https://www.hillelwayne.com/talks/beyond-unit-tests/)
* [Lorem Ipsum](https://www.lipsum.com/)
* [Property Testing](https://en.wikipedia.org/wiki/Property_testing)
* [Python Hypothesis](https://hypothesis.readthedocs.io/en/latest/index.html)
* [QuickCheck](https://en.wikipedia.org/wiki/QuickCheck)
* [QuickCheck: A Lightweight Tool for Random Testing of Haskell Programs by Koen Claessen & John Hughes (1999)](https://www.researchgate.net/publication/2449938_QuickCheck_A_Lightweight_Tool_for_Random_Testing_of_Haskell_Programs) (PDF)
* [QuickCheck: As a test set generator](https://wiki.haskell.org/QuickCheck_as_a_test_set_generator)
* [QuickCheck: A tutorial on generators](https://www.stackbuilders.com/news/a-quickcheck-tutorial-generators)
* [QuickCheck: Automatic testing of Haskell programs](http://hackage.haskell.org/package/QuickCheck)
* [QuickTheories](https://github.com/quicktheories/QuickTheories) a Java QuickCheck style tool (GitHub)
* [Random Testing by Richard Hamlet (1994)](https://pdfs.semanticscholar.org/b02a/67acd634cf04a1c7ca3fa58975c3d6ff1c4b.pdf) (PDF)
* [Simple Smalltalk Testing: With Patterns by Kent Beck (1989)](https://web.archive.org/web/20150315073817/http://www.xprogramming.com/testfram.htm)
* [Source for this article](https://github.com/frankhjung/article-quickcheck) (GitHub)

