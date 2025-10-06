import streamlit as st
import os
import requests
import pandas as pd
import altair as alt

# 🧱 Page Setup
st.set_page_config(
    page_title="GitHub Repo Dashboard",
    page_icon="📊",
    layout="wide"
)

# 🧠 Header
st.title("🚀 GitHub Repo Dashboard")
st.markdown("A clean, structured dashboard that tracks your GitHub repositories and commits.")

# 🔑 Token Setup
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

# 📦 Fetch Functions
@st.cache_data
def get_repos(username):
    url = f"{BASE_URL}/users/{username}/repos"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        st.error(f"Error fetching repos: {response.status_code}")
        return []
    return [repo["name"] for repo in response.json()]

@st.cache_data
def get_commits(username, repo):
    url = f"{BASE_URL}/repos/{username}/{repo}/commits"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return []
    return response.json()

# 🧭 Main Layout Containers
header = st.container()
stats = st.container()
visuals = st.container()
highlights = st.container()
filters = st.container()

# 📊 Header Section
with header:
    st.subheader(f"GitHub User: **{USERNAME}**")

# 🧩 Data Fetching
repos = get_repos(USERNAME)
commits_counts = {}
for repo in repos:
    commits = get_commits(USERNAME, repo)
    commits_counts[repo] = len(commits)

# 🪄 Total Summary
total_commits = sum(commits_counts.values())

# 🧭 Filters Section
with filters:
    st.subheader("🎛️ Choose Repositories")
    selected_repos = st.multiselect(
        "Select repositories to display 👇",
        options=repos,
        default=repos  # all selected initially
    )
    filtered_commits = {repo: commits_counts[repo] for repo in selected_repos}

# 🧮 Stats Overview
with stats:
    col1, col2, col3 = st.columns(3)
    col1.metric("📁 Total Repositories", len(repos))
    col2.metric("🧾 Total Commits", total_commits)
    col3.metric("📅 Data Refreshed", "Live via API")

# 📈 Chart Visualization
with visuals:
    st.subheader("📊 Commit Comparison Across Repositories")
    if filtered_commits:
        df = pd.DataFrame(list(filtered_commits.items()), columns=["Repository", "Commits"])
        chart = (
            alt.Chart(df)
            .mark_bar()
            .encode(
                x="Repository",
                y="Commits",
                color="Repository",
                tooltip=["Repository", "Commits"]
            )
            .properties(height=400)
        )
        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("No commits found for the selected repositories.")

# 🏆 Highlights Section
with highlights:
    if filtered_commits:
        top_repo = max(filtered_commits, key=filtered_commits.get)
        top_commits = filtered_commits[top_repo]
        
        st.subheader("🏆 Top Performer")
        col1, col2 = st.columns([1, 2])
        with col1:
            st.metric(label="🚀 Top Repository", value=top_repo, delta=f"{top_commits} commits")
        with col2:
            st.success(f"🔥 {top_repo} is leading with {top_commits} commits!")
            st.caption("Keep committing daily to stay on top 🚀")

# ✨ Pro Tip
import streamlit as st
import os
import requests
import pandas as pd
import altair as alt

# 🧱 Page Setup
st.set_page_config(
    page_title="GitHub Repo Dashboard",
    page_icon="📊",
    layout="wide"
)

# 🧠 Header
st.title("🚀 GitHub Repo Dashboard")
st.markdown("A clean, structured dashboard that tracks your GitHub repositories and commits.")

# 🔑 Token Setup
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

# 📦 Fetch Functions
@st.cache_data
def get_repos(username):
    url = f"{BASE_URL}/users/{username}/repos"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        st.error(f"Error fetching repos: {response.status_code}")
        return []
    return [repo["name"] for repo in response.json()]

@st.cache_data
def get_commits(username, repo):
    url = f"{BASE_URL}/repos/{username}/{repo}/commits"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return []
    return response.json()

# 🧭 Main Layout Containers
header = st.container()
stats = st.container()
visuals = st.container()
highlights = st.container()
filters = st.container()

# 📊 Header Section
with header:
    st.subheader(f"GitHub User: **{USERNAME}**")

# 🧩 Data Fetching
repos = get_repos(USERNAME)
commits_counts = {}
for repo in repos:
    commits = get_commits(USERNAME, repo)
    commits_counts[repo] = len(commits)

# 🪄 Total Summary
total_commits = sum(commits_counts.values())

# 🧭 Filters Section
with filters:
    st.subheader("🎛️ Choose Repositories")
    selected_repos = st.multiselect(
        "Select repositories to display 👇",
        options=repos,
        default=repos  # all selected initially
    )
    filtered_commits = {repo: commits_counts[repo] for repo in selected_repos}

# 🧮 Stats Overview
with stats:
    col1, col2, col3 = st.columns(3)
    col1.metric("📁 Total Repositories", len(repos))
    col2.metric("🧾 Total Commits", total_commits)
    col3.metric("📅 Data Refreshed", "Live via API")

# 📈 Chart Visualization
with visuals:
    st.subheader("📊 Commit Comparison Across Repositories")
    if filtered_commits:
        df = pd.DataFrame(list(filtered_commits.items()), columns=["Repository", "Commits"])
        chart = (
            alt.Chart(df)
            .mark_bar()
            .encode(
                x="Repository",
                y="Commits",
                color="Repository",
                tooltip=["Repository", "Commits"]
            )
            .properties(height=400)
        )
        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("No commits found for the selected repositories.")

# 🏆 Highlights Section
with highlights:
    if filtered_commits:
        top_repo = max(filtered_commits, key=filtered_commits.get)
        top_commits = filtered_commits[top_repo]
        
        st.subheader("🏆 Top Performer")
        col1, col2 = st.columns([2, 1])
        with col1:
            st.success(f"🔥 {top_repo} is leading with {top_commits} commits!")
            st.caption("Keep committing daily to stay on top 🚀")
        with col2:
            st.metric(label="🚀 Top Repository", value=top_repo, delta=f"{top_commits} commits")

# ✨ Pro Tip
st.markdown("---")
st.markdown("### 💡 Pro Tip")
st.info("💪 Daily commits make your dashboard grow richer every day.")
