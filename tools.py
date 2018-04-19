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
from stix_io import isProjectActive,killchainphasetofile


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
    def __init__(self, parent, list_items, eRow, COLOR_1, COLOR_2, COLOR_3):
        tk.Frame.__init__(self, parent, bg=COLOR_2, bd=3)
        self.parent=parent
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
        self.showlabel.config(text=str(self.selected_items).replace("'", "").replace("[", "").replace("]", ""))
        self.showlabel.grid(row=self.eRow, column=1)
        self.grab_release()

    def widgets(self):
        self.showlabel = tk.Label(self.parent, font=("OpenSans", 10), bg=self.COLOR_1, wraplength=500)
        self.listview = tk.Listbox(self, exportselection=0, font=("OpenSans", 10, "bold"), bd=1, height=9,
                              relief=tk.FLAT, highlightthickness=0, fg=self.COLOR_3, selectmode='multiple')
        self.listview.pack()

        self.donebutton = tk.Button(self, text="Done", command=lambda: self.done_callback())
        self.donebutton.pack(side=tk.LEFT, fill=tk.X, expand=1)
        self.clearbutton = tk.Button(self, text="Clear", command=lambda: self.listview.selection_clear(0, tk.END))
        self.clearbutton.pack(side=tk.RIGHT, fill=tk.X, expand=1)

    def get(self):
        if self.selected_items:
            return self.selected_items
        else:
            return ""

    def set(self, list):
        i = 0
        self.selected_items=list
        self.showlabel.config(text=str(self.selected_items).replace("'", "").replace("[", "").replace("]", ""))
        self.showlabel.grid(row=self.eRow, column=1)
        for item in self.list_items:
            if item in list:
                self.listview.select_set(i)
            i+=1


class KillChainPhaseMaker(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.title("Add a Kill Chain Phase...")
        self.frame = tk.Frame(self)
        self.frame.pack()
        self.__make_layout()
        self.mainloop()

    def __make_layout(self):
        self.frame.killchainlabel = tk.Label(text="Kill Chain Name:")
        self.frame.killchaintext = tk.Entry()
        self.frame.killchainlabel.grid(row=0, column=0)
        self.frame.killchaintext.grid(row=0, column=1)
        self.frame.phaselabel = tk.Label(text="Phase Name:")
        self.frame.phasetext = tk.Entry()
        self.frame.phaselabel.grid(row=1, column=0)
        self.frame.phasetext.grid(row=1, column=1)
        self.frame.addbutton = tk.Button(text="Create", command=lambda : [killchainphasetofile(self.frame.killchaintext.get()+"-"+self.frame.phasetext.get(), stix2.KillChainPhase(kill_chain_name=self.frame.killchaintext.get(), phase_name=self.frame.phasetext.get()))])
        self.frame.addbutton.grid(row=2, column=0, columnspan=2)
        messagebox.showinfo("vale kati...")


KillChainPhaseMaker()


