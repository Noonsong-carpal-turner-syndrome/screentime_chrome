import csv
import os
import sqlite3
import sys
from datetime import datetime

# platform_table maps the name of user's OS to a platform code
platform_table = {
        'linux': 0,
        'linux2': 0,
        'darwin': 1,
        'cygwin': 2,
        'win32': 2,
        }

# it supports Linux, MacOS, and Windows platforms.
try:
    user_platformcode = platform_table[sys.platform]
except KeyError:
    class NotAvailableOS(Exception):
        pass
    raise NotAvailableOS("We only support windows")

    
def get_username() -> str:
    """
    Get username based on their local computers
    """
    platform_code = user_platformcode
    cwd_path = os.getcwd()
    cwd_path_list = []
    cwd_path_list = cwd_path.split('\\')    # windows only
    return cwd_path_list[2]


def get_database_paths() -> dict:
    """
    Get paths to the database of browsers and store them in a dictionary.
    It returns a dictionary: its key is the name of browser in str and its value is the path to database in str.
    """
    platform_code = user_platformcode
    browser_path_dict = dict()

    # windows only
    homepath = os.path.expanduser("~")
    abs_chrome_path = os.path.join(homepath, 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'History')
    abs_firefox_path = os.path.join(homepath, 'AppData', 'Roaming', 'Mozilla', 'Firefox', 'Profiles')
    abs_edge_path = os.path.join(homepath, 'AppData', 'Local', 'Microsoft', 'Edge', 'User Data', 'Default', 'History')
    # it creates string paths to broswer databases
    if os.path.exists(abs_chrome_path):
        browser_path_dict['chrome'] = abs_chrome_path
    if os.path.exists(abs_firefox_path):
        firefox_dir_list = os.listdir(abs_firefox_path)
        for f in firefox_dir_list:
            if f.find('.default') > 0:
                abs_firefox_path = os.path.join(abs_firefox_path, f, 'places.sqlite')
        if os.path.exists(abs_firefox_path):
            browser_path_dict['firefox'] = abs_firefox_path
    if os.path.exists(abs_edge_path):
        browser_path_dict['edge'] = abs_edge_path
   
    return browser_path_dict


def get_browserhistory() -> dict:
    """Get the user's browsers history by using sqlite3 module to connect to the dabases.
       It returns a dictionary: its key is a name of browser in str and its value is a list of
       tuples, each tuple contains four elements, including url, title, and visited_time. 
       Example
       -------
       >>> import browserhistory as bh
       >>> dict_obj = bh.get_browserhistory()
       >>> dict_obj.keys()
       >>> dict_keys(['edge', 'chrome', 'firefox'])
       >>> dict_obj['safari'][0]
       >>> ('https://mail.google.com', 'Mail', '2018-08-14 08:27:26')
    """
    # browserhistory is a dictionary that stores the query results based on the name of browsers.
    browserhistory = {}

    # call get_database_paths() to get database paths.
    paths2databases = get_database_paths()

    for browser, path in paths2databases.items():
        try:
            conn = sqlite3.connect(path)
            cursor = conn.cursor()
            _SQL = ''
            # SQL command for browsers' database table
            if browser == 'chrome':
                _SQL = """SELECT url, title, datetime((last_visit_time/1000000)-11644473600, 'unixepoch', 'localtime') 
                                    AS last_visit_time FROM urls ORDER BY last_visit_time DESC"""
            elif browser == 'firefox':
                _SQL = """SELECT url, title, datetime((visit_date/1000000), 'unixepoch', 'localtime') AS visit_date 
                                    FROM moz_places INNER JOIN moz_historyvisits on moz_historyvisits.place_id = moz_places.id ORDER BY visit_date DESC"""
            elif browser == 'safari':
                _SQL = """SELECT url, title, datetime(visit_time + 978307200, 'unixepoch', 'localtime') 
                                    FROM history_visits INNER JOIN history_items ON history_items.id = history_visits.history_item ORDER BY visit_time DESC"""
            elif browser == 'edge':
                _SQL = """SELECT url, title, datetime((last_visit_time/1000000)-11644473600, 'unixepoch', 'localtime') 
                                    AS last_visit_time FROM urls ORDER BY last_visit_time DESC"""
            else:
                pass
            # query_result will store the result of query
            query_result = []
            try:
                cursor.execute(_SQL)
                # cursor.execute("""SELECT * FROM urls ORDER BY last_visit_time DESC""")
                query_result = cursor.fetchall()
            except sqlite3.OperationalError:
                print('* Notification * ')
                print('Please Completely Close ' + browser.upper() + ' Window')
            except Exception as err:
                print(err)
            # close cursor and connector
            cursor.close()
            conn.close()
            # put the query result based on the name of browsers.
            browserhistory[browser] = query_result
        except sqlite3.OperationalError:
            print('* ' + browser.upper() + ' Database Permission Denied.')

    return browserhistory


def write_browserhistory_csv() -> None:
    """It writes csv files that contain the browser history in
    the current working directory. It will writes csv files base on
    the name of browsers the program detects."""

    browserhistory = get_browserhistory()
    for browser, history in browserhistory.items():
        with open(browser + '_history.csv', mode='w', encoding='utf-8', newline='') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=',',
                            quoting=csv.QUOTE_ALL)
            for data in history:
                csv_writer.writerow(data)

write_browserhistory_csv()