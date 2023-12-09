import requests
import logging
import os
from colorama import init, Fore
from dotenv import load_dotenv
<<<<<<< HEAD
# test
=======

>>>>>>> origin/master
load_dotenv()
init(autoreset=True)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

username = os.getenv('GITHUB_USERNAME')
token = os.getenv('GITHUB_TOKEN')  
unwanted_emails = os.getenv('UNWANTED_KEYWORDS').split(',')
New_Name = os.getenv('NEW_NAME')
New_Email = os.getenv('NEW_EMAIL')
<<<<<<< HEAD
CHANGE_EMAILS = os.getenv('CHANGE_EMAILS') == 'True'

=======
CHANGE_EMAILS = os.getenv('CHANGE_EMAILS')
>>>>>>> origin/master
def fetch_repos(token):
    url = "https://api.github.com/user/repos"
    headers = {'Authorization': f'token {token}'}
    response = requests.get(url, headers=headers)
    return response.json()

def fetch_commits(user, repo, token):
    url = f"https://api.github.com/repos/{user}/{repo}/commits"
    headers = {'Authorization': f'token {token}'}
    response = requests.get(url, headers=headers)
    return response.json()

def check_commits(commits):
    for commit in commits:
        email = commit['commit']['committer']['email']
        name = commit['commit']['committer']['name']
        if any(unwanted_email in email for unwanted_email in unwanted_emails):
<<<<<<< HEAD
            logging.warning(Fore.RED + f"Unsafe commit found: {commit['sha']}: {email} by {name}")
=======
            logging.info(Fore.RED + f"Unwanted email found in commit {commit['sha']}: {email} by {name}")
>>>>>>> origin/master
        else:
            logging.info(Fore.GREEN + f"Commit {commit['sha']} is safe: {email} by {name}")

def clone_repository(repo_url, temp_dir):
    os.makedirs(temp_dir, exist_ok=True)
    os.system(f'git clone {repo_url} {temp_dir}')

def replace_unwanted_info(temp_dir, old_email, old_name, new_email, new_name):
    os.chdir(temp_dir)
<<<<<<< HEAD
=======

>>>>>>> origin/master
    os.system(f'git filter-branch --env-filter \'if [ "$GIT_COMMITTER_EMAIL" = "{old_email}" ]; then export GIT_COMMITTER_EMAIL="{new_email}"; export GIT_COMMITTER_NAME="{new_name}"; fi; if [ "$GIT_AUTHOR_EMAIL" = "{old_email}" ]; then export GIT_AUTHOR_EMAIL="{new_email}"; export GIT_AUTHOR_NAME="{new_name}"; fi;\' --tag-name-filter cat -- --branches --tags')
    os.chdir('..')

def main():
<<<<<<< HEAD
    repos = fetch_repos(f'{token}')
    for repo in repos:
        logging.info(f"Checking repository: {repo['name']}")
        commits = fetch_commits(repo['owner']['login'], repo['name'], token)
        check_commits(commits)

=======

    repos = fetch_repos(f'{token}')

    for repo in repos:
        logging.info(f"Checking repository: {repo['name']}")
        commits = fetch_commits(repo['owner']['login'], repo['name'], token)
>>>>>>> origin/master
        unsafe_commits = [
            commit for commit in commits 
            if any(
                unwanted_detail in commit['commit']['committer']['email'] or
                unwanted_detail in commit['commit']['committer']['name']
                for unwanted_detail in unwanted_emails
            )
        ]

<<<<<<< HEAD
        if unsafe_commits and CHANGE_EMAILS:
            logging.warning(Fore.YELLOW + f"Unsafe commits found in repository: {repo['name']}")
            for commit in unsafe_commits:
                current_commit_email = commit['commit']['committer']['email']
                current_commit_name = commit['commit']['committer']['name']
=======

        if unsafe_commits:
            for commit in unsafe_commits:
                current_commit_email = commit['commit']['committer']['email']
                current_commit_name = commit['commit']['committer']['name']
                logging.warning(Fore.YELLOW + f"Unsafe commits found in repository: {repo['name']}")
>>>>>>> origin/master
                temp_dir = os.path.join('temp/', repo['name'])
                clone_repository(repo['clone_url'], temp_dir)
                replace_unwanted_info(temp_dir, current_commit_email, current_commit_name, New_Email, New_Name)
                logging.info(Fore.GREEN + "Unsafe commits replaced.")
<<<<<<< HEAD

                os.chdir(repo['name'])
                os.system('git push --force --all')
                os.chdir('..')
                logging.info(Fore.GREEN + "Changes pushed to the repository.")

if __name__ == "__main__":
    main()
    logging.info("Finished processing all repositories.")
=======
                
                if CHANGE_EMAILS:
                    os.chdir(repo['name'])
                    os.system('git push --force --all')
                    os.chdir('..')
                    logging.info(Fore.GREEN + "Changes pushed to the repository.")
                    exit()
        check_commits(commits)

if __name__ == "__main__":
    main()  
    logging.info("Finished processing all repositories.")
>>>>>>> origin/master
