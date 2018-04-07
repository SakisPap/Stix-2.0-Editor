import tkinter as tk
from ObjectsPage import Objects
from PIL import Image, ImageTk
import os
from stix_io import OpenProject, LoadEnvironment, readfile, ImportFile, ExportProject, OpenInExplorer
from tkinter import messagebox


def enableOptions():
    editmenu.entryconfig("Import", state=tk.NORMAL)
    editmenu.entryconfig("Export Project", state=tk.NORMAL)
    editmenu.entryconfig("Open in Explorer", state=tk.NORMAL)

def disableOptions():
    editmenu.entryconfig("Import", state=tk.DISABLED)
    editmenu.entryconfig("Export Project", state=tk.DISABLED)
    editmenu.entryconfig("Open in Explorer", state=tk.DISABLED)


root = tk.Tk()
root.geometry("800x480")
root.configure(background = "#AED1D6")
root.resizable(width=False, height=False)
root.title("STIX 2.0 Editor")
try:
    root.iconbitmap(os.path.abspath("logo.ico"))
except: Exception

img = Image.open(os.path.abspath("images/welcome_page.png"))
welcome_page = ImageTk.PhotoImage(img)
welcomeLabel = tk.Label(root, image= welcome_page, bg="#AED1D6")
welcomeLabel.pack()

# create a toplevel menu
menubar = tk.Menu(root, foreground="black", background="#AED1D6", activebackground='#004c99', activeforeground='white')

# create more pulldown menus
editmenu = tk.Menu(menubar, tearoff=0)
editmenu.add_command(label="New Project...", command= lambda : [objects_page.place(x=0,y=0) , objects_page.grab_set(), enableOptions()])
editmenu.add_command(label="Open Existing Project", command= lambda: [(objects_page.place(x=0,y=0), objects_page.grab_set(), objects_page.enlistall()) if OpenProject() else print(""), enableOptions()])
editmenu.add_command(label="Load Previously Opened Project", command= lambda: [LoadEnvironment(readfile(os.path.join(os.path.dirname(os.path.abspath(__file__)), "last"))) ,objects_page.place(x=0,y=0) , objects_page.enlistall(), enableOptions()])
editmenu.add_separator()
editmenu.add_command(label="Import", command=lambda: [ImportFile()])
editmenu.add_command(label="Export Project", command=lambda: [ExportProject()])
editmenu.add_command(label="Open in Explorer", command=lambda: [OpenInExplorer()])

disableOptions()

menubar.add_cascade(label="File", menu=editmenu)

helpmenu = tk.Menu(menubar, tearoff=0)
helpmenu.add_command(label="About")
helpmenu.add_command(label="Contact")
helpmenu.add_command(label="Report Bugs")
menubar.add_cascade(label="Help", menu=helpmenu)

# display the menu
root.config(menu=menubar)

objects_page = Objects(root)
#objects_page.place(x=0,y=0)
helpmenu.grab_release()



root.mainloop()