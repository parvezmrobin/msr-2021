import os
from github import Github
import csv

token = os.getenv('GITHUB_TOKEN', '4d349bfd02f405b839d80cc15aca5e81b0a67f7c')
g = Github(token)


def extracting_repos():
    repos = []
    with open('../dataset/topJavaMavenProjects.csv', 'r') as file:
        count = 0
        reader = csv.reader(file)
        for row in reader:
            count = count + 1
            if count == 1:
                continue
            project_name = row[0][len("https://github.com/"):]
            repos.append(project_name)
        return repos


def extracting_attributes(repos):
    count = 0
    for repo in repos:
        count = count + 1
        if repo == 'b3log/solo':
            continue
        r = g.get_repo(repo)
        print(count, r.size, r.forks)


if __name__ == '__main__':
    projects = extracting_repos()
    extracting_attributes(projects)





