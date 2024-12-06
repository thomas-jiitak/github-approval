import os
from github import Github
import time

# Environment variables
repo_name = os.getenv('GITHUB_REPOSITORY')
token = os.getenv('GITHUB_TOKEN')
title = os.getenv('INPUT_TITLE')
body = os.getenv('INPUT_BODY')
labels = os.getenv('INPUT_LABELS').split(',')
assignees = os.getenv('INPUT_ASSIGNEES', '').split(',')

print(f"Repository: {repo_name}")
print(f"Token provided: {'Yes' if token else 'No'}")

try:
    # Authenticate
    github = Github(token)
    repo = github.get_repo(repo_name)
    print(f"Successfully accessed repository: {repo.full_name}")

    # Create the issue
    issue = repo.create_issue(
        title=title,
        body=body,
        assignees=[a for a in assignees if a],
        labels=[l for l in labels if l]
    )
    print(f"Issue created successfully: {issue.html_url}")

    # Polling for "yes" comments and issue closure
    print("Waiting for the issue to be closed and checking comments...")
    while True:
        # Refresh issue details
        issue = repo.get_issue(issue.number)
        print(f"Issue state: {issue.state}")

        # Check for "yes" in comments
        comments = issue.get_comments()
        yes_found = any("yes" in comment.body.lower().strip() for comment in comments)

        # Detailed debug logs
        for comment in comments:
            print(f"Comment: {comment.body}")

        if yes_found and issue.state == "closed":
            print("Issue closed and 'yes' found. Exiting...")
            exit(0)

        if issue.state == "closed" and not yes_found:
            print("Issue closed but 'yes' not found. Waiting for 'yes' comment...")
        elif not issue.state == "closed":
            print("Issue still open. Rechecking in 60 seconds...")

        time.sleep(60)


except Exception as e:
    print(f"Error: {e}")
    raise