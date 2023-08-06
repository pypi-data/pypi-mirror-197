import subprocess, traceback

from e2e_cli.core.error_logs_service import action_on_exception
from e2e_cli.core.helper_service import Checks
from e2e_cli.core.py_manager import Py_version_manager

from e2e_cli.config.config_routing import ConfigRouting
from e2e_cli.loadbalancer.lb_routing import LBRouting
from e2e_cli.node.node_routing import NodeRouting
from e2e_cli.bucket_store.bucket_routing import BucketRouting
from e2e_cli.dbaas.dbaas_routing import DBaaSRouting


class CommandsRouting:
    def __init__(self, arguments):
        self.arguments = arguments

    def route(self):
        if self.arguments.command is None:
            subprocess.call(['e2e_cli', '-h'])

        elif self.arguments.command == "config":
            try:
                ConfigRouting(self.arguments).route()
            except Exception as e:
                        Py_version_manager.py_print("Oops!! An error occurred for more info, type : debug")
                        if(Py_version_manager.py_input("debug/exit ??").lower()=="debug"):
                                traceback.print_exc()
                            # action_on_exception(e, self.arguments.alias, traceback.print_exc())

        elif self.arguments.command == "node":
            try:
                NodeRouting(self.arguments).route()
            except Exception as e:
                        Py_version_manager.py_print("Oops!! An error occurred for more info, type : debug")
                        if(Py_version_manager.py_input("debug/exit ?? ").lower()=="debug"):
                                traceback.print_exc()

        elif self.arguments.command == "lb":
            try: 
                LBRouting(self.arguments).route()
            except Exception as e:
                        Py_version_manager.py_print("Oops!! An error occurred for more info, type : debug")
                        if(Py_version_manager.py_input("debug/exit ?? ").lower()=="debug"):
                                traceback.print_exc()
                            # action_on_exception(e, self.arguments.alias, traceback.print_exc())
        
        elif self.arguments.command == "bucket":
            try:
                BucketRouting(self.arguments).route()
            except Exception as e:
                    Checks.manage_exception(e)
                            # action_on_exception(e, self.arguments.alias, traceback.print_exc())
            
        elif self.arguments.command == "dbaas":
            try:
                DBaaSRouting(self.arguments).route()
            except Exception as e:
                        Py_version_manager.py_print("Oops!! An error occurred for more info, type : debug")
                        if(Py_version_manager.py_input("debug/exit ?? ").lower()=="debug"):
                                traceback.print_exc()
                            # action_on_exception(e, self.arguments.alias, traceback.print_exc())
