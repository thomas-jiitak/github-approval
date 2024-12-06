import os
from github import Github
import time
from datetime import datetime, timedelta

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

    # Define the timeout for no comments
    timeout = timedelta(minutes=5)
    start_time = datetime.now()

    print("Monitoring comments on the issue...")
    while True:
        # Refresh issue details
        issue = repo.get_issue(issue.number)

        # Fetch comments
        comments = issue.get_comments()
        yes_found = any("yes" in comment.body.lower().strip() for comment in comments)
        no_found = any("no" in comment.body.lower().strip() for comment in comments)

        # If "yes" or "no" is found, close the issue
        if yes_found or no_found:
            print(f"Found {'yes' if yes_found else 'no'} comment. Closing issue...")
            issue.edit(state="closed")
            
            if yes_found:
                print("Proceeding to the next workflow step...")
                exit(0)
            # If "no" is found, close the issue and stop the workflow
            if no_found:
                print("Found 'no' comment. Closing issue and stopping workflow...")
                issue.edit(state="closed")
                exit(1)  # Exit with failure status to stop the workflow

        # If no comments, check the timeout
        if datetime.now() - start_time >= timeout:
            print("No comments within 5 minutes. Closing issue...")
            issue.edit(state="closed")
            exit(1)

        print("No relevant comments yet. Rechecking in 30 seconds...")
        time.sleep(30)

except Exception as e:
    print(f"Error: {e}")
    raise