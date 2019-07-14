from pydrive.drive import GoogleDrive
from pydrive.files import GoogleDriveFile
from pydrive.auth import GoogleAuth
import json
from models import Menu , Submenu , File
from app import db

### requirement 
# - need file Gdrive_Config
# - need file Credential.txt to save credential (auto authenthication)
#      first time Credential.txt. can be blank 
#       after perfrom the Oauth .txt will be filled
#       To changing Production Credential.txt need new )Oauth perform

class Project_Gdrive():

    def __init__(self,Project_name = 'default'):
        self.data = ''
        with open('Gdrive_Config.json','r') as Config:
            self.data = json.load(Config)
            Config.close()
        self.Project_name = Project_name
### create instance google drive with authenthicate
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
        Subfolder = Submenu.query.filter_by(name = folder_name).first()
        Subfolder_id = Subfolder.file_id
        list_permission = self.data['List_Permission']
        # Create Google Drive instance in Folder
        file1 = self.drive.CreateFile({'title': '{}.{}'.format(filename,filetype),'parents':[{'id':Subfolder_id}]})
        ### Sent content from folder data in Project folder
        file1.SetContentFile('data/{}.{}'.format(filename,filetype))
        file1.Upload() # Upload the file.
        permission = file1.InsertPermission({
                            'type': 'user',
                            'value': list_permission,
                            'role': 'reader','withLink': False})
        file1['shareable'] = True
        new_file = File(name = file1['title'],uri = file1['alternateLink'],file_id = file1['id'],submenu = Subfolder)
        new = db.session.add(new_file)
        new = db.session.commit()
        return file1['title'],file1['alternateLink'],file1['id']
    ### return data to store on Database or Line_FlexMessage

    def upload_file_with_permission(self,folder_name,filetype,filename):
        Subfolder = Submenu.query.filter_by(name = folder_name).first()
        Subfolder_id = Subfolder.file_id
        list_permission = self.data['List_Permission']
    # Create Google Drive instance in Folder
        file1 = self.drive.CreateFile({'title': '{}.{}'.format(filename,filetype),'parents':[{'id':Subfolder_id}]})
        ### Sent content from folder data in Project folder
        file1.SetContentFile('data/{}.{}'.format(filename,filetype))
        file1.Upload() # Upload the file.
        permission = file1.InsertPermission({
                            'type': 'user',
                            'value': list_permission,
                            'role': 'reader','withLink': False})
        file1['shareable'] = False
        new_file = File(name = _file['title'],uri = _file['alternateLink'],file_id = _file['id'],submenu = Subfolder)
        new =db.session.add(new_file)
        new =db.session.commit()
        return file1['title'],file1['alternateLink'],file1['id']
        ### return data to store on Database or Line_FlexMessage

    
    ### Get or Update File List in Fodler Name
    def GetFile_FromFolderName(self,folder_name):
        folder = Submenu.query.filter_by(name = folder_name).first()
        folder_id = folder.file_id
        file_list = self.drive.ListFile({'q': folder_id}).GetList()
        db.session.query(folder).delete()
        db.session.commit()
        for i,_file in enumerate(file_list):
            new_file = File(name = _file['title'],uri = _file['alternateLink'],file_id = _file['id'],submenu = folder)
            db.session.commit()


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
            return Folder['id'] , Folder['title'] , Folder['alternateLink']
            
        elif Type == 'Public':
            Folder.Upload()
            Folder['shareable'] = True
            return Folder['id'] , Folder['title'] , Folder['alternateLink']
    
    
    def Create_subdirectory(self,data,name,Type='Public',parent_id=''):
        
        Folder = self.drive.CreateFile({'title': name,'parents':[{'id':parent_id}],'mimeType' : 'application/vnd.google-apps.folder'})        
        if Type == 'Private':
            Folder.Upload()
            Folder['shareable'] = False
            return Folder['id'] , Folder['title'], Folder['alternateLink']
            
        elif Type == 'Public':
            Folder.Upload()
            Folder['shareable'] = True
            return Folder['id'] , Folder['title'], Folder['alternateLink']
    
    def SetUp_Gdrive_Directory(self):
        if self.data['Create_directory'] == "False" :
            db.create_all()
            ### Public Folder
            for i in self.data['Public_Folder']:
                _id , name , Link = self.Create_directory(self.data,i,Type='Public')
                new_folder = Menu(name = name , uri = Link , file_id = _id)
                db.session.add(new_folder)
                db.session.commit()
                print('create {}'.format(i))
                for j in self.data['Subfolder']:
                    sub_id , sub_name , sub_Link= self.Create_subdirectory(self.data,name+"-"+j,Type='Public',parent_id=_id)
                    new_subfolder = Submenu(name = sub_name , uri = sub_Link , file_id = sub_id , menu = new_folder)
                    db.session.add(new_subfolder)
                    db.session.commit()
                    print('create {}'.format(j))

            ### Private Folder
            for i in self.data['Private_Folder']:
                _id , name , Link= self.Create_directory(self.data,i,Type='Private')
                new_folder = Menu(name = name , uri = Link , file_id = _id)
                db.session.add(new_folder)
                db.session.commit()
                print('create {}'.format(i))
                for j in self.data['Subfolder']:
                    sub_id , sub_name , sub_Link = self.Create_subdirectory(self.data,name+"-"+j,Type='Private',parent_id=_id)
                    new_subfolder = Submenu(name = sub_name , uri = sub_Link , file_id = sub_id , menu = new_folder)
                    db.session.add(new_subfolder)
                    db.session.commit()
                    print('create {}'.format(j))

            self.data['Create_directory'] = "True"
        else:
            print('directory was already Create')

if __name__ == '__main__':
    

    project = Project_Gdrive(Project_name="diseno001")
    project.SetUp_Gdrive_Directory()
    project.Save_Json_Config()
