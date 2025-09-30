import json
import pandas as pd
import matplotlib.pyplot as plt
import os
import requests
from datetime import datetime

# -------------------- 1. Setup --------------------
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise Exception("⚠️ No GitHub token found. Run: export GITHUB_TOKEN='your_token_here'")

USERNAME = "harsh-manjhi"
BASE_URL = "https://api.github.com"

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# -------------------- 2. Functions --------------------
def get_repos(username):
    """Fetch all repos of the user"""
    url = f"{BASE_URL}/users/{username}/repos"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error fetching repos: {response.status_code}")
        return []
    return [repo["name"] for repo in response.json()]

def get_commits(username, repo):
    """Fetch commits for a repo, skip if error"""
    url = f"{BASE_URL}/repos/{username}/{repo}/commits"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error fetching {repo}: {response.status_code}")
        return []
    return response.json()

# -------------------- 3. Fetch & Save Commits --------------------
repos = get_repos(USERNAME)
print(f"Your repositories: {repos}\n")

all_commits = {}

for repo in repos:
    commits = get_commits(USERNAME, repo)
    all_commits[repo] = commits  # save full commit info
    print(f"Repo: {repo}, Commits fetched: {len(commits)}")

# Save to commits.json so plotting can use it
with open("commits.json", "w") as f:
    json.dump(all_commits, f, indent=4)
print("\n✅ commits.json saved!\n")

# -------------------- 4. Load commits & process dates --------------------
with open("commits.json", "r") as f:
    commits = json.load(f)

# Extract all commit dates
dates = []
for repo_commits in commits.values():
    for c in repo_commits:
        # c["commit"]["author"]["date"] has the date
        dates.append(datetime.strptime(c["commit"]["author"]["date"], "%Y-%m-%dT%H:%M:%SZ"))

# -------------------- 5. Create DataFrame & weekly counts --------------------
df = pd.DataFrame({"date": dates})
# Group each date into the week it belongs to (Monday start)
df["week"] = df["date"].dt.to_period("W").apply(lambda r: r.start_time)

# Count commits per week
weekly_counts = df.groupby("week").size()

# -------------------- 6. Plot --------------------
plt.figure(figsize=(10,5))
plt.plot(weekly_counts.index, weekly_counts.values, marker="o")
plt.title("Commits Over Time")
plt.xlabel("Week")
plt.ylabel("Number of Commits")
plt.xticks(rotation=45)
plt.tight_layout()

# Save chart
plt.savefig("commits_timeline.png")
print("✅ Chart saved as commits_timeline.png")

# Save chart
plt.savefig("commits_timeline.png")
print("✅ Chart saved as commits_timeline.png")

# Pop up the chart window
plt.show()
