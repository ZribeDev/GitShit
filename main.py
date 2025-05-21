import requests
import logging
import os
import shutil
from colorama import init, Fore
from dotenv import load_dotenv

load_dotenv()
init(autoreset=True)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

username = os.getenv('GITHUB_USERNAME')
token = os.getenv('GITHUB_TOKEN')  
unwanted_emails = os.getenv('UNWANTED_KEYWORDS').split(',')
New_Name = os.getenv('NEW_NAME')
New_Email = os.getenv('NEW_EMAIL')
CHANGE_EMAILS = os.getenv('CHANGE_EMAILS') == 'True'
IS_ORG = os.getenv('IS_ORGANIZATION') == 'True'
ORG_NAME = os.getenv('ORGANIZATION_NAME')
PROGRAM_PATH = os.getcwd()
def fetch_repos(token):
    all_repos = []  
    page = 1  
    while True:  
        url = f"https://api.github.com/{'orgs/' + ORG_NAME if IS_ORG else 'user'}/repos?page={page}"
        headers = {'Authorization': f'token {token}'}
        response = requests.get(url, headers=headers)

        if response.status_code == 200 and response.json():
            all_repos.extend(response.json())
            page += 1
            
        else:
            break
    return all_repos  

def fetch_commits(user, repo, token):
    url = f"https://api.github.com/repos/{user}/{repo}/commits"
    headers = {'Authorization': f'token {token}'}
    response = requests.get(url, headers=headers)
    
    return response.json()

def check_commits(commits):
    for commit in commits:
        committer_email = commit['commit']['committer']['email']
        committer_name = commit['commit']['committer']['name']
        author_email = commit['commit']['author']['email']
        author_name = commit['commit']['author']['name']
        
        if any(unwanted_email in committer_email for unwanted_email in unwanted_emails) or any(unwanted_email in author_email for unwanted_email in unwanted_emails):
            logging.warning(Fore.RED + f"Unsafe commit found: {commit['sha']}: committer {committer_email} by {committer_name}, author {author_email} by {author_name}")
        else:
            logging.info(Fore.GREEN + f"Commit {commit['sha']} is safe: committer {committer_email} by {committer_name}, author {author_email} by {author_name}")

def clone_repository(repo_url, temp_dir):
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir, exist_ok=True)
    
    if repo_url.startswith('https://github.com'):
        modified_url = repo_url.replace('https://', f'https://{token}@')
        os.system(f'git clone {modified_url} {temp_dir}')
    else:
        os.system(f'git clone {repo_url} {temp_dir}')

def replace_unwanted_info(temp_dir, old_email, old_name, new_email, new_name):
    tmpp = os.path.join(PROGRAM_PATH, temp_dir)
    os.chdir(tmpp)
    os.system(f'git filter-branch --env-filter \'if [ "$GIT_COMMITTER_EMAIL" = "{old_email}" ]; then export GIT_COMMITTER_EMAIL="{new_email}"; export GIT_COMMITTER_NAME="{new_name}"; fi; if [ "$GIT_AUTHOR_EMAIL" = "{old_email}" ]; then export GIT_AUTHOR_EMAIL="{new_email}"; export GIT_AUTHOR_NAME="{new_name}"; fi;\' --tag-name-filter cat -- --branches --tags')
    os.chdir(PROGRAM_PATH)

def main():
    repos = fetch_repos(f'{token}')
    for repo in repos:
        logging.info(f"Checking repository: {repo['name']}")
        commits = fetch_commits(repo['owner']['login'], repo['name'], token)
        check_commits(commits)

        unsafe_commits = [
            commit for commit in commits 
            if any(
                unwanted_detail in commit['commit']['committer']['email'] or
                unwanted_detail in commit['commit']['committer']['name'] or
                unwanted_detail in commit['commit']['author']['email'] or
                unwanted_detail in commit['commit']['author']['name']
                for unwanted_detail in unwanted_emails
            )
        ]

        if unsafe_commits and CHANGE_EMAILS:
            logging.warning(Fore.YELLOW + f"Unsafe commits found in repository: {repo['name']}")
            for commit in unsafe_commits:
                current_commit_committer_email = commit['commit']['committer']['email']
                current_commit_committer_name = commit['commit']['committer']['name']
                current_commit_author_email = commit['commit']['author']['email']
                current_commit_author_name = commit['commit']['author']['name']
                temp_dir = os.path.join('temp/', repo['name'])
                clone_repository(repo['clone_url'], temp_dir)
                replace_unwanted_info(temp_dir, current_commit_committer_email, current_commit_committer_name, New_Email, New_Name)
                replace_unwanted_info(temp_dir, current_commit_author_email, current_commit_author_name, New_Email, New_Name)
                logging.info(Fore.GREEN + "Unsafe commits replaced.")
                tmpp = os.path.join(PROGRAM_PATH, temp_dir)
                os.chdir(tmpp)
                os.system('git push --force --all')
                os.chdir(PROGRAM_PATH)
                logging.info(Fore.GREEN + "Changes pushed to the repository.")

if __name__ == "__main__":
    main()
    logging.info("Finished processing all repositories.")