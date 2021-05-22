from scraper_requests import main as scraper_main
from nas_api import main as nas_main
import os
from datetime import datetime
import time

## Download the excel file from Qteam website to data folder
payload = scraper_main()

file_name = f'overzicht_vloot_banden_{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}.xls'

## Save downloaded excel file to Synology NAS server and remove file locally
path_of_parent_folder_on_nas = '/NAS storage/Stefan/Werk/qteam_banden_excels'
nas_main(payload, file_name, path_of_parent_folder_on_nas)
