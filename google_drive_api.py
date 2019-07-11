from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pydrive.files import GoogleDriveFile
import json

gauth = GoogleAuth()
gauth.LocalWebserverAuth() # Creates local webserver and auto handles authentication.

drive = GoogleDrive(gauth)

def upload_file(folder_name,filetype,filename):
    with open('Gdrive_Config.json','r') as Config:
        data = json.load(Config)
        folder_id = data['Folder_Id'][folder_name]
        list_permission = data['List_Permission']
    # Create Google Drive instance in Folder
        file1 = drive.CreateFile({'title': '{}.{}'.format(filename,filetype),'parents':[{'id':folder_id}]})
        file1.SetContentFile('data/{}.{}'.format(filename,filetype))
        file1.Upload() # Upload the file.
        file1['shareable'] = False
        Config.close()
        return file1['title'],file1['alternateLink']
    ### return data to store on Database or Line_FlexMessage

def upload_file_with_permission(folder_name,filetype,filename):
    with open('Gdrive_Config.json','r') as Config:
        data = json.load(Config)
        folder_id = data['Folder_Id'][folder_name]
        list_permission = data['List_Permission']
    # Create Google Drive instance in Folder
        file1 = drive.CreateFile({'title': '{}.{}'.format(filename,filetype),'parents':[{'id':folder_id}]})
        file1.SetContentFile('data/{}.{}'.format(filename,filetype))
        file1.Upload() # Upload the file.
        permission = file1.InsertPermission({
                            'type': 'user',
                            'value': list_permission,
                            'role': 'reader','withLink': False})
        file1['shareable'] = False
        Config.close()
        return file1['title'],file1['alternateLink']
        ### return data to store on Database or Line_FlexMessage

### Get or Update File List in Fodler Name
def GetFile_FromDrive(folder_name):
    All_file_in_folder = {}
    with open('Gdrive_Config.json','r') as Config:
        data = json.load(Config)
        folder_id = data['Folder_Id'][folder_name]
        file_list = drive.ListFile({'q': folder_id}).GetList()
        for i,file1 in enumerate(file_list):
            New_Dict = {i : {"file_name" : file1['title'] , "file_Link" : file1['alternateLink']}}
            New_Dict.update(New_Dict)
        Config.close()
    return All_file_in_folder
### return as json ready to convert into Flex Message List



### use inside Setup_Gdrive method
def Create_directory(name,Type='Public'):
    data = ""
    with open('Gdrive_Config.json','r') as Config:
        data = json.load(Config)
        Config.close()
        Folder = drive.CreateFile({'title': name,'mimeType' : 'application/vnd.google-apps.folder'})
        if Type == 'Private':
            Folder.Upload()
            Folder['shareable'] = False
            data['Folder_Id'][name] = Folder['id']
            print(data['Folder_Id'][name])
            
        
        elif Type == 'Public':
            Folder.Upload()
            Folder['shareable'] = True
            data['Folder_Id'][name] = Folder['id']
            print(data['Folder_Id'][name])
    print(data)
    with open('Gdrive_Config.json','w') as Config:
        json.dump(data,Config)
        Config.close()

#### SET UP ALL FOLDER AND DIRECTORIES

def SetUp_Gdrive_Directory():
    data = ""
    with open('Gdrive_Config.json','r') as Config:
        data = json.load(Config)
        Config.close()
        if data['Create_directory'] == "False" :
            ### Public Folder
            for i in data['Public_Folder']:
                print(i)
                Create_directory(i,Type='Public')
            
            ### Public Folder
            for i in data['Private_Folder']:
                print(i)
                Create_directory(i,Type='Private')
            data['Create_directory'] = "True"
        else :
            data['Create_directory'] = "True"
            return print('directories has been Created')
    with open('Gdrive_Config.json','w') as Config:
        data = json.dump(data,Config,indent=4)
        Config.close()
    
    
if __name__ == '__main__':
    #### create folder ได้แต่ไม่สามารถ เก็บค่า id ได้
    SetUp_Gdrive_Directory()

