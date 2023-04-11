# Chat Review (Python)

This is a Python implementation of the [Chat Review](https://github.com/ikoofe/chat-review) project, which was originally written in TypeScript. The purpose of this project is to use ChatGPT to perform automatic code reviews on GitLab merge requests.

## Installation

Before using this project, make sure you have Python 3.8 or higher installed.

1. Clone this repository:

   ```
   git clone https://github.com/ukewea/chat-review-py.git
   ```

2. Change into the project directory:

   ```
   cd chat-review-python
   ```

3. Install the required dependencies using `poetry`:

   ```
   poetry install
   ```

## Usage

To use the Chat Review script, run using `poetry`:

```
poetry run python.cli.py --chatgpt "$CHATGPT_KEY" --token "$GITLAB_TOKEN" --project "$CI_MERGE_REQUEST_PROJECT_ID" --mr "$CI_MERGE_REQUEST_IID"
```

## Integrate to GitLab CI/CD
Please refer to the README in [Chat Review](https://github.com/ikoofe/chat-review)

## Acknowledgments

This project is a port of the [Chat Review](https://github.com/ikoofe/chat-review) TypeScript project by [ikoofe](https://github.com/ikoofe). We appreciate their work on the original project and credit them for the inspiration and original source code.