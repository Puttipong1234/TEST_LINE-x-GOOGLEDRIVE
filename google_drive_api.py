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

    def __init__(self,Proejct_name = 'default'):
        self.data = ''
        with open('Gdrive_Config.json','r') as Config:
            self.data = json.load(Config)
            Config.close()
        self.Proejct_name = Proejct_name
### create instance google drive with authenthication
        
        gauth = GoogleAuth()

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
    # def SetUp_Gdrive_Directory(self):
    #     if self.data['Create_directory'] == "False" :
    #         ### Public Folder
    #         for i in self.data['Public_Folder']:
    #             _id , name = self.Create_directory(self.data,i,Type='Public')
    #             for j in self.data[]
    #             self.data['Folder_Id'][name] = _id

    #         ### Public Folder
    #         for i in self.data['Private_Folder']:
    #             _id , name = self.Create_directory(self.data,i,Type='Private')
    #             self.data['Folder_Id'][name] = _id
    #         self.data['Create_directory'] = "True"
    #     else :
    #         self.data['Create_directory'] = "True"
    #         return print('directories has been Created')
    
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
    
    
    def Create_subdirectory(self,data,name,Type='Public',parent_id=''):
        
        Folder = self.drive.CreateFile({'title': name,'parents':[{'id':parent_id}],'mimeType' : 'application/vnd.google-apps.folder'})        
        if Type == 'Private':
            Folder.Upload()
            Folder['shareable'] = False
            return Folder['id'] , Folder['title']
            
        elif Type == 'Public':
            Folder.Upload()
            Folder['shareable'] = True
            return Folder['id'] , Folder['title']
    
    def SetUp_Gdrive_Directory(self):
        if self.data['Create_directory'] == "False" :
            ### Public Folder
            for i in self.data['Public_Folder']:
                _id , name = self.Create_directory(self.data,i,Type='Public')
                for j in self.data['Subfolder']:
                    sub__id , sub_name = self.Create_subdirectory(self.data,name+"-"+j,Type='Public',parent_id=_id)
            ### Private Folder
            for i in self.data['Private_Folder']:
                _id , name = self.Create_directory(self.data,i,Type='Private')
                for j in self.data['Subfolder']:
                    sub_id , sub_name = self.Create_subdirectory(self.data,name+"-"+j,Type='Private',parent_id=_id)
        else:
            print('directory is already Create')

if __name__ == '__main__':
    

    project = Project_Gdrive("diseno001")
    
    project.SetUp_Gdrive_Directory()


    ##modified working with subfolder

    #create and authorize your drive client object
    # drive_client = project.drive
    #Create the folder
    # If no parent ID is provided this will automatically go to the root or My Drive 'directory'
    # top_level_folder = drive_client.CreateFile({'title': 'top_level','mimeType' : 'application/vnd.google-apps.folder'})
    # # Upload the file to your drive
    # top_level_folder.Upload()
    # # Grab the ID of the folder we just created
    # parent_id = top_level_folder['id']

    # # Create a sub-directory
    # # Make sure to assign it the proper parent ID
    # child_folder = drive_client.CreateFile({'title': 'level_2', 'parents':[{'id':parent_id}],'mimeType' : 'application/vnd.google-apps.folder'})
    # child_folder.Upload()