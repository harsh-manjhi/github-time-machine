import matplotlib.pyplot as plt

repos = [ "hello_github", "github-time-machine", "dsa-reboot"]
commit_counts = [25, 2, 2]

# Creating a bar chart
plt.figure(figsize=(8,5))

plt.bar(repos, commit_counts, color = "orange", edgecolor="black")

plt.title("Github commits per Repo")
plt.xlabel("Repositories")
plt.ylabel("Number of Commits")
plt.grid(axis="y", linestyle="--", alpha=0.7)

plt.show()