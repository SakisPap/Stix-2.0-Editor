'''
This file is part of STIX 2.0 UoM Editor.

STIX 2.0 UoM Editor is free software: you can redistribute it and/or modify

it under the terms of the GNU General Public License as published by

the Free Software Foundation, either version 3 of the License, or

(at your option) any later version.

STIX 2.0 UoM Editor is distributed in the hope that it will be useful,

but WITHOUT ANY WARRANTY; without even the implied warranty of

MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the

GNU General Public License for more details.

You should have received a copy of the GNU General Public License

along with STIX 2.0 UoM Editor.  If not, see <http://www.gnu.org/licenses/>.
'''
import tkinter as tk
from ObjectsPage import Objects
from PIL import Image, ImageTk
import os
from stix_io import OpenProject, LoadEnvironment, readfile, ImportFile, ExportProject, OpenInExplorer, NewProject, checkcfgfolder, LoadPrevious
from tkinter import messagebox
from tools import Elevate
import pickle
import webbrowser


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

def about_window():
    window = tk.Toplevel(root, relief=tk.FLAT, highlightthickness=0)
    window.geometry("445x175")
    window.resizable(width=False, height=False)
    window.title("About")
    window.attributes('-topmost', 'true')
    window.grab_set()

    text = tk.Label(window, text="\nSTIX 2.0 UoM Editor  Copyright (C) 2018  InfoSec Research Group UoM\n\n"
                         "Contact: stix2ed.team@gmail.com\n\n"
                         "Under GNU GPL v3 license.\n")
    text.pack()
    image = tk.Button(window, image=gpl_img, relief=tk.FLAT, cursor="hand2", command=lambda : [webbrowser.open("https://www.gnu.org/licenses/gpl-3.0.en.html"), window.attributes('-topmost', 'false')])
    image.pack()


def contact_window():
    window = tk.Toplevel(root, relief=tk.FLAT, highlightthickness=0)
    window.geometry("200x210")
    window.resizable(width=False, height=False)
    window.title("Contact")
    window.attributes('-topmost', 'true')
    window.grab_set()

    labelframe = tk.LabelFrame(window, text="Andreas Stavropoulos", font=("OpenSans", 9, "bold"))
    #cname = tk.Label(labelframe, text="\nAndreas Stavropoulos")
    cmail = tk.Label(labelframe, text="\nantrsta@hotmail.com")
    chyper = tk.Label(labelframe, text="Linkedin\n", cursor="hand2", fg="blue")
    chyper.bind("<Button-1>", lambda _: [webbrowser.open_new("https://www.youtube.com/watch?v=dQw4w9WgXcQ"), window.attributes('-topmost', 'false')])
    #cname.pack()
    cmail.pack()
    chyper.pack()
    labelframe.pack(pady=10, padx=10, fill="both", expand="yes")

    labelframe2 = tk.LabelFrame(window, text="Sakis Papageorgiou", font=("OpenSans", 9, "bold"))
    #cname2 = tk.Label(window, text="\nSakis Papageorgiou")
    cmail2 = tk.Label(labelframe2, text="\nsakispap95@gmail.com")
    chyper2 = tk.Label(labelframe2, text="Linkedin\n", cursor="hand2", fg="blue")
    chyper2.bind("<Button-1>", lambda _: [webbrowser.open_new("http://linkedin.com/in/sakis-papageorgiou-5b2517151"), window.attributes('-topmost', 'false')])
    #cname2.pack()
    cmail2.pack()
    chyper2.pack()
    labelframe2.pack(pady=10, padx=10, fill="both", expand="yes")




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

img = Image.open(os.path.abspath("images/gpl_image.png"))
gpl_img = ImageTk.PhotoImage(img)


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
helpmenu.add_command(label="About", command=lambda : about_window())
helpmenu.add_command(label="Contact", command=lambda : contact_window())
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
