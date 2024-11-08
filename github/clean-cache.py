import requests
import os

# Set your GitHub token and organization name
GITHUB_TOKEN = os.environ["CACHE_CLEANUP_TOKEN"]
ORG_NAME = "lyric-tech"

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

# GitHub API base URL
BASE_URL = "https://api.github.com"

# Get all repositories in the organization
def get_org_repos():
    repos = []
    page = 1
    while True:
        url = f"{BASE_URL}/orgs/{ORG_NAME}/repos?page={page}&per_page=100"
        response = requests.get(url, headers=HEADERS)
        data = response.json()
        if len(data) == 0:
            break
        repos.extend([repo['name'] for repo in data])
        page += 1
    return repos

# Get all caches for a given repository (with pagination)
def get_repo_caches(repo_name):
    caches = []
    page = 1
    while True:
        url = f"{BASE_URL}/repos/{ORG_NAME}/{repo_name}/actions/caches?page={page}&per_page=100"
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print(f"Failed to retrieve caches for {repo_name}")
            break
        data = response.json().get('actions_caches', [])
        if len(data) == 0:
            break
        caches.extend(data)
        page += 1
    return caches

# Delete a cache by ID for a given repository
def delete_cache(repo_name, cache_id):
    url = f"{BASE_URL}/repos/{ORG_NAME}/{repo_name}/actions/caches/{cache_id}"
    response = requests.delete(url, headers=HEADERS)
    if response.status_code == 204:
        print(f"Cache {cache_id} deleted for {repo_name}")
    else:
        print(f"Failed to delete cache {cache_id} for {repo_name}")

# Main function to clear caches across all repos
def clear_caches():
    repos = get_org_repos()
    for repo in repos:
        print(f"Checking caches for {repo}...")
        caches = get_repo_caches(repo)
        if caches:
            for cache in caches:
                delete_cache(repo, cache['id'])
        else:
            print(f"No caches found for {repo}")

if __name__ == "__main__":
    clear_caches()
