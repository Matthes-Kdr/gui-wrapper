



class ParameterError(Exception):

    """
    Exception raised for errors in the input salary.

    Attributes:
        param -- value which caused the error
        message -- explanation of the error
    """

    def __init__(self, param, cls_type, length=None, message="Passed parameter are not valid for the desired element."):
        self.param = param
        self.cls_type = cls_type
        self.length = length

        if not self.length:
            self.length = "any"

        empty = ""
        passed =   "Passed value:    " + repr(self.param)
        required = "Required type:   " + repr(self.cls_type)
        length =   "Required length: " + repr(self.length)
        line = "=" * 120
        
        self.message =  "\n".join((empty, passed, required, length, line))
        
        super().__init__(self.message)









def main():
    # Only for testing.

    params = [
        ([123,4], list, 11),
        (123, str),
        [123, list],
    ]

    
    for param in params:

        val, type_= param[0:2]
        
        if len(param) == 3:
            length = param[2]

        if not isinstance(val, type_):
            raise ParameterError(val, type_, length=length)






if __name__ == "__main__":

    main()