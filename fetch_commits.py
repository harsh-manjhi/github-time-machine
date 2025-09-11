import requests

# Replace with your GitHub username
username = "harsh-manjhi"

url = f"https://api.github.com/users/{username}/repos"
response = requests.get(url)
repos = response.json()

print("Your repositories:")
for repo in repos:
    print(repo["name"])
