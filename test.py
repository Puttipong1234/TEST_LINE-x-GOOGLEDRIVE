import json
import pprint
with open('Gdrive_Config copy.json','r') as data:
    json_data = json.load(data)
    a = json_data['Folder_Id']['drawing']['Submenu']['Submenu_id']

    print(a)