import traceback

from e2e_cli.core.py_manager import Py_version_manager

def status_error_check(status):
        if(status['errors']):
                Py_version_manager.py_print("errors : ", status['errors'])
                return False
        else:
              return True
              
def status_msg_check(status):
        if(status['message'].lower()=='success'):
                return True      
        else:
            Py_version_manager.py_print("message : ", status['message'])
            return False
            

def status_data_check(status, req):
        EMPTY_DATA_ALLOWED=["DELETE"]

        if(status['data']):
            return True   
        else:
            if req in EMPTY_DATA_ALLOWED:
                   return True
            Py_version_manager.py_print("Your requested data seems to be empty")
            return False 
              


class Checks:

    @classmethod
    def is_int(self, id):
        try:
            int(id)
            return True
        except:
            return False


    @classmethod
    def status_result(self, status, req):
        msg_result=status_msg_check(status) 
        error_result=status_error_check(status)  
        data_result=status_data_check(status, req)

        if( msg_result and error_result and data_result):
                return True
        else:
                return False
        

    @classmethod
    def manage_exception(self, e):
                Py_version_manager.py_print("Oops!! An error occurred for more info, type : debug")
                if(Py_version_manager.py_input("debug/exit ?? ").lower()=="debug"):
                            
                    if(str(e)=="'data'" or str(e)=="'code'" or str(e)=="'errors'" or str(e)=="'data'" ):
                                Py_version_manager.py_print("Oops!! Your access credentials seems to have expired")
                    else:
                                traceback.print_exc()