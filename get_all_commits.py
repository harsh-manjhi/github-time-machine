import os 
import requests

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise Exception("⚠️ No GitHub token found. Run: export GITHUB_TOKEN='your_token_here'")

# Replace with your GitHub username
USERNAME = "harsh-manjhi"

# Base URL for GitHub API
BASE_URL = "https://api.github.com"

# Headers with authentication
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def get_repos(username):
    """Fetch all repos of the user"""
    url = f"{BASE_URL}/users/{username}/repos"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error fetching repos: {response.status_code}")
        return []
    return [repo["name"] for repo in response.json()]

def get_commits(username, repo):
    """Fetch commits for a given repo"""
    url = f"{BASE_URL}/repos/{username}/{repo}/commits"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error fetching {repo}: {response.status_code}")
        return []
    return response.json()

if __name__ == "__main__":
    repos = get_repos(USERNAME)
    print(f"Your repositories: {repos}\n")

    for repo in repos:
        commits = get_commits(USERNAME, repo)
        print(f"Repo: {repo}, Commits: {len(commits)}")