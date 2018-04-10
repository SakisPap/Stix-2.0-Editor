import tkinter as tk
import tkinter.filedialog
from tkinter import messagebox
from stix2elevator import *
from stix2elevator.options import *
import stix2
from stix_io import filetoitem,itemtofile

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


def BundleImport():
    #check if we are into a project
    bundle=tk.filedialog.askopenfilename(initialdir="/", title="Please select a STIX2 Bundle file to import.",
                                          filetypes=[("json files (STIX2)", "*.json")])
    try:
        stix2bundle = stix2.parse(filetoitem(bundle))
        type = stix2bundle.get("type")
        if not (type=="bundle"):
            tk.messagebox.showwarning("Error", "Selected STIX2 object is not a Bundle.")
            return
        else:
            for o in stix2bundle.get("objects"):
                itemtofile(o)
            tk.messagebox.showinfo("Success", "Selected Bundle was successfully imported into current project.")
    except:
        tk.messagebox.showwarning("Error", "This does not seem to be a valid STIX2 object. Import failed.")
