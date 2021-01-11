import requests
import json
from pprint import pprint
from datetime import datetime

USERNAME = 'nzoishie'
GITHUB_TOKEN = '4d349bfd02f405b839d80cc15aca5e81b0a67f7c'
BASE_URL = 'https://api.github.com'
HEADERS = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'accept': 'application/vnd.github.v3+json',
}

CREATE_DATE_CACHE = {}
COMMIT_CACHE = {}


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


def get_project_age(repo_url: str, sha1: str):
    create_date = None
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


if __name__ == '__main__':
    dataset_path = '../dataset/sstubs'
    with open(dataset_path) as file:
        i = 1
        entries = json.load(file)
        repo = entries[i]['projectName'].replace('.', '/')
        commit_sha1 = entries[i]['fixCommitSHA1']
        file_path = entries[i]['bugFilePath']

        # content = get_repo_tree(repo, commit_sha1)
        # pprint(f'Project Size: {len(content["tree"])}, Truncated: {content["truncated"]}')
        #
        # project_authors = get_num_devs(repo, commit_sha1)
        # file_authors = get_num_devs(repo, commit_sha1, file_path)
        # print(f'Project Authors: {project_authors}')
        # print(f'File Authors: {file_authors}')
        #
        # project_age = get_project_age(repo, commit_sha1)
        # print(f'Project Age: {project_age}')

        dev_exp = get_dev_exp_v2(repo, commit_sha1)
        print(f'Dev Experience: {dev_exp}')
