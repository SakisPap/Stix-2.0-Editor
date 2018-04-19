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
import os
from PIL import Image, ImageTk
from stix_io import filestobundle
from stix_io import LoadEnvironment
import json
from pprint import pprint
#from stix_io import *
from tkinter import messagebox
from stix_io import *
import re
import stix2
import sys
import time
from makers import *
from tools import Multiselect



class Objects(tk.Frame):
    def __init__(self, parent, theme):
        tk.Frame.__init__(self, parent)

        if theme=="sea":
            self.COLOR_1= "#AED1D6"
            self.COLOR_2= "#7584AD"
            self.COLOR_3= "#314570"
        elif theme=="multi":
            self.COLOR_1 = "#B4D2BA"
            self.COLOR_2 = "#D2BF55"
            self.COLOR_3 = "#2A4747"
        elif theme=="semidark":
            self.COLOR_1 = "#F7EBE8"
            self.COLOR_2 = "#444140"
            self.COLOR_3 = "#1E1E24"
        elif theme=="dark":
            self.COLOR_1 = "#9999A1"
            self.COLOR_2 = "#66666E"
            self.COLOR_3 = "#000000"
        elif theme=="bordeu":
            self.COLOR_1 = "#A9927D"
            self.COLOR_2 = "#5E5037"
            self.COLOR_3 = "#49111C"
        elif theme=="green":
            self.COLOR_1 = "#C3D898"
            self.COLOR_2 = "#7A9B76"
            self.COLOR_3 = "#011936"
        #self.rowconfigure(1, weight=2)
        #self.rowconfigure(2, weight=2)
        #self.columnconfigure(0, weight=2)
        #self.columnconfigure(1, weight=1)

        self.object="nothing"

        self.radio_buttons = []


        self.gridHeader = tk.Frame(self, height=35, width=800, bg=self.COLOR_2)
        self.gridHeader.pack(fill=tk.BOTH, side=tk.TOP)
        self.gridHeader.pack_propagate(0)
        self.gridHeader.grid_propagate(0)

        # Paging header
        self.exit = tk.Button(self.gridHeader, text="⌫", font=("OpenSans", 12, "bold"), fg="white", bg="#FF3B30", highlightthickness=0, relief=tk.FLAT, command = lambda : [self.grab_release(), self.place_forget()])
        self.exit.pack(side=tk.RIGHT, fill=tk.Y)
        self.topLabel = tk.Label(self.gridHeader, fg="white", bg=self.COLOR_2, text="Please choose an Object to begin interraction", font=("OpenSans", 16, "bold"))
        self.topLabel.pack()

#-------------------------------------------------------
        self.masterBody = tk.Frame(self)
        self.masterBody.pack()
        self.gridBody = tk.Frame(self.masterBody, height=380, width=400, bg=self.COLOR_3)
        self.gridBody.pack(side=tk.LEFT)
        self.gridBody.pack_propagate(0)
        self.gridBody.grid_propagate(0)

        self.listBody = tk.Frame(self.masterBody, height=380,width=400, bg=self.COLOR_1)
        self.listBody.pack(side=tk.LEFT)
        self.listBody.pack_propagate(0)
        self.listBody.grid_propagate(0)
#-------------------------------------------------------

        self.infoBody = tk.Frame(self, height=65, width=800, bg=self.COLOR_2)
        self.infoBody.pack(fill=tk.X, side=tk.BOTTOM)
        self.infoBody.pack_propagate(0)
        self.infoBody.grid_propagate(0)

        self.infoLabel = tk.Label(self.infoBody, fg="white", bg=self.COLOR_2, text="This is the info tab, click on an Object to learn more", font=("OpenSans", 12, "bold"), wraplength=800)
        self.infoLabel.pack()


        """
        self.gridBody.columnconfigure(0,weight=3)
        self.gridBody.columnconfigure(1, weight=3)
        self.gridBody.columnconfigure(2, weight=3)
        self.gridBody.columnconfigure(3, weight=3)

        self.gridBody.rowconfigure(0, weight=3)
        self.gridBody.rowconfigure(1, weight=3)
        self.gridBody.rowconfigure(2, weight=3)
        self.gridBody.rowconfigure(3, weight=3)
        
        """

        self.widgets()


        self.display_type=tk.BooleanVar()
        self.sortby = tk.StringVar()
        self.viewby = tk.StringVar()
        self.full_list= []
        self.editmode=False




    def widgets(self):
        self.img = Image.open(os.path.abspath("images/attack_pattern.png"))
        self.attack_pattern_img = ImageTk.PhotoImage(self.img)

        self.img = Image.open(os.path.abspath("images/campaign.png"))
        self.campaign_img = ImageTk.PhotoImage(self.img)

        self.img = Image.open(os.path.abspath("images/course_of_action.png"))
        self.course_of_action_img = ImageTk.PhotoImage(self.img)

        self.img = Image.open(os.path.abspath("images/identity.png"))
        self.identity_img = ImageTk.PhotoImage(self.img)

        self.img = Image.open(os.path.abspath("images/indicator.png"))
        self.indicator_img = ImageTk.PhotoImage(self.img)

        self.img = Image.open(os.path.abspath("images/intrusion_set.png"))
        self.intrusion_set_img = ImageTk.PhotoImage(self.img)

        self.img = Image.open(os.path.abspath("images/malware.png"))
        self.malware_img = ImageTk.PhotoImage(self.img)

        self.img = Image.open(os.path.abspath("images/observed_data.png"))
        self.observed_data_img = ImageTk.PhotoImage(self.img)

        self.img = Image.open(os.path.abspath("images/report.png"))
        self.report_img = ImageTk.PhotoImage(self.img)

        self.img = Image.open(os.path.abspath("images/threat_actor.png"))
        self.threat_actor_img = ImageTk.PhotoImage(self.img)

        self.img = Image.open(os.path.abspath("images/tool.png"))
        self.tool_img = ImageTk.PhotoImage(self.img)

        self.img = Image.open(os.path.abspath("images/vulnerability.png"))
        self.vulnerability_img = ImageTk.PhotoImage(self.img)

        self.img = Image.open(os.path.abspath("images/relationship.png"))
        self.relationship_img = ImageTk.PhotoImage(self.img)

        self.img = Image.open(os.path.abspath("images/displayall.png"))
        self.displayall_img = ImageTk.PhotoImage(self.img)


        # Objects Buttons

        PADX = 10
        PADY = 5

        # Row=0
        self.attack_patternButton = tk.Button(self.gridBody, image=self.attack_pattern_img, bg=self.COLOR_3, activebackground=self.COLOR_3, relief=tk.FLAT, height=77, width=77, highlightthickness=0, highlightbackground=self.COLOR_3, command=lambda: self.selector("attack-pattern"))
        self.attack_patternButton.grid(row=0, column=0, padx=PADX, pady=PADY, sticky="nsew")

        self.campaignButton = tk.Button(self.gridBody, image=self.campaign_img, bg=self.COLOR_3, activebackground=self.COLOR_3, relief=tk.FLAT, height=77, width=77, highlightthickness=0, highlightbackground=self.COLOR_3, command=lambda: [self.selector("campaign")])
        self.campaignButton.grid(row=0, column=1, padx=PADX, pady=PADY, sticky="nsew")

        self.course_of_actionButton = tk.Button(self.gridBody, image=self.course_of_action_img, bg=self.COLOR_3, activebackground=self.COLOR_3, relief=tk.FLAT, height=77, width=77, highlightthickness=0, highlightbackground=self.COLOR_3, command=lambda: self.selector("course-of-action"))
        self.course_of_actionButton.grid(row=0, column=2, padx=PADX, pady=PADY, sticky="nsew")

        self.identityButton = tk.Button(self.gridBody, image=self.identity_img, bg=self.COLOR_3, activebackground=self.COLOR_3, relief=tk.FLAT, height=77, width=77, highlightthickness=0, highlightbackground=self.COLOR_3, command=lambda: self.selector("identity"))
        self.identityButton.grid(row=0, column=3, padx=PADX, pady=PADY, sticky="nsew")


        # Row=1
        self.indicatorButton = tk.Button(self.gridBody, image=self.indicator_img, bg=self.COLOR_3, activebackground=self.COLOR_3, relief=tk.FLAT, height=77, width=77, highlightthickness=0, highlightbackground=self.COLOR_3, command=lambda: self.selector("indicator"))
        self.indicatorButton.grid(row=1, column=0, padx=PADX, pady=PADY, sticky="nsew")

        self.intrusion_setButton = tk.Button(self.gridBody, image=self.intrusion_set_img, bg=self.COLOR_3, activebackground=self.COLOR_3, relief=tk.FLAT, height=77, width=77, highlightthickness=0, highlightbackground=self.COLOR_3, command=lambda: self.selector("intrusion-set"))
        self.intrusion_setButton.grid(row=1, column=1, padx=PADX, pady=PADY, sticky="nsew")

        self.malwareButton = tk.Button(self.gridBody, image=self.malware_img, bg=self.COLOR_3, activebackground=self.COLOR_3, relief=tk.FLAT, height=77, width=77, highlightthickness=0, highlightbackground=self.COLOR_3, command=lambda: self.selector("malware"))
        self.malwareButton.grid(row=1, column=2, padx=PADX, pady=PADY, sticky="nsew")

        self.observed_dataButton = tk.Button(self.gridBody, image=self.observed_data_img, bg=self.COLOR_3, activebackground=self.COLOR_3, relief=tk.FLAT, height=77, width=77, highlightthickness=0, highlightbackground=self.COLOR_3, command=lambda: self.selector("observed-data"))
        self.observed_dataButton.grid(row=1, column=3, padx=PADX, pady=PADY, sticky="nsew")


        # Row=2
        self.reportButton = tk.Button(self.gridBody, image=self.report_img, bg=self.COLOR_3, activebackground=self.COLOR_3, relief=tk.FLAT, height=77, width=77, highlightthickness=0, highlightbackground=self.COLOR_3, command=lambda: self.selector("report"))
        self.reportButton.grid(row=2, column=0, padx=PADX, pady=PADY, sticky="nsew")

        self.threat_actorButton = tk.Button(self.gridBody, image=self.threat_actor_img, bg=self.COLOR_3, activebackground=self.COLOR_3, relief=tk.FLAT, height=77, width=77, highlightthickness=0, highlightbackground=self.COLOR_3, command=lambda: self.selector("threat-actor"))
        self.threat_actorButton.grid(row=2, column=1, padx=PADX, pady=PADY, sticky="nsew")

        self.toolButton = tk.Button(self.gridBody, image=self.tool_img, bg=self.COLOR_3, activebackground=self.COLOR_3, relief=tk.FLAT, height=77, width=77, highlightthickness=0, highlightbackground=self.COLOR_3, command=lambda: self.selector("tool"))
        self.toolButton.grid(row=2, column=2, padx=PADX, pady=PADY, sticky="nsew")

        self.vulnerabilityButton = tk.Button(self.gridBody, image=self.vulnerability_img, bg=self.COLOR_3, activebackground=self.COLOR_3, relief=tk.FLAT, height=77, width=77, highlightthickness=0, highlightbackground=self.COLOR_3, command=lambda: self.selector("vulnerability"))
        self.vulnerabilityButton.grid(row=2, column=3, padx=PADX, pady=PADY, sticky="nsew")


        #Row=3
        self.displayall_Button = tk.Button(self.gridBody, image=self.displayall_img, bg=self.COLOR_3, activebackground=self.COLOR_3, relief=tk.FLAT, height=77, width=77, highlightthickness=0, highlightbackground=self.COLOR_3, command=lambda: [self.selector("nothing"), self.enlistall(), print(self.object), self.add_button.configure(state=tk.DISABLED), self.edit_button.configure(state=tk.DISABLED)])
        self.displayall_Button.grid(row=3, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="nsew")

        self.relationship_Button = tk.Button(self.gridBody, image=self.relationship_img, bg=self.COLOR_3, activebackground=self.COLOR_3, relief=tk.FLAT, height=77, width=77, highlightthickness=0, highlightbackground=self.COLOR_3, command=lambda: self.selector("relationship"))
        self.relationship_Button.grid(row=3, column=2, columnspan=2, padx=PADX, pady=PADY, sticky="nsew")

        # --------------------List Body Widgets-----------------------------------------------------

        self.listLabel = tk.Label(self.listBody, text="Existing Objects in project", font=("OpenSans", 12, "bold"), fg=self.COLOR_3, relief=tk.SOLID, bd=0)
        self.listLabel.pack(fill=tk.X)

        self.listbox = tk.Listbox(self.listBody, exportselection=0, font=("OpenSans", 12, "bold"), bd=0, width=30, height=16, relief=tk.FLAT, highlightthickness=0, bg=self.COLOR_1, fg=self.COLOR_3)
        self.listbox.pack()
        self.listbox.bind('<Button-1>', lambda _: [self.edit_button.configure(state=tk.NORMAL) if self.object!="relationship" else print(""), self.delete_button.configure(state=tk.NORMAL)])
        #self.scrollbar = tk.Scrollbar(self.listBody, orient="vertical")
        #self.scrollbar.configure(command=self.listbox.yview)
        #self.scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        #self.listbox.configure(yscrollcommand=self.scrollbar.set)
        #self.scrollbar.lift()


        self.add_button = tk.Button(self.listBody, text="+Add New",font=("OpenSans", 12, "bold"), fg="white", bg="#03AC13", relief=tk.FLAT, highlightthickness=0, height=3, command=lambda : self.editor(self.masterBody, self.object, 0))
        self.add_button.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.add_button.configure(state=tk.DISABLED)
        self.edit_button = tk.Button(self.listBody, text="Edit",font=("OpenSans", 12, "bold"), fg="white", bg="#FF9500", relief=tk.FLAT, highlightthickness=0, height=3, command=lambda : self.editor(self.masterBody, self.object, 1))
        self.edit_button.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.edit_button.configure(state=tk.DISABLED)
        self.delete_button = tk.Button(self.listBody, text="Delete", font=("OpenSans", 12, "bold"), fg="white", bg="#FF3B30", relief=tk.FLAT, highlightthickness=0, height=3, command=lambda : [delete(self.object,self.listbox.get(self.listbox.curselection())), self.updatelist(self.object)if self.object != "nothing" else self.enlistall()])
        self.delete_button.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.delete_button.configure(state=tk.DISABLED)




#--------------LISTING FOR MAIN PAGE----------------------------------
    #---Enlist all objects in project, exclusively run when project is opened or show all is clicked
    def enlistall(self):
        self.listbox.delete(0, tk.END)
        self.full_list =[]
        for itemname in filestoarr2(self.sortby.get()):
            if itemname.get("type") != "relationship":
                self.full_list.append(itemname.get("type")+": "+itemname.get("name")+": "+itemname.get("id"))
            else:
                self.full_list.append(itemname.get("type") + ": "+itemname.get("id"))
        for itemname in self.full_list:
            itemname=itemname.split(": ")
            if (itemname[0] != "relationship" and self.viewby.get() == "name"):
                if self.display_type.get():
                    self.listbox.insert(tk.END, itemname[0] + ": " + itemname[1])
                else:
                    self.listbox.insert(tk.END, itemname[1])

            elif (itemname[0] != "relationship" and self.viewby.get() == "id"):
                self.listbox.insert(tk.END, itemname[2])
            else:
                self.listbox.insert(tk.END, itemname[1])




    def updatelist(self, object):
        self.listbox.delete(0, tk.END)
        self.full_list =[]
        for itemname in filestoarr2obj(object, self.sortby.get()):
            if itemname.get("type") != "relationship":
                self.full_list.append(itemname.get("type")+": "+itemname.get("name")+": "+itemname.get("id"))
            else:
                self.full_list.append(itemname.get("type") + ": "+itemname.get("id"))

        for itemname in self.full_list:
            itemname=itemname.split(": ")
            if (itemname[0] != "relationship" and self.viewby.get() == "name"):
                if self.display_type.get():
                    self.listbox.insert(tk.END, itemname[0] + ": " + itemname[1])
                else:
                    self.listbox.insert(tk.END, itemname[1])

            elif (itemname[0] != "relationship" and self.viewby.get() == "id"):
                self.listbox.insert(tk.END, itemname[2])
            else:
                self.listbox.insert(tk.END, itemname[1])

#--------------------------------------------------------------------


    def selector(self, object):
        self.add_button.configure(state=tk.NORMAL)
        self.object=object
        self.add_button.configure(command=lambda: self.editor(self.masterBody, self.object, 0))
        self.edit_button.configure(state=tk.DISABLED)
        self.delete_button.configure(state=tk.DISABLED)
        if object=="attack-pattern":
            self.infoLabel.configure(text="Attack Pattern: A type of Tactics, Techniques, and Procedures (TTP) that describes ways threat actors attempt to compromise targets.")
            self.topLabel.config(text="Selected Object: Attack Pattern")
            self.listLabel.config(text="Existing Attack Patterns in project")
        elif object=="campaign":
            self.infoLabel.configure(text="Campaign: A grouping of adversarial behaviors that describes a set of malicious activities or attacks that occur over a period of time against a specific set of targets.")
            self.topLabel.config(text="Selected Object: Campaign")
            self.listLabel.config(text="Existing Campaigns in project")
        elif object=="course-of-action":
            self.infoLabel.configure(text="Course of Action: An action taken to either prevent an attack or respond to an attack.")
            self.topLabel.config(text="Selected Object: Course of Action")
            self.listLabel.config(text="Existing Courses of Action in project")
        elif object=="identity":
            self.infoLabel.configure(text="Identity: Individuals, organizations, or groups, as well as classes of individuals, organizations, or groups.")
            self.topLabel.config(text="Selected Object: Identity")
            self.listLabel.config(text="Existing Identities in project")
        elif object=="indicator":
            self.infoLabel.configure(text="Indicator: Contains a pattern that can be used to detect suspicious or malicious cyber activity.")
            self.topLabel.config(text="Selected Object: Indicator")
            self.listLabel.config(text="Existing Indicators in project")
        elif object=="intrusion-set":
            self.infoLabel.configure(text="Intrusion Set: A grouped set of adversarial behaviors and resources with common properties believed to be orchestrated by a single threat actor.")
            self.topLabel.config(text="Selected Object: Intrusion Set")
            self.listLabel.config(text="Existing Intrusion Sets in project")
        elif object=="malware":
            self.infoLabel.configure(text="Malware: A type of TTP, also known as malicious code and malicious software, used to compromise the confidentiality, integrity, or availability of a victim’s data or system.")
            self.topLabel.config(text="Selected Object: Malware")
            self.listLabel.config(text="Existing Malwares in project")
        elif object=="observed-data":
            self.infoLabel.configure(text="Observed Data: Conveys information observed on a system or network (e.g., an IP address).")
            self.topLabel.config(text="Selected Object: Observed Data")
            self.listLabel.config(text="Existing Observed Data in project")
        elif object=="report":
            self.infoLabel.configure(text="Report: Collections of threat intelligence focused on one or more topics, such as a description of a threat actor, malware, or attack technique, including contextual details.")
            self.topLabel.config(text="Selected Object: Report")
            self.listLabel.config(text="Existing Reports in project")
        elif object=="threat-actor":
            self.infoLabel.configure(text="Threat Actor: Individuals, groups, or organizations believed to be operating with malicious intent.")
            self.topLabel.config(text="Selected Object: Threat Actor")
            self.listLabel.config(text="Existing Threat Actors in project")
        elif object=="tool":
            self.infoLabel.configure(text="Tool: Legitimate software that can be used by threat actors to perform attacks.")
            self.topLabel.config(text="Selected Object: Tool")
            self.listLabel.config(text="Existing Tools in project")
        elif object == "vulnerability":
            self.infoLabel.configure(text="Vulnerability: A mistake in software that can be directly used by a hacker to gain access to a system or network.")
            self.topLabel.config(text="Selected Object: Vulnerability")
            self.listLabel.config(text="Existing Vulnerabilities in project")
        elif object == "relationship":
            self.infoLabel.configure(text="Relationship: Used to link two SDOs and to describe how they are related to each other.")
            self.topLabel.config(text="Selected Object: Relationship")
            self.listLabel.config(text="Existing Relationships in project")
            self.add_button.configure(command=lambda : self.relationships(self.masterBody))
        else:
            self.infoLabel.configure(text="This is the info tab, click on an Object to learn more")
            self.listLabel.config(text="Existing Objects in project")
            self.topLabel.configure(text="Please choose an Object to begin interraction")

        #---Show in Main-list specific objects
        try:
            self.updatelist(object)
        except:
            self.enlistall()
            print("Error in update list: no " + str(self.object) + " folder")



    def hover(self, label):
        if label == "name":
            self.infoLabel.configure(text="Name: A name used to identify the "+self.object)
        elif label == "labels":
            self.infoLabel.configure(text="Labels: This property is an Open Vocabulary that specifies the type of "+self.object)
        elif label == "pattern":
            self.infoLabel.configure(text="Pattern: The detection pattern for this Indicator is a STIX Pattern as specified in STIX Patterning Docs.\n Format Example: [ipv4:value='192.168.1.1'] ")
        elif label == "valid_from":
            self.infoLabel.configure(text="Valid From: The time from which this Indicator should be considered valuable intelligence.")



#--------------------List Body Widgets-----------------------------------------------------



#----------THIS IS THE STARTING POINT OF THE EDITOR TAB----------------------------------


    def editor(self, parent, object, type_of_editor):
        self.editorFrame = tk.Frame(parent, width=800, height=380)
        self.editorFrame.place(x=0, y=0)
        self.editorFrame.grid_propagate(0)
        self.editorFrame.pack_propagate(0)
        self.editorFrame.grab_set()

        self.editorFrame.columnconfigure(0, weight=1)
        self.editorFrame.columnconfigure(1, weight=4)
        self.widget_list = []
        self.type_of_editor = type_of_editor



        #------------------MANDATORY EDITOR FRAME WIDGETS------------------------------
        eRow=0

        self.mandatoryFrame = tk.Frame(self.editorFrame)
        self.mandatoryFrame.pack(fill=tk.X)

        #---Name---
        if object != "observed-data":                                                   #Indicator's name can be optional according to docs but messes with the GUI understanding
            self.nameLabel = tk.Label(self.mandatoryFrame, text="*Name:", font=("OpenSans", 12))
            self.nameLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            self.nameEntry = tk.Entry(self.mandatoryFrame, font=("OpenSans", 12))
            self.nameEntry.grid(row=eRow, column=1, sticky=tk.W, pady=5)
            self.nameEntry.bind('<KeyPress>', self.keyPress)
            self.nameLabel.bind("<Enter>", lambda _: self.hover("name"))
            self.nameLabel.bind("<Leave>", lambda _: self.selector(self.object))


            self.widget_list.append([self.nameEntry, "name"])
            eRow+=1


        if object == "identity":
            self.identity_classLabel = tk.Label(self.mandatoryFrame, text="*Identity Class:", font=("OpenSans", 12))
            self.identity_classLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            self.identity_classVar = tk.StringVar()
            #---default---
            self.identity_classVar.set("")
            self.identity_classOption = tk.OptionMenu(self.mandatoryFrame, self.identity_classVar, "individual", "group", "organization", "class", "unknown")
            self.identity_classOption.grid(row=eRow, column=1, sticky=tk.W, pady=5)

            self.widget_list.append([self.identity_classVar, "identity_class"])
            eRow+=1

        if object == "indicator" or object == "malware" or object == "report" or object == "threat-actor" or object == "tool":
            self.labels_reqLabel = tk.Label(self.mandatoryFrame, text="*Label:", font=("OpenSans", 12))
            self.labels_reqLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            self.labels_reqLabel.bind("<Enter>", lambda _: self.hover("labels"))
            self.labels_reqLabel.bind("<Leave>", lambda _: self.selector(self.object))

            self.labels_reqEntry = tk.Entry(self.mandatoryFrame, font=("OpenSans", 12), width=50) #---Please also add vocab options (Toplevel with radiobuttons)
            self.labels_reqEntry.grid(row=eRow, column=1, sticky=tk.W, pady=5)
            self.labels_reqEntry.bind('<KeyPress>', self.keyPress)

            self.widget_list.append([self.labels_reqEntry, "labels"])
            eRow+=1

        if object == "indicator":
            self.patternLabel = tk.Label(self.mandatoryFrame, text="*Pattern:", font=("OpenSans", 12))
            self.patternLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            self.patternLabel.bind("<Enter>", lambda _: self.hover("pattern"))
            self.patternLabel.bind("<Leave>", lambda _: self.selector(self.object))
            self.patternEntry = tk.Entry(self.mandatoryFrame, font=("OpenSans", 12), width=50)
            self.patternEntry.grid(row=eRow, column=1, sticky=tk.W, pady=5)
            #self.patternEntry.bind('<KeyPress>', self.keyPress)

            self.widget_list.append([self.patternEntry, "pattern"])
            eRow+=1

            self.valid_fromVar = tk.StringVar()
            self.valid_fromLabel = tk.Label(self.mandatoryFrame, text="*Valid From:", font=("OpenSans", 12))
            self.valid_fromLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            self.valid_fromLabel.bind("<Enter>", lambda _: self.hover("valid_from"))
            self.valid_fromLabel.bind("<Leave>", lambda _: self.selector(self.object))

            self.valid_fromEntry = tk.Entry(self.mandatoryFrame, font=("OpenSans", 12), width=18, textvariable=self.valid_fromVar)
            self.valid_fromEntry.grid(row=eRow, column=1, sticky=tk.W, pady=5)
            self.valid_fromEntry.bind('<KeyPress>', lambda event, type="timestamp": self.keyPressDict(event, type))
            self.valid_fromVar.set(time.strftime("%d/%m/%Y %H:%M:%S"))
            """
            self.valid_fromDEntry = tk.Entry(self.mandatoryFrame, font=("OpenSans", 12), width=10, textvariable=self.valid_fromVar)
            self.valid_fromDEntry.grid(row=eRow, column=1, sticky=tk.W, pady=5)
            self.valid_fromDEntry.bind('<KeyPress>', lambda event, type = "date" : self.keyPressDict(event, type))
            self.valid_fromDEntry.insert(tk.END, time.strftime("%d/%m/%Y"))
            self.valid_fromTEntry = tk.Entry(self.mandatoryFrame, font=("OpenSans", 12), width=8, textvariable=self.valid_fromVar)
            self.valid_fromTEntry.grid(row=eRow, column=2, sticky=tk.W, pady=5)
            self.valid_fromTEntry.bind('<KeyPress>', lambda event, type = "time" : self.keyPressDict(event, type))
            self.valid_fromTEntry.insert(tk.END, time.strftime("%H:%M:%S"))
            """

            self.widget_list.append([self.valid_fromVar, "valid_from"])

            eRow+=1

        ###########OBJECT SPECIFIC OPTIONALS----------#############################################OBJECT SPECIFIC OPTIONALS----------##################################
        #description (featured in all excpt)
        if(object!="observed-data"):
            self.descriptionLabel = tk.Label(self.mandatoryFrame, text="Description:", font=("OpenSans", 12))
            self.descriptionLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            self.descriptionEntry = tk.Entry(self.mandatoryFrame, font=("OpenSans", 12), width=60)
            self.descriptionEntry.grid(row=eRow, column=1, sticky=tk.W, pady=5)
            self.widget_list.append([self.descriptionEntry,"description"])
            eRow+=1

        #kill chain phases
        if(object=="attack-pattern" or object=="indicator" or object=="malware" or object=="tool"):
            self.kill_chain_phasesLabel = tk.Label(self.mandatoryFrame, text="Kill Chain Phases:", font=("OpenSans", 12)) #Management!!
            self.kill_chain_phasesLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            self.kill_chain_phasesButton = tk.Button(self.mandatoryFrame, font = ("OpenSans", 12), text="Add...")
            self.kill_chain_phasesButton.grid(row=eRow, column=1, sticky=tk.W, pady=5)
            #ADD TOPLEVEL AND KILL CHAIN PHASE MANAGEMENT!!!!!
            eRow+=1

        #aliases - arr string
        if (object=="campaign" or object=="intrusion-set" or object=="threat-actor"):
            self.aliasesLabel = tk.Label(self.mandatoryFrame, text="Aliases:", font=("OpenSans", 12))
            self.aliasesLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            self.aliasesEntry = tk.Entry(self.mandatoryFrame, font=("OpenSans", 12))
            self.aliasesEntry.grid(row=eRow, column=1, sticky=tk.W, pady=5)
            self.widget_list.append([self.aliasesEntry, "aliases"])
            eRow+=1

        #first_seen ts
        if (object=="campaign" or object=="intrusion-set"):
            self.first_seenLabel = tk.Label(self.mandatoryFrame, text="First Seen:", font=("OpenSans", 12))
            self.first_seenLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            self.first_seenEntry = tk.Entry(self.mandatoryFrame, font=("OpenSans", 12))
            self.first_seenEntry.grid(row=eRow, column=1, sticky=tk.W, pady=5)
            self.widget_list.append([self.first_seenEntry, "first_seen"])
            eRow += 1

        # last_seen ts
        if (object == "campaign" or object == "intrusion-set"):
            self.last_seenLabel = tk.Label(self.mandatoryFrame, text="Last Seen:", font=("OpenSans", 12))
            self.last_seenLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            self.last_seenEntry = tk.Entry(self.mandatoryFrame, font=("OpenSans", 12))
            self.last_seenEntry.grid(row=eRow, column=1, sticky=tk.W, pady=5)
            self.widget_list.append([self.last_seenEntry, "last_seen"])
            eRow += 1

        # objective str
        if(object=="campaign"):
            self.objectiveLabel = tk.Label(self.mandatoryFrame, text="Objective:", font=("OpenSans", 12))
            self.objectiveLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            self.objectiveEntry = tk.Entry(self.mandatoryFrame, font=("OpenSans", 12))
            self.objectiveEntry.grid(row=eRow, column=1, sticky=tk.W, pady=5)
            self.widget_list.append([self.objectiveEntry, "objective"])
            eRow += 1


        if(object=="identity"):
            listitems = ["agriculture", "aerospace", "automotive", "communications", "construction", "defence", "education", "energy", "entertainment", "financial-services", "government-national", "government-regional", "government-local", "government-public-services", "healthcare", "hospitality-leisure", "infrastructure", "insurance", "manufacturing", "mining", "non-profit", "pharmaceuticals", "retail", "technology", "telecommunications", "transportation", "utilities"]
            self.multiselect = Multiselect(self.mandatoryFrame, listitems, eRow, self.COLOR_1, self.COLOR_2, self.COLOR_3)
            self.sectorsLabel = tk.Label(self.mandatoryFrame, text="Sectors:", font=("OpenSans", 12))
            self.sectorsLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            self.sectorsButton = tk.Button(self.mandatoryFrame, font = ("OpenSans", 12), text="...", command=lambda : [self.multiselect.place(x=225, y=5), self.mandatoryFrame.lift(), self.multiselect.lift(), self.multiselect.grab_set()])
            self.sectorsButton.grid(row=eRow, column=1, sticky=tk.W, pady=5)
            self.widget_list.append([self.multiselect, "sectors"])
            eRow += 1

            self.contant_informationLabel = tk.Label(self.mandatoryFrame, text="Contant Information:", font=("OpenSans", 12))
            self.contant_informationLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            self.contant_informationEntry = tk.Entry(self.mandatoryFrame, font=("OpenSans", 12))
            self.contant_informationEntry.grid(row=eRow, column=1, sticky=tk.W, pady=5)
            self.widget_list.append([self.contant_informationEntry, "contact_information"])
            eRow += 1

        if(object=="indicator"):
            self.valid_untilLabel = tk.Label(self.mandatoryFrame, text="Valid Until:", font=("OpenSans", 12))
            self.valid_untilLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            self.valid_untilEntry = tk.Entry(self.mandatoryFrame, font=("OpenSans", 12))
            self.valid_untilEntry.grid(row=eRow, column=1, sticky=tk.W, pady=5)
            self.widget_list.append([self.valid_untilEntry, "valid_until"])
            eRow += 1

        if(object=="intrusion-set" or object=="threat-actor"):
            #GOALS, array str
            self.goalsLabel = tk.Label(self.mandatoryFrame, text="Goals:", font=("OpenSans", 12))
            self.goalsLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            self.goalsEntry = tk.Entry(self.mandatoryFrame, font=("OpenSans", 12))
            self.goalsEntry.grid(row=eRow, column=1, sticky=tk.W, pady=5)
            self.widget_list.append([self.goalsEntry, "goals"])
            eRow += 1

            self.resource_levelLabel = tk.Label(self.mandatoryFrame, text="Resource Level:", font=("OpenSans", 12))
            self.resource_levelLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            self.resource_levelVar = tk.StringVar()
            self.resource_levelVar.set("")
            self.resource_levelOption = tk.OptionMenu(self.mandatoryFrame, self.resource_levelVar, "individual", "club", "contest", "team", "organization", "government")
            self.resource_levelOption.grid(row=eRow, column=1, sticky=tk.W, pady=5)
            self.widget_list.append([self.resource_levelVar, "resource_level"])
            eRow += 1

            self.primary_motivationLabel = tk.Label(self.mandatoryFrame, text="Primary Motivation:", font=("OpenSans", 12))
            self.primary_motivationLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            self.primary_motivationVar = tk.StringVar()
            self.primary_motivationVar.set("")
            self.primary_motivationOption = tk.OptionMenu(self.mandatoryFrame, self.primary_motivationVar, "accidental", "coercion", "dominance", "ideology", "notoriety", "organizational-gain", "personal-gain",
"personal-satisfaction", "revenge", "unpredictable")
            self.primary_motivationOption.grid(row=eRow, column=1, sticky=tk.W, pady=5)
            self.widget_list.append([self.primary_motivationVar, "primary_motivation"])

            #ADD SECONDARY MOTIVATIONS!

        if(object=="threat-actor"):
            #... add later
            print("")

        if(object=="tool"):
            self.tool_versionLabel = tk.Label(self.mandatoryFrame, text="Tool Version:", font=("OpenSans", 12))
            self.tool_versionLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            self.tool_versionEntry = tk.Entry(self.mandatoryFrame, font=("OpenSans", 12))
            self.tool_versionEntry.grid(row=eRow, column=1, sticky=tk.W, pady=5)
            self.widget_list.append([self.tool_versionEntry, "tool_version"])
            eRow += 1


        #OPEN EDITOR IN EDIT MODE
        if self.type_of_editor == 1:
            self.edit()



        #-----------------Autofill Tab-----------------------------------------------------
        self.afLabel = tk.Label(self.editorFrame, text="▶ Show Autofill Properties", font=("OpenSans", 10), bg=self.COLOR_1,
                              fg=self.COLOR_3)
        self.afLabel.pack(side=tk.TOP, anchor=tk.W, padx=3)
        self.afLabel.bind("<Button-1>", lambda _: afClick(self))

        self.afFrame = tk.Frame(self.editorFrame, bg=self.COLOR_1)

        self.afFlag = True

        def afClick(self):
            if self.afFlag == True:
                self.afLabel.configure(text="▼ Hide Autofill Properties")
                self.afFlag = not self.afFlag
                self.afFrame.pack(fill=tk.BOTH)
            else:
                self.afLabel.configure(text="▶ Show Autofill Properties")
                self.afFlag = not self.afFlag
                self.afFrame.pack_forget()


        #------------------AUTOFILL EDITOR FRAME WIDGETS--------------WARNING!!! Add disclaimer! Use at own risk--------------------------------
        self.idLabel=tk.Label(self.afFrame, text="ID:", font=("OpenSans", 12),bg=self.COLOR_1)
        self.idLabel.grid(row=0, column=0, sticky=tk.E, padx=5)
        self.idEntry = tk.Entry(self.afFrame, font=("OpenSans", 12), width=64)
        self.idEntry.grid(row=0, column=1, sticky=tk.W, pady=5)
        self.widget_list.append([self.idEntry, "id"])

        self.createdLabel = tk.Label(self.afFrame, text="Created:", font=("OpenSans", 12), bg=self.COLOR_1)
        self.createdLabel.grid(row=1, column=0, sticky=tk.E, padx=5)
        self.createdEntry = tk.Entry(self.afFrame, font=("OpenSans", 12))
        self.createdEntry.grid(row=1, column=1, sticky=tk.W, pady=5)

        self.modifiedLabel = tk.Label(self.afFrame, text="Modified:", font=("OpenSans", 12), bg=self.COLOR_1)
        self.modifiedLabel.grid(row=2, column=0, sticky=tk.E, padx=5)
        self.modifiedEntry = tk.Entry(self.afFrame, font=("OpenSans", 12))
        self.modifiedEntry.grid(row=2, column=1, sticky=tk.W, pady=5)


        #--------------------GLOBAL OPTIONALS-------------------------------------------------------------------------------------------------------------
        self.goLabel = tk.Label(self.editorFrame, text="▶ Show Global Optionals", font=("OpenSans", 10),
                                bg=self.COLOR_1,
                                fg=self.COLOR_3)
        self.goLabel.pack(side=tk.TOP, anchor=tk.W, padx=3)
        self.goLabel.bind("<Button-1>", lambda _: goClick(self))

        self.goFrame = tk.Frame(self.editorFrame, bg=self.COLOR_1)

        self.goFlag = True

        def goClick(self):
            if self.goFlag == True:
                self.goLabel.configure(text="▼ Hide Global Optionals")
                self.goFlag = not self.goFlag
                self.goFrame.pack(fill=tk.BOTH)
            else:
                self.goLabel.configure(text="▶ Show Global Optionals")
                self.goFlag = not self.goFlag
                self.goFrame.pack_forget()

        # ------------------Global optional frame widgets----------------------------------
        self.created_by_refLabel = tk.Label(self.goFrame, text="Created by Reference:", font=("OpenSans", 12), bg=self.COLOR_1)
        self.created_by_refLabel.grid(row=0, column=0, sticky=tk.E, padx=5)
        self.created_by_refButton = tk.Button(self.goFrame, font=("OpenSans", 12), text="Select Identity...")#Add toplevel and function!
        self.created_by_refButton.grid(row=0, column=1, sticky=tk.W, pady=5)

        self.revokedCheckButton=tk.Checkbutton(self.goFrame, text="Revoked?", font=("OpenSans", 12), bg=self.COLOR_1)#Add revoked management
        self.revokedCheckButton.grid(row=1,column=0,sticky=tk.E, padx=5)

        self.external_referencesLabel = tk.Label(self.goFrame, text="External References:", font=("OpenSans", 12), bg=self.COLOR_1)#Add external reference management
        self.external_referencesLabel.grid(row=2, column=0, sticky=tk.E, padx=5)
        self.external_referencesButton = tk.Button(self.goFrame, font=("OpenSans",12), text="Add...")
        self.external_referencesButton.grid(row=2, column=1, sticky=tk.W, pady=5)


        #add markings, object_marking_refs and granualr markings



        #-----Frame Buttons----------------------
        self.buttonHolder = tk.Frame(self.editorFrame)
        self.buttonHolder.pack(side=tk.BOTTOM)
        self.submitButton = tk.Button(self.buttonHolder, text="Submit", font=("OpenSans", 12, "bold"), fg="white", bg="#03AC13", relief=tk.FLAT, highlightthickness=0, command = lambda : [self.callback(), self.updatelist(self.object)])
        self.submitButton.pack(side=tk.LEFT)
        self.cancelButton = tk.Button(self.buttonHolder, text="Cancel", font=("OpenSans", 12, "bold"), fg="white", bg="#FF3B30", relief=tk.FLAT, highlightthickness=0, command=lambda: [self.editorFrame.destroy()])
        self.cancelButton.pack(side=tk.LEFT)


#-----------------------------------------------------EDIT---------------------------------------------------------------------


    def edit(self):
        name = self.full_list[self.listbox.curselection()[0]]
        name = name.split(": ")
        stix2object = filestoarr2obj4edit(name[0], name[1])
        keys = getkeys(stix2object)

        for item in self.widget_list:
            if item[1] in keys: #keys
                try:
                    item[0].insert(tk.END, stix2object[item[1]])
                except:
                    item[0].set(stix2object[item[1]])

        self.editmode=True
        self.oname=self.nameEntry.get()
#-----------------------------------------------------EDIT-END-----------------------------------------------------------------



    #This gets called upon frame submit---
    def callback(self):
        object = self.object


        dict = {}
        for item in self.widget_list:
            temp = item[0].get()
            if item[1] == "labels" or item[1] == "kill-chain-phase":
                temp = temp.split(" ")
            if temp != "":
                dict.update({item[1] : temp})

            elif (item[1] in ["name"]):
                tk.messagebox.showwarning("Error", "Entries marked with '*' cannot be left blank!", parent = self.editorFrame)
                return

        if not self.editmode:
            flag, debug = getattr(sys.modules[__name__], "%s_maker" % object.replace("-", "_"))(**dict)
            print(debug)
            if flag=="True":
                tk.messagebox.showinfo("Object Creation Successfull!", object + " " + self.nameEntry.get() + " created seccessfully!", parent = self.editorFrame)
                pass
            self.editorFrame.destroy()
        else:
            if (self.oname!=self.nameEntry.get()):
                ans=tk.messagebox.askyesno("Warning", "You have modified the name of the object. As a result, all data will be stored into another object and not into the current one. Would you like to revert the name back to default?")
                if(ans):
                    self.nameEntry.delete(0,tk.END)
                    self.nameEntry.insert(0, self.oname)
                else:
                    ans2=tk.messagebox.askyesno("Replication", "Would you like to create a new object with the current properties?")
                    if(ans2):
                        flag, debug = getattr(sys.modules[__name__], "%s_maker" % object.replace("-", "_"))(**dict)
                        print(debug)
                        tk.messagebox.showinfo("Object Replication Successfull!",
                                                   object + " " + self.nameEntry.get() + " was created seccessfully, while "+ self.oname + " was left intact.",
                                                   parent=self.editorFrame)
                        self.editmode=False
                        pass
                        self.editorFrame.destroy()
            else:
                flag, debug = getattr(sys.modules[__name__], "%s_maker" % object.replace("-", "_"))(**dict)
                print(debug)
                if flag == "True":
                    tk.messagebox.showinfo("Object Edit Successfull!",
                                           object + " " + self.nameEntry.get() + " was edited seccessfully!",
                                           parent=self.editorFrame)
                    self.editmode=False
                    pass
                self.editorFrame.destroy()



    #---------------RELATIONSHIPS TAB----------------------------------------------------------------

    def constructRelation(self, evt):

        self.rel_type_var.set("null")
        #self.listboxRight.delete(0, tk.END)
        self.relationshipEntry.configure(state=tk.NORMAL)

        for radio_button in self.radio_buttons:
            radio_button.configure(state=tk.DISABLED)
        #self.ok_button.configure(state=tk.NORMAL)

        object = self.listboxLeft.get(self.listboxLeft.curselection())
        #print("Left selected No: "+ str(self.listboxLeft.curselection()[0]))
        object = object.split(":")
        object = object[0]
        #print(object)


        if object == "attack-pattern":
            btn_list = ["targets", "uses"]
            semi_list = ["vulnerability", "identity", "malware", "tool"]
        elif object == "campaign":
            btn_list = ["attributed-to", "targets", "uses"]
            semi_list = ["intrusion-set", "threat-actor", "vulnerability", "identity", "attack-pattern", "malware", "tool"]
        elif object == "course-of-action":
            btn_list = ["mitigates"]
            semi_list = ["vulnerability", "attack-pattern", "malware", "tool"]
        elif object == "indicator":
            btn_list = ["indicates"]
            semi_list = ["intrusion-set", "threat-actor", "attack-pattern", "malware", "tool", "campaign"]
        elif object == "intrusion-set":
            btn_list = ["attributed-to", "targets", "uses"]
            semi_list = ["threat-actor", "vulnerability", "identity", "attack-pattern", "malware", "tool"]
        elif object == "malware":
            btn_list = ["targets", "uses", "variant-of"]
            semi_list = ["identity", "malware", "tool"]
        elif object == "threat-actor":
            btn_list = ["attributed-to", "impersonates", "targets", "uses"]
            semi_list = ["vulnerability", "identity", "attack-pattern", "malware", "tool"]
        elif object == "tool":
            btn_list = ["targets"]
            semi_list = ["identity", "vulnerability"]
        else:
            btn_list = []
            semi_list = []
            print("out of value index")

        #---- enbale corresponding radio buttons
        for radio_button in self.radio_buttons:
            for item in btn_list:
                if radio_button.cget("value") == item:
                    radio_button.configure(state=tk.NORMAL)

        #---- add the semi-list to the right list
        self.listboxRight.delete(0, tk.END)
        for item in semi_list:
            for itemname in filestoarr2obj(item,"alph"):
                self.listboxRight.insert(tk.END, itemname.get("type")+": "+itemname.get("name"))


            #self.listboxRight.insert(tk.END, str(item))


    def completeRelation(self):
        relation = self.rel_type_var.get()
        object = self.listboxLeft.get(self.listboxLeft.curselection())
        #print("Right selected No: " + str(self.listboxLeft.curselection()[0]))
        object = object.split(":")
        object = object[0]

        self.listboxRight.delete(0, tk.END)
        self.ok_button.configure(state=tk.DISABLED)

        #---initialize for custom
        complete_list = ["attack-pattern", "campaign", "course-of-action", "indicator", "intrusion-set", "malware",
                         "threat-actor", "tool"]

        if object == "attack-pattern":
            if relation == "targets":
                complete_list = ["vulnerability", "identity"]
            elif relation == "uses":
                complete_list = ["malware", "tool"]

        elif object == "campaign":
            if relation == "attributed-to":
                complete_list = ["intrusion-set", "threat-actor"]
            elif relation == "targets":
                complete_list = ["vulnerability", "identity"]
            elif relation == "uses":
                complete_list = ["attack-pattern", "malware", "tool"]

        elif object == "course-of-action":
            if relation == "mitigates":
                complete_list = ["attack-pattern", "malware", "tool", "vulnerability"]

        elif object == "indicator":
            if relation == "indicates":
                complete_list = ["attack-pattern", "campaign", "intrusion-set", "malware", "threat-actor", "tool"]

        elif object == "intrusion-set":
            if relation == "attributed-to":
                complete_list = ["threat-actor", "identity"]
            elif relation == "targets":
                complete_list = ["identity", "vulnerability"]
            elif relation == "uses":
                complete_list = ["attack-pattern", "malware", "tool"]

        elif object == "malware":
            if relation == "targets":
                complete_list = ["identity"]
            elif relation == "uses":
                complete_list = ["tool"]
            elif relation == "variant-of":
                complete_list = ["malware"]

        elif object == "threat-actor":
            if relation == "attributed-to":
                complete_list = ["identity"]
            elif relation == "impersonates":
                complete_list = ["identity"]
            elif relation == "targets":
                complete_list = ["identyty", "vulnerability"]
            elif relation == "uses":
                complete_list = ["attack-pattern", "malware", "tool"]

        elif object == "tool":
            if relation == "targets":
                complete_list = ["identity", "vulnerability"]

        else:
            print("out of value index")

        # ---- add the semi-list to the right list
        self.listboxRight.delete(0, tk.END)
        for item in complete_list:
            for itemname in filestoarr2obj(item,"alph"):
                self.listboxRight.insert(tk.END, itemname.get("type") + ": " + itemname.get("name"))


    #---This is the final function, relationship gets created here
    def createRelationship(self):
        if self.rel_type_var.get() != "custom":
            #print("LEFT " + self.listboxLeft.get(self.listboxLeft.curselection()))
            #print("RELATIONSHIP " + self.rel_type_var.get())
            #print("RIGHT " + self.listboxRight.get(self.listboxLeft.curselection()))
            tk.messagebox.showinfo(parent=self.relationshipsFrame, title="Success!",
                                   message="Relationship: \n" + self.listboxLeft.get(
                                       self.listboxLeft.curselection()) + " ➜ " + self.rel_type_var.get() + " ➜ " + self.listboxRight.get(
                                       self.listboxRight.curselection()) + "\ncreated successfully!")

            #---Call the Rel Maker with proper args
            debug = relationship_maker(filetoitemfromlist(self.listboxLeft.get(self.listboxLeft.curselection())), self.rel_type_var.get(), filetoitemfromlist(self.listboxRight.get(self.listboxRight.curselection())))
            print(debug)

        elif self.rel_type_var.get() == "custom" and self.relationshipEntry.get() != "User custom":
            #print("LEFT " + self.listboxLeft.get(self.listboxLeft.curselection()))
            #print("RELATIONSHIP " + self.relationshipEntry.get())
            #print("RIGHT " + self.listboxRight.get(self.listboxLeft.curselection()))
            tk.messagebox.showinfo(parent=self.relationshipsFrame, title="Success!",
                                   message="Relationship: \n" + self.listboxLeft.get(
                                       self.listboxLeft.curselection()) + " ➜ " + self.relationshipEntry.get() + " ➜ " + self.listboxRight.get(
                                       self.listboxRight.curselection()) + "\ncreated successfully!")

            #---Call the Rel Maker with proper args (user custom value)
            debug = relationship_maker(filetoitemfromlist(self.listboxLeft.get(self.listboxLeft.curselection())), self.relationshipEntry.get(), filetoitemfromlist(self.listboxRight.get(self.listboxRight.curselection())))
            print(debug)
        else:
            tk.messagebox.showwarning(parent=self.relationshipsFrame, title="Warning!", message="Please insert a custom value!")


    #---Dictionary check function on the Relationship Entry Box
    def keyPress(self, event):
        if event.char in ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
                          "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
                          "-", " "):
            print
            event.char
        elif event.keysym not in ('BackSpace', 'Delete', 'Tab', 'Left', 'Right'):
            print
            event.keysym
            return 'break'

    #---Dictionary check fo date and time------
    def keyPressDict(self, event, type):
        if type == "timestamp":
            chars = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "/", ":", " ")
        elif type == "something else":
            chars = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ":")
        if event.char in chars:
            print
            event.char
        elif event.keysym not in ('BackSpace', 'Delete', 'Tab', 'Left', 'Right'):
            print
            event.keysym
            return 'break'

    #---Relationship main routine----
    def relationships(self, parent):
        PADX = 20
        PADY = 10


        #----List All in Left List-------

        self.rel_type_var = tk.StringVar()
        self.entryFlag = False

        self.infoLabel.configure(
            text="Relationship: Used to link two SDOs and to describe how they are related to each other.")
        self.topLabel.config(text="Select an Object from the left list to relate it")

        self.relationshipsFrame = tk.Frame(parent, width=800, height=380, bg="#97ADA9")
        self.relationshipsFrame.place(x=0, y=0)
        self.relationshipsFrame.grid_propagate(0)
        self.relationshipsFrame.pack_propagate(0)
        self.relationshipsFrame.grab_set()

        self.radioFrame = tk.Frame(self.relationshipsFrame, bg="#97ADA9")

        self.listboxLeft = tk.Listbox(self.relationshipsFrame, exportselection=0, font=("OpenSans", 10, "bold"), bd=0, width=30, height=23, relief=tk.FLAT, highlightthickness=0, bg=self.COLOR_1, fg=self.COLOR_3)
        self.listboxLeft.pack(side=tk.LEFT, padx=PADX)
        self.listboxLeft.bind('<<ListboxSelect>>', self.constructRelation)

        # ----List All in Left List-------
        # -----------LISTING FOR RELATIONSHIP TAB-----------------------------

        for itemname in filestoarr2("alph"):
            if itemname.get("type")!= "relationship":
                self.listboxLeft.insert(tk.END, itemname.get("type")+": "+itemname.get("name"))
            #stix2obj.get("type") + "-> " + stix2obj.get("name")

        # --------------------------------------------------------------------

        MODES = [
            ("Targets", "targets"),
            ("Uses", "uses"),
            ("Atributed to", "attributed-to"),
            ("Mitigates", "mitigates"),
            ("Indicates", "indicates"),
            ("Impersonates", "impersonates"),
            ("Variant of", "variant-of"),
        ]


        for text, mode in MODES:
            self.relationshipRadio = tk.Radiobutton(self.radioFrame, command=lambda : self.completeRelation(), text=text, variable=self.rel_type_var, value=mode, indicator=0, font=("OpenSans", 12, "bold"), fg="white", width=15, bg="#A37F6F", relief=tk.FLAT, highlightthickness=0, height=1, pady=5, selectcolor="#E09873")
            self.relationshipRadio.pack(pady=3)
            self.radio_buttons.append(self.relationshipRadio)

        self.relationshipEntry = tk.Entry(self.radioFrame, width=15, font=("OpenSans", 12, "bold"), highlightthickness=2, highlightcolor="#E09873")
        self.relationshipEntry.pack(pady=3)
        self.relationshipEntry.insert(tk.END, "User custom")
        self.relationshipEntry.bind("<1>", lambda _ : [self.rel_type_var.set("custom"), self.completeRelation()])
        self.relationshipEntry.bind('<KeyPress>', self.keyPress)

        #disable radio button by default
        for radio_button in self.radio_buttons:
            radio_button.configure(state=tk.DISABLED)
        self.relationshipEntry.configure(stat=tk.DISABLED)


        self.radioFrame.pack(side=tk.LEFT)

        self.listboxRight = tk.Listbox(self.relationshipsFrame, exportselection=0, font=("OpenSans", 10, "bold"), bd=0, width=30, height=23, relief=tk.FLAT, highlightthickness=0, bg=self.COLOR_1, fg=self.COLOR_3, highlightcolor="red")
        self.listboxRight.pack(side=tk.LEFT, padx=PADX)
        self.listboxRight.bind('<<ListboxSelect>>', lambda _:  self.ok_button.configure(state=tk.NORMAL) if self.rel_type_var.get() != "null" else self.ok_button.configure(state=tk.DISABLED))



        self.ok_button = tk.Button(self.radioFrame, text="Relate", font=("OpenSans", 12, "bold"), fg="white", width=5,
                                    bg="#03AC13", relief=tk.FLAT, highlightthickness=0, height=1,
                                    command=lambda: [self.relationshipsFrame.place_forget(), self.relationshipsFrame.grab_release(), self.selector(self.object), self.createRelationship()])
        self.ok_button.pack(side=tk.LEFT, pady=20, padx=5)

        self.cancel_button = tk.Button(self.radioFrame, text="Abort", font=("OpenSans", 12, "bold"), fg="white",
                                       width=5, bg="#FF3B30", relief=tk.FLAT, highlightthickness=0, height=1,
                                       command=lambda: [self.relationshipsFrame.place_forget(), self.relationshipsFrame.grab_release(), self.selector(self.object)])
        self.cancel_button.pack(side=tk.LEFT, pady=20, padx=5)

        self.ok_button.configure(state=tk.DISABLED)


        """
        #----debug--------

        objects = ["attack-pattern", "campaign", "course-of-action", "indicator", "intrusion-set", "malware", "threat-actor", "tool"]

        for item in objects:
            #self.listboxLeft.insert(tk.END, "LEFT "+ str(item))

            self.listboxLeft.insert(tk.END, str(item))
        #----debug end----
        """






















