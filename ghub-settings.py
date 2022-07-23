#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Part of this program was made with code from:
# https://pynative.com/python-sqlite-blob-insert-and-retrieve-digital-data/

import datetime
import os
import sys
import shutil
import sqlite3

DEFAULT_FOLDER_LG_GHUB_SETTINGS = None

if sys.platform.startswith('win'): # Windows
    DEFAULT_FOLDER_LG_GHUB_SETTINGS = os.path.expandvars('%LOCALAPPDATA%/LGHUB/') # Must end with /
elif sys.platform.startswith('darwin'): # MacOS
    DEFAULT_FOLDER_LG_GHUB_SETTINGS = os.path.expandvars('$HOME/Library/Application Support/lghub/') # Must end with /
else:
    error_message = """
ERROR: Unsupported platform
{platform}
    """
    print(error_message.format(platform=sys.platform))
    exit(1)

DEFAULT_FILENAME_SETTINGS_DB = 'settings.db'
DEFAULT_FILENAME_SETTINGS_JSON = 'EDIT_ME.json'
DEFAULT_PATH_SETTINGS_DB = DEFAULT_FOLDER_LG_GHUB_SETTINGS + DEFAULT_FILENAME_SETTINGS_DB


def make_backup(file_path):
    backup_file_path = file_path + datetime.datetime.now().strftime('.%Y-%m-%d_%H-%M-%S')
    try:
        shutil.copy(file_path, backup_file_path)
        backup_message = """
A backup of the settings.db file has been made to:
{backup_file_path}        
        """
        print(backup_message.format(backup_file_path=backup_file_path))
    except Exception as error:
        error_message = """
ERROR: Failed to make a backup of the settings.db file! From:
{source_path}
To:
{destination_path}
Since this is a critical failure, the program will quit.
Error:
{exception_message}
        """
        print(error_message.format(source_path=file_path, destination_path=backup_file_path, exception_message=error))
        exit(42)

def get_latest_id(file_path):
    sqlite_connection = 0
    try:
        sqlite_connection = sqlite3.connect(file_path)
        cursor = sqlite_connection.cursor()

        sql_get_latest_id = 'select MAX(_id) from DATA'
        cursor.execute(sql_get_latest_id)
        record = cursor.fetchall()
        latest_id = record[0][0]

        return latest_id
    except sqlite3.Error as error:
        error_message = """
ERROR: Failed to read latest id from the table inside settings.db file:
{file_path}
This program will quit.
Error:
{exception_message}
        """
        print(error_message.format(file_path=file_path, exception_message=error))
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def write_to_file(data, file_path):
    # Convert binary data to proper format and write it on Hard Disk
    try:
        with open(file_path, 'wb') as file:
            file.write(data)
        print("Stored blob data into: ", file_path, "\n")
    except Exception as error:
        error_message = """
ERROR: Failed to write the following file:
{file_path}
Error:
{exception_message}
        """
        print(error_message.format(file_path=file_path, exception_message=error))


def read_blob_data(data_id, file_path):
    sqlite_connection = 0
    try:
        sqlite_connection = sqlite3.connect(file_path)
        cursor = sqlite_connection.cursor()

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


def convert_to_binary_data(file_path):
    try:
        with open(file_path, 'rb') as file:
            blob_data = file.read()
        return blob_data
    except Exception as error:
        error_message = """
ERROR: Failed to read the following file:
{file_path}
This program will quit.
Error:
{exception_message}
        """
        print(error_message.format(file_path=file_path, exception_message=error))
        exit(24)


def insert_blob(data_id, updated_settings_file_path, db_file_path):
    sqlite_connection = 0
    try:
        sqlite_connection = sqlite3.connect(db_file_path)
        cursor = sqlite_connection.cursor()
        sqlite_replace_blob_query = """ Replace INTO DATA
                                  (_id, _date_created, FILE) VALUES (?, ?, ?)"""

        blob = convert_to_binary_data(updated_settings_file_path)
        # Convert data into tuple format
        data_tuple = (data_id, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), blob)
        cursor.execute(sqlite_replace_blob_query, data_tuple)
        sqlite_connection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


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
    latest_id = get_latest_id(DEFAULT_PATH_SETTINGS_DB)
    file_written = read_blob_data(latest_id, DEFAULT_PATH_SETTINGS_DB)
    make_backup(DEFAULT_PATH_SETTINGS_DB)
    print("IMPORTANT: PLEASE CLOSE LG G HUB NOW")
    print("The extracted file will be open after you press Enter.")
    print("Please edit it and don't forget to save the file then close the file (and the program that opened with)")
    input()
    if sys.platform.startswith('win'): # Windows
        os.system(file_written)
    elif sys.platform.startswith('darwin'): # MacOS
        os.system('open "' + file_written + '"')
    else:
        print(file_written)
    insert_blob(latest_id, file_written, DEFAULT_PATH_SETTINGS_DB)
    print("The settings have been updated.")
    exit(0)
