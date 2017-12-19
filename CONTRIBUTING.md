# How to contribute?
All contributions are much welcome and greatly appreciated! Expect to be credited for you effort.

Please follow the [general guidelines][pr-guide] and check off the todos when you submit a pull request.

This document is adapted from the cookiecutter [CONTRIBUTING.rst][cookie-contrib].


## General
Generally try to limit the scope of any Pull Request to an atomic update if possible. This way, it's much easier to assess and review your changes.

You should expect a considerably faster turn around if you submit two or more PRs instead of baking them all into one major PR.


## Issue tracker
Chanjo uses the excellent [GitHub issue tracker][issues].

Personally, I also recommend giving [ZenHub][zenhub] a try. After installing the Google Chrome plugin, visit the [Chanjo boards][chanjo-boards]. This way, it's very easy to get an overview of the current bug/feature request situation.


## Types of contributions
There are many ways you can help out and improve this repository.

### Report bugs
Report bugs at [https://github.com/robinandeer/chanjo/issues][issues].

Consider the following data in your bug report:

- Your operating system name and version
- Any details about your local setup that might be helpful in troubleshooting
- If you can, provide detailed steps to reproduce the bug
- If you don't have steps to reproduce the bug, just note your observations in as much detail as you can. Questions to start a discussion about the issue are welcome.


### Fix bugs
Look through the [GitHub issues][issues] for bugs. Anything tagged with "bug" is open to whoever wants to implement it.


### Implement features
Look through the [GitHub issues][issues] for features. Anything tagged with "enhancement" is open to whoever wants to implement it.


### Write Documentation
Chanjo could always use more documentation, whether as part of the official documentation, in inline docstrings, or even on the web in blog posts, articles, and such.

If you have written your own tutorial or review of the software, please consider adding a refferal link to the repository.


### Submit Feedback
The best way to send feedback is to [open a new issue][issues].

If you are requesting a feature:

- Explain in detail how it would work
- Keep the scope as narrow as possible, to make it easier to implement.


## Setting up the development environment
Over time my ambition is to provide a reproducable and automated setup through Vagrant. In the mean time, follow the steps below:

1. Fork the [Chanjo repository][repo] on GitHub.

2. Clone your fork locally

	```bash
	$ git clone git@github.com:your_name_here/cookiecutter.git
	$ cd chanjo
	```

	I would personally recommend [GitHub for Mac][gh-mac] to easily manage pull requests and [SourceTree][sourcetree] as an excellent GUI for git.

3. Install your local copy into a [Conda][miniconda] environment

	```bash
	$ conda create -n chanjo python=3 pip  # or python=2
	$ conda install --yes --file requirements/conda.txt
	$ pip install -r requirements/development.txt
	$ pip install --editable .
	```

	Conda is great since you will be installing Numpy and SQLAlchemy later.

4. Create a branch for local development

	```bash
	$ git checkout -b name-of-your-bugfix-or-feature
	```

5. Make you changes locally

6. When you're done making changes, check that your updated code passes the tests and flake8.

	```bash
	$ flake8 chanjo tests
	$ invoke test
	$ tox
	```

7. Commit your changes and push your branch to GitHub

	```bash
	$ git add .
	$ git commit -m "Your detailed description of your changes."
	$ git push origin name-of-your-bugfix-or-feature
	```

8. Check that the test coverage hasn't dropped

	```bash
	$ invoke coverage
	```

9. Submit a pull request through the GitHub website. I would encourage you to submit your pull request early in the process. This makes it easier to maintain an overview of current development and opens up for continous discussion.


## Contributor Guidelines

### Pull Request Guidelines
Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put your new functionality into a function with a docstring, and add the feature to the list in README.rst.
3. The pull request should work for Python 2.6, 2.7, 3.3, and PyPy. Check https://travis-ci.org/audreyr/cookiecutter/pull_requests and make sure that the tests pass for all supported Python versions.


### Coding standards
Generally I recommend two ways to stay up-to-date on Chanjo coding standards.

1. Read and pay attention to current code in the repository

2. Install a plugin for [EditorConfig][editorconfig] and let it handle some of the detailed settings for you.


### Tips
To run a particular test:

```bash
$ python -m pytest tests.test_find.TestFind.test_find_template
```

To run a subset of tests:

```bash
$ python -m pytest tests.test_find
```


[chanjo-boards]: https://github.com/Clinical-Genomics/chanjo/issues#boards
[cookie-contrib]: https://github.com/audreyr/cookiecutter/blob/master/CONTRIBUTING.rst
[editorconfig]: http://editorconfig.org/
[gh-mac]: https://mac.github.com/
[issues]: https://github.com/Clinical-Genomics/chanjo/issues
[miniconda]: http://conda.pydata.org/miniconda.html
[pr-guide]: https://help.github.com/articles/using-pull-requests
[repo]: https://github.com/Clinical-Genomics/chanjo
[sourcetree]: http://www.sourcetreeapp.com/
[zenhub]: https://www.zenhub.io/
