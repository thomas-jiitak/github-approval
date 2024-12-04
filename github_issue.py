import requests
import os
import sys

# Retrieve the GitHub token from GitHub Actions context
token = os.getenv("GITHUB_TOKEN")

if not token:
    print("Error: GitHub token not found!")
    sys.exit(1)

headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github.v3+json"
}

data = {
    "title": "Testing issue from GitHub Action",
    "body": "This is a test issue created via GitHub Action.",
}

username = os.getenv("GITHUB_ACTOR")  # Automatically gets the username of the action runner
repository = os.getenv("GITHUB_REPOSITORY")  # Automatically gets the repository in the form 'owner/repository'

# Check if the repository and username are valid
if not username or not repository:
    print("Error: GitHub username or repository not found!")
    sys.exit(1)

url = f"https://api.github.com/repos/{repository}/issues"  # Using the repository in 'owner/repository' format

try:
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()  # Raise an exception for HTTP errors

    if response.status_code == 201:
        print("Issue created successfully!")
        print("Issue URL:", response.json().get("html_url"))
    else:
        print(f"Failed to create issue. Status code: {response.status_code}")
        print("Response:", response.text)

except requests.RequestException as e:
    print(f"Request failed: {e}")
    sys.exit(1)