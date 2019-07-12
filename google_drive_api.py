from pydrive.drive import GoogleDrive
from pydrive.files import GoogleDriveFile
from pydrive.auth import GoogleAuth
import json


### requirement 
# - need file Gdrive_Config
# - need file Credential.txt to save credential (auto authenthication)
#      first time Credential.txt. can be blank 
#       after perfrom the Oauth .txt will be filled
#       To changing Production Credential.txt need new )Oauth perform

class Project_Gdrive():

    def __init__(self,Proejct_name):
        with open('Gdrive_Config.json','r') as Config:
            data = json.load(Config)
            Config.close()
        self.Proejct_name = Proejct_name
        self.data = data
### create instance google drive with authenthication
        
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()

        gauth.LoadCredentialsFile("credentials.txt")
        if gauth.credentials is None:
            gauth.LocalWebserverAuth()
        elif gauth.access_token_expired:
            gauth.Refresh()
        else:
            gauth.Authorize()

        gauth.SaveCredentialsFile("credentials.txt")

        self.drive = GoogleDrive(gauth)



    ### use inside Setup_Gdrive method
                
    def upload_file_Public(self,folder_name,filetype,filename):
        folder_id = self.data['Folder_Id'][folder_name]
        list_permission = self.data['List_Permission']
    # Create Google Drive instance in Folder
        file1 = self.drive.CreateFile({'title': '{}.{}'.format(filename,filetype),'parents':[{'id':folder_id}]})
        ### Sent content from folder data in Project folder
        file1.SetContentFile('data/{}.{}'.format(filename,filetype))
        file1.Upload() # Upload the file.
        file1['shareable'] = False
        return file1['title'],file1['alternateLink']
    ### return data to store on Database or Line_FlexMessage

    def upload_file_with_permission(self,folder_name,filetype,filename):
        folder_id = self.data['Folder_Id'][folder_name]
        list_permission = self.data['List_Permission']
    # Create Google Drive instance in Folder
        file1 = self.drive.CreateFile({'title': '{}.{}'.format(filename,filetype),'parents':[{'id':folder_id}]})
        ### Sent content from folder data in Project folder
        file1.SetContentFile('data/{}.{}'.format(filename,filetype))
        file1.Upload() # Upload the file.
        permission = file1.InsertPermission({
                            'type': 'user',
                            'value': list_permission,
                            'role': 'reader','withLink': False})
        file1['shareable'] = False
        return file1['title'],file1['alternateLink']
        ### return data to store on Database or Line_FlexMessage



    #### SET UP ALL FOLDER AND DIRECTORIES
    def SetUp_Gdrive_Directory(self):
        if self.data['Create_directory'] == "False" :
            ### Public Folder
            for i in self.data['Public_Folder']:
                _id , name = self.Create_directory(self.data,i,Type='Public')
                self.data['Folder_Id'][name] = _id

            ### Public Folder
            for i in self.data['Private_Folder']:
                _id , name = self.Create_directory(self.data,i,Type='Private')
                self.data['Folder_Id'][name] = _id
            self.data['Create_directory'] = "True"
        else :
            self.data['Create_directory'] = "True"
            return print('directories has been Created')
    
    ### Get or Update File List in Fodler Name
    def GetFile_FromFolderName(self,folder_name):
        All_file_in_folder = {}
        folder_id = self.data['Folder_Id'][folder_name]
        file_list = self.drive.ListFile({'q': folder_id}).GetList()
        for i,file1 in enumerate(file_list):
            New_Dict = {i : {"file_name" : file1['title'] , "file_Link" : file1['alternateLink']}}
            New_Dict.update(New_Dict)
        return All_file_in_folder
    ### return as json ready to convert into Flex Message List
    
    def Save_Json_Config(self):
        with open('Gdrive_Config.json','w') as Config:
            json.dump(self.data,Config,indent=3)
            Config.close()
    #### save json config as a database


    def Create_directory(self,data,name,Type='Public'):
        Folder = self.drive.CreateFile({'title': name,'mimeType' : 'application/vnd.google-apps.folder'})
        if Type == 'Private':
            Folder.Upload()
            Folder['shareable'] = False
            return Folder['id'] , Folder['title']
            
        elif Type == 'Public':
            Folder.Upload()
            Folder['shareable'] = True
            return Folder['id'] , Folder['title']

if __name__ == '__main__':
    

    project = Project_Gdrive("diseno001")
    project.SetUp_Gdrive_Directory()

    ##modified working with subfolder