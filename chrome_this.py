import argparse
import json
import os
import platform
import subprocess

from termcolor import colored

import colorama
from colorama import Back, Fore, Style

colorama.init()


def _get_bookmark_location():
    home_path = os.environ["HOME"]
    if(platform.system() == 'Linux'):
        bookmark_location = "{}/.config/google-chrome/default/Bookmarks".format(
            home_path)
    elif(platform.system() == 'Darwin'):
        if args.flavor == 'chrome':
            bookmark_location = "{}/Library/Application Support/Google/Chrome/Default/Bookmarks".format(
                home_path)
        elif args.flavor == 'canary':
            bookmark_location = "{}/Library/Application Support/Google/Chrome Canary/Default/Bookmarks".format(
                home_path)
        else:
            print("{} flavor of chrome is not supported".format(args.flavor))
            raise Exception
    return bookmark_location


def _get_bookmark_collection():
    path = _get_bookmark_location()
    with open(path, "r") as file:
        bookmark_collection = file.read()
    return bookmark_collection


def _get_current_bookmark_collection():
    bookmark = json.loads(_get_bookmark_collection())
    current_bookmark_collection = bookmark['roots']['bookmark_bar']['children']
    return current_bookmark_collection


def _get_current_project():
    if not bool(args.git):
        return os.getcwd().split('/')[-1]
    repo_root = subprocess.Popen(['git', 'rev-parse', '--show-toplevel'],
                                 stdout=subprocess.PIPE).communicate()[0].rstrip().decode('utf-8')
    absolute_repo_root = repo_root.split('/')[-1]
    git_repo_root = f"{repo_root}/.git"
    with open(f"{git_repo_root}/HEAD", 'r') as file:
        ref = file.read()
        branch_name = ref.split('/')[-1]

    return f"{absolute_repo_root}::{branch_name}".strip()


def _write_bookmark(current_project_bookmark, links):
    for index, each_bookmark in enumerate(current_project_bookmark):
        number = index + 1
        name = each_bookmark['name']
        url = each_bookmark['url']
        link = "\n{} - {} \n {}\n".format(number, name, url)
        links.write(link)


def _git_handler(file_name):
    should_git_add = bool(args.ga)
    should_git_add_and_commit = bool(args.gac)
    if should_git_add or should_git_add_and_commit:
        try:
            git_add = subprocess.Popen(
                ['git', 'add', file_name], stdout=subprocess.PIPE)
            git_add.wait()
        except Exception as e:
            print(f"Could not add the file\n\n{e}")
            raise
        if should_git_add_and_commit:
            try:
                git_commit = subprocess.Popen(
                    ['git', 'commit', '-m', 'Add docklinks'], stdout=subprocess.PIPE)
                git_commit.wait()
                git_show = subprocess.Popen(
                    ['git', 'show', 'HEAD'], stdout=subprocess.PIPE).communicate()
                print(
                    colored(f"{git_show[0].rstrip().decode('utf-8')}", 'green', attrs=['bold']))
            except Exception as e:
                print(f"Could not commit changes\n\n{e}")
                raise


def create_the_document():
    curr_proj = _get_current_project()
    bookmark_collection = _get_current_bookmark_collection()
    is_a_git_repo = bool(args.git)
    file_name = f"bookmark_links_{curr_proj.split('::')[-1]}" if is_a_git_repo else 'bookmark_links'
    with open(file_name, 'w') as links:
        for each_bookmark in bookmark_collection:
            if "children" in each_bookmark and curr_proj == each_bookmark['name']:
                current_project_bookmark = each_bookmark['children']
            else:
                continue
            _write_bookmark(current_project_bookmark, links)

    with open(file_name, 'r') as bml:
        print(bml.read())

    if is_a_git_repo:
        _git_handler(file_name)


def _parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-flv", "--flavor", dest="flavor",
                        default="chrome", help="flavor")
    parser.add_argument("-g", "--git", dest="git", default=False, help="git")
    parser.add_argument("-ga", "--gitadd", dest="ga",
                        default=False, help="git add")
    parser.add_argument("-gac", "--gitaddcommit", dest="gac",
                        default=False, help="git add and commit")
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = _parse_arguments()
    create_the_document()
