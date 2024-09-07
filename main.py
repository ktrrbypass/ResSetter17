from exploit.restore import restore_file
from pathlib import Path
import plistlib
import sys
import requests
from bs4 import BeautifulSoup


def generate_plist(file_name, height, width):
    plist_dict = {
        'canvas_height': str(height),
        'canvas_width': str(width)
    }
    with open(file_name, 'wb') as file:
        plistlib.dump(plist_dict, file)

def scrape_iphone_resolution(model):
    response = requests.get('https://www.ios-resolution.com/')
    soup = BeautifulSoup(response.content, 'html.parser')
    tables = soup.find_all('table')

    for table in tables:
        rows = table.find_all('tr')
        for row in rows[1:]:
            columns = row.find_all('td')
            if len(columns) >= 3:
                current_model = columns[0].text.strip()
                if current_model.lower() == model.lower():
                    width = ''.join(filter(str.isdigit, columns[3].text.strip()))
                    height = ''.join(filter(str.isdigit, columns[4].text.strip()))
                    with open(plist_path, 'rb') as plist_file:
                        plist_data = plistlib.load(plist_file)

                    plist_data['canvas_height'] = str(height)
                    plist_data['canvas_width'] = str(width)
                    
                    with open(plist_path, 'wb') as plist_file:
                        plistlib.dump(plist_data, plist_file)

plist_path = Path.joinpath(Path.cwd(), 'com.apple.iokit.IOMobileGraphicsFamily.plist')

print(r'''__________                   _________         __     __                  ____ _________ 
\______   \  ____    ______ /   _____/  ____ _/  |_ _/  |_   ____ _______/_   |\______  \
 |       _/_/ __ \  /  ___/ \_____  \ _/ __ \\   __\\   __\_/ __ \\_  __ \|   |    /    /
 |    |   \\  ___/  \___ \  /        \\  ___/ |  |   |  |  \  ___/ |  | \/|   |   /    / 
 |____|_  / \___  >/____  >/_______  / \___  >|__|   |__|   \___  >|__|   |___|  /____/  
        \/      \/      \/         \/      \/                   \/                       
''')
input("Press Enter to continue... ")

choice = input("Would you like to restore a default plist or customize one? (restore/customize): ")

if choice.lower() == 'restore':
    model_input = input('Enter iPhone model, (e.g. iPhone 12 Pro Max): ')
    scrape_iphone_resolution(model_input)
    input("Plist file successfully generated. Press Enter to begin write... ")
    restore_file(fp=plist_path, restore_path=f'/var/mobile/Library/Preferences/', restore_name='com.apple.iokit.IOMobileGraphicsFamily.plist')
    sys.exit()

if choice.lower() == 'customize':
    pass

print('Generating plist file... '); generate_plist('com.apple.iokit.IOMobileGraphicsFamily.plist', 'height', 'width')

input("The plist file has been generated with default values. Press enter to continue... ")

height = int(input("Enter the height of the resolution: "))
width = int(input("Enter the width of the resolution: "))

with open(plist_path, 'rb') as plist_file:
    plist_data = plistlib.load(plist_file)

plist_data['canvas_height'] = str(height)
plist_data['canvas_width'] = str(width)

with open(plist_path, 'wb') as plist_file:
    plistlib.dump(plist_data, plist_file)
input("The plist file has been generated with selected values. Press enter to begin to write... ")   
restore_file(fp=plist_path, restore_path=f'/var/mobile/Library/Preferences/', restore_name='com.apple.iokit.IOMobileGraphicsFamily.plist')
