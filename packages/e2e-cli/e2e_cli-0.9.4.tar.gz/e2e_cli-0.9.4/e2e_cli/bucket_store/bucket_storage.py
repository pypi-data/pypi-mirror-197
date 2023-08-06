from prettytable import PrettyTable
import re

from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.core.request_service import Request
from e2e_cli.core.alias_service import get_user_cred
from e2e_cli.core.helper_service import Checks

class bucketCrud:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        if(get_user_cred(kwargs['alias'])):
            self.API_key=get_user_cred(kwargs['alias'])[1]
            self.Auth_Token=get_user_cred(kwargs['alias'])[0]
            self.possible=True
        else:
            self.possible=False
        
    def bucket_name_validity(self, bucket_name):
         return (bool(re.findall("[A-Z]", bucket_name)) or bool(re.findall('[!@#$%^&*)(_+=}{|/><,.;:"?`~]', bucket_name)) or bool(re.findall("'", bucket_name)) or bool(re.search("]", bucket_name)) or bool(re.search("[[]", bucket_name)))


    def create_bucket(self):
        Py_version_manager.py_print("Creating")
        my_payload= {}  
        bucket_name=Py_version_manager.py_input("input name of your new bucket : ")
        while(self.bucket_name_validity(bucket_name)):
                bucket_name=Py_version_manager.py_input("Only following chars are supported: lowercase letters (a-z) or numbers(0-9)  Re-enter : ")
        API_key=self.API_key
        Auth_Token=self.Auth_Token
        url = "https://api.e2enetworks.com/myaccount/api/v1/storage/buckets/"+ bucket_name +"/?apikey="+API_key+"&location=Delhi"
        req="POST"
        status=Request(url, Auth_Token, my_payload, req).response.json()
        if (status['code'] == 200):
            x = PrettyTable()
            x.field_names = ["ID", "Name", "Created at"]
            x.add_row([status['data']['id'], status['data']['name'], status['data']['created_at']])
            Py_version_manager.py_print(x)
        else:
            Py_version_manager.py_print("There seems to be an error")
            Checks.status_result(status)
            



    def delete_bucket(self):
        my_payload={}
        bucket_name=Py_version_manager.py_input("input name of the bucket you want to delete : ")
        while(self.bucket_name_validity(bucket_name)):
                bucket_name=Py_version_manager.py_input("Only following chars are supported: lowercase letters (a-z) or numbers(0-9)  Re-enter : ")
        API_key=self.API_key
        Auth_Token=self.Auth_Token
        url = "https://api.e2enetworks.com/myaccount/api/v1/storage/buckets/"+ bucket_name +"/?apikey="+API_key+"&location=Delhi"
        req="DELETE"
        status=Request(url, Auth_Token, my_payload, req).response.json()
        if(status['code']==200):
                if Checks.status_result(status):
                        Py_version_manager.py_print("Bucket Successfully deleted")
                        Py_version_manager.py_print("use following command -> e2e_cli bucket list <alias> to check if bucket has been deleted")
        else :
                Py_version_manager.py_print("There seems to be an error, retry with the correct name")
                Checks.status_result(status)


    
    def list_bucket(self):
        my_payload={}
        API_key= self.API_key  
        Auth_Token= self.Auth_Token 
        url = "https://api.e2enetworks.com/myaccount/api/v1/storage/buckets/?apikey="+ API_key+"&location=Delhi"
        req="GET"
        Py_version_manager.py_print("Your Buckets : ")
        status=Request(url, Auth_Token, my_payload, req).response.json()
        list=status['data']
        try:
            i=1
            if (list):
                x = PrettyTable()
                x.field_names = ["index", "ID", "Name", "Created at", "bucket size"]
                for element in list:
                    x.add_row([i, element['id'], element['name'], element['created_at'], element['bucket_size']])
                    i = i+1
                Py_version_manager.py_print(x)
            else:
                if Checks.status_result(status):
                    Py_version_manager.py_print("Either list is empty or an error occurred!!")
        except:
            Py_version_manager.py_print("There seems to be an error")
            Checks.status_result(status)
    

