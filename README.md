# Logitech G Hub settings extractor

This is a small python tool to extract the json file stored inside the "settings.db" file of the Logitech G Hub app. This allows you to update the json and then replace the file blob inside the db with the new json.

## Requirements

Tested on Windows and macOS.

You need [Python](https://www.python.org/downloads/) installed. I've tested with 3.9 but I think 2.x versions should work too.

## How to use

Simply follow the instructions after executing the py file.

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
