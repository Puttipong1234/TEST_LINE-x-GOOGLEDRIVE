import json
data = ""

with open('Gdrive_Config.json','r') as Config:
    data = json.load(Config)
    data['Folder_Id']['projectinfo']='book'
    Config.close()
with open('Gdrive_Config.json','w') as Config:
    json.dump(data,Config)
    Config.close()