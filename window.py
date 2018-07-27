#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      lgallego
#
# Created:     23/02/2017
# Copyright:   (c) lgallego 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from tkinter import *
#from ttk import *


root = Tk()
root.title('Notebook')

#menu
menubar = Menu(root)
filemenu= Menu(menubar)
filemenu.add_command(label="Open File")
filemenu.add_command(label="Close")
filemenu.add_separator()

menubar.add_cascade(label="File",menu=filemenu)
helpmenu = Menu(menubar)
helpmenu.add_command(label="Help Index")
helpmenu.add_command(label="About")
menubar.add_cascade(label="Help",menu=helpmenu)
root.config(menu=menubar)

root.title("Cristal Mat - IPEN")
root.geometry("650x380+10+10")
root.mainloop()
