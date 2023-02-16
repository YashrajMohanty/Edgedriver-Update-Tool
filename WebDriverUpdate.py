'''Can be used for quickly updating MS Edge webdrivers.
   Cannot be used if a version of webdriver isn't already installed.'''

import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from zipp import zipfile
import os

def read_config():
    '''Read config.txt'''

    config = open("Config.txt", "r")
    edge_path = config.readline().split('=')[1].strip()
    if (not os.path.exists(edge_path)):
        print("Invalid path. Set path in config.txt")
        quit()
    download_auto_confirm = config.readline().split('=')[1].strip().lower()
    download_auto_confirm = download_auto_confirm == 'true'
    print(edge_path, download_auto_confirm)
    return (edge_path, download_auto_confirm)

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
            lv_link = 'https://msedgedriver.azureedge.net/' + latest_version + '/edgedriver_win64.zip'
            print(lv_link)
            return lv_link
    print("The latest version of webdriver is already installed")
    return

def find_current_version(edge_path):
    '''Provides version of the currently installed webdriver.'''

    opts = Options()
    opts.add_argument('--headless')
    opts.add_experimental_option('excludeSwitches', ['enable-logging']) #disable devtools listening
    try:
        driver = webdriver.Edge(options=opts, service=Service(edge_path + "\msedgedriver.exe")) #apply options and start session (headless)
        current_version = driver.capabilities['msedge']['msedgedriverVersion'].split(' ')[0]
    except:
        print("Webdriver not installed")
        quit()
    print('Current version:', current_version)
    return '110.0.1587.45'

def find_latest_version():
    '''Provides the latest webdriver version'''

    r = requests.get('https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver') #edge webdriver site
    #print(r) # response
    parsed_html = bs(r.text, features='html.parser') #parse html code
    latest_version = parsed_html.body.find('p', attrs={'class':'driver-download__meta'}).text #retrieve text
    latest_version = latest_version[9:-23] #slicing string to get version number
    print("Latest Stable Release:", latest_version) #print version number
    return latest_version

def download_file(link, edge_path):
    '''Download the request object (latest webdriver version)
    as a zip file and install it in the given directory (edge_path)'''

    print('Initiated download')
    update_request = requests.get(link, stream=True) #edge webdriver download
    #update_request.raise_for_status()
    f = open("Edge webdriver.zip", "wb")

    for chunk in update_request.iter_content(chunk_size=3*(10**6)): # 3MB chunk size
    #f.write(update_request.content)
        f.write(chunk)
        f.flush()

    f.close
    print('Download complete')
    zfile = zipfile.ZipFile('Edge webdriver.zip')
    zfile.extractall(edge_path)
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


edge_path, download_auto_confirm = read_config()
current_version = find_current_version(edge_path)
latest_version = find_latest_version()
link = check_version(current_version, latest_version)

if (link != None) and (current_version != None):
    if download_auto_confirm:
        download_file(link, edge_path)
        delete_file("Edge webdriver.zip")
    else:
        download_permission = input("Download [Y/N]?\n")
        download_permission = download_permission.lower()
        if download_permission == 'y':
            download_file(link, edge_path)
            delete_file("Edge webdriver.zip")
        elif download_permission == 'n':
            pass
        else:
            print('Invalid response')