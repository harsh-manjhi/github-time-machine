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

    commits_counts = {}

    for repo in repos:
        commits = get_commits(USERNAME, repo)
        commits_counts[repo] = len(commits)
        print(f"Repo: {repo}, Commits: {len(commits)}")

    print("\nCommits counts dict :",commits_counts)


import matplotlib.pyplot as plt 

# Sort repos by commit count descending
sorted_repos = sorted(commits_counts.items(), key=lambda x: x[1], reverse=True)
repos, counts = zip(*sorted_repos)

colors = ["green" if c == max(counts) else "orange" for c in counts]

repos = list(commits_counts.keys())
counts = list(commits_counts.values())

plt.figure(figsize=(10,6))
plt.bar(repos, counts, color = "orange", edgecolor = "black")
plt.grid(axis="y",linestyle = "--", alpha = 0.7)

plt.xlabel("Repositories")
plt.ylabel("Number of Repositories")
plt.title("Dynamic Commit Counts per Repo")

for i, count in enumerate(counts):
    plt.text(i, count + 0.5, str(count), ha='center')

# Save chart as image
plt.savefig("github_commit_wrapup.png", dpi=300, bbox_inches="tight")


plt.show(block="False")