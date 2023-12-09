# GitShit

## Description

"GitShit" is a straightforward Python script designed to identify and modify author names and emails in git commits. It scans for specified unwanted keywords within commit author details and replaces them with user-defined values.



## Setup and Installation

### Compatibility Note
While "GitShit" has only been tested on Pop!_OS, a Debian-based distribution, its reliance on Python and Bash suggests it could also be compatible with non-Debian based Linux distributions. However, this broader compatibility has not been explicitly verified.

### Prerequisites

- Python 3.x
- Git

### Installation Steps

1. **Clone the Repository**
   Clone the GitShit repository to your local machine:

   ```bash
   git clone https://github.com/ZribeDev/GitShit
   cd GitShit
   ```
2. **Create and Configure the Environment File**

   - Rename `.env.example` to `.env`:
     ```bash
     mv .env.example .env
     ```
   - Edit the `.env` file with your specific details:
     - `GITHUB_USERNAME`: Your GitHub username.
     - `GITHUB_TOKEN`: Your personal GitHub token.
     - `UNWANTED_KEYWORDS`: Comma-separated list of unwanted keywords.
     - `NEW_NAME`: New name for replacing in commits.
     - `NEW_EMAIL`: New email for replacing in commits.
     - `CHANGE_EMAILS`: Set to `True` to enable email modifications.
3. **Generate a GitHub Token**

   - Navigate to [GitHub Tokens](https://github.com/settings/tokens) to generate a new token with necessary permissions.
   - Place this token in the `GITHUB_TOKEN` field in your `.env` file.
4. **Install Dependencies**

   - Install the required Python modules using pip:
     ```bash
     pip install -r requirements.txt
     ```
5. **Prepare the Execution Script**

   - Make the `start.sh` script executable:
     ```bash
     chmod +x start.sh
     ```

## Usage

<<<<<<< HEAD
- To execute the script once:
=======
- To execute the script once (will only change a single repository if `CHANGE_EMAILS` is set to `True`):
>>>>>>> origin/master
  ```bash
  python main.py
  ```
- To run the script multiple times, use:
  ```bash
  bash start.sh [amount]
  ```

  Replace `[amount]` with the number of times you want to run the script. If `[amount]` is not specified, the script will run once by default.

## Contributing

Feel free to fork the repository and submit pull requests with your contributions.

## License

This project is open-sourced under the MIT License.
