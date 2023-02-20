'''Can be used for quickly updating MS Edge, Google Chrome and Mozilla Firefox webdrivers.
   NOTE: For MS Edge, cannot be used if a version of webdriver isn't already installed (due to permission issues).
   NOTE: Chrome and Firefox aren't completely tested'''

import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.edge.service import Service as edgeservice
from selenium.webdriver.edge.options import Options as edgeoptions
from selenium.webdriver.chrome.service import Service as chromeservice
from selenium.webdriver.chrome.options import Options as chromeoptions
from selenium.webdriver.firefox.service import Service as firefoxservice
from selenium.webdriver.firefox.options import Options as firefoxoptions
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from zipp import zipfile
import os

def read_config():
    '''Read config.txt'''

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

    download_auto_confirm = config.readline().split('=')[1].strip().lower()
    download_auto_confirm = download_auto_confirm == 'true'
    print(edge_path, download_auto_confirm)
    return (edge_path, chrome_path, firefox_path, download_auto_confirm)

def check_version(current_version, latest_version):
    '''Compares current webdriver version with the latest version.
    If outdated, provides URL for the latest version.'''

    if browser_select == '3': #cannot compare for firefox due to unavailable current version check
        print('Current version check unavailable\nDownload latest geckodriver release below')
        lv_link = 'https://github.com/mozilla/geckodriver/releases/download/v' + latest_version + '/geckodriver-v' + latest_version + '-win32.zip'
        print(lv_link)
        return lv_link

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
            print(lv_link)
            return lv_link
    print("The latest version of webdriver is already installed")
    return

class msedge():

    def find_current_version(edge_path):
        '''Provides version of the currently installed MS Edge webdriver.'''

        opts = edgeoptions()
        opts.add_argument('--headless')
        opts.add_experimental_option('excludeSwitches', ['enable-logging']) #disable devtools listening
        try:
            driver = webdriver.Edge(options=opts, service=edgeservice(edge_path + "\msedgedriver.exe")) #apply options and start session (headless)
            current_version = driver.capabilities['msedge']['msedgedriverVersion'].split(' ')[0]
        except Exception as e:
            print(e)
            print("Edge webdriver not installed")
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

        opts = chromeoptions()
        opts.add_argument('--headless')
        opts.add_experimental_option('excludeSwitches', ['enable-logging']) #disable devtools listening

        try:
            driver = webdriver.Chrome(options=opts, service=chromeservice(chrome_path + "\chromedriver.exe")) #apply options and start session (headless)
            current_version = driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0]
        except Exception as e:
            print(e)
            print("Error")
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
        '''Provides version of the currently installed Google Chrome webdriver.'''
        opts = firefoxoptions()
        opts.binary_location = 'C:/Program Files/Mozilla Firefox/firefox.exe'
        opts.add_argument('--headless')
        #opts.add_experimental_option('excludeSwitches', ['enable-logging']) #disable devtools listening

        try:
            driver = webdriver.Firefox(options=opts, service=firefoxservice(firefox_path + "\geckodriver.exe"), log_path=None) #apply options and start session (headless)
            current_version = driver.capabilities['firefox']['moz:geckodriverVersion'].split(' ')[0]
        except Exception as e:
            print(e)
            print("Error")
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


edge_path, chrome_path, firefox_path, download_auto_confirm = read_config()

print('Select browser:-')
if edge_path != None:
    print('[1] MS Edge')
if chrome_path != None:
    print('[2] Google Chrome')
if firefox_path != None:
    print('[3] Mozilla Firefox (Current version check unavailable)')
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
    #current_version = firefox.find_current_version(firefox_path)
    latest_version = firefox.find_latest_version()
if browser_select == 'q':
    quit()


link = check_version(current_version, latest_version)

if (link != None):
    if current_version == None:
        if browser_select == '3': #current version check unavailable for firefox
            download_permission = input("Download [Y/N]?\n")
            download_permission = download_permission.lower()
            if download_permission == 'y':
                download_file(link, firefox_path)
                delete_file("Webdriver.zip")
                quit()
            elif download_permission == 'n':
                quit()
            else:
                print('Invalid response')
                quit()
    else:
        quit()

    if download_auto_confirm:
        if browser_select == '1':
            download_file(link, edge_path)
        if browser_select == '2':
            download_file(link, chrome_path)
        delete_file("Webdriver.zip")
    else:
        download_permission = input("Download [Y/N]?\n")
        download_permission = download_permission.lower()
        if download_permission == 'y':
            if browser_select == '1':
                download_file(link, edge_path)
            if browser_select == '2':
                download_file(link, chrome_path)

            delete_file("Webdriver.zip")

        elif download_permission == 'n':
            quit()
        else:
            print('Invalid response')