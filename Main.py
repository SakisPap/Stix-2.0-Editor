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
from stix_io import OpenProject, LoadEnvironment, readfile, ImportFile, ExportProject, OpenInExplorer, NewProject, checkcfgfolder, LoadPrevious, getcfgfile
from tkinter import messagebox
from tools import Elevate, bugreport, BundleManage
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

def picklesave(displaytype, sort, view):
    sav = open(getcfgfile(), "wb")
    pickle.dump([displaytype, sort, view], sav)
    sav.close()

def options_command():
    picklesave(displaytype.get(), sort.get(), view.get())
    objects_page.display_type.set(displaytype.get())
    objects_page.viewby.set(view.get())
    objects_page.sortby.set(sort.get())
    if objects_page.object != "nothing":
        objects_page.updatelist(objects_page.object)
    else:
        try:
            objects_page.enlistall()
        except:
            print("exception in options_command possibly bc of filesystem not being loaded")



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




def bugreport_window():
    window = tk.Toplevel(root, relief=tk.FLAT, highlightthickness=0)
    window.geometry("445x210")
    window.resizable(width=False, height=False)
    window.title("Report Bug")
    window.attributes('-topmost', 'true')
    window.grab_set()

    label = tk.Label(window, text="Please describe the issue with as many details as possible,\nprovide your contact info if you want us to reach you back.")
    label.pack(pady=5)
    reportEntry = tk.Text(window, font=("OpenSans", 9), width=60, height=8, wrap=tk.WORD)
    reportEntry.pack(padx=10)

    submit = tk.Button(window, text="Submit", command = lambda : [(label.config(text="Sending the report...\n", fg="black"), submit.config(text="Please wait..."), label.update(), submit.update(), bugreport(window, reportEntry.get("1.0", tk.END))) if not reportEntry.compare("end-1c", "==", "1.0") else label.config(text="Warning: You cannot submit an empty form!\n", fg="red")])
    submit.pack(pady=10)



def bundle_management_window():
    window = tk.Toplevel(root, relief=tk.FLAT, highlightthickness=0)
    window.geometry("285x70")
    window.resizable(width=False, height=False)
    window.title("Bundle Management")
    window.attributes('-topmost', 'true')
    window.grab_set()

    importButton = tk.Button(window,text="Import Bundle Objects into current Project", command= lambda : [window.destroy(), BundleManage("import")])
    importButton.pack(padx=1)

    extractButton = tk.Button(window, text="Extract Bundle Objects into a directory", command=lambda: [window.destroy(), BundleManage("extract")])
    extractButton.pack(padx=1)



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
helpmenu.add_command(label="Report Bugs", command=lambda : bugreport_window())
menubar.add_cascade(label="Help", menu=helpmenu)

toolsmenu = tk.Menu(menubar, tearoff=0)
toolsmenu.add_command(label="Convert STIX1 item to STIX2...", command=lambda : [Elevate()])
toolsmenu.add_command(label="Bundle Management...", command=lambda : [bundle_management_window()])
menubar.add_cascade(label="Tools", menu=toolsmenu)

# display the menu
root.config(menu=menubar)

objects_page = Objects(root)
#objects_page.place(x=0,y=0)



displaytype = tk.BooleanVar()
sort = tk.StringVar()
view = tk.StringVar()


try:
    sav = open(getcfgfile(), "rb")
    displaytype1, sort1, view1 = pickle.load(sav)
    displaytype.set(displaytype1)
    sort.set(sort1)
    view.set(view1)
    sav.close()
    print("open-dis " + str(displaytype.get()))
    print("open-dis " + str(sort.get()))
    print("open-dis " + str(view.get()))
except:
    picklesave(True, "alph", "name")
    displaytype.set(True)
    sort.set("alph")
    view.set("name")
    print("i am in here")

objects_page.display_type.set(displaytype.get())
objects_page.viewby.set(view.get())
objects_page.sortby.set(sort.get())
optionsmenu = tk.Menu(menubar, tearoff=0)
viewbyMenu = tk.Menu(menubar)
sortbyMenu = tk.Menu(menubar)

optionsmenu.add_separator()
optionsmenu.add_checkbutton(label="Display objects type", onvalue=True, offvalue=False, variable=displaytype, command=lambda : options_command())
optionsmenu.add_separator()

optionsmenu.add_cascade(label="View by", menu=viewbyMenu)
viewbyMenu.add_radiobutton(label="Name", variable=view, value="name", command=lambda : options_command())
viewbyMenu.add_radiobutton(label="Id", variable=view, value="id", command=lambda : options_command())
optionsmenu.add_separator()


optionsmenu.add_cascade(label="Sort by", menu=sortbyMenu)
sortbyMenu.add_radiobutton(label="Alphabetical ▲", variable=sort, value="alph", command=lambda : options_command())
sortbyMenu.add_radiobutton(label="Alphabetical ▼", variable=sort, value="alphdesc", command=lambda : options_command())
sortbyMenu.add_separator()
sortbyMenu.add_radiobutton(label="Last Modified ▲", variable=sort, value="lm", command=lambda : options_command())
sortbyMenu.add_radiobutton(label="Last Modified ▼", variable=sort, value="lmdesc", command=lambda : options_command())
optionsmenu.add_separator()


menubar.add_cascade(label="Options", menu=optionsmenu)







helpmenu.grab_release()







checkcfgfolder()
root.mainloop()
