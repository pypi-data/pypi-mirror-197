import subprocess

from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.node.node import NodeCrud

class NodeRouting:
    def __init__(self, arguments):
        self.arguments = arguments
        

    def route(self):
        if self.arguments.node_commands is None:
            subprocess.call(['e2e_cli', 'node', '-h'])

        elif self.arguments.node_commands == 'create':
            Node_operations = NodeCrud(alias=self.arguments.alias )
            if(Node_operations.possible):
                        try:
                           Node_operations.create_node()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")  
                        except Exception as e:
                            if(str(e)=="'data'" or str(e)=="'code'"):
                                Py_version_manager.py_print("Oops!! Your access credentials seems to have expired")
                            else:
                                raise e      

        elif self.arguments.node_commands == 'delete':
            Node_operations = NodeCrud(alias=self.arguments.alias)
            if(Node_operations.possible):
                        try:
                           Node_operations.delete_node()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
                        except Exception as e:
                            if(str(e)=="'data'" or str(e)=="'code'"):
                                Py_version_manager.py_print("Oops!! Your access credentials seems to have expired")
                            else:
                                raise e

        elif self.arguments.node_commands == 'get':
            Node_operations = NodeCrud(alias=self.arguments.alias)
            if(Node_operations.possible):
                        try:
                           Node_operations.get_node_by_id()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
                        except Exception as e:
                            if(str(e)=="'data'" or str(e)=="'code'"):
                                Py_version_manager.py_print("Oops!! Your access credentials seems to have expired")
                            else:
                                raise e
                                    
        elif self.arguments.node_commands == 'list':
            Node_operations = NodeCrud(alias=self.arguments.alias)
            if(Node_operations.possible):
                        try: 
                           Node_operations.list_node()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
                        except Exception as e:
                            if(str(e)=="'data'" or str(e)=="'code'"):
                                Py_version_manager.py_print("Oops!! Your access credentials seems to have expired")
                            else:
                                raise e
                            
