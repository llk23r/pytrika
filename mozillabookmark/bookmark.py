#!/usr/bin/python3
import os


class BookMarkLocation(object):
    def __init__(self):
        self.firefox_bookmark_location = "{}/Library/Application Support/Firefox".format(
            os.environ['HOME'])

    def get_bookmark_location(self):
        for root, dirs, files in os.walk(self.firefox_bookmark_location):
            for file in files:
                if file.endswith("places.sqlite"):
                    return os.path.join(root, file)
