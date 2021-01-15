import requests
import json
from pprint import pprint
from datetime import datetime
import warnings
import pandas as pd

with open('../config.json') as configFile:
    GITHUB_TOKEN = json.load(configFile)['githubToken']
USERNAME = 'nzoishie'
BASE_URL = 'https://api.github.com'
HEADERS = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'accept': 'application/vnd.github.v3+json',
}

CREATE_DATE_CACHE = {}
COMMIT_CACHE = {}


def get_repo_size(repo_url: str, sha1: str):
    url = f'{BASE_URL}/repos/{repo_url}/git/trees/{sha1}'
    response = requests.get(
        url=url,
        params={
            'recursive': '1'
        },
        headers=HEADERS,
    )

    content = response.json()
    if content["truncated"]:
        warnings.warn(f'Truncated content for {repo_url}@{sha1}')
    return len(content["tree"])


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


def get_project_age(repo_url: str, sha1: str):
    if repo_url in CREATE_DATE_CACHE:
        create_date = CREATE_DATE_CACHE[repo_url]
    else:
        url = f'{BASE_URL}/repos/{repo_url}'
        response = requests.get(
            url=url,
            headers=HEADERS,
        )

        content = response.json()
        date = parse_datetime(content['created_at'])
        create_date = CREATE_DATE_CACHE[repo_url] = date

    url = f'{BASE_URL}/repos/{repo_url}/commits/{sha1}'
    response = requests.get(
        url=url,
        headers=HEADERS
    )

    content = response.json()
    commit_date = parse_datetime(content['commit']['author']['date'])
    return commit_date - create_date


def parse_datetime(date_string: str):
    return datetime.fromisoformat(date_string.replace('Z', ''))


def get_dev_exp(repo_url: str, sha1: str):
    url = f'{BASE_URL}/repos/{repo_url}/commits/{sha1}'
    response = requests.get(url=url, headers=HEADERS)

    content = response.json()
    username = content['author']['login']
    username = 'nzoishie'
    print('username', username)
    email = content['commit']['author']['email']

    org_url = f'{BASE_URL}/users/{username}/orgs'
    org_response = requests.get(url=org_url, headers=HEADERS)
    org_content = org_response.json()
    repo_urls = [
        f'{BASE_URL}/users/{username}/repos'
    ]
    for org_entry in org_content:
        repo_urls.append(org_entry['repos_url'])

    commit_urls = set()
    pprint(repo_urls)
    for repo_url in repo_urls:
        repo_response = requests.get(url=repo_url, headers=HEADERS)
        repo_content = repo_response.json()
        # the url is in format 'https://api.github.com/repos/tijsrademakers/activiti-jobexecutor/commits{/sha}'
        # remove '{/sha}' from the end of the url
        new_commit_urls = map(lambda commit: commit['commits_url'][:-6], repo_content)
        commit_urls = commit_urls.union(new_commit_urls)

    def filter_by_username(commit):
        if commit['author'] is not None:
            return commit['author']['login'].lower() == username.lower()
        return commit['commit']['author']['email'].lower() == email.lower()

    print(f'Total {len(commit_urls)} repos')
    commits = []
    i = 0
    for commit_url in commit_urls:
        print(i, commit_url)
        i += 1
        commit_response = requests.get(url=commit_url, headers=HEADERS)
        commit_content = commit_response.json()
        commits_of_author = filter(filter_by_username, commit_content)
        commits.extend(map(lambda commit: commit['sha'], commits_of_author))

    return len(commits)


def get_dev_exp_v2(repo_url: str, sha1: str):
    url = f'{BASE_URL}/repos/{repo_url}/commits/{sha1}'
    response = requests.get(url=url, headers=HEADERS)
    content = response.json()
    email = content['commit']['author']['email']

    commit_url = f'{BASE_URL}/repos/{repo_url}/commits'
    commit_response = requests.get(
        url=commit_url,
        params={'sha': sha1, 'author': email},
        headers=HEADERS,
    )
    commit_content = commit_response.json()
    total_commits_of_dev_in_repo = len(commit_content)
    return total_commits_of_dev_in_repo


def get_days_since_last_change(repo_url: str, sha1: str, parent_sha1: str):
    url = f'{BASE_URL}/repos/{repo_url}/commits/{sha1}'
    response = requests.get(url=url, headers=HEADERS)
    content = response.json()
    date1 = parse_datetime(content['commit']['author']['date'])

    url = f'{BASE_URL}/repos/{repo_url}/commits/{parent_sha1}'
    response = requests.get(url=url, headers=HEADERS)
    content = response.json()
    date2 = parse_datetime(content['commit']['author']['date'])

    return date1 - date2


if __name__ == '__main__':
    dataset_path = '../dataset/sstubs'
    with open(dataset_path, encoding='utf-8') as file:
        entries = json.load(file)
    print(f'Iterating over {len(entries)} entries')
    data = []
    for i, entry in enumerate(entries):
        print(i)
        repo = entry['projectName'].replace('.', '/')
        commit_sha1 = entry['fixCommitSHA1']
        parent_sha1 = entry['fixCommitParentSHA1']
        file_path = entry['bugFilePath']

        repo_size = get_repo_size(repo, commit_sha1)
        # print(f'Repo Size: {repo_size}')

        project_authors = get_num_devs(repo, commit_sha1)
        file_authors = get_num_devs(repo, commit_sha1, file_path)
        # print(f'Project Authors: {project_authors}')
        # print(f'File Authors: {file_authors}')

        project_age = get_project_age(repo, commit_sha1)
        # print(f'Project Age: {project_age}')

        dev_exp = get_dev_exp_v2(repo, commit_sha1)
        # print(f'Dev Experience: {dev_exp}')

        distance = get_days_since_last_change(repo, commit_sha1, parent_sha1)
        # print(f'Days since last change: {distance}')
        data.append([repo_size, project_authors, file_authors, project_age, dev_exp, distance])

    columns = ['repo_size', 'project_authors', 'file_authors', 'project_age', 'dev_exp', 'distance']
    df = pd.DataFrame(data=data, columns=columns)
    df.to_csv('../database/meta-data.csv', index=False)
