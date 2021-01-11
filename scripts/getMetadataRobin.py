import requests
import json
from pprint import pprint

USERNAME = 'nzoishie'
GITHUB_TOKEN = '4d349bfd02f405b839d80cc15aca5e81b0a67f7c'
BASE_URL = 'https://api.github.com'
HEADERS = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'accept': 'application/vnd.github.v3+json',
}


def get_repo_tree(repo_url: str, sha1: str):
    url = f'{BASE_URL}/repos/{repo_url}/git/trees/{sha1}'
    response = requests.get(
        url=url,
        params={
            'recursive': '1'
        },
        headers=HEADERS,
    )

    return response.json()


def get_num_devs(repo_url: str, sha1: str, file: str = None):
    url = f'{BASE_URL}/repos/{repo_url}/commits'
    params = {'sha': sha1}
    if file is not None:
        params['path'] = file
    response = requests.get(
        url=url,
        params=params,
        headers=HEADERS
    )

    content = response.json()
    unq_authors = set()
    for entry in content:
        unq_authors.add(entry['commit']['author']['email'])
    return len(unq_authors)


if __name__ == '__main__':
    dataset_path = '../dataset/sstubs'
    with open(dataset_path) as file:
        entries = json.load(file)
        repo = entries[0]['projectName'].replace('.', '/')
        commit_sha1 = entries[0]['fixCommitSHA1']
        file_path = entries[0]['bugFilePath']
        content = get_repo_tree(repo, commit_sha1)

        pprint(f'Project Size: {len(content["tree"])}, Truncated: {content["truncated"]}')

        project_authors = get_num_devs(repo, commit_sha1)
        file_authors = get_num_devs(repo, commit_sha1, file_path)

        print(f'Project Authors: {project_authors}')
        print(f'File Authors: {file_authors}')
