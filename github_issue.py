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

    # Define the timeout for no comments
    timeout = timedelta(minutes=1)
    start_time = datetime.now()

    # Shared variable to capture user input
    user_input = None

    # Function to capture user input
    def capture_input():
        global user_input
        user_input = input("\nType your approval ('yes' or 'no'): ")

    # Start a thread for capturing user input
    print("Starting input thread...")
    input_thread = threading.Thread(target=capture_input)
    input_thread.daemon = True  # Ensure the thread exits when the main program exits
    input_thread.start()

    print("Monitoring comments on the issue...")

    while True:
        # Check for timeout
        if datetime.now() - start_time >= timeout:
            print("\nTime's up! No comments received. Closing the issue.")
            print("Issue closed.")
            exit(1)  # Exit with failure status to stop the workflow

        # Continuously display the message
        print("Pending approval, yes or no for approval...", end="\r", flush=True)

        # Check for user input
        if user_input:
            user_input = user_input.strip().lower()
            if user_input == "yes":
                print("\nApproval received: 'yes'. Closing the issue.")
                print("Issue closed.")
                exit(0)  # Exit with success status to continue the workflow
            elif user_input == "no":
                print("\nApproval denied: 'no'. Closing the issue.")
                print("Issue closed.")
                exit(1)  # Exit with failure status to stop the workflow
            else:
                print("\nInvalid input. Please type 'yes' or 'no'.")
                user_input = None  # Reset input for another attempt

        # Sleep briefly to reduce CPU usage
        time.sleep(0.5)

except Exception as e:
    print(f"Error: {e}")
    raise