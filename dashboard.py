import streamlit as st
import matplotlib.pyplot as plt
import os
import requests

# 🔑 GitHub token from environment
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    st.error("⚠️ No GitHub token found. Run: export GITHUB_TOKEN='your_token_here'")
    st.stop()

USERNAME = "harsh-manjhi"
BASE_URL = "https://api.github.com"
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def get_repos(username):
    url = f"{BASE_URL}/users/{username}/repos"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        st.error(f"Error fetching repos: {response.status_code}")
        return []
    return [repo["name"] for repo in response.json()]

def get_commits(username, repo):
    url = f"{BASE_URL}/repos/{username}/{repo}/commits"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return []
    return response.json()

# 🚀 Streamlit UI
st.title("GitHub Repo Dashboard")
st.subheader("Repository Stats")

repos = get_repos(USERNAME)
commits_counts = {}

for repo in repos:
    commits = get_commits(USERNAME, repo)
    commits_counts[repo] = len(commits)
    st.write(f"**{repo}** → {len(commits)} commits")

# 📊 Chart
if commits_counts:
    fig, ax = plt.subplots()
    ax.bar(commits_counts.keys(), commits_counts.values(), color="#3498db", edgecolor="black")
    ax.set_title("Commits Comparison")
    ax.set_xlabel("Repositories")
    ax.set_ylabel("Commits")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    st.pyplot(fig)
else:
    st.info("No commits found for the user.")


