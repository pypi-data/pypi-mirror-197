# Changelog Genie

![](changelog-genie.png)

Image Credit: DALL-E

## Overview

Changelog Genie is a simple and pragmatic changelog generator, implemented in Python, that utilizes the GitHub 
REST API to produce changelog content very efficiently, avoiding GitHub API rate limits. It was built out of necessity 
as a replacement for [github-changelog-generator](https://github.com/github-changelog-generator/github-changelog-generator),
which served well for many Apache Arrow projects for a long time but eventually became unworkable as the number of 
issues and pull requests continued to grow.

Roadmap/Status:

- [x] Basic functionality in place
- [ ] Make sections and labels configurable
- [ ] Support reading [github-changelog-generator](https://github.com/github-changelog-generator/github-changelog-generator) configuration files
- [ ] Write the content into an existing changelog file

## Installation

```pip3 install changelog-genie```

## Usage

```text
$ changelog_genie --help
usage: cli.py [-h] project tag1 tag2

positional arguments:
  project     The project name e.g. apache/arrow-datafusion
  tag1        The previous release tag
  tag2        The current release tag

options:
  -h, --help  show this help message and exit

```

There is currently a two-step process for generating a changelog. This will be improved in a future release.

### Step 1: Generate Partial Changelog 

Run the ChangeLog Genie script to fetch the commits between two tags from GitHub and produce the changelog 
content. Providing a GitHub token is necessary to achieve a higher rate limit for interaction with the GitHub REST API. 

```shell
GITHUB_TOKEN=<token> changelog_genie andygrove/changelog-genie 0.1.0 0.2.0 > changelog-0.2.0.md
```

### Step 2: Copy and paste into existing changelog

This will be automated in a future release.

## Contributing

```shell
python3 -m venv venv
# activate the venv
source venv/bin/activate
# update pip itself if necessary
python -m pip install -U pip
# install dependencies (for Python 3.8+)
python -m pip install -r requirements.in

Poetry

```shell
sudo apt install python3-poetry
```

Testing

```shell
poetry build
poetry install
```

