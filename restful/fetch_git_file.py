import gitlab
import subprocess


def main():
    gl = gitlab.Gitlab('http://lvyue.ncoppo.com:66/', private_token='-1PVzXdzAxzdzSYznSh2')

    projects = gl.projects.list(all=True, as_list=False)

    for project in projects:
        if 'ui' in project.name:
            git_url = project.http_url_to_repo
            subprocess.call(['git', 'clone', git_url])
    pass


if __name__ == '__main__':
    main()
