from pydrive.auth import GoogleAuth

gauth = GoogleAuth()
auth_url =gauth.CommandLineAuth() # Create authentication url user needs to visit

print(auth_url)