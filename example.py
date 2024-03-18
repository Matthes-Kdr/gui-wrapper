
from gui_elements import GuiElementsRow
import textwrap
import tkinter as tk
import sys




class DemoExample:

    def __init__(self):

        self.title = "Demo-Gui"
        self.build_layout()
        self.main_window.mainloop()



    def build_layout(self):
        """
        Define the layout of the gui via calls for each row.
        """
        self.main_window = tk.Tk()
        self.main_window.config(width=900, height=500)
        self.main_window.title(self.title)

        y = 0

        space_y = 30
        y_space_next_step = 55 
        x_label = 200 # x position of the label with discribtion of the task

        chars_per_line = 130

        y += 10
        y = GuiElementsRow(root=self.main_window, y=y, elements=[
            (50, "lbl_html",  textwrap.fill("<h3>Demo-GUI</h3>", width=chars_per_line)),
        ]
        ).get_last_y()


        y += y_space_next_step
        self.state_checkbox1 = tk.IntVar()

        y = GuiElementsRow(root=self.main_window, y=y, elements=[
            (50, "chkbx",  ("Step 1:", self.state_checkbox1)),
            (x_label, "lbl", textwrap.fill("Do something", width=chars_per_line)),
        ]
        ).get_last_y()


        y += y_space_next_step
        self.state_radio1 = tk.IntVar(value=1)

        y = GuiElementsRow(root=self.main_window, y=y, elements=[
            (50, "radiobtn",  ("Choose this", self.state_radio1)),
            (x_label, "lbl", textwrap.fill("Or choose nothing", width=chars_per_line)),
        ]
        ).get_last_y()

        y += y_space_next_step
        self.state_radio2 = tk.IntVar(value=0)

        y = GuiElementsRow(root=self.main_window, y=y, elements=[
            (50, "radiobtn",  ("Choose nothing", self.state_radio2)),
            (x_label, "lbl", textwrap.fill("Or choose this", width=chars_per_line)),
        ]
        ).get_last_y()


        y += y_space_next_step

        y = GuiElementsRow(root=self.main_window, y=y, elements=[
            (50, "img_html", "demo_screenshot.png"),
        ]
        ).get_last_y()


        y += y_space_next_step *1.5

        y = GuiElementsRow(root=self.main_window, y=y, elements=[
            (50, "lbl_html", "Click <a href='readme.html'>here</a> for opening the readme"),
        ]
        ).get_last_y()









        y += space_y *1.5
        y = GuiElementsRow(root=self.main_window, y=y, elements=[
            (50, "btn",  ("Close here", self.close)),
            (200, "btn",  ("Close there", self.close)),
        ]
        ).get_last_y()






    def close(self):
        sys.exit()





# =============================================================================
#### MAIN: 
# =============================================================================
def main():

    demo_gui  =  DemoExample()
    



if __name__ == '__main__':

    main()

    print(chr(13), '>>>>>>> ENDE FROM {}.'.format(__file__))