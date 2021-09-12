#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Part of this program was made with code from:
# https://pynative.com/python-sqlite-blob-insert-and-retrieve-digital-data/

import os
import sqlite3

DEFAULT_PATH_SETTINGS_DB = os.path.expandvars('%LOCALAPPDATA%/LGHUB/settings.db')

if __name__ == '__main__':
    program_introduction_notification = """
    This program is intended to extract and replace the settings.json inside the settings.db used by Logitech G Hub. 
    Press Enter to continue.
    """
    print(program_introduction_notification)

    # TODO: press enter notification

    if not os.path.exists(DEFAULT_PATH_SETTINGS_DB):
        failure_to_find_settings_db = """
        ERROR: The file settings.db was not found! The path below was checked:
        {path}
        Quitting...
        """
        print(failure_to_find_settings_db.format(path=DEFAULT_PATH_SETTINGS_DB))
        exit(10)


def writeTofile(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)
    print("Stored blob data into: ", filename, "\n")


def readBlobData(empId):
    try:
        sqlite_connection = sqlite3.connect('SQLite_Python.db')
        cursor = sqlite_connection.cursor()
        print("Connected to SQLite")

        sql_fetch_blob_query = """SELECT * from new_employee where id = ?"""
        cursor.execute(sql_fetch_blob_query, (empId,))
        record = cursor.fetchall()
        for row in record:
            print("Id = ", row[0], "Name = ", row[1])
            name = row[1]
            photo = row[2]
            resumeFile = row[3]

            print("Storing employee image and resume on disk \n")
            photoPath = "E:\pynative\Python\photos\db_data\\" + name + ".jpg"
            resumePath = "E:\pynative\Python\photos\db_data\\" + name + "_resume.txt"
            writeTofile(photo, photoPath)
            writeTofile(resumeFile, resumePath)

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read blob data from sqlite table", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("sqlite connection is closed")
