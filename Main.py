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
from stix_io import OpenProject, LoadEnvironment, readfile, ImportFile, ExportProject, OpenInExplorer, NewProject, checkcfgfolder, LoadPrevious, getcfgfile, getcfgfile2, getcfgfile3
from tkinter import messagebox
from tools import *
import pickle
import webbrowser
import sys, subprocess


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


def datatypehelp(datatype):
    if(datatype=="string"):
        messagebox.showinfo("String", "A series of unicode characters. Text that can contain any character,whitespaces and symbols, with only exception the Name property.\n\n Example: \"This is a Threat Actor Object.\"")
    elif(datatype=="list"):
        messagebox.showinfo("List",
                            "A sequence of values ordered based on how they appear in the list. The phrasing “list of type <type>” is used to indicate that all values within the list MUST conform to the specified type.\n\n"
                            "The most common encountered lists are of type String and Identifier (ID).\nA single whitespace is used to seperate the strings in list. On any other occasion (e.g. identifier list or open-vocab list you only have to click one or multiple entries on the Multi-Selection feature of the GUI.\n\n"
                            "String List Example (properties such as Labels, Aliases, Goals: \"damage fraud threat-actor\" will produce a list of 3 elements, damage, fraud and threat-actor. Please remember than multiple entries in String List are seperated with space, not with comma or any other character."
                            "\n\nFinally, in any other case, you will have to ultilize Multi-Selection mechanic, as mentioned above. Please refer to the proper section in the Manual if you need help about it.")
    elif(datatype=="open-vocab"):
        messagebox.showinfo("Vocabulary", "open-vocab A value from a STIX open (open-vocab) or suggested vocabulary.\n\nIt is ultilized in a drop-down list, or a Multi-Selection with all the allowed values for the specific property. User makes a selection instead of typing and manually inputting. \n\nSelecting the blank option from the drop-down list ignores the specific property, but please note that this is valid only for optional properties, on which there is an option for reset, (in case user selected a value but then wants to revert it) by selecting the first, blank option.")
    elif(datatype=="identifier"):
        messagebox.showinfo("Identifier", "An identifier universally and uniquely identifies a SDO, SRO, Bundle, or Marking Definition. Identifiers MUST follow the form object-type--UUIDv4, where object-type is the exact value (all type names are lowercase strings, by definition) from the type property of the object being identified or referenced and where the UUIDv4 is an RFC 4122-compliant Version 4 UUID. The UUID MUST be generated according to the algorithm(s) defined in RFC 4122.\n\nNOTE: By default the ID is automatically generated. It is located in the third page of Object Editor (auto generated properties) and it is recommended to non-advanced users to leave this property empty.")
    elif(datatype=="timestamp"):
        tk.messagebox.showinfo("Timestamp", "A time value (date and time). The timestamp property MUST be a valid RFC 3339-formatted timestamp [RFC3339] using the format YYYY-MM-DDTHH:mm:ss[.s+]Z where the “s+” represents 1 or more sub-second values. The brackets denote that sub-second precision is optional, and that if no digits are provided, the decimal place MUST NOT be present. The timestamp MUST be represented in the UTC timezone and MUST use the “Z” designation to indicate this.\n\nA timestamp example of the above format would be:\n\"2018-04-30T14:10:31.661Z\"\n\nAlternatively, for ease of access, you could enter the timestamp in the format YYYY/MM/DD hh:mm:ss (please include the backslashes, whitespace and colon), for example \"27/04/2018 18:44:22\".")
    elif(datatype=="boolean"):
        tk.messagebox.showinfo("Boolean", "A value of true or false. All boolean values are presented with a checkbox.\n\nA ticked checkbox means that the property is True while an unticked, False.")
    elif(datatype=="integer"):
        tk.messagebox.showinfo("Integer", "A whole number, in the range of ([-(2**63)+1, (2**63)-1].\n\nFor example, a valid integer is 48921 but not 3,9841 or 8421.421. It should contain numbers and only.")
    elif(datatype=="external-reference"):
        tk.messagebox.showinfo("External Reference", "A non-STIX identifier or reference to other related external content. Being non-STIX, its non-project related and it can be created from the Tools menu. Every constructed External Reference is accessible to any project.")
    elif(datatype=="kill-chain-phase"):
        tk.messagebox.showinfo("Kill Chain Phase", "The kill-chain-phase represents a phase in a kill chain, which describes the various phases an attacker may undertake in order to achieve their objectives. Not being a STIX object, its non-project related and it can be created from the Tools menu. Every constructed Kill Chain Phase is accessible to any project.")


def about_window():
    window = tk.Toplevel(root, relief=tk.FLAT, highlightthickness=0)
    window.geometry("445x175")
    window.resizable(width=False, height=False)
    window.title("About")
    window.attributes('-topmost', 'true')
    try:
        window.iconbitmap(os.path.join(getExecPath(), "logo.ico"))
    except:
        img = tkinter.PhotoImage(file=os.path.join(getExecPath(), "logo.gif"))
        window.tk.call('wm', 'iconphoto', window._w, img)
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
    try:
        window.iconbitmap(os.path.join(getExecPath(), "logo.ico"))
    except:
        img = tkinter.PhotoImage(file=os.path.join(getExecPath(), "logo.gif"))
        window.tk.call('wm', 'iconphoto', window._w, img)
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
    try:
        window.iconbitmap(os.path.join(getExecPath(), "logo.ico"))
    except:
        img = tkinter.PhotoImage(file=os.path.join(getExecPath(), "logo.gif"))
        window.tk.call('wm', 'iconphoto', window._w, img)
    window.grab_set()

    label = tk.Label(window, text="Please describe the issue with as many details as possible,\nprovide your contact info if you want us to reach you back.")
    label.pack(pady=5)
    reportEntry = tk.Text(window, font=("OpenSans", 9), width=60, height=8, wrap=tk.WORD)
    reportEntry.pack(padx=10)

    submit = tk.Button(window, text="Submit", command = lambda : [(label.config(text="Sending the report...\n", fg="black"), submit.config(text="Please wait..."), label.update(), submit.update(), bugreport(window, reportEntry.get("1.0", tk.END))) if not reportEntry.compare("end-1c", "==", "1.0") else label.config(text="Warning: You cannot submit an empty form!\n", fg="red")])
    submit.pack(pady=10)



def bundle_management_window():
    window = tk.Toplevel(root, relief=tk.FLAT, highlightthickness=0)
    #window.geometry("285x70")
    window.resizable(width=False, height=False)
    window.title("Bundle Management")
    window.attributes('-topmost', 'true')
    window.grab_set()

    importButton = tk.Button(window,text="Import Bundle Objects into current Project", command= lambda : [window.destroy(), BundleManage("import")])
    importButton.pack(padx=5, pady=5, fill=tk.X)

    extractButton = tk.Button(window, text="Extract Bundle Objects into a directory", command=lambda: [window.destroy(), BundleManage("extract")])
    extractButton.pack(padx=5, pady=5, fill=tk.X)



#*****************************BEGIN MAIN EXEC***********************************
checkcfgfolder()
try:
    theme_file = open(getcfgfile2(), "rb")
    theme = pickle.load(theme_file)
    theme_file.close()
except:
    theme_file = open(getcfgfile2(), "wb")
    theme = "sea"
    pickle.dump(theme, theme_file)
    theme_file.close()

try:
    rez_file = open(getcfgfile3(), "rb")
    resolution = pickle.load(rez_file)
    theme_file.close()
except:
    rez_file = open(getcfgfile3(), "wb")
    resolution = "1050x600"
    pickle.dump(resolution, rez_file)
    theme_file.close()

#--color decleration--
if theme == "sea":
    COLOR_1 = "#AED1D6"
elif theme == "multi":
    COLOR_1 = "#B4D2BA"
elif theme == "semidark":
    COLOR_1 = "#F7EBE8"
elif theme == "dark":
    COLOR_1 = "#9999A1"
elif theme == "bordeu":
    COLOR_1 = "#A9927D"
elif theme == "green":
    COLOR_1 = "#C3D898"

root = tk.Tk()
root.geometry(resolution)
root.configure(background = COLOR_1)
#root.resizable(width=False, height=False)
root.minsize(1050, 600)
root.title("STIX 2.0 Editor")
def save_rez(event):
    rez_file = open(getcfgfile3(), "wb")
    resolution = str(root.winfo_width())+"x"+str(root.winfo_height())
    #print(resolution)
    pickle.dump(resolution, rez_file)
    theme_file.close()
root.bind( "<Configure>", save_rez)


try:
    root.iconbitmap(os.path.abspath("logo.ico"))
except:
    img = tkinter.PhotoImage(file='logo.gif')
    root.tk.call('wm', 'iconphoto', root._w, img)


img = Image.open(os.path.abspath("images/welcome_page.png"))
welcome_page = ImageTk.PhotoImage(img)
welcomeLabel = tk.Label(root, image= welcome_page, bg=COLOR_1)
welcomeLabel.pack(fill=tk.BOTH, expand=True)

img = Image.open(os.path.abspath("images/gpl_image.png"))
gpl_img = ImageTk.PhotoImage(img)


# create a toplevel menu
menubar = tk.Menu(root, foreground="black", background= COLOR_1, activebackground='#004c99', activeforeground='white')

# create more pulldown menus
editmenu = tk.Menu(menubar, tearoff=0)
editmenu.add_command(label="New Project...", command= lambda : [(welcomeLabel.pack_forget(), objects_page.pack(fill=tk.BOTH, expand=True), enableOptions()) if NewProject() else print("")])
editmenu.add_command(label="Open Existing Project", command= lambda: [(welcomeLabel.pack_forget(), objects_page.pack(fill=tk.BOTH, expand=True), objects_page.enlistall(), enableOptions()) if OpenProject() else print("")])
editmenu.add_command(label="Load Previously Opened Project", command= lambda: [(welcomeLabel.pack_forget(), objects_page.pack(fill=tk.BOTH, expand=True) , objects_page.enlistall(), enableOptions()) if LoadPrevious() else print("")])
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
mngmntMenu = tk.Menu(menubar)#
toolsmenu.add_command(label="Convert STIX1 item to STIX2...", command=lambda : [Elevate()])
#toolsmenu.add_command(label="Bundle Management...", command=lambda : [bundle_management_window()])
toolsmenu.add_cascade(label="Bundle Management...", menu=mngmntMenu) #
mngmntMenu.add_command(label="Import Bundle Objects into current Project", command= lambda : [BundleManage("import"), objects_page.enlistall(), objects_page.selector("nothing")])#
mngmntMenu.add_separator()#
mngmntMenu.add_command(label="Extract Bundle Objects into a directory", command=lambda: [BundleManage("extract")])#
mngmntMenu.add_separator()#


datatypesmenu=tk.Menu(menubar, tearoff=0)
datatypesmenu.add_command(label="String", command = lambda : [datatypehelp("string")])
datatypesmenu.add_command(label="List", command = lambda : [datatypehelp("list")])
datatypesmenu.add_command(label="Open Vocabulary", command = lambda : [datatypehelp("open-vocab")])
datatypesmenu.add_command(label="Identifier (ID)", command = lambda : [datatypehelp("identifier")])
datatypesmenu.add_command(label="Timestamp", command = lambda : [datatypehelp("timestamp")])
datatypesmenu.add_command(label="Boolean", command = lambda : [datatypehelp("boolean")])
datatypesmenu.add_command(label="Integer", command = lambda : [datatypehelp("integer")])
datatypesmenu.add_command(label="External Reference", command = lambda : [datatypehelp("external-reference")])
datatypesmenu.add_command(label="Kill Chain Phase", command = lambda : [datatypehelp("kill-chain-phase")])
menubar.add_cascade(label="Data Types Help", menu=datatypesmenu)


def killchainStart():
    killchainphasemaker = KillChainPhaseMaker(root)
    killchainphasemaker.grab_set()
    #killchainphasemaker.lift()
    killchainphasemaker.attributes('-topmost', 'true')

def externalStart():
    externalreferencesmaker = ExternalReferenceMaker(root)
    externalreferencesmaker.grab_set()
    #killchainphasemaker.lift()
    externalreferencesmaker.attributes('-topmost', 'true')

toolsmenu.add_command(label="Manage Kill Chain Phases...", command=lambda : [killchainStart()])
toolsmenu.add_command(label="Manage External References...", command=lambda : [externalStart()])
backupMenu = tk.Menu(menubar)
toolsmenu.add_cascade(label="Backup", menu=backupMenu)
backupMenu.add_command(label="Create...", command= lambda : [backup()])#

backupMenu.add_command(label="Restore...", command=lambda: [restore()])#


menubar.add_cascade(label="Tools", menu=toolsmenu)

# display the menu
root.config(menu=menubar)

objects_page = Objects(root, theme)
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
except:
    picklesave(True, "alph", "name")
    displaytype.set(True)
    sort.set("alph")
    view.set("name")

objects_page.display_type.set(displaytype.get())
objects_page.viewby.set(view.get())
objects_page.sortby.set(sort.get())
optionsmenu = tk.Menu(menubar, tearoff=0)
viewbyMenu = tk.Menu(menubar)
sortbyMenu = tk.Menu(menubar)
themeMenu = tk.Menu(menubar)


optionsmenu.add_checkbutton(label="Display objects type", onvalue=True, offvalue=False, variable=displaytype, command=lambda : options_command())

optionsmenu.add_cascade(label="View by", menu=viewbyMenu)
viewbyMenu.add_radiobutton(label="Name", variable=view, value="name", command=lambda : options_command())
viewbyMenu.add_radiobutton(label="Id", variable=view, value="id", command=lambda : options_command())


optionsmenu.add_cascade(label="Sort by", menu=sortbyMenu)
sortbyMenu.add_radiobutton(label="Alphabetical ▲", variable=sort, value="alph", command=lambda : options_command())
sortbyMenu.add_radiobutton(label="Alphabetical ▼", variable=sort, value="alphdesc", command=lambda : options_command())

sortbyMenu.add_radiobutton(label="Date Modified ▲", variable=sort, value="lm", command=lambda : options_command())
sortbyMenu.add_radiobutton(label="Date Modified ▼", variable=sort, value="lmdesc", command=lambda : options_command())
optionsmenu.add_separator()

def getExecPath():
    try:
        sFile = os.path.abspath(sys.modules['__main__'].__file__)
    except:
        sFile = sys.executable
    return os.path.dirname(sFile)

def restart():
    os.chdir(getExecPath())
    python = sys.executable
    script = os.path.join(getExecPath(), "Main.py")
    subprocess.Popen([python, script])
    sys.exit(0)


def change(theme):
    theme_file = open(getcfgfile2(), "wb")
    pickle.dump(theme, theme_file)
    theme_file.close()
    #ans=tk.messagebox.askyesno("Info", "Theme changes will take place after you restart the application!\nWould you like to restart now?")
    #if(ans):
        #restart()
    tk.messagebox.showinfo("Info", "Theme changes will take place after you restart the application!")


placeholder = tk.IntVar()
placeholder.set(theme)
optionsmenu.add_cascade(label="Theme", menu=themeMenu)
themeMenu.add_radiobutton(label="Sea", variable=placeholder, value="sea", command=lambda : change("sea"))
themeMenu.add_radiobutton(label="Multi", variable=placeholder, value="multi", command=lambda : change("multi"))
themeMenu.add_radiobutton(label="Semidark", variable=placeholder, value="semidark", command=lambda : change("semidark"))
themeMenu.add_radiobutton(label="Dark", variable=placeholder, value="dark", command=lambda : change("dark"))
themeMenu.add_radiobutton(label="Bordeu", variable=placeholder, value="bordeu", command=lambda : change("bordeu"))
themeMenu.add_radiobutton(label="Green", variable=placeholder, value="green", command=lambda : change("green"))

optionsmenu.add_command(label="Reset window geometry", command=lambda : root.geometry("1050x600"))






menubar.add_cascade(label="Options", menu=optionsmenu)

helpmenu.grab_release()
root.mainloop()

