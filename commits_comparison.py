
import os
import requests
import matplotlib.pyplot as plt

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise Exception("⚠️ No GitHub token found. Run: export GITHUB_TOKEN='your_token_here'")

USERNAME = "harsh-manjhi"
BASE_URL = "https://api.github.com"

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

    print("\n✅ Final Commits Count Dict:", commits_counts)

    # 📊 Visualization — Bar Chart for Comparison
    repos = list(commits_counts.keys())
    counts = list(commits_counts.values())

    plt.figure(figsize=(8, 5))
    bars = plt.bar(repos, counts, color="#3498db", edgecolor="black")

    # 🎨 Visual polish
    plt.title("📊 Commits Comparison Across Repositories", fontsize=14, pad=15)
    plt.xlabel("Repositories", fontsize=12)
    plt.ylabel("Number of Commits", fontsize=12)
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    # 🧠 Add commit count labels above bars
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.5, str(yval),
                 ha='center', va='bottom', fontsize=10, fontweight='bold')

    # 💾 Save chart instead of just showing it
    plt.tight_layout()
    plt.savefig("commits_comparison.png", dpi=150)
    plt.show()

    plt.figure(figsize=(6,6))
    plt.pie(counts, labels=repos, autopct="%1.1f%%", startangle=140,
        colors=plt.cm.Blues([c/max(counts) for c in counts]))
    plt.title("Commit Distribution Across Repos", fontsize=14, pad=15)
    plt.tight_layout()
    plt.show()

    # -----------------------------
    # Quick Insights
    # -----------------------------
    total_commits = sum(counts)
    avg_commits = round(total_commits / len(counts), 2)
    top_repo = repos[counts.index(max(counts))]
    top_commits = max(counts)

    print("\n📊 Repo Insights:")
    print(f"Total commits: {total_commits}")
    print(f"Average commits per repo: {avg_commits}")
    print(f"Top repo: {top_repo} with {top_commits} commits")