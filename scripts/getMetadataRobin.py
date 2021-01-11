import requests
import json
from pprint import pprint

USERNAME = 'nzoishie'
GITHUB_TOKEN = '4d349bfd02f405b839d80cc15aca5e81b0a67f7c'
BASE_URL = 'https://api.github.com'


def get_repo_tree(repo_url: str, sha1: str):
    url = f'{BASE_URL}/repos/{repo_url}/git/trees/{sha1}'
    response = requests.get(
        url=url,
        params={
            'recursive': '1'
        },
        headers={
            'Authorization': f'token {GITHUB_TOKEN}',
            'accept': 'application/vnd.github.v3+json',
        },
    )

    return response.json()


if __name__ == '__main__':
    dataset_path = '../dataset/sstubs'
    with open(dataset_path) as file:
        entries = json.load(file)
        repo = entries[0]['projectName'].replace('.', '/')
        commit_sha1 = entries[0]['fixCommitSHA1']
        content = get_repo_tree(repo, commit_sha1)

        pprint(f'Project Size: {len(content["tree"])}, Truncated: {content["truncated"]}')
