import tkinter as tk
from ObjectsPage import Objects
from PIL import Image, ImageTk
import os
from stix_io import OpenProject, LoadEnvironment, readfile, ImportFile, ExportProject, OpenInExplorer, NewProject, checkcfgfolder, LoadPrevious
from tkinter import messagebox
from tools import Elevate
import pickle


def enableOptions():
    editmenu.entryconfig("Import", state=tk.NORMAL)
    editmenu.entryconfig("Export Project", state=tk.NORMAL)
    editmenu.entryconfig("Open in Explorer", state=tk.NORMAL)

def disableOptions():
    editmenu.entryconfig("Import", state=tk.DISABLED)
    editmenu.entryconfig("Export Project", state=tk.DISABLED)
    editmenu.entryconfig("Open in Explorer", state=tk.DISABLED)

def picklesave(temp):
    sav = open("sav.dat", "wb")
    pickle.dump(temp, sav)
    sav.close()

def options_command():
    picklesave(displaytype.get())
    objects_page.display_type.set(displaytype.get())
    if objects_page.object != "nothing":
        objects_page.updatelist(objects_page.object)




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
editmenu.add_command(label="New Project...", command= lambda : [(objects_page.place(x=0,y=0) , objects_page.grab_set(), enableOptions()) if NewProject() else print("")])
editmenu.add_command(label="Open Existing Project", command= lambda: [(objects_page.place(x=0,y=0), objects_page.grab_set(), objects_page.enlistall(), enableOptions()) if OpenProject() else print("")])
editmenu.add_command(label="Load Previously Opened Project", command= lambda: [(objects_page.place(x=0,y=0) , objects_page.enlistall(), enableOptions()) if LoadPrevious() else print("")])
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

toolsmenu = tk.Menu(menubar, tearoff=0)
toolsmenu.add_command(label="Convert STIX1 item to STIX2...", command=lambda : [Elevate()])
toolsmenu.add_command(label="Bundle Management...")
menubar.add_cascade(label="Tools", menu=toolsmenu)

# display the menu
root.config(menu=menubar)

objects_page = Objects(root)
#objects_page.place(x=0,y=0)



displaytype = tk.BooleanVar()

try:
    sav = open("sav.dat","rb")
    temp = pickle.load(sav)
    sav.close()
    print("open-dis " + str(temp))
except:
    picklesave(True)
    temp=True
    print("i am in here")

displaytype.set(temp)
objects_page.display_type.set(temp)
optionsmenu = tk.Menu(menubar, tearoff=0)
optionsmenu.add_checkbutton(label="Display type", onvalue=True, offvalue=False, variable=displaytype, command=lambda : options_command())
optionsmenu.add_separator()
menubar.add_cascade(label="Options", menu=optionsmenu)

helpmenu.grab_release()


checkcfgfolder()
root.mainloop()
