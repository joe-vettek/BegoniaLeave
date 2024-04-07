import requests

def get_latest_release(repo_owner, repo_name):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("tag_name")
    else:
        return None

# 示例用法
repo_owner = "MaaXYZ"
repo_name = "MaaFramework"
latest_release = get_latest_release(repo_owner, repo_name)
if latest_release:
    print(f"Latest release version for {repo_owner}/{repo_name}: {latest_release}")
else:
    print(f"Unable to retrieve release information for {repo_owner}/{repo_name}")
