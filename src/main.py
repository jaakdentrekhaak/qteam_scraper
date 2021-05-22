from scraper_requests import main as scraper_main
from nas_api import main as nas_main
import os
from datetime import datetime
import time

## Download the excel file from Qteam website to data folder
scraper_main()


## Rename downloaded file to be unique (date + time)
data_path = f'{os.path.dirname(os.path.realpath(__file__))}/../data/'

# Wait for file to be recognized by os
it = 0
while it < 10 and len(os.listdir(data_path)) == 0 :
    time.sleep(0.5)
    it += 1

if it == 10:
    print('Downloaded file not found')
    exit()

file_name = os.listdir(data_path)[-1]
new_file_name = file_name.split('.xls')[0] + '_' + datetime.now().strftime("%d-%m-%Y_%H-%M-%S") + '.xls'
os.rename(data_path+file_name, data_path + new_file_name)


## Save downloaded excel file to Synology NAS server and remove file locally
path_of_parent_folder_on_nas = '/NAS storage/Stefan/Werk/qteam_banden_excels'
nas_main(data_path+new_file_name, path_of_parent_folder_on_nas)


## Delete downloaded file
os.remove(data_path+new_file_name)
