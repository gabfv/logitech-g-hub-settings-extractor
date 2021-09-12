#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Part of this program was made with code from:
# https://pynative.com/python-sqlite-blob-insert-and-retrieve-digital-data/

import os
import sqlite3

DEFAULT_FOLDER_LG_GHUB_SETTINGS = os.path.expandvars('%LOCALAPPDATA%/LGHUB/')  # Must end with /
DEFAULT_FILENAME_SETTINGS_DB = 'settings.db'
DEFAULT_FILENAME_SETTINGS_JSON = 'EDIT_ME.json'
DEFAULT_PATH_SETTINGS_DB = DEFAULT_FOLDER_LG_GHUB_SETTINGS + DEFAULT_FILENAME_SETTINGS_DB


# def getLatestId(file_path):
#    try:


def write_to_file(data, file_path):
    # Convert binary data to proper format and write it on Hard Disk
    try:
        with open(file_path, 'wb') as file:
            file.write(data)
        print("Stored blob data into: ", file_path, "\n")
    except Exception as error:
        error_message = """
Failed to write the following file:
{file_path}
Error:
{exception_message}
        """
        print(error_message.format(file_path=file_path, exception_message=error))


def read_blob_data(data_id, file_path):
    try:
        sqlite_connection = sqlite3.connect(file_path)
        cursor = sqlite_connection.cursor()
        print("Connected to SQLite")

        sql_fetch_blob_query = """SELECT _id, FILE from DATA where _id = ?"""
        cursor.execute(sql_fetch_blob_query, (data_id,))
        record = cursor.fetchall()
        settings_file_path = DEFAULT_FOLDER_LG_GHUB_SETTINGS + DEFAULT_FILENAME_SETTINGS_JSON
        for row in record:
            print("Id = ", row[0])
            settings_data = row[1]
            write_to_file(settings_data, settings_file_path)
        cursor.close()

        return settings_file_path
    except sqlite3.Error as error:
        print("Failed to read blob data from sqlite table", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("sqlite connection is closed")


if __name__ == '__main__':
    if not os.path.exists(DEFAULT_PATH_SETTINGS_DB):
        failure_to_find_settings_db = """
ERROR: The file settings.db was not found! The path below was checked:
{path}
Quitting...
        """
        print(failure_to_find_settings_db.format(path=DEFAULT_PATH_SETTINGS_DB))
        exit(10)

    program_introduction_notification = """
This program is intended to extract and replace the settings.json inside the settings.db used by Logitech G Hub.
 
Press Enter to continue.
    """
    print(program_introduction_notification)
    input()
    print("This program will extract the settings from the database...")
    file_written = read_blob_data(1, DEFAULT_PATH_SETTINGS_DB)
    print("The extracted file will be open after you press Enter. Please edit it and don't forget to save the file!")
    input()
    os.system(file_written)
