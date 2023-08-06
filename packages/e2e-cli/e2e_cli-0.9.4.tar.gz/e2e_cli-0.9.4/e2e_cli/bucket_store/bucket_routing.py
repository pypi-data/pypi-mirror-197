import subprocess

from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.bucket_store.bucket_storage import bucketCrud

class BucketRouting:
    def __init__(self, arguments):
        self.arguments = arguments
        
        
    def route(self):
        if self.arguments.bucket_commands is None:
            subprocess.call(['e2e_cli', 'bucket', '-h'])

        elif self.arguments.bucket_commands == 'create':
            bucket_operations = bucketCrud(alias=self.arguments.alias )
            if(bucket_operations.possible):
                        try:
                            bucket_operations.create_bucket()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
                        except Exception as e:
                            if(str(e)=="'data'" or str(e)=="'code'"):
                                Py_version_manager.py_print("Oops!! Your access credentials seems to have expired")
                            else:
                                raise e

        elif self.arguments.bucket_commands == 'delete':
            bucket_operations = bucketCrud(alias=self.arguments.alias)
            if(bucket_operations.possible):
                        try:
                            bucket_operations.delete_bucket()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
                        except Exception as e:
                            if(str(e)=="'data'" or str(e)=="'code'"):
                                Py_version_manager.py_print("Oops!! Your access credentials seems to have expired")
                            else:
                                raise e
        
        elif self.arguments.bucket_commands == 'list':
            bucket_operations = bucketCrud(alias=self.arguments.alias)
            if(bucket_operations.possible):
                        try:
                            bucket_operations.list_bucket()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
                        except Exception as e:
                            if(str(e)=="'data'" or str(e)=="'code'"):
                                Py_version_manager.py_print("Oops!! Your access credentials seems to have expired")
                            else:
                                raise e


