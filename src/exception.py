import sys
import logging
import logger

# why is sys- sys is used provides functions and variables which are used to manipulate different parts of the Python Runtime Environment. It lets us access system-specific parameters and functions

def error_message_detail(error, error_detail:sys):
    _,_,exc_tb = error_detail.exc_info()   #-- this has 3 variable 1st 2 are not important but 3rd exc_tb gives the detail about where in which file & line the exception has occurred
    
    filename = exc_tb.tb_frame.f_code.co_filename 
    # Ths gives the file name where exception hass occured (google custom exception handling doc)

    error_message = f"Error message occured in scripty[{filename}] line number [{exc_tb.tb_lineno}], error: [{str(error)}]"

    return error_message

class CustomException(Exception):
    def __init__(self, error_message, error_detail:sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_detail=error_detail)

    def __str__(self):
        return self.error_message
    

# Demo to check if its working 
# if __name__ == '__main__':
    
#     try:
#         a = 1/0
#     except Exception as e:
#         logging.info("Divide by Zeror Error")
#         raise CustomException(e, sys)
