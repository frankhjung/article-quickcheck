# Thoughts on Random Number Generators

This is part 2 in the series on Random numbers. The series contains:

1. [Random Number Generators in bash scripts](https://gitlab.com/theMarloGroup/articles/random)
2. [Random Number Generators to test code](https://gitlab.com/theMarloGroup/articles/quickcheck)
3. [Random Number Generators in simulation](https://gitlab.com/theMarloGroup/articles/simulation)


## Building

To render a HTML or PDF version of the article, use:

```bash
make quickcheck.html
make quickcheck.pdf
```

This will generate documents into the `public` directory.

The pipeline will render the document and published to pages:
* [GitHub](https://frankhjung.github.io/article-quickcheck/)
* [GitLab](https://themarlogroup.gitlab.io/articles/quickcheck/).

See also the GitLab pipeline configuration, [.gitlab-ci.yml](./gitlab-ci.yml).

