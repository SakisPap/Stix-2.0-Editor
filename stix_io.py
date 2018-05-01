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
import stix2
import tempfile
import os
import pathlib
import datetime, time
import shutil
import sys
import tkinter as tk
import tkinter.filedialog
from tkinter import messagebox
#from stix2elevator import elevate_string, elevate_file,
from stix2elevator import *
from stix2elevator.options import *



def itemtofile(item):
    if item.get("type") == "relationship" or item.get("type") == "observed-data" or item.get("type") == "marking-definition" or item.get("type")=="sighting":
        filename=item.get("type")+"/"+item.get("id")+".json"
    else:
        filename=item.get("type")+"/"+item.get("name")+".json"

    if not (os.path.isfile(filename)):
        file = open(filename, "w")
        file.write(str(item))
        file.close()
    else:
        if item.get("type")!="marking-definition" and item.get("type")!="sighting":
            ans = tk.messagebox.askyesno("Confirm Update?", item.get("type") + " " + item.get("name") +" was last modified at " +str(item.get("modified")) + "\n Would you like to update it?")
        else:
            ans = tk.messagebox.askyesno("Confirm Update?",item.get("id") + "Would you like to update it?")

        if ans ==  True:
            file = open(filename, "w")
            file.write(str(item))
            file.close()
            return "True"
        else:
            return "False"

def killchainphasetofile(filename, item):
    file=os.path.join(getkcpfolder(), filename+".kcp")
    file = open(file, "w")
    file.write(str(item))
    file.close()

def exreftofile(filename, item):
    file=os.path.join(getexreffolder(), filename+".ext")
    file = open(file, "w")
    file.write(str(item))
    file.close()

def killchainphasedelete(filename, parent):
    ans = tk.messagebox.askyesno("Confirm Delete?", "Are you sure that you want to delete the selected Kill Chain Phase?", parent=parent)
    if ans:
        os.remove(os.path.join(getkcpfolder(), filename+".kcp"))

def externalrefdelete(filename, parent):
    ans = tk.messagebox.askyesno("Confirm Delete?", "Are you sure that you want to delete the selected External Reference?", parent=parent)
    if ans:
        os.remove(os.path.join(getexreffolder(), filename+".ext"))

def getcfgfolder():
    return os.path.join(os.path.expanduser("~"), "STIX2Editor")

def getkcpfolder():
    return os.path.join(getcfgfolder(), "kill-chain-phases")

def getexreffolder():
    return os.path.join(getcfgfolder(), "external-references")

def getKillChainPhases():
    return [pathlib.Path(x).stem for x in os.listdir(getkcpfolder()) if x.endswith(".kcp")]

def getExternalRefs():
    return [pathlib.Path(x).stem for x in os.listdir(getexreffolder()) if x.endswith(".ext")]

def checkcfgfolder():
    cfgfolder=getcfgfolder()
    if not (os.path.exists(cfgfolder)):
        os.makedirs(cfgfolder)
    kcpfolder=getkcpfolder()
    exreffolder=getexreffolder()
    if not (os.path.exists(kcpfolder)):
        os.makedirs(kcpfolder)
    if not (os.path.exists(exreffolder)):
        os.makedirs(exreffolder)

def getcfgfile():
    return os.path.join(getcfgfolder(), "sav.dat")
def getcfgfile2():
    return os.path.join(getcfgfolder(), "theme.dat")
def getcfgfile3():
    return os.path.join(getcfgfolder(), "rez.dat")


def setlastproject(ppath):
    lastfile=os.path.join(getcfgfolder(),"last.cfg")
    file = open(lastfile, "w")
    file.write(ppath)
    file.close()

def getFolderArray():
    return ['attack-pattern', 'campaign', 'course-of-action', 'identity', 'indicator', 'intrusion-set', 'malware', 'observed-data', 'report', 'threat-actor', 'tool', 'vulnerability', 'relationship', 'marking-definition', 'sighting']

def isProjectActive():
    for folder in getFolderArray():
        if not (os.path.exists(folder)):
            return False
    return True


def getFilesJson(path, lm):#Xwris to extension plz   lm=0 -> alplhabetical
    if(lm==0):
        return [pathlib.Path(x).stem for x in os.listdir(path) if x.endswith(".json")] #Den paizoun symbolic links swsta? Alliws vale resolve kai meta stem
    else:
        temp = [pathlib.Path(x).stem for x in os.listdir(path) if x.endswith(".json")]
        temp.sort(key=lambda x: os.path.getmtime(path + "/" + str(x)+".json"), reverse=True) #Last modified descending!
        return temp


def getFilesJsonExt(path,sortby):#Me to extension
        temp = [x for x in os.listdir(path) if x.endswith(".json")]
        if (sortby=="alph"):
            return temp
        elif (sortby=="alphdesc"):
            return reversed(temp)
        elif (sortby=="lm"):
            temp.sort(key=lambda x: os.path.getmtime(path + "/" + str(x)))  # Last modified ascending!
            return temp
        elif (sortby=="lmdesc"):
            temp.sort(key=lambda x: os.path.getmtime(path + "/" + str(x)),reverse=True)  # Last modified ascending!
            return temp


def getAllIDs():
    ids=[]
    for folder in getFolderArray():
        for file in getFilesJsonExt(folder,"alph"):
            stix2obj=filetoitem(os.path.join(folder,file))
            if stix2obj.get("type") != "relationship" and stix2obj.get("type") != "marking-definition" and stix2obj.get("type") != "sighting":
                ids.append(stix2obj.get("name")+": "+stix2obj.get("id"))

    return ids

def getIdentityRef():
    identitylist=[]
    folder="identity"
    for file in getFilesJsonExt(folder, "alph"):
        identity=filetoitem(os.path.join(folder, file))
        identitylist.append(identity.get("name")+" : "+identity.get("id"))
    return identitylist

def getObjectIDs(type):
    idlist=[]
    for file in getFilesJsonExt(type, "alph"):
        stix2obj=filetoitem(os.path.join(type, file))
        idlist.append(stix2obj.get("id"))
    return idlist

def InitNewEnvironment(projectpath):
    if not (os.path.exists(projectpath)):
        os.makedirs(projectpath) # warning: full path or poitner to wpath -- RECURSIVE!
    os.chdir(projectpath)
    for folder in getFolderArray():#warning:must be empty! check lol
        if not (os.path.exists(folder)):
            os.mkdir(folder)

def NewProject():
    ppath = tk.filedialog.askdirectory(initialdir="/", title="Please select the folder of your new STIX2 project.")
    if ppath:
        InitNewEnvironment(ppath)
        tk.messagebox.showinfo("New Project", "Your new project has been created and set as active.")
        setlastproject(ppath)
        return True
    else:
        return False

def OpenProject():
    ppath = tk.filedialog.askdirectory(initialdir="/", title="Please select the folder of your STIX2 project.")
    if ppath:
        LoadEnvironment(ppath)
        setlastproject(ppath)
        return True
    else:
        return False

def LoadPrevious():
    prevfile=os.path.join(getcfgfolder(), "last.cfg")
    if (os.path.isfile(prevfile)):
        lastpath=readfile(prevfile)
        if(os.path.exists(lastpath)):
            LoadEnvironment(lastpath)
            return True
        else:
            tk.messagebox.showwarning("Error", "Previously opened project path seems removed. Load was unsuccessful.")
            return False
    else:
        tk.messagebox.showwarning("Error", "It appears no valid STIX2 Project has been opened yet.")
        return False


def OpenInExplorer():
    os.startfile(os.getcwd())


def ImportFile():
    fpath=tk.filedialog.askopenfilenames(initialdir = "/",title = "Please select a STIX2 file to import.",filetypes = (("json files (STIX2)","*.json"),("xml files (STIX1)","*.xml")))
    if fpath:
        files=list(fpath)
        imports=0
        for file in files:
            if (pathlib.Path(file).suffix==".json"):
                try:
                    stix2obj=stix2.parse(filetoitem(file))
                    type=stix2obj.get("type")
                    if not (type=="bundle"):
                        shutil.copy2(file,os.path.join(type,stix2obj.get("name")+".json"))
                        imports+=1
                    else:
                        tk.messagebox.showwarning("Error",file + " is a Bundle. Please use Bundle Management from Tools to import it.")
                except:
                    tk.messagebox.showwarning("Error",file + " does not seem to be a valid STIX2 object. Import failed.")
            else:
                try:
                    initialize_options()
                    stix1obj=elevate_file(file)
                    type = stix1obj.get("type")
                    if not (type == "bundle"):
                        itemtofile(stix1obj)
                        imports += 1
                    else:
                        tk.messagebox.showwarning("Error",
                                                  file + " is a Bundle. Please use Bundle Management from Tools to import it.")

                except:
                    tk.messagebox.showwarning("Error",file + " does not seem to be a valid STIX1 object or version missmatch. Import failed.")
        tk.messagebox.showinfo("Imports", "There have been "+str(imports)+" successful imports.")


def ExportProject():
    items=filestoarr2("alph")
    if not items:
        tk.messagebox.showwarning("Error", "Current project seems empty. There is nothing to export.")
        return
    bpath=tk.filedialog.asksaveasfilename(title="Export entire project into a STIX2 Bundle file.",defaultextension=".json", filetypes=[("json file","*.json")])
    if bpath:
        bundle=stix2.Bundle(items)
        file = open(bpath, "w")
        file.write(str(bundle))
        file.close()
        tk.messagebox.showinfo("Success", "Current project was exported into a STIX2 Bundle file.")



def LoadEnvironment(projectpath):
     os.chdir(projectpath)
     valid=1
     for folder in getFolderArray():
         if not os.path.exists(folder):
            valid=0
     if(valid==0):
        choice=tk.messagebox.showwarning("Warning", "One or more required folders within the selected project directory were not found. Please check if " + projectpath +" is a valid STIX2 project directory. Should the Editor attempt to repair the selected path?", type="yesno")
        if(choice=="yes"):
            InitNewEnvironment(projectpath)
        else:
            tk.messagebox.showerror("Open Project", "Project did not load successfully. Editor will now exit...")
            sys.exit(0)


def InitTempEnvironment():
    now=str(datetime.datetime.now().time())
    tmp=now.replace(":","").replace(".","")
    tmpdir=tempfile.gettempdir()+"stix2"+tmp
    os.makedirs(tmpdir)
    InitNewEnvironment(tmpdir)
    os.chdir(tmpdir)

def filetoitem(file):
    jsonfile = open(file, "r")
    item=stix2.parse(jsonfile)
    return item

def filestoarr():
     items = []
     for folder in getFolderArray():
        for file in getFilesJsonExt(folder):
            stix2obj=stix2.parse(filetoitem(folder + "/" + file))
            items.append(stix2obj.get("type") + "-> " + stix2obj.get("name"))
     return items


def filestoarr2(sortby):
    items = []
    for folder in getFolderArray():
        for file in getFilesJsonExt(folder,sortby):
            stix2obj = stix2.parse(filetoitem(folder + "/" + file))
            items.append(stix2obj)
    return items

def filestoarr2obj(object,sort):
    items = []
    for file in getFilesJsonExt(object, sort):
        stix2obj = stix2.parse(filetoitem(object + "/" + file))
        if stix2obj.get("type") == object:
            items.append(stix2obj)
    return items


#--New addition, check that Dre
def filestoarr2obj4edit(object, name):
    for file in getFilesJsonExt(object, sortby="alph"):
        stix2obj = stix2.parse(filetoitem(object + "/" + file))
        if stix2obj.get("type") == object and stix2obj.get("name")==name:
            return stix2obj


def filestobundle():     #prepei kai logika 8a exoume idi chdir()
    items=[]
    for folder in getFolderArray():
        for file in getFilesJsonExt(folder):
            items.append(stix2.parse(filetoitem(folder+"/"+file)))
    return stix2.Bundle(items), items



#---------------------DELETE OBJECT INFASTRUCTURE---------------
def delete(type,string):
    if ":" in string:
         temparr=string.split(": ")
         ans=tk.messagebox.askquestion("Confirm", "Are you sure that you want to delete "+ temparr[1]+" ?")
         if (ans=="yes"):
            os.remove(temparr[0]+"/"+temparr[1]+".json")
    else:#name only
        ans = tk.messagebox.askquestion("Confirm", "Are you sure that you want to delete " + string + " ?")
        if (ans == "yes"):
            os.remove(type + "/" + string + ".json")
#---------------------------------------------------------------


def currtimestamp(t):
     if(t=="D"):
         year = str(datetime.now().year)
         month = str(datetime.now().month)
         day = str(datetime.now().day)
         return(year + "/" + month + "/" + day)
     else:
         hour=str(datetime.now().hour)
         min=str(datetime.now().minute)
         return(hour+"/"+min)


def readfile(file):
     file = open(file, "r")
     return file.read()



def filetoitemfromlist(string):
    temparr = string.split(": ")
    return filetoitem(temparr[0] + "/" + temparr[1] + ".json")


def getkeys(stix2obj):
    keys = []
    for key in stix2obj.keys():
        keys.append(key)
    return keys

def filesto2obj(type,object):
    for file in getFilesJsonExt(type,"alph"):
        stix2obj = stix2.parse(filetoitem(type + "/" + file))
        if stix2obj.get("name") == object:
            return stix2obj

def filesto2objid(id):
    for folder in getFolderArray():
        for file in getFilesJsonExt(folder,"alph"):
            stix2obj = stix2.parse(filetoitem(folder+ "/" + file))
            if stix2obj.get("id") == id:
                return stix2obj
