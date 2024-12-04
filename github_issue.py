import os
from github import Github

# Extracting all the input from environment variables
title = os.getenv('INPUT_TITLE')
token = os.getenv('GITHUB_TOKEN')  # Using the automatically provided GITHUB_TOKEN
labels = os.getenv('INPUT_LABELS')
assignees = os.getenv('INPUT_ASSIGNEES')
body = os.getenv('INPUT_BODY')

# Check if title is provided
if not title:
    raise ValueError("Title is missing. Please provide a valid title for the issue.")

# If labels are provided, split by ',' to make it a list
if labels and labels != '':
    labels = labels.split(',')
else:
    labels = []  # Default to an empty list if no labels

# If assignees are provided, split by ',' to make it a list
if assignees and assignees != '':
    assignees = assignees.split(',')
else:
    assignees = []  # Default to an empty list if no assignees

# Use the GitHub token to authenticate
github = Github(token)

# GITHUB_REPOSITORY is automatically available in GitHub Actions
repo = github.get_repo(os.getenv('GITHUB_REPOSITORY'))

# Create the issue
issue = repo.create_issue(
    title=title,
    body=body,
    assignees=assignees,
    labels=labels
)

print(f"Issue created successfully: {issue.html_url}")