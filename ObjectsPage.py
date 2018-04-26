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
from RelationshipPage import Relationship
from EditorPage import Editor



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




        self.gridHeader = tk.Frame(self, bg=self.COLOR_2, height=35)
        self.gridHeader.pack(fill=tk.X, side=tk.TOP)
        self.gridHeader.pack_propagate(0)
        self.gridHeader.grid_propagate(0)

        # Paging header
        self.exit = tk.Button(self.gridHeader, text="⌫", font=("OpenSans", 12, "bold"), fg="white", bg="#FF3B30", highlightthickness=0, relief=tk.FLAT, command = lambda : [self.grab_release(), self.place_forget()])
        self.exit.pack(side=tk.RIGHT, fill=tk.Y)
        self.topLabel = tk.Label(self.gridHeader, fg="white", bg=self.COLOR_2, text="Please choose an Object to begin interraction", font=("OpenSans", 17, "bold"))
        self.topLabel.pack(fill=tk.BOTH, expand=True)

#-------------------------------------------------------
        self.masterBody = tk.Frame(self)
        self.masterBody.pack(fill=tk.BOTH, expand=True)
        self.gridBody = tk.Frame(self.masterBody, bg=self.COLOR_3)
        self.gridBody.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.gridBody.pack_propagate(0)
        self.gridBody.grid_propagate(0)

        self.listBody = tk.Frame(self.masterBody, bg=self.COLOR_1)
        self.listBody.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.listBody.pack_propagate(0)
        self.listBody.grid_propagate(0)
#-------------------------------------------------------

        self.infoBody = tk.Frame(self, bg=self.COLOR_2, height=60)
        self.infoBody.pack(fill=tk.X, side=tk.BOTTOM)
        self.infoBody.pack_propagate(0)
        self.infoBody.grid_propagate(0)

        self.infoLabel = tk.Label(self.infoBody, fg="white", bg=self.COLOR_2, text="This is the info tab, click on an Object to learn more", font=("OpenSans", 12, "bold"), wraplength=800)
        self.infoLabel.pack(fill=tk.BOTH, expand=True)


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
        self.displayall_Button.grid(row=3, column=0, padx=PADX, pady=PADY, sticky="nsew")

        self.marking_defsButton = tk.Button(self.gridBody, image=self.relationship_img, bg=self.COLOR_3, activebackground=self.COLOR_3, relief=tk.FLAT, height=77, width=77, highlightthickness=0, highlightbackground=self.COLOR_3, command=lambda: self.selector("marking-definition"))
        self.marking_defsButton.grid(row=3, column=1, padx=PADX, pady=PADY, sticky="nsew")

        self.relationship_Button = tk.Button(self.gridBody, image=self.relationship_img, bg=self.COLOR_3, activebackground=self.COLOR_3, relief=tk.FLAT, height=77, width=77, highlightthickness=0, highlightbackground=self.COLOR_3, command=lambda: self.selector("relationship"))
        self.relationship_Button.grid(row=3, column=2, padx=PADX, pady=PADY, sticky="nsew")


        for i in range(4):
            self.gridBody.columnconfigure(i, weight=1)
            self.gridBody.rowconfigure(i, weight=1)


        # --------------------List Body Widgets-----------------------------------------------------

        self.listLabel = tk.Label(self.listBody, text="Existing Objects in project", font=("OpenSans", 12, "bold"), fg=self.COLOR_3, relief=tk.SOLID, bd=0)
        self.listLabel.pack(fill=tk.X)

        self.listbox = tk.Listbox(self.listBody, exportselection=0, font=("OpenSans", 12, "bold"), bd=0, width=50, relief=tk.FLAT, highlightthickness=0, bg=self.COLOR_1, fg=self.COLOR_3)
        self.listbox.pack(fill=tk.Y, expand=True, padx=10, pady=5)
        self.listbox.bind('<Button-1>', lambda _: [self.edit_button.configure(state=tk.NORMAL) if self.object!="relationship" else print(""), self.delete_button.configure(state=tk.NORMAL)])
        #self.scrollbar = tk.Scrollbar(self.listBody, orient="vertical")
        #self.scrollbar.configure(command=self.listbox.yview)
        #self.scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        #self.listbox.configure(yscrollcommand=self.scrollbar.set)
        #self.scrollbar.lift()

        self.listbody_bottomFrame = tk.Frame(self.listBody)
        self.listbody_bottomFrame.pack(side=tk.BOTTOM, fill=tk.X)
        self.add_button = tk.Button(self.listbody_bottomFrame, text="+Add New",font=("OpenSans", 12, "bold"), fg="white", bg="#03AC13", relief=tk.FLAT, highlightthickness=0, command=lambda : self.start_Editor(0))
        self.add_button.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.add_button.configure(state=tk.DISABLED)
        self.edit_button = tk.Button(self.listbody_bottomFrame, text="Edit",font=("OpenSans", 12, "bold"), fg="white", bg="#FF9500", relief=tk.FLAT, highlightthickness=0, command=lambda : [self.start_Editor(1)])
        self.edit_button.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.edit_button.configure(state=tk.DISABLED)
        self.delete_button = tk.Button(self.listbody_bottomFrame, text="Delete", font=("OpenSans", 12, "bold"), fg="white", bg="#FF3B30", relief=tk.FLAT, highlightthickness=0, command=lambda : [delete(self.full_list[self.listbox.curselection()[0]].split(": ")[0], self.full_list[self.listbox.curselection()[0]].split(": ")[1]), self.updatelist(self.object)if self.object != "nothing" else self.enlistall()])
        self.delete_button.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.delete_button.configure(state=tk.DISABLED)


    def start_Relationship(self):
        relationship = Relationship(self, self.masterBody)
        relationship.pack(fill=tk.BOTH, expand=True)

    def start_Editor(self, type_of_editor):
        try:
            if self.object == "nothing" and type_of_editor == 1:
                # set object for when in display all
                self.object = self.full_list[self.listbox.curselection()[0]].split(": ")[0]
                editor = Editor(self, self.masterBody, self.full_list[self.listbox.curselection()[0]].split(": ")[0],
                                type_of_editor)
            else:
                editor = Editor(self, self.masterBody, self.object, type_of_editor)
            editor.pack(fill=tk.BOTH, expand=True)
        except:
            self.packer(0)
            tk.messagebox.showwarning("Warning",
                                      "Relationship Objects are not editable, however feel free to recreate them!")



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
        self.add_button.configure(command=lambda: self.start_Editor(0))
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
        elif object == "marking-definition":
            self.infoLabel.configure(text="Marking Definition: The marking-definition object represents a specific marking. Data markings typically represent handling or sharing requirements for data.")
            self.topLabel.config(text="Selected Object: Marking Definition")
            self.listLabel.config(text="Existing Marking Definitions in project")
        elif object == "relationship":
            self.infoLabel.configure(text="Relationship: Used to link two SDOs and to describe how they are related to each other.")
            self.topLabel.config(text="Selected Object: Relationship")
            self.listLabel.config(text="Existing Relationships in project")
            self.add_button.configure(command=lambda : self.start_Relationship())
        else:
            self.infoLabel.configure(text="This is the info tab, click on an Object to learn more")
            self.listLabel.config(text="Existing Objects in project")
            self.topLabel.configure(text="Please choose an Object to begin interraction")
            self.object="nothing"

        #---Show in Main-list specific objects
        try:
            self.updatelist(object)
        except:
            self.enlistall()
            print("Error in update list: no " + str(self.object) + " folder")


#--------------------List Body Widgets-----------------------------------------------------



#----------THIS IS THE STARTING POINT OF THE EDITOR TAB----------------------------------
    def packer(self, flag):
        if flag:
            self.listBody.pack_forget()
            self.gridBody.pack_forget()
        else:
            self.gridBody.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.listBody.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)































