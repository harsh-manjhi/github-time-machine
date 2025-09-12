import os
import requests

# Step 1: Load GitHub token from environment
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Step 2: Add headers with token for authentication
headers = {"Authorization": f"token {GITHUB_TOKEN}"}

# Step 3: Repo details (test with dsa-reboot)
owner = "harsh-manjhi"
repo = "dsa-reboot"

# Step 4: GitHub API endpoint for commits
url = f"https://api.github.com/repos/{owner}/{repo}/commits"

# Step 5: Send the request
response = requests.get(url, headers=headers)

# Step 6: Handle response
if response.status_code == 200 :
    commits = response.json()
    for c in commits[:5] :
        print(f"{c['sha'][:7]} - {c['commit']['message']} - {c['commit']['author']['date']}")
else :
    print("Error :", response.status_code, response.text)

    