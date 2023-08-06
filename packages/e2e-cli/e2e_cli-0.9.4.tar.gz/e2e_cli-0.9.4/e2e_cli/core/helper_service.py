from e2e_cli.core.py_manager import Py_version_manager

class Checks:

    @classmethod
    def is_int(self, id):
        try:
            int(id)
            return True
        except:
            return False
        
    @classmethod
    def status_result(self, status):
        if(status['errors']):
                Py_version_manager.py_print("errors : ", status['errors'])
        if(not status['message'] in ['Success', 'success']):
                Py_version_manager.py_print("message : ", status['message'])
        if( (not status['errors']) and (status['message'] in ['Success', 'success'] )):
                return True