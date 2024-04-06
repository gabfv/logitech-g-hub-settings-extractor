# Logitech G Hub settings extractor

This is a small python tool to extract the json file stored inside the "settings.db" file of the Logitech G Hub app. This allows you to update the json and then replace the file blob inside the db with the new json.

## Requirements

Tested on Windows and macOS.

You need [Python](https://www.python.org/downloads/) installed. I've tested with 3.9 but I think 2.x versions should work too.

## How to use

Simply follow the instructions after executing the py file.

In summary:
It extracts the JSON. It asks you to close Logitech G Hub then, once it's done, you can press Enter to continue.
The script open it into your editor (the default app per OS settings for json files, or the OS will let ask you what to open it with). You edit the file as you like. Then, you save the file and close the editor.
As soon as you close the editor, it automatically insert the modified JSON into Logitech G Hub sqlite db. When you open Logitech G Hub again, it should reflects the changes you've made.

## Script parameters (all are optional)

```
usage: G Hub Settings Extractor [-h] [-d DB_PATH] [-s SETTINGS_PATH]

Extract and replace the settings.json inside the settings.db used by Logitech G Hub.

options:
  -h, --help            show this help message and exit
  -d DB_PATH, --db_path DB_PATH
                        Path to an alternate settings.db file to edit. The result will not be written back to this file but in the default LGHUB settings folder (unless one has been provided with -s(--settings_path)).
  -s SETTINGS_PATH, --settings_path SETTINGS_PATH
                        Path to the LGHUB settings folder
```

### Windows

In a cmd or PowerShell window, type the following in the same folder as the py file.

(You can "Shift+Right Click" into an explorer window to open a cmd/PowerShell window in the same folder):

```
python ghub-settings.py
```

### macOS

Open [Terminal](https://support.apple.com/guide/terminal/open-or-quit-terminal-apd5265185d-f365-44cb-8b09-71a064a42125/mac)

```
cd path/where/you/downloaded/the/py/file
python ghub-settings.py
```
