from prettytable import PrettyTable
import json

from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.core.request_service import Request
from e2e_cli.core.alias_service import get_user_cred
from e2e_cli.core.helper_service import Checks

class nodeActions:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        if(get_user_cred(kwargs['alias'])):
            self.API_key=get_user_cred(kwargs['alias'])[1]
            self.Auth_Token=get_user_cred(kwargs['alias'])[0]
            self.possible=True
        else:
            self.possible=False


    def enable_recovery(self):
        my_payload= json.dumps({
                       "type": "enable_recovery_mode"
                }) 
        node_id = Py_version_manager.py_input("please enter node id ")
        while(not Checks.is_int(node_id)):
              node_id = Py_version_manager.py_input("please enter node id (integer only) ")
        
        API_key=self.API_key
        Auth_Token=self.Auth_Token
        url = "https://api.e2enetworks.com/myaccount/api/v1/nodes/"+ node_id +"/actions/?apikey="+API_key+"&location=Delhi"
        req="POST"
        status=Request(url, Auth_Token, my_payload, req).response.text
        Py_version_manager.py_print(status)            
            


    def disable_recovery(self):
        my_payload= json.dumps({
                      "type": "disable_recovery_mode"
               })  
        node_id = Py_version_manager.py_input("please enter node id ")
        while(not Checks.is_int(node_id)):
              node_id = Py_version_manager.py_input("please enter node id (integer only) ")
        
        API_key=self.API_key
        Auth_Token=self.Auth_Token
        url = "https://api.e2enetworks.com/myaccount/api/v1/nodes/"+ node_id +"/actions/?apikey="+API_key+"&location=Delhi"
        req="POST"
        status=Request(url, Auth_Token, my_payload, req).response.json()
        Py_version_manager.py_print(status)
               


    def reinstall(self):
        my_payload= json.dumps({
                        "type": "reinstall"
                      })  
        node_id = Py_version_manager.py_input("please enter node id ")
        while(not Checks.is_int(node_id)):
              node_id = Py_version_manager.py_input("please enter node id (integer only) ")
        
        API_key=self.API_key
        Auth_Token=self.Auth_Token
        url = "https://api.e2enetworks.com/myaccount/api/v1/nodes/"+ node_id +"/actions/?apikey="+API_key+"&location=Delhi"
        req="POST"
        status=Request(url, Auth_Token, my_payload, req).response.json()
        Py_version_manager.py_print(status)     
         


    def reboot(self):
        my_payload= json.dumps({
                           "type": "reboot"
                        })  
        node_id = Py_version_manager.py_input("please enter node id ")
        while(not Checks.is_int(node_id)):
              node_id = Py_version_manager.py_input("please enter node id (integer only) ")
        
        API_key=self.API_key
        Auth_Token=self.Auth_Token
        url = "https://api.e2enetworks.com/myaccount/api/v1/nodes/"+ node_id +"/actions/?apikey="+API_key+"&location=Delhi"
        req="POST"
        status=Request(url, Auth_Token, my_payload, req).response.json()
        Py_version_manager.py_print(status)                   



    def power_on(self):
        my_payload= json.dumps({
                        "type": "power_on"
                  }) 
        node_id = Py_version_manager.py_input("please enter node id ")
        while(not Checks.is_int(node_id)):
              node_id = Py_version_manager.py_input("please enter node id (integer only) ")
        
        API_key=self.API_key
        Auth_Token=self.Auth_Token
        url = "https://api.e2enetworks.com/myaccount/api/v1/nodes/"+ node_id +"/actions/?apikey="+API_key+"&location=Delhi"
        req="POST"
        status=Request(url, Auth_Token, my_payload, req).response.json()
        Py_version_manager.py_print(status)               
        


    def power_off(self):
        my_payload= json.dumps({
                         "type": "power_off"
                 })  
        node_id = Py_version_manager.py_input("please enter node id ")
        while(not Checks.is_int(node_id)):
              node_id = Py_version_manager.py_input("please enter node id (integer only) ")
        
        API_key=self.API_key
        Auth_Token=self.Auth_Token
        url = "https://api.e2enetworks.com/myaccount/api/v1/nodes/"+ node_id +"/actions/?apikey="+API_key+"&location=Delhi"
        req="POST"
        status=Request(url, Auth_Token, my_payload, req).response.json()
        Py_version_manager.py_print(status)              
    


    def rename_node(self):
        node_id = Py_version_manager.py_input("please enter node id ")
        while(not Checks.is_int(node_id)):
              node_id = Py_version_manager.py_input("please enter node id (integer only) ")
        new_name=Py_version_manager.py_input("please enter new name for the node : ")
        my_payload= json.dumps({
                       "name": new_name,
                       "type": "rename"
                  })  
        
        API_key=self.API_key
        Auth_Token=self.Auth_Token
        url = "https://api.e2enetworks.com/myaccount/api/v1/nodes/"+ node_id +"/actions/?apikey="+API_key+"&location=Delhi"
        req="POST"
        status=Request(url, Auth_Token, my_payload, req).response.json()
        Py_version_manager.py_print(status)
               
        

    def unlock_vm(self):
        my_payload= json.dumps({
                        "type": "unlock_vm"
                 })  
        node_id = Py_version_manager.py_input("please enter node id ")
        while(not Checks.is_int(node_id)):
              node_id = Py_version_manager.py_input("please enter node id (integer only) ")
        
        API_key=self.API_key
        Auth_Token=self.Auth_Token
        url = "https://api.e2enetworks.com/myaccount/api/v1/nodes/"+ node_id +"/actions/?apikey="+API_key+"&location=Delhi"
        req="POST"
        status=Request(url, Auth_Token, my_payload, req).response.json()
        Py_version_manager.py_print(status)
               
    

    def lock_vm(self):
        my_payload= json.dumps({
                        "type": "lock_vm"
                 })  
        node_id = Py_version_manager.py_input("please enter node id ")
        while(not Checks.is_int(node_id)):
              node_id = Py_version_manager.py_input("please enter node id (integer only) ")
        
        API_key=self.API_key
        Auth_Token=self.Auth_Token
        url = "https://api.e2enetworks.com/myaccount/api/v1/nodes/"+ node_id +"/actions/?apikey="+API_key+"&location=Delhi"
        req="POST"
        status=Request(url, Auth_Token, my_payload, req).response.json()
        Py_version_manager.py_print(status)
               
        
        
    