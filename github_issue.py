import requests
import os

# Retrieve the GitHub token from environment variables
token = os.getenv("GITHUB_TOKEN")  # GitHub token is automatically set by GitHub Actions
if not token:
    raise ValueError("GitHub token not found! Please ensure the 'issues: write' permission is granted.")

headers = {"Authorization": f"token {token}"}
data = {
    "title": "Testing issue from GitHub Action",
    "body": "This is a test issue created via GitHub Action.",
}

username = os.getenv("GITHUB_ACTOR")  # Automatically gets the username of the action runner
repository = os.getenv("GITHUB_REPOSITORY")  # Automatically gets the repository in the form 'owner/repository'

# Check if the repository and username are valid
if not username or not repository:
    raise ValueError("GitHub username or repository not found! Please ensure the repository exists.")

url = f"https://api.github.com/repos/{repository}/issues"  # Using the repository in 'owner/repository' format

response = requests.post(url, headers=headers, json=data)

if response.status_code == 201:
    print("Issue created successfully!")
    print("Issue URL:", response.json().get("html_url"))
else:
    print(f"Failed to create issue. Status code: {response.status_code}")
    print("Response:", response.text)