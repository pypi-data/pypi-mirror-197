import argparse
import sys
from github import Github
import os


def print_pulls(repo_name, title, pulls):
    if len(pulls)  > 0:
        print("**{}:**".format(title))
        print()
        for (pull, commit) in pulls:
            url = "https://github.com/{}/pull/{}".format(repo_name, pull.number)
            print("- {} [#{}]({}) ({})".format(pull.title, pull.number, url, commit.author.login))
        print()


def generate_changelog(repo, repo_name, tag1, tag2):

    # get a list of commits between two tags
    comparison = repo.compare(tag1, tag2)

    # get the pull requests for these commits
    unique_pulls = []
    all_pulls = []
    for commit in comparison.commits:
        pulls = commit.get_pulls()
        for pull in pulls:
            # there can be multiple commits per PR if squash merge is not being used and
            # in this case we should get all the author names, but for now just pick one
            if pull.number not in unique_pulls:
                unique_pulls.append(pull.number)
                all_pulls.append((pull, commit))

    # we split the pulls into categories
    #TODO: make categories configurable
    breaking = []
    bugs = []
    docs = []
    enhancements = []

    # categorize the pull requests based on GitHub labels
    for (pull, commit) in all_pulls:
        labels = [label.name for label in pull.labels]
        if 'api change' in labels:
            breaking.append((pull, commit))
        elif 'bug' in labels:
            bugs.append((pull, commit))
        elif 'enhancement' in labels:
            enhancements.append((pull, commit))
        elif 'documentation' in labels:
            docs.append((pull, commit))

    # produce the changelog content
    print_pulls(repo_name, "Breaking changes", breaking)
    print_pulls(repo_name, "Implemented enhancements", enhancements)
    print_pulls(repo_name, "Fixed bugs", bugs)
    print_pulls(repo_name, "Documentation updates", docs)
    print_pulls(repo_name, "Merged pull requests", all_pulls)


def cli(args=None):
    """Process command line arguments."""
    if not args:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument("project", help="The project name e.g. apache/arrow-datafusion")
    parser.add_argument("tag1", help="The previous release tag")
    parser.add_argument("tag2", help="The current release tag")
    args = parser.parse_args()

    token = os.getenv("GITHUB_TOKEN")

    g = Github(token)
    repo = g.get_repo(args.project)
    generate_changelog(repo, args.project, args.tag1, args.tag2)

if __name__ == "__main__":
    cli()