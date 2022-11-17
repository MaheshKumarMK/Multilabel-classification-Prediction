import sys

def error_message_details(error, error_details:sys):
    _,_,exc_tb =error_details.exc_info()  #tuple which returns type(e), e, e.traceback

    file_name=exc_tb.tb_frame.f_code.co_filename   #gives filename(eg: main.py) from sys package

    error_message= "error occurred python script name [{0}] line number [{1}] error message [{2}]".format(
        file_name, exc_tb.tb_lineno, str(error)   #error here is error_message
    )

    return error_message

class RatingsException(Exception):
    def __init__(self, error_message, error_details):
        """
        :param error_message: error message in string format
        """
        super().__init__(error_message) #super() instatinated using parent class

        self.error_message=error_message_details(
            error_message, error_details=error_details  #error_message=e, error_details=sys
        )

        def __str__(self):       #use to print or display the content
            return self.error_message