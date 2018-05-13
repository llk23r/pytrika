# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import sqlite3
from sqlite3 import Error

from mozillabookmark import bookmark
from currentproject import project


class DocumentThis(object):

    @classmethod
    def get_bookmark_location(cls):
        cls.db_file = bookmark.BookMarkLocation()
        return cls.db_file.get_bookmark_location()

    @classmethod
    def set_current_project(cls):
        cls.current_project = project.ProjectLocation()
        return cls.current_project.get_project_location()

    @classmethod
    def create_connection(cls):
        try:
            conn = sqlite3.connect(cls.get_bookmark_location())
            print("Connection established for {}".format(
                cls.set_current_project()))
            return conn
        except Error as e:
            print(e)

        return None

    @classmethod
    def filter_bookmark(cls, conn):
        cur = conn.cursor()
        query = "SELECT moz_bookmarks.title, moz_places.url\
                 FROM moz_places\
                JOIN moz_bookmarks ON (moz_places.id=moz_bookmarks.fk)\
                WHERE moz_bookmarks.parent = (\
                SELECT id FROM moz_bookmarks\
                WHERE moz_bookmarks.title= ? AND type=2)"
        result = cur.execute(query, [DocumentThis.set_current_project()])
        return result

    @classmethod
    def fetch_bookmark(cls, result, conn):
        book_dict = {}
        rows = cls.filter_bookmark(conn).fetchall()
        book_id = 1
        for row in rows:
            book_dict.update(
                {
                    '{}'.format(book_id):
                    {
                        "title": '{}'.format(row[0]),
                        "url": '{}'.format(row[1])
                    }
                }
            )
            book_id += 1

        with open('../doclinks.json', 'w') as links:
            json.dump(book_dict, links, sort_keys=True, indent=4)

    @classmethod
    def main(cls):
        connection = DocumentThis.create_connection()
        bookmarks = DocumentThis.filter_bookmark(connection)
        DocumentThis.fetch_bookmark(bookmarks, connection)


if __name__ == '__main__':
    DocumentThis.main()
