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
import tkinter.filedialog
from tkinter import messagebox
from stix2elevator import *
from stix2elevator.options import *
import stix2
from stix_io import filetoitem,itemtofile,InitNewEnvironment
import urllib
from urllib.parse import *
from urllib.request import *
from urllib.response import *
from stix_io import *
import json


def Elevate():
    #disclaminer, show once add config ...
    tk.messagebox.showinfo("Elevation", "Please note that this function is non-project related. If you would like to import a STIX1 xml into a project just use the Import function and the elevation will be carried out automatically.")
    fpath = tk.filedialog.askopenfilename(initialdir="/", title="Please select a STIX1 xml file to elevate.",
                                          filetypes=[("xml files (STIX1)", "*.xml")])
    if fpath:
        try:
            initialize_options()
            stix1obj = elevate_file(fpath)
            # messagebox pou na rwatei an 8a ginei import sto project h oxi klp 8aexei kai save as
            spath=tk.filedialog.asksaveasfilename(initialdir="/",defaultextension=".json", title="Convert completed. Please select where would you like to save the item.",
                                          filetypes=[("json files (STIX2)", "*.json")])
            if spath:
                file = open(spath, "w")
                file.write(str(stix1obj))
                file.close()
                tk.messagebox.showinfo("Success", "Converted file has been saved.")
        except:
            tk.messagebox.showwarning("Error", "Selected file does not seem to be a valid STIX1 object. Import failed.")


def BundleManage(mode):
    if (mode == "import"):
        if not (isProjectActive()):
            tk.messagebox.showwarning("Error", "You are not into a project. Please Load or Create a project in order to import the Bundle Objects into it otherwise you could use the extract function.")
            return
    bundle=tk.filedialog.askopenfilename(initialdir="/", title="Please select a STIX2 Bundle file.",
                                          filetypes=[("json files (STIX2)", "*.json")])
    try:
        stix2bundle = stix2.parse(filetoitem(bundle))
        type = stix2bundle.get("type")
        if not (type=="bundle"):
            tk.messagebox.showwarning("Error", "Selected STIX2 object is not a Bundle.")
            return
        else:
            if (mode=="import"):
                for o in stix2bundle.get("objects"):
                    itemtofile(o)
                tk.messagebox.showinfo("Success", "Selected Bundle was successfully imported into current project.")
            else:#mode=="extract"
                dest = tk.filedialog.askdirectory(initialdir="/",
                                                  title="Please select a folder to extract the Bundle to.")
                if dest:
                    backupcwd = os.getcwd()
                    InitNewEnvironment(dest)
                    for o in stix2bundle.get("objects"):
                        itemtofile(o)
                    os.chdir(backupcwd)
                    tk.messagebox.showinfo("Success", "Selected Bundle was successfully extracted to the selected directory.")
    except:
        tk.messagebox.showwarning("Error", "This does not seem to be a valid STIX2 object. Import failed.")


def bugreport(parent, msg):
    try:
        message = urllib.parse.quote_plus(msg)
        req = urllib.request.Request("http://hubverifier.ddns.net/bugreport.php?bodyofmessage=" + message)
        req.add_header("Content-type", "application/x-www-form-urlencoded")
        urllib.request.urlopen(req)
        tk.messagebox.showinfo("Success!", "Bug report submitted successfully.\nThank you very much for your involvement!", parent=parent)
    except:
        tk.messagebox.showerror("Error", "Failed to send bug report.\n Check your internet connection and try again later.", parent=parent)
    parent.destroy()





class Multiselect(tk.Frame):
    def __init__(self, parent, labelparent, list_items, eRow, COLOR_1, COLOR_2, COLOR_3, flag=None):
        tk.Frame.__init__(self, parent, bg=COLOR_2, bd=3)
        self.parent=parent
        self.flag=flag
        self.labelparent = labelparent
        self.COLOR_1 = COLOR_1
        self.COLOR_2 = COLOR_2
        self.COLOR_3 = COLOR_3
        self.widgets()
        self.eRow = eRow
        self.list_items = list_items
        self.selected_items=[]

        for item in self.list_items:
            self.listview.insert(tk.END, item)


    def show_callback(self):
        self.pack(side=tk.LEFT)
        self.grab_set()
        try:
            self.showlabel.pack_forget()
        except:
            pass

    def done_callback(self):
        self.selected_items = []
        for item in self.listview.curselection():
            self.selected_items.append(self.listview.get(item))
        self.place_forget()
        tex = str(self.selected_items).replace("'", "").replace("[", "").replace("]", "")
        self.showlabel.config(text=tex)
        self.showlabel.grid(row=self.eRow, column=1)
        if tex == "":
            self.showlabel.grid_forget()
        self.grab_release()

    def widgets(self):
        self.showlabel = tk.Label(self.labelparent, font=("OpenSans", 10), bg=self.COLOR_1, wraplength=500)
        self.listview = tk.Listbox(self, exportselection=0, font=("OpenSans", 10, "bold"), bd=1, height=15,
                              relief=tk.FLAT, highlightthickness=0, fg=self.COLOR_3, selectmode='multiple')
        self.listview.pack()

        self.donebutton = tk.Button(self, text="Done", fg="white", bg="#03AC13", command=lambda: self.done_callback())
        self.donebutton.pack(side=tk.LEFT, fill=tk.X, expand=1)
        self.clearbutton = tk.Button(self, text="Clear", fg="white", bg="#FF9500", command=lambda: self.listview.selection_clear(0, tk.END))
        self.clearbutton.pack(side=tk.RIGHT, fill=tk.X, expand=1)
        self.xbutton = tk.Button(self, text="X", fg="white", bg="#FF3B30", command=lambda: [self.grab_release(), self.place_forget()])
        self.xbutton.pack(side=tk.RIGHT, fill=tk.X, expand=1)

    def get(self):
        if not self.flag:
            if self.selected_items:
                return self.selected_items
            else:
                return ""
        elif self.flag=="killchain":
            killchains=[]
            for item in self.selected_items:
                try:
                    killchains.append(json.load(open(os.path.join(getkcpfolder(), item+".kcp"))))
                except:
                    killchains.append(stix2.KillChainPhase(kill_chain_name=item.split("_")[0], phase_name=item.split("_")[1]))
                    tk.messagebox.showinfo("Notice", item+" is not present in the filesystem.")
            return killchains
        else:
            exrefs=[]
            for item in self.selected_items:
                exrefs.append(json.load(open(os.path.join(getexreffolder(),item+".ext"))))
            return exrefs

    def set(self, list):
        i = 0
        chain_text=[]
        ext_text=[]
        if self.flag=="killchain":
            for item in list:
                entity = item.get("kill_chain_name")+"_"+item.get("phase_name")
                chain_text.append(entity)
            list = chain_text
        elif self.flag=="exref":
            for item in list:
                entity = item.get("source_name")
                ext_text.append(entity)
            list = ext_text


        self.selected_items=list
        self.showlabel.config(text=str(self.selected_items).replace("'", "").replace("[", "").replace("]", ""))
        self.showlabel.grid(row=self.eRow, column=1)

        for item in self.list_items:
            if item in list:
                self.listview.select_set(i)
            i+=1







class KillChainPhaseMaker(tk.Toplevel):
    def __init__(self, root):
        tk.Toplevel.__init__(self, root)
        self.title("Manage Kill Chain Phases...")
        #self.geometry("400x110")
        self.resizable(width=False, height=False)
        self.frame = tk.Frame(self)
        self.frame.pack()
        self.frame.columnconfigure(1, weight=3)


        self.btframe = tk.Frame(self)
        self.btframe.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
        self.widgets()

    def keyPress(self, event):
        if event.char in ("-",
                          "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
                         " "):
            print
            event.char
        elif event.keysym not in ('BackSpace', 'Delete', 'Tab', 'Left', 'Right'):
            print
            event.keysym
            return 'break'

    def getlist(self):
        self.listview.delete(0, tk.END)
        for item in getKillChainPhases():
            self.listview.insert(tk.END, item)

    def widgets(self):
        self.killchainlabel = tk.Label(self.frame, text="Kill Chain Name:", font=("OpenSans", 12))
        self.killchainlabel.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)

        self.killchaintext = tk.Entry(self.frame, font=("OpenSans", 12))
        self.killchaintext.grid(row=0, column=1, padx=5, pady=5)
        self.killchaintext.bind('<KeyPress>', lambda event : self.keyPress(event))

        self.phaselabel = tk.Label(self.frame, text="Phase Name:", font=("OpenSans", 12))
        self.phaselabel.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)

        self.phasetext = tk.Entry(self.frame, font=("OpenSans", 12))
        self.phasetext.grid(row=1, column=1, padx=5, pady=5)

        self.label = tk.Label(self.btframe, font=("OpenSans", 8, "bold"), text="Existing Kill Chain Phase into workspace:", bg="black", fg="white")
        self.label.pack(fill=tk.X, padx=10)

        self.listview = tk.Listbox(self.btframe, font=("OpenSans", 10, "bold"), height=5)
        self.listview.pack(fill=tk.X, expand=True, padx=10)

        self.getlist()

        self.addbutton = tk.Button(self.btframe, text="Create", font=("OpenSans", 12), fg="white", bg="#03AC13", command=lambda : [(killchainphasetofile(self.killchaintext.get()+"_"+self.phasetext.get(), stix2.KillChainPhase(kill_chain_name=self.killchaintext.get(), phase_name=self.phasetext.get())), self.getlist(), tk.messagebox.showinfo("Success", "Kill Chain Phase created successfully!", parent=self)) if self.killchaintext.get()!="" and self.phasetext.get()!="" else tk.messagebox.showerror("Error", "Input fields cannot be empty!", parent=self)])
        self.addbutton.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)

        self.cancelbutton = tk.Button(self.btframe, text="Delete", font=("OpenSans", 12), fg="white", bg="#FF3B30", command=lambda : [(killchainphasedelete(self.listview.get(tk.ACTIVE), self), self.getlist()) if self.listview.get(tk.ACTIVE)!="" else print("")])
        self.cancelbutton.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)






class ExternalReferenceMaker(tk.Toplevel):
    def __init__(self, root):
        tk.Toplevel.__init__(self, root)
        self.title("Manage External References...")
        # self.geometry("400x110")
        self.resizable(width=False, height=False)
        self.frame = tk.Frame(self)
        self.frame.pack()
        self.frame.columnconfigure(1, weight=3)

        self.btframe = tk.Frame(self)
        self.btframe.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
        self.widgets()

    """
    def keyPress(self, event):
        if event.char in ("-",
                          "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r",
                          "s", "t", "u", "v", "w", "x", "y", "z",
                          " "):
            print
            event.char
        elif event.keysym not in ('BackSpace', 'Delete', 'Tab', 'Left', 'Right'):
            print
            event.keysym
            return 'break'
    """

    def getlist(self):
        self.listview.delete(0, tk.END)
        for item in getExternalRefs():
            self.listview.insert(tk.END, item)

    def Maker(self):
        flag=False
        if self.sourcetext.get() == "":
            tk.messagebox.showerror("Error", "Source name cannot be empty!", parent=self)
            return

        dict = {}
        dict.update({"source_name" : self.sourcetext.get()})
        if not (len(self.desctext.get())==0):
            dict.update({"description": self.desctext.get()})
            flag=True
        if not (len(self.urltext.get())==0):
            dict.update({"url": self.urltext.get()})
            flag=True
            if not (len(self.hashestext.get())==0):
                dict2 = {}
                dict2.update({self.hash_var.get() : self.hashestext.get()})
                dict.update({"hashes" : dict2})
        if not (len(self.ext_idtext.get())==0):
            dict.update({"external_id": self.ext_idtext.get()})
            flag=True

        if not (flag):
            tk.messagebox.showerror("Error", "At least one of the Description, URL, or External ID properties must be present.", parent=self)
            return
        try:
            exreftofile(self.sourcetext.get(), stix2.ExternalReference(**dict))
        except Exception as e:
            tk.messagebox.showerror("Error", str(e), parent=self)
            return
        self.getlist()
        tk.messagebox.showinfo("Success", "External Reference created successfully!", parent=self)



    def widgets(self):
        self.sourcelabel = tk.Label(self.frame, text="*Source Name:", font=("OpenSans", 12))
        self.sourcelabel.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.sourcetext = tk.Entry(self.frame, font=("OpenSans", 12))
        self.sourcetext.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        #self.killchaintext.bind('<KeyPress>', lambda event: self.keyPress(event))

        self.desclabel = tk.Label(self.frame, text="Description:", font=("OpenSans", 12))
        self.desclabel.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.desctext = tk.Entry(self.frame, font=("OpenSans", 12),  width=60)
        self.desctext.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)


        self.urllabel = tk.Label(self.frame, text="URL:", font=("OpenSans", 12))
        self.urllabel.grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        self.urltext = tk.Entry(self.frame, font=("OpenSans", 12), width=30)
        self.urltext.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)


        self.hasheslabel = tk.Label(self.frame, text="**Hashes:", font=("OpenSans", 12))
        self.hasheslabel.grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        self.hash_var = tk.StringVar()
        self.hash_var.set("          ")
        self.hashesoption = tk.OptionMenu(self.frame, self.hash_var, "MD5", "MD6", "RIPEMD-160", "SHA-1", "SHA-224", "SHA-256", "SHA-384", "SHA-512", "SHA3-224", "SHA3-256", "SHA3-384", "SHA3-512", "ssdeep", "WHIRLPOOL")
        self.hashesoption.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        self.hashestext = tk.Entry(self.frame, font=("OpenSans", 12), width=48)
        self.hashestext.grid(row=3, column=1, padx=5, pady=5, sticky=tk.E)

        self.ext_idlabel = tk.Label(self.frame, text="External ID:", font=("OpenSans", 12))
        self.ext_idlabel.grid(row=4, column=0, padx=5, pady=5, sticky=tk.E)
        self.ext_idtext = tk.Entry(self.frame, font=("OpenSans", 12), width=35)
        self.ext_idtext.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)

        self.hashesdesclaimer = tk.Label(self.frame, text="**Hashes will be omitted if URL is not present.", font=("OpenSans", 8))
        self.hashesdesclaimer.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W)





        self.label = tk.Label(self.btframe, font=("OpenSans", 8, "bold"),
                              text="Existing External References into workspace:", bg="black", fg="white")
        self.label.pack(fill=tk.X, padx=10)

        self.listview = tk.Listbox(self.btframe, font=("OpenSans", 10, "bold"), height=5)
        self.listview.pack(fill=tk.X, padx=10)

        self.getlist()

        self.addbutton = tk.Button(self.btframe, text="Create", font=("OpenSans", 12), fg="white", bg="#03AC13",
                                   command=lambda: [self.Maker()])

        self.addbutton.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)

        self.cancelbutton = tk.Button(self.btframe, text="Delete", font=("OpenSans", 12), fg="white", bg="#FF3B30",
                                      command=lambda: [(externalrefdelete(self.listview.get(tk.ACTIVE), self),
                                                        self.getlist()) if self.listview.get(
                                          tk.ACTIVE) != "" else print("")])
        self.cancelbutton.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)





class CreatedByRef():
    def __init__(self, goFrame, goRow):
        self.goFrame=goFrame
        self.goRow=goRow

    def pop(self, root, goFrame):
        self.top = tk.Toplevel(root)
        self.top.title("Identity Selection")
        self.top.grab_set()
        self.top.attributes("-topmost", "true")
        #self.geometry("1900x950")
        self.top.resizable(width=False, height=False)
        self.frame = tk.Frame(self.top)
        self.frame.pack(fill=tk.X,pady=5)
        self.goFrame=goFrame

        self.selected_value = ""


        self.widgets()

    def getlist(self):
        self.listview.delete(0, tk.END)
        for item in getIdentityRef():
            self.listview.insert(tk.END, item)

    def callback(self):
        try:
            self.created_by_refLabel2.destroy()
        except: pass
        self.selected_value=self.listview.get(self.listview.curselection()).split(": ")[1]
        self.created_by_refLabel2 = tk.Label(self.goFrame, font=("OpenSans", 10))
        self.created_by_refLabel2.grid(row=self.goRow, column=1, pady=5)
        self.created_by_refLabel2.configure(text=self.selected_value)

    def get(self):
        try:
            return self.selected_value
        except:
            try:
                return self.created_by_refLabel2.cget("text")
            except:
                return ""

    def set(self, item):
        self.created_by_refLabel2 = tk.Label(self.goFrame, font=("OpenSans", 10))
        self.created_by_refLabel2.grid(row=self.goRow, column=1, pady=5)
        self.created_by_refLabel2.configure(text=item)


    def widgets(self):

        self.createdbyrefdesclaimer = tk.Label(self.frame, text="Please select the Identity that describes the entity that created the current object you are constructing.", font=("OpenSans", 10))
        self.createdbyrefdesclaimer.pack()



        self.label = tk.Label(self.frame, font=("OpenSans", 8, "bold"),
                              text="Existing Identities into workspace: (Format <name> : <id>", bg="black", fg="white")
        self.label.pack(fill=tk.X, padx=10)

        self.listview = tk.Listbox(self.frame, font=("OpenSans", 10, "bold"))
        self.listview.pack(fill=tk.X, expand=True, padx=10)

        self.getlist()

        self.addbutton = tk.Button(self.frame, text="Select", font=("OpenSans", 12), fg="white", bg="#03AC13",
                                   command=lambda: [self.callback(), self.top.destroy()])

        self.addbutton.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)

        self.cancelbutton = tk.Button(self.frame, text="Cancel", font=("OpenSans", 12), fg="white", bg="#FF3B30",
                                      command=lambda: [self.top.destroy()])
        self.cancelbutton.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)



class SightingOfRef():
    def __init__(self, mandatoryFrame, eRow):
        self.mandatoryFrame=mandatoryFrame
        self.eRow=eRow

    def pop(self, mandatoryFrame):
        self.top = tk.Toplevel(mandatoryFrame)
        self.top.title("Object Selection")
        self.top.grab_set()
        self.top.attributes("-topmost", "true")
        #self.geometry("1900x950")
        self.top.resizable(width=False, height=False)
        self.frame = tk.Frame(self.top)
        self.frame.pack(fill=tk.X,pady=5)
        self.mandatoryFrame=mandatoryFrame

        self.selected_value = ""


        self.widgets()

    def getlist(self):
        self.listview.delete(0, tk.END)
        for item in getAllIDs():
            self.listview.insert(tk.END, item)

    def callback(self):
        try:
            self.sighting_of_refLabel2.destroy()
        except: pass
        self.selected_value=self.listview.get(self.listview.curselection()).split(": ")[1]
        self.sighting_of_refLabel2 = tk.Label(self.mandatoryFrame, font=("OpenSans", 10))
        self.sighting_of_refLabel2.grid(row=self.eRow, column=1, pady=5)
        self.sighting_of_refLabel2.configure(text=self.selected_value)

    def get(self):
        try:
            return self.selected_value
        except:
            return self.sighting_of_refLabel2.cget("text")

    def set(self, item):
        self.sighting_of_refLabel2 = tk.Label(self.mandatoryFrame, font=("OpenSans", 10))
        self.sighting_of_refLabel2.grid(row=self.eRow, column=1, pady=5)
        self.sighting_of_refLabel2.configure(text=item)


    def widgets(self):

        self.sightingofrefdesclaimer = tk.Label(self.frame, text="Please select the Identity that describes the entity that created the current object you are constructing.", font=("OpenSans", 10))
        self.sightingofrefdesclaimer.pack()



        self.label = tk.Label(self.frame, font=("OpenSans", 8, "bold"),
                              text="Existing Identities into workspace: (Format <name> : <id>", bg="black", fg="white")
        self.label.pack(fill=tk.X, padx=10)

        self.listview = tk.Listbox(self.frame, font=("OpenSans", 10, "bold"), height=30)
        self.listview.pack(fill=tk.X, expand=True, padx=10)

        self.getlist()

        self.addbutton = tk.Button(self.frame, text="Select", font=("OpenSans", 12), fg="white", bg="#03AC13",
                                   command=lambda: [self.callback(), self.top.destroy()])

        self.addbutton.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)

        self.cancelbutton = tk.Button(self.frame, text="Cancel", font=("OpenSans", 12), fg="white", bg="#FF3B30",
                                      command=lambda: [self.top.destroy()])
        self.cancelbutton.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)


class HoverManager():
    def __init__(self, object_class):
        self.object_class=object_class

    def show(self, event, widget):
        print(str(widget))
        try:
            self.object_class.configure(cursor="question_arrow")
        except:
            print("Cursor not compatible with OS!")
        if widget == "name":
            text="Name: A name used to identify the "+self.object_class.object
        elif widget == "labels":
            text="Labels: This property is an Open Vocabulary that specifies the type of "+self.object_class.object
        elif widget == "pattern":
            text="Pattern: The detection pattern for this Indicator is a STIX Pattern as specified in STIX Patterning Docs.\n Format Example: [ipv4:value='192.168.1.1'] "
        elif widget == "valid_from":
            text = "Valid From: The time from which this Indicator should be considered valuable intelligence."
        elif widget == "description":
            text = "A description that provides more details and context about the "+self.object_class.object+", potentially including its purpose and its key characteristics."
        elif widget == "kill_chain_phases":
            text = "The list of Kill Chain Phases for which this "+self.object_class.object+" is used."
        elif widget == "aliases":
            text = "Alternative names used to identify this "+self.object_class.object+"."
        elif widget == "first_seen":
            text = "The time that this "+self.object_class.object+" was first seen.\n Format example: 1/1/1995"
        elif widget == "last_seen":
            text = "The time that this "+self.object_class.object+" was last seen.\n Format example: 1/1/1995"
        elif widget == "objective":
            text = "This property defines the Campaign’s primary goal, objective, desired outcome, or intended effect — what the Threat Actor hopes to accomplish with this Campaign."
        elif widget == "sectors":
            text = "The list of industry sectors that this "+self.object_class.object+" belongs to."
        elif widget == "contact_information":
            text = "The contact information (e-mail, phone number, etc.) for this "+self.object_class.object+"."
        elif widget == "valid_from":
            text = "The time from which this "+self.object_class.object+" should be considered valuable intelligence."
        elif widget == "valid_until":
            text = "The time from which this "+self.object_class.object+" should no longer be considered valuable intelligence."
        elif widget == "goals":
            text = "The high level goals of this Intrusion Set, namely, what are they trying to do."
        elif widget == "resource_level":
            text = "This defines the organizational level at which this "+self.object_class.object+" typically works, which in turn determines the resources available to this "+self.object_class.object+" for use in an attack."
        elif widget == "primary_motivation":
            text = "The primary reason, motivation, or purpose behind this "+self.object_class.object+". The motivation is why the "+self.object_class.object+" wishes to achieve the goal (what they are trying to achieve)."
        elif widget == "secondary_motivations":
            text = "The secondary reasons, motivations, or purposes behind this "+self.object_class.object+". These motivations can exist as an equal or near-equal cause to the primary motivation. However, it does not replace or necessarily magnify the primary motivation, but it might indicate additional context."
        elif widget == "published":
            text = "The date that this Report object was officially published by the creator of this "+self.object_class.object+"."
        elif widget == "object_refs":
            text = "Specifies the STIX Objects that are referred to by this "+self.object_class.object+"."
        elif widget == "sophistication":
            text = "The skill, specific knowledge, special training, or expertise a "+self.object_class.object+" must have to perform the attack."
        elif widget == "personal_motivations":
            text = "The personal reasons, motivations, or purposes of the "+self.object_class.object+" regardless of organizational goals."
        elif widget == "roles":
            text = "A list of roles the "+self.object_class.object+" plays."

        # POPULATE HERE...

        else:
            text = "!!Missing "+widget+" info for this "+self.object_class.object

        self.object_class.infoLabel.configure(text=text)

