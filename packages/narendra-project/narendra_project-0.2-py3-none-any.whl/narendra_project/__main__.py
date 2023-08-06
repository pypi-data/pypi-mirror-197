import os
import requests
import maskpass
import json

def main():   
    AUTH_URL="http://3.108.252.238/api/auth/"
    URL="http://3.108.252.238/api/files/"

    path=os.getcwd()
    dir_list = os.listdir(path)
    files=[]
    for file in dir_list:
        if file != '__pycache__':
            files.append(('file',open(path+'/'+str(file),"rb")))
    
    print("Enter your username and password...")
    username=input("Enter Username: ")
    password=maskpass.askpass(mask="*") 
    user_auth={'username':username,'password':password}
    user_auth=json.dumps(user_auth)
    headers = {'Content-type': 'application/json'}
    auth_request=requests.post(url=AUTH_URL,data=user_auth,headers=headers)
    auth_response=auth_request.json()
    print(auth_response['message'])

    if auth_response['message'] == 'Authentication Successful!':
        file_upload_request=requests.post(url=URL,files=files)
        file_upload_response=file_upload_request.json()
        print(file_upload_response['message'])

if __name__ == "__main__":
    main()

