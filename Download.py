
import requests
from google_drive_api import Project_Gdrive
import os

def download_file(messageid,folder_name,filetype,filename,Permit = 'Public'):

  Project = Project_Gdrive()
    
  LINE_API = 'https://api.line.me/v2/bot/message/{}/content'.format(messageid)

  Authorization = 'Bearer 1RfIiAbjneORMpj+sIGYx+Yi0esjdG/F/VQxyIc6/dFoCVym6hZzDrBqxpd5Ui8XFLsdzohfRuvZRU1dsCP0yaSN3Rdx7U3PeT/0kZfnkrAXrmtrclZaw0v/tA6vOe2fM93R+JvDab5xhxN/4vtGYQdB04t89/1O/w1cDnyilFU='

  headers = {'Content-Type': 'application/json; charset=UTF-8',
  'Authorization': Authorization}


  r = requests.get(LINE_API, headers=headers ) # ส่งข้อมูล
  open('data/{}.{}'.format(filename,filetype), 'wb').write(r.content)

  if Permit == 'Public':
    up = Project.upload_file_Public(folder_name,filetype,filename)
  else :
    up = Project.upload_file_with_permission(folder_name,filetype,filename)


  os.remove('data/{}.{}'.format(filename,filetype))

  return print(LINE_API +"\n" + up)