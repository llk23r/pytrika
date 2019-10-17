import json
import os
import platform
import argparse


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
    return os.getcwd().split('/')[-1]


def _write_bookmark(current_project_bookmark, links):
    for index, each_bookmark in enumerate(current_project_bookmark):
        number = index + 1
        name = each_bookmark['name']
        url = each_bookmark['url']
        link = "\n{} - {} \n {}\n".format(number, name, url)
        links.write(link)


def create_the_document():
    bookmark_collection = _get_current_bookmark_collection()
    with open('bookmark_links', 'w') as links:
        for each_bookmark in bookmark_collection:
            if "children" in each_bookmark and _get_current_project() == each_bookmark['name']:
                current_project_bookmark = each_bookmark['children']
            else:
                continue
            _write_bookmark(current_project_bookmark, links)
    with open('bookmark_links', 'r') as bml:
        print(bml.read())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-flv", "--flavor", dest="flavor",
                        default="chrome", help="flavor")
    args = parser.parse_args()
    create_the_document()
