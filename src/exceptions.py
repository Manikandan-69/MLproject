import sys
"""The sys module is versatile and widely used for managing Python programs' interaction with the operating system and runtime environment. 
It's particularly useful for command-line scripts, debugging, and handling system-level tasks."""


def error_message_details(error,error_details:sys):
    _,_,exc_tb=error_details.exc_info()
    file_name=exc_tb.tb_frame.f_code.co_filename
    error_message="Error occured in python script name [{0}] line number [{1}] error message [{2}]".format(
        file_name,exc_tb.tb_lineno,str(error))
    
    return error_message

class CustomException(Exception):
    def __init__(self,error_message,error_details:sys):
        super().__init__()
        self.error_msg=error_message_details(error_message,error_details=error_details)

    def __str__(self):
        return self.error_msg

"""
if __name__=="__main__":
    try:
        a=1/0
    except Exception as e:
        raise CustomException(e,sys)
"""