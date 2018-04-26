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
from tools import Multiselect, CreatedByRef, HoverManager



class Editor(tk.Frame):
    def __init__(self, object_class, parent, object,  type_of_editor):
        tk.Frame.__init__(self, parent)
        object_class.packer(1)
        self.infoLabel = object_class.infoLabel
        self.topLabel = object_class.topLabel
        self.COLOR_1 = object_class.COLOR_1
        self.COLOR_2 = object_class.COLOR_2
        self.COLOR_3 = object_class.COLOR_3
        self.full_list = object_class.full_list
        self.listbox = object_class.listbox
        self.editmode = object_class.editmode

        self.grid_propagate(0)
        self.pack_propagate(0)
        self.object = object

        object_class.packer(1)


        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=4)
        self.widget_list = []
        self.type_of_editor = type_of_editor
        self.current_page = 1

        self.widgets(object_class)




        #------------------MANDATORY EDITOR FRAME WIDGETS------------------------------
    def widgets(self, object_class):
        eRow=0

        object=object_class.object
        self.mandatoryFrame = tk.Frame(self)
        self.mandatoryFrame.pack(fill=tk.X)



        #---Name---
        if object != "observed-data":                                                   #Indicator's name can be optional according to docs but messes with the GUI understanding
            self.nameLabel = tk.Label(self.mandatoryFrame, text="*Name:", font=("OpenSans", 12))
            self.nameLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            self.nameEntry = tk.Entry(self.mandatoryFrame, font=("OpenSans", 12))
            self.nameEntry.grid(row=eRow, column=1, sticky=tk.W, pady=5)
            self.nameEntry.bind('<KeyPress>', self.keyPress)
            self.nameLabel.bind("<Enter>", lambda _: self.hover("name"))
            self.nameLabel.bind("<Leave>", lambda _: object_class.selector(self.object))
            self.widget_list.append([self.nameEntry, "name"])
            eRow+=1

        if object ==  "observed-data":
            self.first_observedLabel = tk.Label(self.mandatoryFrame, text="*First Observed:", font=("OpenSans", 12))
            self.first_observedLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            self.first_observedEntry = tk.Entry(self.mandatoryFrame, font=("OpenSans", 12))
            self.first_observedEntry.grid(row=eRow, column=1, sticky=tk.W, pady=5)
            self.widget_list.append([self.first_observedEntry, "first_observed"])
            eRow += 1

            self.last_observedLabel = tk.Label(self.mandatoryFrame, text="*Last Observed:", font=("OpenSans", 12))
            self.last_observedLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            self.last_observedEntry = tk.Entry(self.mandatoryFrame, font=("OpenSans", 12))
            self.last_observedEntry.grid(row=eRow, column=1, sticky=tk.W, pady=5)
            self.widget_list.append([self.last_observedEntry, "last_observed"])
            eRow += 1

            self.number_observedLabel = tk.Label(self.mandatoryFrame, text="*Number Observed:", font=("OpenSans", 12))
            self.number_observedLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            self.number_observedEntry = tk.Entry(self.mandatoryFrame, font=("OpenSans", 12))
            self.number_observedEntry.grid(row=eRow, column=1, sticky=tk.W, pady=5)
            self.widget_list.append([self.number_observedEntry, "number_observed"])
            eRow += 1

            self.objectsLabel = tk.Label(self.mandatoryFrame, text="*Objects:", font=("OpenSans", 12))
            self.objectsLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            self.objectsButton = tk.Button(self.mandatoryFrame, text="Add...", font=("OpenSans", 12))
            self.objectsButton.grid(row=eRow, column=1, sticky=tk.W, pady=5)
            self.widget_list.append([self.number_observedEntry, "number_observed"])
            eRow += 1



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
            self.labels_reqLabel = tk.Label(self.mandatoryFrame, text="*Labels:", font=("OpenSans", 12))
            self.labels_reqLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            self.labels_reqLabel.bind("<Enter>", lambda _: self.hover("labels"))
            self.labels_reqLabel.bind("<Leave>", lambda _: object_class.selector(self.object))

            self.labels_reqEntry = tk.Entry(self.mandatoryFrame, font=("OpenSans", 12), width=50) #---Please also add vocab options (Toplevel with radiobuttons)
            self.labels_reqEntry.grid(row=eRow, column=1, sticky=tk.W, pady=5)
            self.labels_reqEntry.bind('<KeyPress>', self.keyPress)

            self.widget_list.append([self.labels_reqEntry, "labels"])
            eRow+=1

        if object == "indicator":
            self.patternLabel = tk.Label(self.mandatoryFrame, text="*Pattern:", font=("OpenSans", 12))
            self.patternLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            self.patternLabel.bind("<Enter>", lambda _: self.hover("pattern"))
            self.patternLabel.bind("<Leave>", lambda _: object_class.selector(self.object))
            self.patternEntry = tk.Entry(self.mandatoryFrame, font=("OpenSans", 12), width=50)
            self.patternEntry.grid(row=eRow, column=1, sticky=tk.W, pady=5)
            #self.patternEntry.bind('<KeyPress>', self.keyPress)

            self.widget_list.append([self.patternEntry, "pattern"])
            eRow+=1

            self.valid_fromVar = tk.StringVar()
            self.valid_fromLabel = tk.Label(self.mandatoryFrame, text="*Valid From:", font=("OpenSans", 12))
            self.valid_fromLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            self.valid_fromLabel.bind("<Enter>", lambda _: self.hover("valid_from"))
            self.valid_fromLabel.bind("<Leave>", lambda _: object_class.selector(self.object))

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

        if(object=="report"):
            self.publishedLabel = tk.Label(self.mandatoryFrame, text="*Published:", font=("OpenSans", 12))
            self.publishedLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            self.publishedEntry = tk.Entry(self.mandatoryFrame, font=("OpenSans", 12))
            self.publishedEntry.grid(row=eRow, column=1, sticky=tk.W, pady=5)
            self.widget_list.append([self.publishedEntry, "published"])
            eRow+=1

            self.object_refsLabel = tk.Label(self.mandatoryFrame, text="*Object Referred:", font=("OpenSans", 12))
            self.object_refsLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            listitems = getAllIDs()
            self.multiselect_object_refs = Multiselect(self, self.mandatoryFrame, listitems, eRow, self.COLOR_1, self.COLOR_2, self.COLOR_3)
            #WARNING!! FIX MULTISELECT LOCATION
            self.object_refsButton = tk.Button(self.mandatoryFrame, font=("OpenSans", 12), text="...",
                                           command=lambda: [self.multiselect_object_refs.place(x=225, y=5),
                                                            self.mandatoryFrame.lift(), self.multiselect_object_refs.lift(),
                                                            self.multiselect_object_refs.grab_set()])
            self.object_refsButton.grid(row=eRow, column=1, sticky=tk.W, pady=5)
            self.widget_list.append([self.multiselect_object_refs, "object_refs"])
            eRow += 1


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
            listitems=getKillChainPhases()
            self.multiselect_kill_chain_phases= Multiselect(self, self.mandatoryFrame, listitems, eRow, self.COLOR_1, self.COLOR_2, self.COLOR_3, flag="killchain")
            self.kill_chain_phasesButton = tk.Button(self.mandatoryFrame, font = ("OpenSans", 12), text="Add...", command=lambda: [self.multiselect_kill_chain_phases.place(x=230, y=50),
                                                            self.multiselect_kill_chain_phases.lift(),
                                                            self.multiselect_kill_chain_phases.grab_set()])
            self.kill_chain_phasesButton.grid(row=eRow, column=1, sticky=tk.W, pady=5)
            self.widget_list.append([self.multiselect_kill_chain_phases, "kill_chain_phases"])
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
            self.multiselect_sectors = Multiselect(self, self.mandatoryFrame, listitems, eRow, self.COLOR_1, self.COLOR_2, self.COLOR_3)
            self.sectorsLabel = tk.Label(self.mandatoryFrame, text="Sectors:", font=("OpenSans", 12))
            self.sectorsLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            self.sectorsButton = tk.Button(self.mandatoryFrame, font = ("OpenSans", 12), text="...", command=lambda : [self.multiselect_sectors.place(x=230, y=50), self.multiselect_sectors.grab_set(), self.multiselect_sectors.lift()])
            self.sectorsButton.grid(row=eRow, column=1, sticky=tk.W, pady=5)
            self.widget_list.append([self.multiselect_sectors, "sectors"])
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
            eRow +=1

            self.secondary_motivationsLabel = tk.Label(self.mandatoryFrame, text="Secondary Motivations:", font=("OpenSans", 12))
            self.secondary_motivationsLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            listitems=["accidental", "coercion", "dominance", "ideology", "notoriety", "organizational-gain", "personal-gain",
"personal-satisfaction", "revenge", "unpredictable"]
            self.multiselect_secondary_motivations = Multiselect(self, self.mandatoryFrame, listitems, eRow, self.COLOR_1, self.COLOR_2, self.COLOR_3)
            self.secondary_motivationsButton = tk.Button(self.mandatoryFrame, font=("OpenSans", 12), text="...",
                                           command=lambda: [self.multiselect_secondary_motivations.place(x=225, y=5),
                                                            self.mandatoryFrame.lift(), self.multiselect_secondary_motivations.lift(),
                                                            self.multiselect_secondary_motivations.grab_set()])
            self.secondary_motivationsButton.grid(row=eRow, column=1, sticky=tk.W, pady=5)

            self.widget_list.append([self.multiselect_secondary_motivations, "secondary_motivations"])
            eRow += 1


        if(object=="threat-actor"):
            self.personal_motivationsLabel = tk.Label(self.mandatoryFrame, text="Personal Motivations:",
                                                       font=("OpenSans", 12))
            self.personal_motivationsLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            listitems = ["accidental", "coercion", "dominance", "ideology", "notoriety", "organizational-gain",
                         "personal-gain",
                         "personal-satisfaction", "revenge", "unpredictable"]
            self.multiselect_personal_motivations = Multiselect(self, self.mandatoryFrame, listitems, eRow, self.COLOR_1,
                                                                 self.COLOR_2, self.COLOR_3)
            self.personal_motivationsButton = tk.Button(self.mandatoryFrame, font=("OpenSans", 12), text="...",
                                                         command=lambda: [
                                                             self.multiselect_personal_motivations.place(x=225, y=5),
                                                             self.mandatoryFrame.lift(),
                                                             self.multiselect_personal_motivations.lift(),
                                                             self.multiselect_personal_motivations.grab_set()])
            self.personal_motivationsButton.grid(row=eRow, column=1, sticky=tk.W, pady=5)

            self.widget_list.append([self.multiselect_personal_motivations, "personal_motivations"])
            eRow += 1


            self.rolesLabel = tk.Label(self.mandatoryFrame, text="Roles:", font=("OpenSans", 12))
            self.rolesLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            listitems = ["agent", "director", "independent", "infrastructure-architect", "infrastructure-operator", "malware-author", "sponsor"]
            self.multiselect_roles = Multiselect(self, self.mandatoryFrame, listitems, eRow, self.COLOR_1, self.COLOR_2, self.COLOR_3)
            self.rolesButton = tk.Button(self.mandatoryFrame, font=("OpenSans", 12), text="...",
                                                         command=lambda: [
                                                             self.multiselect_roles.place(x=225, y=5),
                                                             self.mandatoryFrame.lift(),
                                                             self.multiselect_roles.lift(),
                                                             self.multiselect_roles.grab_set()])
            self.rolesButton.grid(row=eRow, column=1, sticky=tk.W, pady=5)

            self.widget_list.append([self.multiselect_roles, "roles"])
            eRow+=1

            self.sophisticationLabel = tk.Label(self.mandatoryFrame, text="Sophistication:", font=("OpenSans", 12))
            self.sophisticationLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            self.sophisticationVar = tk.StringVar()
            self.sophisticationVar.set("")
            self.sophisticationOption = tk.OptionMenu(self.mandatoryFrame, self.sophisticationVar, "none", "minimal", "intermediate", "advanced", "expert", "innovator", "strategic")
            self.sophisticationOption.grid(row=eRow, column=1, sticky=tk.W, pady=5)
            self.widget_list.append([self.sophisticationVar, "sophistication"])
            eRow += 1




        if(object=="tool"):
            self.tool_versionLabel = tk.Label(self.mandatoryFrame, text="Tool Version:", font=("OpenSans", 12))
            self.tool_versionLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            self.tool_versionEntry = tk.Entry(self.mandatoryFrame, font=("OpenSans", 12))
            self.tool_versionEntry.grid(row=eRow, column=1, sticky=tk.W, pady=5)
            self.widget_list.append([self.tool_versionEntry, "tool_version"])
            eRow += 1




#-----------------------------------------------------Autofill Tab-----------------------------------------------------

        self.afFrame = tk.Frame(self, bg=self.COLOR_1)
        self.afFrame.columnconfigure(1, weight=3)

        afRow=0
        #------------------AUTOFILL EDITOR FRAME WIDGETS--------------

        self.afLabel = tk.Label(self.afFrame, text="Parameters in this page are auto generated by stix and is best to be left as is.", font=("OpenSans", 10, "italic"), bg=self.COLOR_1,
                                fg=self.COLOR_3)
        self.afLabel.grid(row=afRow, column=0, columnspan=2, pady=10)

        afRow+=1

        self.idLabel=tk.Label(self.afFrame, text="ID:", font=("OpenSans", 12),bg=self.COLOR_1)
        self.idLabel.grid(row=afRow, column=0, sticky=tk.E, padx=5)
        self.idEntry = tk.Entry(self.afFrame, font=("OpenSans", 12), width=64)
        self.idEntry.grid(row=afRow, column=1, sticky=tk.W, pady=5)
        self.widget_list.append([self.idEntry, "id"])

        afRow+=1

        self.createdLabel = tk.Label(self.afFrame, text="Created:", font=("OpenSans", 12), bg=self.COLOR_1)
        self.createdLabel.grid(row=afRow, column=0, sticky=tk.E, padx=5)
        self.createdEntry = tk.Entry(self.afFrame, font=("OpenSans", 12))
        self.createdEntry.grid(row=afRow, column=1, sticky=tk.W, pady=5)
        self.widget_list.append([self.createdEntry, "created"])

        afRow+=1

        self.modifiedLabel = tk.Label(self.afFrame, text="Modified:", font=("OpenSans", 12), bg=self.COLOR_1)
        self.modifiedLabel.grid(row=afRow, column=0, sticky=tk.E, padx=5)
        self.modifiedEntry = tk.Entry(self.afFrame, font=("OpenSans", 12))
        self.modifiedEntry.grid(row=afRow, column=1, sticky=tk.W, pady=5)
        self.widget_list.append([self.modifiedEntry, "modified"])







#--------------------GLOBAL OPTIONALS-------------------------------------------------------------------------------------------------------------

        self.goFrame = tk.Frame(self, bg=self.COLOR_1)
        self.goFrame.columnconfigure(1, weight=3)


        goRow=0

        # ------------------Global optional frame widgets----------------------------------
        self.goLabel = tk.Label(self.goFrame, text="Parameters in this page are found globally in all SDO's.", font=("OpenSans", 10, "italic"),
                                bg=self.COLOR_1,
                                fg=self.COLOR_3)
        self.goLabel.grid(row=goRow, column=0, columnspan=2, pady=10)

        goRow += 1

        self.created_by_refLabel = tk.Label(self.goFrame, text="Created by Reference:", font=("OpenSans", 12), bg=self.COLOR_1)
        self.created_by_refLabel.grid(row=goRow, column=0, sticky=tk.E, padx=5)

        self.createdbyref = CreatedByRef(self.goFrame, goRow)
        self.created_by_refButton = tk.Button(self.goFrame, font=("OpenSans", 12), text="Select Identity...", command= lambda : [self.createdbyref.pop(self.mandatoryFrame, self.goFrame)])
        self.created_by_refButton.grid(row=goRow, column=1, sticky=tk.W, pady=5)
        self.widget_list.append([self.createdbyref, "created_by_ref"])

        goRow+=1

        self.revokedCheckButton=tk.Checkbutton(self.goFrame, text="Revoked?", font=("OpenSans", 12), bg=self.COLOR_1)#Add revoked management
        self.revokedCheckButton.grid(row=goRow,column=0,sticky=tk.E, padx=5)

        goRow+=1

        self.external_referencesLabel = tk.Label(self.goFrame, text="External References:", font=("OpenSans", 12), bg=self.COLOR_1)
        self.external_referencesLabel.grid(row=goRow, column=0, sticky=tk.E, padx=5)
        listitems=getExternalRefs()
        self.multiselect_external_references= Multiselect(self, self.goFrame, listitems, goRow, self.COLOR_1, self.COLOR_2, self.COLOR_3, flag="exref")
        self.external_referencesButton = tk.Button(self.goFrame, font = ("OpenSans", 12), text="Add...", command=lambda: [self.multiselect_external_references.place(x=230, y=50),
                                                        self.multiselect_external_references.lift(),
                                                        self.multiselect_external_references.grab_set()])
        self.external_referencesButton.grid(row=goRow, column=1, sticky=tk.W, pady=5)
        self.widget_list.append([self.multiselect_external_references, "external_references"])




        #add markings, object_marking_refs and granualr markings




        # OPEN EDITOR IN EDIT MODE
        if self.type_of_editor == 1:
            self.edit()



        #-----Frame Buttons----------------------
        self.buttonHolder = tk.Frame(self)
        self.buttonHolder.pack(side=tk.BOTTOM, fill=tk.X)
        self.backButton = tk.Button(self.buttonHolder, text="Previous Page", highlightthickness=0, font=("OpenSans", 12, "bold"), fg="white", bg=self.COLOR_3, command=lambda : self.switch_page("left"), relief=tk.FLAT)
        self.backButton.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.backButton.configure(state=tk.DISABLED)
        self.submitButton = tk.Button(self.buttonHolder, text="Submit", font=("OpenSans", 12, "bold"), fg="white", bg="#03AC13", relief=tk.FLAT, highlightthickness=0, command = lambda : [self.callback(object_class), object_class.packer(0), object_class.updatelist(self.object)])
        self.submitButton.pack(side=tk.LEFT)
        self.cancelButton = tk.Button(self.buttonHolder, text="Cancel", font=("OpenSans", 12, "bold"), fg="white", bg="#FF3B30", relief=tk.FLAT, highlightthickness=0, command=lambda: [self.destroy(), object_class.packer(0)])
        self.cancelButton.pack(side=tk.LEFT)
        self.frontButton = tk.Button(self.buttonHolder, text="   Next Page  ", highlightthickness=0, font=("OpenSans", 12, "bold"), fg="white", bg=self.COLOR_3, command=lambda : self.switch_page("right"), relief=tk.FLAT)
        self.frontButton.pack(side=tk.LEFT, fill=tk.X, expand=True)


    def switch_page(self, side):
        self.mandatoryFrame.pack_forget()
        self.goFrame.pack_forget()
        self.afFrame.pack_forget()
        self.backButton.configure(state=tk.NORMAL)
        self.frontButton.configure(state=tk.NORMAL)

        if side=="left":
            if self.current_page==3:
                self.current_page-=1
                self.goFrame.pack(fill=tk.BOTH)
            elif self.current_page==2:
                self.current_page-=1
                self.mandatoryFrame.pack(fill=tk.BOTH)
                self.backButton.configure(state=tk.DISABLED)
            elif self.current_page==1:
                self.mandatoryFrame.pack(fill=tk.BOTH)
        else:
            if self.current_page==1:
                self.current_page+=1
                self.goFrame.pack(fill=tk.BOTH)
            elif self.current_page==2:
                self.current_page+=1
                self.afFrame.pack(fill=tk.BOTH)
                self.frontButton.configure(state=tk.DISABLED)
            elif self.current_page==3:
                self.mandatoryFrame.pack(fill=tk.BOTH)






    def hover(self, label):
        if label == "name":
            self.infoLabel.configure(text="Name: A name used to identify the "+self.object)
        elif label == "labels":
            self.infoLabel.configure(text="Labels: This property is an Open Vocabulary that specifies the type of "+self.object)
        elif label == "pattern":
            self.infoLabel.configure(text="Pattern: The detection pattern for this Indicator is a STIX Pattern as specified in STIX Patterning Docs.\n Format Example: [ipv4:value='192.168.1.1'] ")
        elif label == "valid_from":
            self.infoLabel.configure(text="Valid From: The time from which this Indicator should be considered valuable intelligence.")


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
    def callback(self, object_class):
        object = self.object
        object_class.selector(object)


        dict = {}
        for item in self.widget_list:
            temp = item[0].get()


            if item[1] == "labels" or item[1] == "aliases" or item[1] == "goals":
                if temp != "":
                    temp = temp.split(" ")


            if isinstance(temp, list):
                if temp:
                    dict.update({item[1]: temp})
            elif temp != "":
                dict.update({item[1] : temp})

            elif (item[1] in ["name"]):
                tk.messagebox.showwarning("Error", "Entries marked with '*' cannot be left blank!", parent = self)
                return

        if not self.editmode:
            try:
                flag, debug = getattr(sys.modules[__name__], "%s_maker" % object.replace("-", "_"))(**dict)
                print(debug)
            except Exception as e:
                tk.messagebox.showerror("Error", str(e), parent = self)
                return
            if flag=="True":
                tk.messagebox.showinfo("Object Creation Successfull!", object + " " + self.nameEntry.get() + " created seccessfully!", parent = self)
                pass
            self.destroy()
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
                                                   parent=self)
                        self.editmode=False
                        pass
                        self.destroy()
            else:
                flag, debug = getattr(sys.modules[__name__], "%s_maker" % object.replace("-", "_"))(**dict)
                print(debug)
                if flag == "True":
                    tk.messagebox.showinfo("Object Edit Successfull!",
                                           object + " " + self.nameEntry.get() + " was edited seccessfully!",
                                           parent=self)
                    self.editmode=False
                    pass
                self.destroy()




    # ---Dictionary check function on the Relationship Entry Box
    def keyPress(self, event):
        if event.char in (
                "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S",
                "T", "U",
                "V", "W", "X", "Y", "Z",
                "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s",
                "t", "u",
                "v", "w", "x", "y", "z",
                "-", " "):
            print
            event.char
        elif event.keysym not in ('BackSpace', 'Delete', 'Tab', 'Left', 'Right'):
            print
            event.keysym
            return 'break'

    # ---Dictionary check fo date and time------
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