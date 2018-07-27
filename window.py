#-------------------------------------------------------------------------------
# Purpose:
#
# Author:      Andre Santos Barros da Silva
#
# Created:     27/07/2018
# Copyright:   
# Licence:     
#-------------------------------------------------------------------------------
from tkinter import *



root = Tk()
root.title('Notebook')



texto = Label(root,text='SHOW').place(x=10,y=5)

horizontal=0
vertical=40

btnPlotar = Button(root, text="SAMPLE").place(x=horizontal,y=vertical)
vertical+=30
btnPlotar = Button(root, text="PLOT").place(x=horizontal,y=vertical)
vertical+=30
btnResetar = Button(root, text="RESET").place(x=horizontal,y=vertical)
vertical+=30
btnPlotar = Button(root, text="CLOSE").place(x=horizontal,y=vertical)
vertical+=30
btnPlotar = Button(root, text="BACK").place(x=horizontal,y=vertical)
vertical+=30
btnPlotar = Button(root, text="DOWNLOAD").place(x=horizontal,y=vertical)




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

root.title("Cristal Mat - Xtress - IPEN")
root.geometry("650x380+10+10")
root.mainloop()
