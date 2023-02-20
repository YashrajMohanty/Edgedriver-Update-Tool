'''Can be used for quickly updating MS Edge, Google Chrome and Mozilla Firefox webdrivers.
   NOTE: For MS Edge, cannot be used if a version of webdriver isn't already installed
   (due to permission issues).'''

import requests
from bs4 import BeautifulSoup as bs
from zipp import zipfile
import os
import subprocess

def read_config():
    '''Reads config.txt'''

    config = open("Config.txt", "r")
    edge_path = config.readline().split('=')[1].strip()
    chrome_path = config.readline().split('=')[1].strip()
    firefox_path = config.readline().split('=')[1].strip()
    if (not os.path.exists(edge_path)):
        edge_path = None
        print("Invalid Edge webdriver path. Set path in config.txt")
    if (not os.path.exists(chrome_path)):
        chrome_path = None
        print("Invalid Chrome webdriver path. Set path in config.txt")
    if (not os.path.exists(firefox_path)):
        firefox_path = None
        print("Invalid Firefox webdriver path. Set path in config.txt")

    print('Edge path: ' + edge_path + '\nChrome path: ' + chrome_path + '\nFirefox path: ' + firefox_path + '\n')
    return (edge_path, chrome_path, firefox_path)

def check_version(current_version, latest_version):
    '''Compares current webdriver version with the latest version.
    If outdated, provides URL for the latest version.'''

    cv = current_version.split('.')
    lv = latest_version.split('.')
    
    for i in range(len(cv)):
        if (int(cv[i]) >= int(lv[i])):
            continue
        else:
            print("Download latest stable webdriver release below")
            if browser_select == '1':
                lv_link = 'https://msedgedriver.azureedge.net/' + latest_version + '/edgedriver_win64.zip'
            if browser_select == '2':
                lv_link = 'https://chromedriver.storage.googleapis.com/' + latest_version + '/chromedriver_win32.zip'
            if browser_select == '3':
                lv_link = 'https://github.com/mozilla/geckodriver/releases/download/v' + latest_version + '/geckodriver-v' + latest_version + '-win32.zip'
            print(lv_link)
            return lv_link
    print("The latest version of webdriver is already installed")
    return

class msedge():

    def find_current_version(edge_path):
        '''Provides version of the currently installed MS Edge webdriver.'''
        version_cmd = edge_path + '\msedgedriver -v'
        try:
            current_version = str(subprocess.check_output(version_cmd))
            current_version = current_version.split(' ')[3]
        except Exception as e:
            print("ERROR:", e)
            quit()
        print('Edge webdriver current version:', current_version)
        return current_version

    def find_latest_version():
        '''Provides the latest MS Edge webdriver version'''

        r = requests.get('https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver') #edge webdriver site
        #print(r) # response
        parsed_html = bs(r.text, features='html.parser') #parse html code
        latest_version = parsed_html.body.find('p', attrs={'class':'driver-download__meta'}).text #retrieve text
        latest_version = latest_version[9:-23].split(':')[0] #slicing string to get version number
        print("Edge webdriver latest release:", latest_version) #print version number
        return latest_version

class chrome():

    def find_current_version(chrome_path):
        '''Provides version of the currently installed Google Chrome webdriver.'''
        version_cmd = chrome_path + '\chromedriver -v'
        try:
            current_version = str(subprocess.check_output(version_cmd))
            current_version = current_version.split(' ')[1]
        except Exception as e:
            print("ERROR:", e)
            quit()
        print('Chrome webdriver current version:', current_version)
        return current_version

    def find_latest_version():
        '''Provides the latest Google Chrome webdriver version'''

        r = requests.get('https://chromedriver.chromium.org/downloads') #edge webdriver site
        #print(r) # response
        parsed_html = bs(r.text, features='html.parser') #parse html code
        latest_version = parsed_html.body.find('a', attrs={'class':'XqQF9c'}).text #retrieve text
        latest_version = latest_version[13:] #slicing string to get version number
        print("Chrome webdriver latest release:", latest_version) #print version number
        return latest_version

class firefox():

    def find_current_version(firefox_path):
        '''Provides version of the currently installed Firefox geckodriver.'''
        version_cmd = firefox_path + '\geckodriver --version'
        try:
            current_version = str(subprocess.check_output(version_cmd))
            current_version = current_version.split(' ')[1]
        except Exception as e:
            print("ERROR:", e)
            quit()
        print('Firefox webdriver current version:', current_version)
        return current_version

    def find_latest_version():
        '''Provides the latest firefox webdriver(geckodriver) version'''

        r = requests.get('https://github.com/mozilla/geckodriver/releases') #edge webdriver site
        #print(r) # response
        parsed_html = bs(r.text, features='html.parser') #parse html code
        latest_version = parsed_html.body.find('a', attrs={'class':'Link--primary'}).text #retrieve text
        print("Firefox webdriver latest release:", latest_version) #print version number
        return latest_version


def download_file(link, path):
    '''Download the request object (latest webdriver version)
    as a zip file and install it in the given directory (edge_path)'''

    print('Initiated download')
    update_request = requests.get(link, stream=True) #edge webdriver download
    #update_request.raise_for_status()
    f = open("Webdriver.zip", "wb")

    for chunk in update_request.iter_content(chunk_size=5*(10**6)): # 5MB chunk size
    #f.write(update_request.content)
        f.write(chunk)
        f.flush()

    f.close
    print('Download complete')
    zfile = zipfile.ZipFile('Webdriver.zip')
    zfile.extractall(path)
    print('Installation complete')
    return

def delete_file(filename):
    '''Delete the zip file after installation'''

    if os.path.exists(filename):
        os.remove(filename)
        print("Cleanup successful")
    else:
        print("File does not exist.")
    return


edge_path, chrome_path, firefox_path = read_config()

print('Select browser:-')
if edge_path != None:
    print('[1] MS Edge')
if chrome_path != None:
    print('[2] Google Chrome')
if firefox_path != None:
    print('[3] Mozilla Firefox')
print('[Q] Quit')

browser_select = input().lower()
current_version = None
latest_version = None

if browser_select == '1':
    current_version = msedge.find_current_version(edge_path)
    latest_version = msedge.find_latest_version()
if browser_select == '2':
    current_version = chrome.find_current_version(chrome_path)
    latest_version = chrome.find_latest_version()
if browser_select == '3': #current version check unavailable
    current_version = firefox.find_current_version(firefox_path)
    latest_version = firefox.find_latest_version()
if browser_select == 'q':
    print('Exiting')
    quit()


link = check_version(current_version, latest_version)

if (link != None) and (current_version != None):

        download_permission = input("Download [Y/N]?\n")
        download_permission = download_permission.lower()
        if download_permission == 'y':
            if browser_select == '1':
                download_file(link, edge_path)
            if browser_select == '2':
                download_file(link, chrome_path)
            if browser_select == '3':
                download_file(link, firefox_path)
            delete_file("Webdriver.zip")

        else:
            print('Error encountered. Exiting')
            quit()