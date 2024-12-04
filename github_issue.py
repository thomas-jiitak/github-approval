import requests
import os

# Ensure the GitHub token is securely set in the environment
token = os.getenv("GITHUB_TOKEN")  # GitHub token should be stored in secrets or as an environment variable
if not token:
    raise ValueError("GitHub token not found! Please set the GITHUB_TOKEN environment variable.")

# Retrieve the repository and username from environment variables
username = os.getenv("GITHUB_USERNAME")  # GitHub username (e.g., 'thomas-jiitak')
repository = os.getenv("GITHUB_REPOSITORY")  # GitHub repository name (e.g., 'github-approval')

# Set the URL for creating an issue in the specified repository
url = f"https://api.github.com/repos/{username}/{repository}/issues"

# Headers for authentication
headers = {"Authorization": f"token {token}"}

# Data for the new issue
data = {
    "title": "Testing issue from GitHub Action",
    "body": "This is a test issue created via GitHub Action.",
}

# Make the API request to create the issue
response = requests.post(url, headers=headers, json=data)

# Check if the issue was successfully created
if response.status_code == 201:
    print("Issue created successfully!")
    print("Issue URL:", response.json().get("html_url"))
else:
    print(f"Failed to create issue. Status code: {response.status_code}")
    print("Response:", response.text)