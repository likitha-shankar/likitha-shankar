import os
import re
import requests

USERNAME = os.environ.get("GITHUB_USERNAME", "likitha-shankar")
TOKEN = os.environ.get("GITHUB_TOKEN", "")

headers = {"Authorization": f"token {TOKEN}"} if TOKEN else {}


def get_latest_repos(n=4):
    url = f"https://api.github.com/users/{USERNAME}/repos"
    params = {"sort": "updated", "direction": "desc", "per_page": n + 1, "type": "owner"}
    response = requests.get(url, headers=headers, params=params)
    repos = response.json()

    # Skip the profile README repo itself
    repos = [r for r in repos if r["name"] != USERNAME][:n]
    return repos


def build_table(repos):
    rows = []
    for repo in repos:
        name = repo["name"]
        url = repo["html_url"]
        description = repo.get("description") or "No description provided"
        language = repo.get("language") or "-"
        rows.append(f"| [{name}]({url}) | {description} | {language} |")

    rows_str = "\n".join(rows)
    return f"""<!-- LATEST-REPOS:START -->
| Project | Description | Built with |
|---|---|---|
{rows_str}
<!-- LATEST-REPOS:END -->"""


def update_readme(table):
    with open("README.md", "r") as f:
        content = f.read()

    pattern = r"<!-- LATEST-REPOS:START -->.*?<!-- LATEST-REPOS:END -->"
    updated = re.sub(pattern, table, content, flags=re.DOTALL)

    with open("README.md", "w") as f:
        f.write(updated)
    print("README updated successfully.")


if __name__ == "__main__":
    repos = get_latest_repos(4)
    table = build_table(repos)
    update_readme(table)
