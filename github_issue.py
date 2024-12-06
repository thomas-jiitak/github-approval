import os
from github import Github
import time

# Extract inputs
title = os.getenv('INPUT_TITLE', 'Bug Report')  # Default title
token = os.getenv('GITHUB_TOKEN')  # Automatically provided by GitHub Actions
labels = os.getenv('INPUT_LABELS', 'bug')  # Default label
assignees = os.getenv('INPUT_ASSIGNEES', '')
body = os.getenv('INPUT_BODY', 'No issue description provided.')  # Default body

# Split labels and assignees if provided
labels = labels.split(',') if labels else []
valid_assignees = [user.strip() for user in assignees.split(',') if user.strip()] if assignees else []

# Authenticate with GitHub
github = Github(token)
repo = github.get_repo(os.getenv('GITHUB_REPOSITORY'))

# Create the issue
try:
    issue = repo.create_issue(
        title=title,
        body=body,
        assignees=valid_assignees,
        labels=labels
    )
    print(f"Issue created successfully: {issue.html_url}")
except Exception as e:
    print(f"Error creating issue: {e}")
    raise

# Poll issue comments for "yes"
print("Waiting for the keyword 'yes' in issue comments...")

while True:
    try:
        comments = issue.get_comments()
        for comment in comments:
            if "yes" in comment.body.lower():
                print("Keyword 'yes' found in issue comments. Proceeding to next workflow...")
                exit(0)
        print("Keyword not found yet. Checking again in 30 seconds...")
        time.sleep(30)
    except Exception as e:
        print(f"Error while polling issue comments: {e}")
        raise