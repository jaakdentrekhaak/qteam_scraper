# About
Author: Jens Putzeys  

This program scrapes a website (Qteam) for an Excel file with information about tires.  
Then it uploads this Excel file to a Synology NAS server.  

NOTE: I made this project and decided to upload it to Github. This is not meant to be used by anyone, but you can get ideas from this.

# How to use
Create a config.json file in the src-folder like this:  
```json
{
    "qteam": {
        "username": "",
        "password": ""
    },
    "synology": {
        "username": "",
        "password": "",
        "url": ""
    }
}
```
Fill in the username and password for the qteam website.  
Fill in the username and password for your synology account (username has to be url-encoded: e.g. Hello Günter -> Hello%20G%C3%BCnter).  
Enter the url for your synology NAS: E.g. https://myds.com:port  

Change the folder where the files are saved on the NAS in main.py > path_of_parent_folder_on_nas