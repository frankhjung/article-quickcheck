---
title: 'Random Values in Testing'
author: '[frank.jung@marlo.com.au](mailto:frank.jung@marlo.com.au)'
date: '15 August 2019'
output:
  html_document: default
---


# Random Values in Testing

In the part 1 of this series, I explored how to generate and test (pseudo)random
values. In this article I want to explore how random values can be used in
testing.

The first question you may be asking is why would you use random values in
testing? Doesn't that defeat the purpose of unit testing, where known values are
tested to known responses? Well, no. Not if you think of testing the
*properties* of your code. [Property based testing](#references) seeks to verify
a large range of applicable input values to your program code. Are you
delivering solutions using microservice and lambda functions? If so, then
property testing may well be suited to your needs.


# History

These concepts aren't new. Tools like [Lorem Ipsum](https://www.lipsum.com) have
been around since the 1960's to model text content. [Kent Beck](#references)
stressed unit testing in 1989. These tests required to be hand crafted. Then, in
1999 an influential paper by Claessen and Hughes, [QuickCheck: A Lightweight
Tool for Random Testing of Haskell Programs](#references) added a whole new way
of testing. Their paper was written with respect to the functional programming
language, [Haskell](https://www.haskell.org), but it quickly spawned a suite of
property based testing tools for many other languages. A useful list of current
implementations appears on the [QuickCheck](#references) Wikipedia page.


# Features

The main feature of QuickCheck style property based testing is as follows:

*Suppose you can generate a wide suite of test cases simply and easily for your
functions?*

QuickCheck goes one step further and shrinks a failed test to a minimal set?

Randomness appears in generators. These are specific functions used to provide a
custom value. Some common generators are Booleans, various numeric types,
strings, lists, maps and dates. Once you have a primitive generator, then you
can build up from this to more complex generators and structures. That is, you
can build your own. Furthermore, you can shape the random distribution to suite
your context and needs.

Where QuickCheck (Haskell) goes further:

* Validation of rules / laws

Provides tools to generate sample data for:

* safe data for product promotion (think [Lorem Ipsum](https://www.lipsum.com), but, for data)
* performance testing


# Summary

In this article we looked at using random values for tests. Randomness is
intrinsic to QuickCheck test tools. Using generators you can shape the
distribution of test values to your use cases. Using random seeds you can repeat
specific test runs.

The QuickCheck family of test tools focuses on [Unit
Testing](https://en.wikipedia.org/wiki/Unit_testing). They don't replace unit
tests, rather they augment existing tests. By thinking on properties, test cases
become more general.


# References

* [Property Testing](https://en.wikipedia.org/wiki/Property_testing)
* [QuickCheck: A Lightweight Tool for Random Testing of Haskell Programs by Claessen, Koen & Hughes, John first released 1999](http://www.eecs.northwestern.edu/~robby/courses/395-495-2009-fall/quick.pdf)
* [QuickCheck](https://en.wikipedia.org/wiki/QuickCheck)
* [QuickTheories](https://github.com/quicktheories/QuickTheories)
* [Simple Smalltalk Testing: With Patterns by Kent Beck (BECK)](https://web.archive.org/web/20150315073817/http://www.xprogramming.com/testfram.htm)
* [Source for this article (GitHub)](https://github.com/frankhjung/article-quickcheck)

