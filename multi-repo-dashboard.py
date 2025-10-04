import streamlit as st
import os
import requests
import altair as alt
import pandas as pd

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

# User-Driven Repo Selection
st.subheader("🎛️ Choose Repositories")

selected_repos = st.multiselect(
    "Select repositories to display 👇",
    options=repos,
    default=repos  # all preselected initially
)

# Filter commit data based on selection
filtered_commits = {repo: commits_counts[repo] for repo in selected_repos}

# Convert dict into DataFrame
if filtered_commits:
    # Convert commits dict → DataFrame
    df = pd.DataFrame(list(filtered_commits.items()), columns=["Repository", "Commits"])
    
    # Altair interactive bar chart with unique colors per repo
    chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x="Repository",
            y="Commits",
            color=alt.Color("Repository", legend=None),  # unique color per repo
            tooltip=["Repository", "Commits"]
        )
        .properties(title="📊 Commits Comparison (Interactive & Colorful)")
    )
    
    # Render chart
    st.altair_chart(chart, use_container_width=True)
else:
    st.info("No commits found for the user.")

# Highlight Top Repo Dynamically
if filtered_commits:
    top_repo = max(filtered_commits, key=filtered_commits.get)
    top_commits = filtered_commits[top_repo]
    st.markdown(f"### 🏅 Top Repo: **{top_repo}** with **{top_commits} commits!** 🎉")

st.markdown("## 🏆 Repo Highlights")
st.write("")  # adds spacing

col1, col2 = st.columns(2)

with col1:
    st.metric(
        label="🚀 Top Repository",
        value=top_repo,
        delta=f"{top_commits} commits",
    )

with col2:
    st.success(f"🔥 Keep it up! {top_repo} is leading the pack!")

# Summary Insight
total_commits = sum(filtered_commits.values())
repo_count = len(filtered_commits)
st.markdown("---")
st.markdown(
    f"**Summary:** You've made **{total_commits} commits** across **{repo_count} repositories**. "
    "That's solid consistency, keep the streak alive! 💪"
)
st.divider()

# Fun Stats Panel
st.subheader("🏆 Highlights")

col1, col2, col3 = st.columns(3)

with col1:
    st.success("🔥 Longest Streak: 10 days")

with col2:
    st.warning("🚀 Most Active Month: July 2025")

with col3:
    st.info("📊 Avg Commits/Week: 5.3")


st.markdown("🏆 Keep pushing! Your streak is awesome!")
st.markdown("⚡ Tip: Daily commits make the dashboard shine!")
