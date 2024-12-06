import os
from github import Github
import time
from datetime import datetime, timedelta
import threading

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

###################################################################

    # Define the timeout for no comments
    timeout = timedelta(minutes=5)
    start_time = datetime.now()

    print("Monitoring comments on the issue...")
    print("Pending approval. Provide 'yes' or 'no' as a comment on the issue.")

    while True:
        # Refresh issue details
        issue = repo.get_issue(issue.number)

        # Fetch comments
        comments = issue.get_comments()
        yes_found = any("yes" in comment.body.lower().strip() for comment in comments)
        no_found = any("no" in comment.body.lower().strip() for comment in comments)

        # If "yes" is found, close the issue and proceed with the workflow
        if yes_found:
            print("Approval received: 'yes'. Proceeding with the workflow...")
            issue.create_comment("Approval received: 'yes'. Closing the issue.")
            issue.edit(state="closed")
            exit(0)  # Exit with success status to continue the workflow

        # If "no" is found, close the issue and stop the workflow
        if no_found:
            print("Approval denied: 'no'. Stopping the workflow...")
            issue.create_comment("Approval denied: 'no'. Closing the issue.")
            issue.edit(state="closed")
            exit(1)  # Exit with failure status to stop the workflow

        # If no comments, check the timeout
        if not comments:
            elapsed_time = datetime.now() - start_time
            if elapsed_time < timeout:
                print("Pending approval. Waiting for 'yes' or 'no' comment...")
            else:
                print("No response within the timeout. Stopping the workflow...")
                issue.create_comment("No response within the time frame. Closing the issue.")
                issue.edit(state="closed")
                exit(1)  # Exit with failure status to stop the workflow
        else:
            print("Comment detected. Waiting for 'yes' or 'no' to decide...")

        # Sleep briefly to reduce API usage
        time.sleep(10)


except Exception as e:
    print(f"Error: {e}")
    raise