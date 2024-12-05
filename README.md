# GitHub Issue Creator Action

This GitHub Action allows you to programmatically create issues in a GitHub repository based on user-defined inputs such as title, body, labels, and assignees.

## Features

	•	Create issues with a title and description.
	•	Add labels and assign users to the issue.
	•	Fully customizable using input parameters.

## Inputs


| Input              | Description                                  | Required | Default                |
|--------------------|----------------------------------------------------------------------------------|
| `GITHUB_TOKEN`     | Token for authenticating GitHub API.         | yes      | `secrets.GITHUB_TOKEN` |
| `INPUT_TITLE`      | Title of the issue.                          | No       | N/A                    |
| `INPUT_BODY`       | Body of the issue.                           | No       | N/A                    |
| `INPUT_LABELS`     | Comma-separated list of labels.              | No       | N/A                    |
| `INPUT_ASSIGNEES`  | Comma-separated list of assignees.           | No       | N/A                    |


## Usage

Here’s an example of how to use this action in your GitHub Actions workflow:

name: Create GitHub Issue
```yaml

on:
  workflow_dispatch:

jobs:
  create-issue:
    runs-on: ubuntu-latest
    steps:
      - name: Create GitHub Issue
        uses: thomasvjoseph/github-issues@v0.0.8
        with:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          INPUT_TITLE: "Bug Report"
          INPUT_BODY: "Description of the bug."
          INPUT_LABELS: "bug, urgent"
          INPUT_ASSIGNEES: "username1,username2"
```
## How It Works

	1.	Inputs: You provide the title, body, labels, and assignees for the issue via the workflow file.
	2.	Execution: The Action uses the GitHub API to create the issue in the repository where the workflow is executed.



## Contributing

Contributions are welcome! Feel free to submit issues or pull requests to improve this project.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for more details.


## Author:  
thomas joseph
- [linkedin](https://www.linkedin.com/in/thomas-joseph-88792b132/)
- [medium](https://medium.com/@thomasvjoseph)