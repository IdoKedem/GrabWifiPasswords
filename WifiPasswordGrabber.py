import os
from bs4 import BeautifulSoup
import glob
import time


cwd = os.getcwd()
passwords_dir = fr"{cwd}\Passwords"

print("Looking for directory...")
if not os.path.exists(passwords_dir):
    print("Directory not found")
    os.mkdir(passwords_dir)
    print("Creating directory...")
else:
    print('Directory Found')

os.popen(f'netsh wlan export profile folder={passwords_dir} key=clear')
print('Grabbing Passwords...')
time.sleep(2)

file_names = glob.glob(fr'{passwords_dir}\*.xml')

print("Creating output file...")
with open(fr'{passwords_dir}\passwords.txt', 'a') as f:
    password_counter = 0
    if not file_names:
        print("Wifi profiles not found")
    else:
        for filename in file_names:
            with open(filename, 'r') as xml_file:
                xml_data = xml_file.read()
                bs_data = BeautifulSoup(xml_data, 'xml')

            ssid = bs_data.find('name').text

            if not bs_data.find('keyMaterial'):
                continue
            password = bs_data.find('keyMaterial').text

            credentials = f'{ssid} = {password} \n'
            f.write(credentials)
            password_counter += 1
            print(f'Got {password_counter} passwords!')

    print('Finished Successfully')


time.sleep(5)
