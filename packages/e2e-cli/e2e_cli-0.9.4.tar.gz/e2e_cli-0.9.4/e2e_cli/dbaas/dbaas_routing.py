import subprocess

from e2e_cli.dbaas.dbaas import DBaaSClass
from e2e_cli.core.py_manager import Py_version_manager


class DBaaSRouting:
    def __init__(self, arguments):
        self.arguments = arguments

    def route(self):
        if self.arguments.dbaas_commands is None:
            subprocess.call(['e2e_cli', 'dbaas', '-h'])

        elif self.arguments.dbaas_commands == 'create':
            if "alias=" in self.arguments.alias:
                alias_name = self.arguments.alias.split("=")[1]
            else:
                alias_name = self.arguments.alias
            dbaas_class_object = DBaaSClass(alias=alias_name)
            try:
              dbaas_class_object.create_dbaas()
            except KeyboardInterrupt:
                Py_version_manager.py_print(" ")
            except Exception as e:
                            if(str(e)=="'data'" or str(e)=="'code'"):
                                Py_version_manager.py_print("Oops!! Your access credentials seems to have expired")
                            else:
                                raise e

        elif self.arguments.dbaas_commands == 'list' or self.arguments.dbaas_commands == 'ls':
            if "alias=" in self.arguments.alias:
                alias_name = self.arguments.alias.split("=")[1]
            else:
                alias_name = self.arguments.alias
            dbaas_class_object = DBaaSClass(alias=alias_name)
            try:
                dbaas_class_object.list_dbaas()
            except KeyboardInterrupt:
                Py_version_manager.py_print(" ")
            except Exception as e:
                            if(str(e)=="'data'" or str(e)=="'code'"):
                                Py_version_manager.py_print("Oops!! Your access credentials seems to have expired")
                            else:
                                raise e

        elif self.arguments.dbaas_commands == 'delete':
            if "alias=" in self.arguments.alias:
                alias_name = self.arguments.alias.split("=")[1]
            else:
                alias_name = self.arguments.alias
            dbaas_class_object = DBaaSClass(alias=alias_name)
            try:
                dbaas_class_object.delete_dbaas_by_name()
            except KeyboardInterrupt:
                Py_version_manager.py_print(" ")
            except Exception as e:
                            if(str(e)=="'data'" or str(e)=="'code'"):
                                Py_version_manager.py_print("Oops!! Your access credentials seems to have expired")
                            else:
                                raise e
            
