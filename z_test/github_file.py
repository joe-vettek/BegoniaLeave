import requests

def get_release_assets(repo_owner, repo_name, release_tag):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/tags/{release_tag}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return [asset.get("name") for asset in data.get("assets", [])]
    else:
        return None

# 示例用法
repo_owner = "MaaXYZ"
repo_name = "MaaFramework"
release_tag = "v1.7.0-alpha.3"
assets_list = get_release_assets(repo_owner, repo_name, release_tag)
if assets_list:
    print(f"Assets for {repo_owner}/{repo_name} {release_tag}:")
    for asset in assets_list:
        print(asset)
else:
    print(f"Unable to retrieve assets for {repo_owner}/{repo_name} {release_tag}")
