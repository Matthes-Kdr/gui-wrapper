'''

Provides a class to build a GUI quickly row-by-row with TKinter.
The ways to access to the most common elements (for my useCases) are shortend a bit...

'''

import sys
from tkinter import messagebox, ttk
import tkinter as tk

import textwrap

from typing import Union

try:
    from tkhtmlview import HTMLLabel
except ModuleNotFoundError as error:
    print("ERROR: ", error, "\n\nAll html labels will be replaced by usual lables without html!")

from exceptions import ParameterError




class GuiElementsRow:


    def __init__(self, root:tk.Tk, y:int, elements:list[tuple[str]]) -> None:
        """ 
        Available keywords for tuple in elements:
            - "lbl"      : Param:  "caption_for_label"          
            - "btn"      : Param:  ("caption", command_function)
            - "cmb"      : Param:  ("option1", "option2")       
            - "chkbx"    : Param:  ["lbl_caption", tk.IntVar()] 
            - "radiobtn" : Param:  ["lbl_caption", tk.IntVar()] 
            - "sep"      : Param:  vertical_distance 
            - "lbl_html" : Param:  "caption <u> with </u> html"   
            - "img_html" : Param:  "path/to/image/source.png"  
            - "txt"      : Param:  ??? # TODO...          
        
        Structure of each tuple of the tuple in elements:
            (x_position, ELEMENT_KEYWORD, PARAM)
                with the followiing datatypes:
            (int, str, DEPENDS_ON_ELEMENT)
        
            
        Example for a row with following elements in the row (from left to right):
            - checkbox with a label
            - label 
            - button with a label on it and the command=sys.exit

            Thereby self.root is a tk.Tk object and implemented in an extra class.
            By the method 'get_last_y' the last y-position will be stored in y,
            so this y can be used for the next row (with adding an offset before...)

            All needed tk-Variables have to be initialized (and optionally they have
            to be set to an initial value)  before calling this method, 
            so that the variable can be passed into the constructor.
            
        #### -------------------------------------------------------------

        self.state_checkbox = tk.IntVar() 

        y = GuiElementsRow(root=self.root, y=10, elements=[
            (10, "chkbx", ("Text of checkbox", self.state_checkbox)),
            (100, "lbl", "This is the caption of the label"),
            (200, "btn", ("Cancel", sys.exit)),
        ]).get_last_y()

        #### -------------------------------------------------------------

        Available options for ELEMENT_KEYWORD and corresponding datatype/structure for its PARAM:

            KEYWORD    | element       | datatype| example & meaning of PARAM    |
                       |               |of PARAM |                               |
            -----------|---------------|---------|-------------------------------|
            "lbl"      | label         | str     | "caption_for_label"           |
            "btn"      | button        | tuple   | ("caption", command_function) |
            "cmb"      | combobox      | tuple   | ("option1", "option2")        |
            "chkbx"    | checkbox      | tuple   | ["lbl_caption", tk.IntVar()]  |
            "radiobtn" | radiobutton   | tuple   | ["lbl_caption", tk.IntVar()]  |
            "sep"      | seperatorline | int     | vertical_distance             |
            "txt"      | Entry         | ???     | # TODO...                     |
            "lbl_html" | label (html)  | str     | "caption_with_<h1>html</h1>"  |
            "img_html" | image (html)  | str     | "path/to/image/file.png"      |

            
        """

        # Buffering in object for easyer access: (instead of passing them as args)
        self.root = root
        self.y = y
        self.elements = elements
        self.y_last = y

        self.load_cases()

        for x, element_type, param in elements:

            func = self.cases[element_type]
            func(x, param)




    def load_cases(self):
        """
        Initialize a dictionary for matching the right function.
        """

        self.cases = {
                "lbl" : self.__new_label,
                "lbl_html" : self.__new_label_html,
                "img_html" : self.__new_image_html,
                "cmb" : self.__new_combobox,
                "btn" : self.__new_button,
                "chkbx" : self.__new_checkbox,
                "radiobtn" : self.__new_radiobutton,
                "sep" : self.__new_seperator_line,
                "txt" : self.__new_textbox,
            }
        


    def get_last_y(self) -> int:
        return self.y_last







    @staticmethod
    def validate_param(param, datatype_cls, length=None):
        """
        Raises a ParameterError if passed param is not the type of cls
        or if the length (if it is provided) does not fit.

        Args:
            param : Any parameter passed
            datatype_cls : required datatype class for param
            length : required length, if any, then None
                e.g.:    tuple, 10
                e.g.:    str
        """
        if datatype_cls == callable:
            if not  callable(param):
                raise ParameterError(param, datatype_cls, length)

        elif not isinstance(param, datatype_cls):
            raise ParameterError(param, datatype_cls, length)

        if length == None:
            return True
    
        if len(param) != length:
            raise ParameterError(param, datatype_cls, length)


        return True


    def __new_label(self, x:int, param:str):
        """
        Creates a new label and place it to the GUI.

        Args:
            x (int): x-location of the startpoint of the element
            param (str): text to be displayed.
        """

        self.validate_param(param, str)

        label = ttk.Label(self.root, text=param)
        label.place(x=x, y=self.y)





    def __new_combobox(self, x:int, param:tuple[str]):
        """
        Creates a new combobox and place it to the GUI.

        Args:
            x (int): x-location of the startpoint of the element
            param (tuple[str]): tuples with strings as options
        """

        self.validate_param(param, tuple)

        combo = ttk.Combobox(self.root, state="readonly", values=param)
        combo.place(x=x, y=self.y)






    def __new_button(self, x:int, param:tuple[str]):
        """
        Creates a new button and place it to the GUI.

        Args:
            x (int): x-location of the startpoint of the element
            param (tuple[str, function]): tuples with string as label and function as command
        """

        self.validate_param(param, (tuple, 2))

        caption = param[0]
        command_func = param[1]

        self.validate_param(caption, str)
        self.validate_param(command_func, callable)

        button = ttk.Button(self.root, text=caption, command=command_func)
        button.place(x=x, y=self.y)






    def __new_checkbox(self, x:int, param:tuple[str, tk.IntVar]):
        """
        Creates a new checkbox and place it to the GUI with linking to a tkinter-variable.
        The initial value of the element should be set via setting the tk.IntVar before.

        Args:
            x (int): x-location of the startpoint of the element
            param (tuple[str, tk.IntVar]): tuples with:
                                                            string as label
                                                            tkinterVariable as var
        """

        self.validate_param(param, tuple)

        caption = param[0]
        var = param[1]
   
        self.validate_param(caption, str)
        self.validate_param(var, tk.IntVar)
           


        button = ttk.Checkbutton(self.root, text=caption, variable=var)
        button.place(x=x, y=self.y)






    def __new_radiobutton(self, x:int, param:tuple[str, tk.IntVar]):
        """
        Creates a new radiobutton and place it to the GUI with linking to a tkinter-variable.
        The initial value of the element should be set via setting the tk.IntVar before.

        Args:
            x (int): x-location of the startpoint of the element
            param (tuple[str, tk.IntVar]): tuples with:
                                            string as label
                                            tkinterVariable as var
        
        
        # TODO: Does not work properly by now because the group/id is missing...
        
        """

        self.validate_param(param, tuple)

        caption = param[0]
        var = param[1]


        self.validate_param(caption, str)
        self.validate_param(var, tk.IntVar)
        
        button = ttk.Radiobutton(self.root, text=caption, variable=var)
        button.place(x=x, y=self.y) 






    def __new_textbox(self, x:int, param:tuple[tk.StringVar, str]):
        """
        Creates a new textbox as input-field and place it to the GUI with linking to a tkinter-variable.

        Args:
            x (int): x-location of the startpoint of the element
            param (tuple[str, tk.StringVar, optional:str]): tuples with:
                                                            tkinterVariable as var
                                                            str as OPTIONAL default value (defaults to "")
        """

        self.validate_param(param, tuple)

        var = param[0]

        if len(param) > 1:
            init_value = param[1]
        else:
            init_value = ""


        self.validate_param(var, tk.StringVar)
        self.validate_param(init_value, str)
        
        var.set(init_value)

        
        button = ttk.Entry(self.root, textvariable=var)
        button.place(x=x, y=self.y) 





    def __new_seperator_line(self, x:int, param:int):
        """
        Creates a new seperator line and place it to the GUI.

        Args:
            x (int): x-location of the startpoint of the element
            param (int): y_distance below

        # TODO: Does not work properly by now...
        """

        self.validate_param(param, int)

        separator = ttk.Separator(self.root, orient='horizontal')
        separator.place(relx=0, y=self.y + param, relwidth=1, relheight=0.2)

        self.y_last = self.y_last + param

        label = ttk.Label(self.root, text=param)
        label.place(x=x, y=self.y)






    def __consider_availability_htmlview(self, x, param:str) -> bool:
        """
        Checks wheather import of tkhtmlview  was successfull. 
        If not, use x and param to generate and place an usual label to the gui instead.

        Args:
            x (int): x-location of the label
            param (str): alternative-text.

        Returns:
            bool: True if tkhtmlview was imported correctly,
                  False if this module is not available.
        """

        if "tkhtmlview" not in sys.modules:

            self.__new_label(x, param)

            return False
        
        return True



    def __new_label_html(self, x:int, param:str):
        """
        Creates a new HTML label and place it to the GUI.
        If module 'tkhtmlview' was not included, it will create an usual label instead and only print an Warning via print-statement! (No error will be raised!)

        Args:
            x (int): x-location of the startpoint of the label
            param (str): text to be displayed.
        """

        self.validate_param(param, str)

        if not self.__consider_availability_htmlview(x, param):

            
            return
    
        label = HTMLLabel(self.root, html=param)
        label.place(x=x, y=self.y)





    def __new_image_html(self, x:int, param:str):
        """
        Creates a new HTML image and place it to the GUI.
        If module 'tkhtmlview' was not included, it will create an usual label with the path of the image instead and only print an Warning via print-statement! (No error will be raised!)

        Args:
            x (int): x-location of the startpoint of the label
            param (str): path to the image
        """

        self.validate_param(param, str)

        if not self.__consider_availability_htmlview(
            x, 
            param=f"<Image can not be displayed here as tkhtmlview was not imported correctly. Path of the image: '{param}'>"
        ):
            return

        html=f"<img src={param}>"
        img = HTMLLabel(self.root, html=html)
        img.place(x=x, y=self.y)





       


# =============================================================================
#### MAIN: 
# =============================================================================
def main():

    print("To test and display an example, run  'python example.py'")
    






if __name__ == '__main__':

    main()

    print(chr(13), '>>>>>>> ENDE FROM {}.'.format(__file__))