import json
from prettytable import PrettyTable


from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.core.alias_service import get_user_cred
from e2e_cli.core.request_service import Request
from e2e_cli.core.helper_service import Checks
from e2e_cli.node.node_crud.node_listing_service import Nodelisting


    
class payload:
    def __init__(self, alias):
        Option=Py_version_manager.py_input("How would u like to proceed?? For Manual input type 'manual' ")

        if(Option.lower()=="manual"):
            self.image = Py_version_manager.py_input("please enter OS you require : ")
            self.plan = Py_version_manager.py_input("please enter system requirements/plans : ")
            self.region= Py_version_manager.py_input("please enter region in where server is required : ")
        else :
            node_specifications=Nodelisting(alias).node_listing()
            self.image = node_specifications['image']
            self.plan = node_specifications['plan']
            if(node_specifications['location']=='Delhi'):
                    self.region='ncr'
            else:
                    self.region='mumbai'
                    
        self.security_group_id = Py_version_manager.py_input("please enter security group id : ")
        self.name = Py_version_manager.py_input("please enter name of your node : ")
        self.ssh_keys = []


class NodeCrud:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        if (get_user_cred(kwargs['alias'])):
            self.API_key = get_user_cred(kwargs['alias'])[1]
            self.Auth_Token = get_user_cred(kwargs['alias'])[0]
            self.possible = True
        else:
            self.possible = False


    def create_node(self):
        Py_version_manager.py_print("Creating")
        my_payload = payload(self.kwargs['alias'])
        API_key = self.API_key
        Auth_Token = self.Auth_Token
        url = "https://api.e2enetworks.com/myaccount/api/v1/nodes/?apikey=" + API_key+"&location=Delhi"
        req = "POST"
        status = Request(url, Auth_Token, json.dumps(
            my_payload.__dict__), req).response.json()
        if (status['code'] == 200):
            x = PrettyTable()
            x.field_names = ["ID", "Name", "Created at", "disk", "Status", "Plan"]
            try :
                x.add_row([status['data']['id'], status['data']['name'],
                      status['data']['created_at'], status['data']['disk'], status['data']['status'], status['data']['plan']])
                Py_version_manager.py_print(x)
            except :
                Checks.status_result(status, req)
        else:
            Py_version_manager.py_print("oops errors !!")
            Checks.status_result(status, req)


    def delete_node(self):
        my_payload = {}
        API_key = self.API_key
        Auth_Token = self.Auth_Token
        node_id = Py_version_manager.py_input("please enter node id : ")
        while(not Checks.is_int(node_id)):
              node_id = Py_version_manager.py_input("please enter node id (integer only) ")
        url = "https://api.e2enetworks.com/myaccount/api/v1/nodes/" + str(node_id) + "/?apikey="+API_key
        req = "DELETE"
        confirmation =Py_version_manager.py_input("are you sure you want to delete press y for yes, else any other key : ")
        if(confirmation.lower()=="y"):
            status = Request(url, Auth_Token, my_payload, req).response.json()
            if (status['code'] == 200):
                    if Checks.status_result(status, req):
                        Py_version_manager.py_print("Node Successfully deleted")
            else:
                Checks.status_result(status, req)
        


    def get_node_by_id(self):
        my_payload = {}
        API_key = self.API_key
        Auth_Token = self.Auth_Token
        node_id = Py_version_manager.py_input("please enter node id ")
        while(not Checks.is_int(node_id)):
              node_id = Py_version_manager.py_input("please enter node id (integer only) ")
        url = "https://api.e2enetworks.com/myaccount/api/v1/nodes/" + str(node_id) + "/?apikey="+API_key
        req = "GET"
        status = Request(url, Auth_Token, my_payload, req).response.json()
        if (status['code'] == 200):
            try:
                x = PrettyTable()
                x.field_names = ["VM id", "Name", "Created at", "disk", "Plan", "Public IP", "Status"]
                x.add_row([ status['data']['vm_id'], status['data']['name'], status['data']['created_at'], status['data']['disk'],  status['data']['plan'], status['data']['public_ip_address'], status['data']['status'] ])
                Py_version_manager.py_print(x)
            except:
                Checks.status_result(status, req)
        else:
            Py_version_manager.py_print("oops errors !!")
            Checks.status_result(status, req)


    def list_node(self, parameter=0):
        my_payload = {}
        API_key = self.API_key
        Auth_Token = self.Auth_Token
        url = "https://api.e2enetworks.com/myaccount/api/v1/nodes/?apikey=" + API_key+"&location=Delhi"
        req = "GET"
        status = Request(url, Auth_Token, my_payload,
                       req).response.json()
        list=status['data']
        try:
            if parameter == 0:               
                i = 1
                Py_version_manager.py_print("Your Nodes : ")
                if (list):
                    x = PrettyTable()
                    x.field_names = ["index", "ID", "Name", "Created at", "disk", "Plan", "Status"]
                    for element in list:
                        x.add_row([i, element['id'], element['name'],
                                element['created_at'], element['disk'],  element['plan'],  element['status']])
                        i = i+1
                    Py_version_manager.py_print(x)
                else:
                    Py_version_manager.py_print("Either list is empty or an error occurred!!")
            else:
                return list
        except:
            Py_version_manager.py_print("oops errors !!")
            Checks.status_result(status, req)

    def update_node(self):
        API_key = self.API_key
        Auth_Token = self.Auth_Token
        Py_version_manager.py_print("update call")
