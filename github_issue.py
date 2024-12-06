import os
from github import Github
import time

# Environment variables
repo_name = os.getenv('GITHUB_REPOSITORY')
token = os.getenv('GITHUB_TOKEN')
title = os.getenv('INPUT_TITLE', 'Bug Report')
body = os.getenv('INPUT_BODY', 'No issue description provided.')
labels = os.getenv('INPUT_LABELS', 'bug').split(',')
assignees = os.getenv('INPUT_ASSIGNEES', '').split(',')

# Debugging outputs
print(f"Repository: {repo_name}")
print(f"Token provided: {'Yes' if token else 'No'}")
print(f"Title: {title}")
print(f"Body: {body}")
print(f"Labels: {labels}")
print(f"Assignees: {assignees}")

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
        # Refresh the issue details
        issue = repo.get_issue(issue.number)

        # Check for "yes" in comments
        comments = issue.get_comments()
        yes_found = any("yes" in comment.body.lower() for comment in comments)

        # Check if the issue is closed
        if issue.state == "closed":
            if yes_found:
                print("Issue closed with a 'yes' comment. Proceeding to the next workflow step...")
                # Trigger the next step or add logic here
                exit(0)
            else:
                print("Issue closed without a 'yes' comment. Exiting...")
                exit(1)

        print("Issue still open. Rechecking in 30 seconds...")
        time.sleep(30)

except Exception as e:
    print(f"Error: {e}")
    raise