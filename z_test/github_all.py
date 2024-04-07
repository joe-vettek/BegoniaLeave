import requests

def get_all_releases(repo_owner, repo_name):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return [release.get("tag_name") for release in data]
    else:
        return None


# 示例用法
repo_owner = "MaaXYZ"
repo_name = "MaaFramework"
all_releases = get_all_releases(repo_owner, repo_name)
if all_releases:
    print(f"All releases for {repo_owner}/{repo_name}:")
    for release in all_releases:
        print(release)
else:
    print(f"Unable to retrieve release information for {repo_owner}/{repo_name}")
