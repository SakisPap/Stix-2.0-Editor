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
from tools import Multiselect, CreatedByRef, HoverManager, SightingOfRef



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

        self.configure(bg=self.COLOR_1)

        self.grid_propagate(0)
        self.pack_propagate(0)
        self.object = object

        object_class.packer(1)


        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=4)
        self.widget_list = []
        self.hover_labels_list = []
        self.type_of_editor = type_of_editor
        self.current_page = 1

        self.widgets(object_class)




        #------------------MANDATORY EDITOR FRAME WIDGETS------------------------------
    def widgets(self, object_class):
        eRow=0

        object=object_class.object
        self.mandatoryFrame = tk.Frame(self, bg=self.COLOR_1)
        self.mandatoryFrame.pack(fill=tk.X)
        self.mandatoryFrame.columnconfigure(1, weight=3)

        Xsize = 320
        Ysize = 50

        Xsize2 = 250
        Ysize2 = 50



        #---Name---
        if (object != "observed-data" and object != "marking-definition" and object!= "sighting"):                                                   #Indicator's name can be optional according to docs but messes with the GUI understanding
            self.nameLabel = tk.Label(self.mandatoryFrame, text="*Name:", font=("OpenSans", 12))
            self.nameLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            self.nameEntry = tk.Entry(self.mandatoryFrame, font=("OpenSans", 12), width=60)
            self.nameEntry.grid(row=eRow, column=1, sticky=tk.W, pady=5)
            self.nameEntry.bind('<KeyPress>', self.keyPress)
            self.widget_list.append([self.nameEntry, "name"])
            self.hover_labels_list.append(self.nameLabel) #hover
            eRow+=1

        if (object == "sighting"):
            # WARNING: Implement id selection toplevel OF ALL OBJECTS
            self.mandatoryFrame.columnconfigure(1, weight=3)
            self.sighting_of_refLabel = tk.Label(self.mandatoryFrame, text="*Sighting of Reference:",
                                                 font=("OpenSans", 12))
            self.sighting_of_refLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            self.sightingofref=SightingOfRef(self.mandatoryFrame, eRow)
            self.sighting_of_refButton = tk.Button(self.mandatoryFrame, font=("OpenSans", 12), text="Select...",
                                                   command=lambda : self.sightingofref.pop(self.mandatoryFrame))
            self.sighting_of_refButton.grid(row=eRow, column=1, sticky=tk.W, pady=5)
            self.widget_list.append([self.sightingofref, "sighting_of_ref"])
            self.hover_labels_list.append(self.sighting_of_refLabel) #hover
            eRow += 1

            self.countLabel = tk.Label(self.mandatoryFrame, text="Count:", font=("OpenSans", 12))  # integer
            self.countLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            self.countEntry = tk.Entry(self.mandatoryFrame, font=("OpenSans", 12))
            self.countEntry.grid(row=eRow, column=1, sticky=tk.W, padx=5)
            self.widget_list.append([self.countEntry, "count"])
            self.hover_labels_list.append(self.countLabel) #hover

            eRow += 1


            self.observed_data_refsLabel = tk.Label(self.mandatoryFrame, text="Observed Data References:",
                                                    font=("OpenSans", 12))
            self.observed_data_refsLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            listitems = getObjectIDs("observed-data")
            self.multiselect_observed_data_refs = Multiselect(self, self.mandatoryFrame, listitems, eRow, self.COLOR_1,
                                                              self.COLOR_2,
                                                              self.COLOR_3)
            self.observed_data_refsButton = tk.Button(self.mandatoryFrame, font=("OpenSans", 12), text="...",
                                                      command=lambda: [
                                                          self.multiselect_observed_data_refs.place(x=Xsize2, y=Ysize2),
                                                          self.mandatoryFrame.lift(),
                                                          self.multiselect_observed_data_refs.lift(),
                                                          self.multiselect_observed_data_refs.grab_set()])
            self.observed_data_refsButton.grid(row=eRow, column=1, sticky=tk.W, pady=5)

            self.widget_list.append([self.multiselect_observed_data_refs, "observed_data_refs"])
            self.hover_labels_list.append(self.observed_data_refsLabel) #hover

            eRow += 1

            self.where_sighted_refsLabel = tk.Label(self.mandatoryFrame, text="Where Sighted References:",
                                                    font=("OpenSans", 12))
            self.where_sighted_refsLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            listitems = getObjectIDs("identity")
            self.multiselect_where_sighted_refs = Multiselect(self, self.mandatoryFrame, listitems, eRow, self.COLOR_1,
                                                              self.COLOR_2,
                                                              self.COLOR_3)
            self.where_sighted_refsButton = tk.Button(self.mandatoryFrame, font=("OpenSans", 12),
                                                      text="Select Identity IDs",
                                                      command=lambda: [
                                                          self.multiselect_where_sighted_refs.place(x=Xsize2, y=Ysize2),
                                                          self.mandatoryFrame.lift(),
                                                          self.multiselect_where_sighted_refs.lift(),
                                                          self.multiselect_where_sighted_refs.grab_set()])
            self.where_sighted_refsButton.grid(row=eRow, column=1, sticky=tk.W, pady=5)
            self.widget_list.append([self.multiselect_where_sighted_refs, "where_sighted_refs"])
            self.hover_labels_list.append(self.where_sighted_refsLabel) #hover

            eRow += 1

            self.summaryVar=tk.BooleanVar()
            self.summaryCheckButton = tk.Checkbutton(self.mandatoryFrame, text="Summary", font=("OpenSans", 12),
                                                     bg=self.COLOR_1, variable=self.summaryVar)
            self.summaryCheckButton.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            self.widget_list.append([self.summaryVar, "summary"])
            self.hover_labels_list.append(self.summaryCheckButton) #hover

            eRow += 1

        if object ==  "observed-data":
            self.first_observedLabel = tk.Label(self.mandatoryFrame, text="*First Observed:", font=("OpenSans", 12))
            self.first_observedLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            self.first_observedEntry = tk.Entry(self.mandatoryFrame, font=("OpenSans", 12))
            self.first_observedEntry.grid(row=eRow, column=1, sticky=tk.W, pady=5)
            self.widget_list.append([self.first_observedEntry, "first_observed"])
            self.hover_labels_list.append(self.first_observedLabel) #hover

            eRow += 1

            self.last_observedLabel = tk.Label(self.mandatoryFrame, text="*Last Observed:", font=("OpenSans", 12))
            self.last_observedLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            self.last_observedEntry = tk.Entry(self.mandatoryFrame, font=("OpenSans", 12))
            self.last_observedEntry.grid(row=eRow, column=1, sticky=tk.W, pady=5)
            self.widget_list.append([self.last_observedEntry, "last_observed"])
            self.hover_labels_list.append(self.last_observedLabel) #hover

            eRow += 1

            self.number_observedLabel = tk.Label(self.mandatoryFrame, text="*Number Observed:", font=("OpenSans", 12))
            self.number_observedLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            self.number_observedEntry = tk.Entry(self.mandatoryFrame, font=("OpenSans", 12))
            self.number_observedEntry.grid(row=eRow, column=1, sticky=tk.W, pady=5)
            self.widget_list.append([self.number_observedEntry, "number_observed"])
            self.hover_labels_list.append(self.number_observedLabel) #hover

            eRow += 1

            self.objectsLabel = tk.Label(self.mandatoryFrame, text="*Objects:", font=("OpenSans", 12))
            self.objectsLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            self.objectsButton = tk.Button(self.mandatoryFrame, text="Add...", font=("OpenSans", 12))
            self.objectsButton.grid(row=eRow, column=1, sticky=tk.W, pady=5)
            self.widget_list.append([self.number_observedEntry, "number_observed"])
            self.hover_labels_list.append(self.objectsLabel) #hover

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
            self.hover_labels_list.append(self.identity_classLabel) #hover

            eRow+=1

        if object == "indicator" or object == "malware" or object == "report" or object == "threat-actor" or object == "tool":
            self.labels_reqLabel = tk.Label(self.mandatoryFrame, text="*Labels:", font=("OpenSans", 12))
            self.labels_reqLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            self.labels_reqEntry = tk.Entry(self.mandatoryFrame, font=("OpenSans", 12), width=70) #---Please also add vocab options (Toplevel with radiobuttons)
            self.labels_reqEntry.grid(row=eRow, column=1, sticky=tk.W, pady=5)
            self.labels_reqEntry.bind('<KeyPress>', self.keyPress)

            self.widget_list.append([self.labels_reqEntry, "labels"])
            self.hover_labels_list.append(self.labels_reqLabel) #hover

            eRow+=1

        if object == "indicator":
            self.patternLabel = tk.Label(self.mandatoryFrame, text="*Pattern:", font=("OpenSans", 12))
            self.patternLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            self.patternEntry = tk.Entry(self.mandatoryFrame, font=("OpenSans", 12), width=80)
            self.patternEntry.grid(row=eRow, column=1, sticky=tk.W, pady=5)
            #self.patternEntry.bind('<KeyPress>', self.keyPress)

            self.widget_list.append([self.patternEntry, "pattern"])
            self.hover_labels_list.append(self.patternLabel) #hover

            eRow+=1

            self.valid_fromVar = tk.StringVar()
            self.valid_fromLabel = tk.Label(self.mandatoryFrame, text="*Valid From:", font=("OpenSans", 12))
            self.valid_fromLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)


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
            self.hover_labels_list.append(self.valid_fromLabel) #hover


            eRow+=1

        if(object=="report"):
            self.publishedLabel = tk.Label(self.mandatoryFrame, text="*Published:", font=("OpenSans", 12))
            self.publishedLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            self.publishedEntry = tk.Entry(self.mandatoryFrame, font=("OpenSans", 12))
            self.publishedEntry.grid(row=eRow, column=1, sticky=tk.W, pady=5)
            self.widget_list.append([self.publishedEntry, "published"])
            self.hover_labels_list.append(self.publishedLabel) #hover

            eRow+=1

            self.object_refsLabel = tk.Label(self.mandatoryFrame, text="*Object Referred:", font=("OpenSans", 12))
            self.object_refsLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            listitems = getAllIDs()
            self.multiselect_object_refs = Multiselect(self, self.mandatoryFrame, listitems, eRow, self.COLOR_1, self.COLOR_2, self.COLOR_3)
            #WARNING!! FIX MULTISELECT LOCATION
            self.object_refsButton = tk.Button(self.mandatoryFrame, font=("OpenSans", 12), text="...",
                                           command=lambda: [self.multiselect_object_refs.place(x=Xsize2, y=Ysize2),
                                                            self.mandatoryFrame.lift(), self.multiselect_object_refs.lift(),
                                                            self.multiselect_object_refs.grab_set()])
            self.object_refsButton.grid(row=eRow, column=1, sticky=tk.W, pady=5)
            self.widget_list.append([self.multiselect_object_refs, "object_refs"])
            self.hover_labels_list.append(self.object_refsLabel) #hover

            eRow += 1


        ###########OBJECT SPECIFIC OPTIONALS----------#############################################OBJECT SPECIFIC OPTIONALS----------##################################
        #description (featured in all excpt)
        if(object!="observed-data" and object!="marking-definition" and object!="sighting"):
            self.descriptionLabel = tk.Label(self.mandatoryFrame, text="Description:", font=("OpenSans", 12))
            self.descriptionLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            self.descriptionEntry = tk.Text(self.mandatoryFrame, font=("OpenSans", 12), width=80, height=3, wrap=tk.WORD)
            self.descriptionEntry.grid(row=eRow, column=1, sticky=tk.W, pady=5)
            self.widget_list.append([self.descriptionEntry,"description"])
            self.hover_labels_list.append(self.descriptionLabel) #hover

            eRow+=1

        #kill chain phases
        if(object=="attack-pattern" or object=="indicator" or object=="malware" or object=="tool"):
            self.kill_chain_phasesLabel = tk.Label(self.mandatoryFrame, text="Kill Chain Phases:", font=("OpenSans", 12)) #Management!!
            self.kill_chain_phasesLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            listitems=getKillChainPhases()
            self.multiselect_kill_chain_phases= Multiselect(self, self.mandatoryFrame, listitems, eRow, self.COLOR_1, self.COLOR_2, self.COLOR_3, flag="killchain")
            self.kill_chain_phasesButton = tk.Button(self.mandatoryFrame, font = ("OpenSans", 12), text="Add...", command=lambda: [self.multiselect_kill_chain_phases.place(x=Xsize2, y=Ysize2),
                                                            self.multiselect_kill_chain_phases.lift(),
                                                            self.multiselect_kill_chain_phases.grab_set()])
            self.kill_chain_phasesButton.grid(row=eRow, column=1, sticky=tk.W, pady=5)
            self.widget_list.append([self.multiselect_kill_chain_phases, "kill_chain_phases"])
            self.hover_labels_list.append(self.kill_chain_phasesLabel) #hover

            eRow+=1

        #aliases - arr string
        if (object=="campaign" or object=="intrusion-set" or object=="threat-actor"):
            self.aliasesLabel = tk.Label(self.mandatoryFrame, text="Aliases:", font=("OpenSans", 12))
            self.aliasesLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            self.aliasesEntry = tk.Entry(self.mandatoryFrame, font=("OpenSans", 12), width=60)
            self.aliasesEntry.grid(row=eRow, column=1, sticky=tk.W, pady=5)
            self.widget_list.append([self.aliasesEntry, "aliases"])
            self.hover_labels_list.append(self.aliasesLabel) #hover

            eRow+=1

        #first_seen ts
        if (object=="campaign" or object=="intrusion-set" or object=="sighting"):
            self.first_seenLabel = tk.Label(self.mandatoryFrame, text="First Seen:", font=("OpenSans", 12))
            self.first_seenLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            self.first_seenEntry = tk.Entry(self.mandatoryFrame, font=("OpenSans", 12))
            self.first_seenEntry.grid(row=eRow, column=1, sticky=tk.W, pady=5)
            self.widget_list.append([self.first_seenEntry, "first_seen"])
            self.hover_labels_list.append(self.first_seenLabel) #hover

            eRow += 1

        # last_seen ts
        if (object == "campaign" or object == "intrusion-set" or object=="sighting"):
            self.last_seenLabel = tk.Label(self.mandatoryFrame, text="Last Seen:", font=("OpenSans", 12))
            self.last_seenLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            self.last_seenEntry = tk.Entry(self.mandatoryFrame, font=("OpenSans", 12))
            self.last_seenEntry.grid(row=eRow, column=1, sticky=tk.W, pady=5)
            self.widget_list.append([self.last_seenEntry, "last_seen"])
            self.hover_labels_list.append(self.last_seenLabel) #hover

            eRow += 1

        # objective str
        if(object=="campaign"):
            self.objectiveLabel = tk.Label(self.mandatoryFrame, text="Objective:", font=("OpenSans", 12))
            self.objectiveLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            self.objectiveEntry = tk.Entry(self.mandatoryFrame, font=("OpenSans", 12))
            self.objectiveEntry.grid(row=eRow, column=1, sticky=tk.W, pady=5)
            self.widget_list.append([self.objectiveEntry, "objective"])
            self.hover_labels_list.append(self.objectiveLabel) #hover

            eRow += 1


        if(object=="identity"):
            listitems = ["agriculture", "aerospace", "automotive", "communications", "construction", "defence", "education", "energy", "entertainment", "financial-services", "government-national", "government-regional", "government-local", "government-public-services", "healthcare", "hospitality-leisure", "infrastructure", "insurance", "manufacturing", "mining", "non-profit", "pharmaceuticals", "retail", "technology", "telecommunications", "transportation", "utilities"]
            self.multiselect_sectors = Multiselect(self, self.mandatoryFrame, listitems, eRow, self.COLOR_1, self.COLOR_2, self.COLOR_3)
            self.sectorsLabel = tk.Label(self.mandatoryFrame, text="Sectors:", font=("OpenSans", 12))
            self.sectorsLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            self.sectorsButton = tk.Button(self.mandatoryFrame, font = ("OpenSans", 12), text="...", command=lambda : [self.multiselect_sectors.place(x=Xsize, y=Ysize), self.multiselect_sectors.grab_set(), self.multiselect_sectors.lift()])
            self.sectorsButton.grid(row=eRow, column=1, sticky=tk.W, pady=5)
            self.widget_list.append([self.multiselect_sectors, "sectors"])
            self.hover_labels_list.append(self.sectorsLabel) #hover

            eRow += 1

            self.contant_informationLabel = tk.Label(self.mandatoryFrame, text="Contant Information:", font=("OpenSans", 12))
            self.contant_informationLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            self.contant_informationEntry = tk.Entry(self.mandatoryFrame, font=("OpenSans", 12))
            self.contant_informationEntry.grid(row=eRow, column=1, sticky=tk.W, pady=5)
            self.widget_list.append([self.contant_informationEntry, "contact_information"])
            self.hover_labels_list.append(self.contant_informationLabel) #hover

            eRow += 1

        if(object=="indicator"):
            self.valid_untilLabel = tk.Label(self.mandatoryFrame, text="Valid Until:", font=("OpenSans", 12))
            self.valid_untilLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            self.valid_untilEntry = tk.Entry(self.mandatoryFrame, font=("OpenSans", 12))
            self.valid_untilEntry.grid(row=eRow, column=1, sticky=tk.W, pady=5)
            self.widget_list.append([self.valid_untilEntry, "valid_until"])
            self.hover_labels_list.append(self.valid_untilLabel) #hover

            eRow += 1

        if(object=="intrusion-set" or object=="threat-actor"):
            #GOALS, array str
            self.goalsLabel = tk.Label(self.mandatoryFrame, text="Goals:", font=("OpenSans", 12))
            self.goalsLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            self.goalsEntry = tk.Entry(self.mandatoryFrame, font=("OpenSans", 12), width=60)
            self.goalsEntry.grid(row=eRow, column=1, sticky=tk.W, pady=5)
            self.widget_list.append([self.goalsEntry, "goals"])
            self.hover_labels_list.append(self.goalsLabel) #hover

            eRow += 1

            self.resource_levelLabel = tk.Label(self.mandatoryFrame, text="Resource Level:", font=("OpenSans", 12))
            self.resource_levelLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            self.resource_levelVar = tk.StringVar()
            self.resource_levelVar.set("")
            self.resource_levelOption = tk.OptionMenu(self.mandatoryFrame, self.resource_levelVar, "", "individual", "club", "contest", "team", "organization", "government")
            self.resource_levelOption.grid(row=eRow, column=1, sticky=tk.W, pady=5)
            self.widget_list.append([self.resource_levelVar, "resource_level"])
            self.hover_labels_list.append(self.resource_levelLabel) #hover

            eRow += 1

            self.primary_motivationLabel = tk.Label(self.mandatoryFrame, text="Primary Motivation:", font=("OpenSans", 12))
            self.primary_motivationLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            self.primary_motivationVar = tk.StringVar()
            self.primary_motivationVar.set("")
            self.primary_motivationOption = tk.OptionMenu(self.mandatoryFrame, self.primary_motivationVar, "", "accidental", "coercion", "dominance", "ideology", "notoriety", "organizational-gain", "personal-gain",
"personal-satisfaction", "revenge", "unpredictable")
            self.primary_motivationOption.grid(row=eRow, column=1, sticky=tk.W, pady=5)
            self.widget_list.append([self.primary_motivationVar, "primary_motivation"])
            self.hover_labels_list.append(self.primary_motivationLabel) #hover

            eRow +=1

            self.secondary_motivationsLabel = tk.Label(self.mandatoryFrame, text="Secondary Motivations:", font=("OpenSans", 12))
            self.secondary_motivationsLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            listitems=["accidental", "coercion", "dominance", "ideology", "notoriety", "organizational-gain", "personal-gain",
"personal-satisfaction", "revenge", "unpredictable"]
            self.multiselect_secondary_motivations = Multiselect(self, self.mandatoryFrame, listitems, eRow, self.COLOR_1, self.COLOR_2, self.COLOR_3)
            self.secondary_motivationsButton = tk.Button(self.mandatoryFrame, font=("OpenSans", 12), text="...",
                                           command=lambda: [self.multiselect_secondary_motivations.place(x=Xsize2, y=Ysize2),
                                                            self.mandatoryFrame.lift(), self.multiselect_secondary_motivations.lift(),
                                                            self.multiselect_secondary_motivations.grab_set()])
            self.secondary_motivationsButton.grid(row=eRow, column=1, sticky=tk.W, pady=5)

            self.widget_list.append([self.multiselect_secondary_motivations, "secondary_motivations"])
            self.hover_labels_list.append(self.secondary_motivationsLabel) #hover

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
                                                             self.multiselect_personal_motivations.place(x=Xsize2, y=Ysize2),
                                                             self.mandatoryFrame.lift(),
                                                             self.multiselect_personal_motivations.lift(),
                                                             self.multiselect_personal_motivations.grab_set()])
            self.personal_motivationsButton.grid(row=eRow, column=1, sticky=tk.W, pady=5)

            self.widget_list.append([self.multiselect_personal_motivations, "personal_motivations"])
            self.hover_labels_list.append(self.personal_motivationsLabel) #hover

            eRow += 1


            self.rolesLabel = tk.Label(self.mandatoryFrame, text="Roles:", font=("OpenSans", 12))
            self.rolesLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            listitems = ["agent", "director", "independent", "infrastructure-architect", "infrastructure-operator", "malware-author", "sponsor"]
            self.multiselect_roles = Multiselect(self, self.mandatoryFrame, listitems, eRow, self.COLOR_1, self.COLOR_2, self.COLOR_3)
            self.rolesButton = tk.Button(self.mandatoryFrame, font=("OpenSans", 12), text="...",
                                                         command=lambda: [
                                                             self.multiselect_roles.place(x=Xsize2, y=Ysize2),
                                                             self.mandatoryFrame.lift(),
                                                             self.multiselect_roles.lift(),
                                                             self.multiselect_roles.grab_set()])
            self.rolesButton.grid(row=eRow, column=1, sticky=tk.W, pady=5)

            self.widget_list.append([self.multiselect_roles, "roles"])
            self.hover_labels_list.append(self.rolesLabel) #hover

            eRow+=1

            self.sophisticationLabel = tk.Label(self.mandatoryFrame, text="Sophistication:", font=("OpenSans", 12))
            self.sophisticationLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            self.sophisticationVar = tk.StringVar()
            self.sophisticationVar.set("")
            self.sophisticationOption = tk.OptionMenu(self.mandatoryFrame, self.sophisticationVar, "", "none", "minimal", "intermediate", "advanced", "expert", "innovator", "strategic")
            self.sophisticationOption.grid(row=eRow, column=1, sticky=tk.W, pady=5)
            self.widget_list.append([self.sophisticationVar, "sophistication"])
            self.hover_labels_list.append(self.sophisticationLabel) #hover

            eRow += 1




        if(object=="tool"):
            self.tool_versionLabel = tk.Label(self.mandatoryFrame, text="Tool Version:", font=("OpenSans", 12))
            self.tool_versionLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            self.tool_versionEntry = tk.Entry(self.mandatoryFrame, font=("OpenSans", 12))
            self.tool_versionEntry.grid(row=eRow, column=1, sticky=tk.W, pady=5)
            self.widget_list.append([self.tool_versionEntry, "tool_version"])
            self.hover_labels_list.append(self.tool_versionLabel) #hover

            eRow += 1



        if(object=="marking-definition"):
            def markdef(event):
                if(self.definition_typeVar.get()=="statement"):
                    self.tlpLabel.config(state=tk.DISABLED)
                    self.tlpOption.config(state=tk.DISABLED)
                    self.statementLabel.config(state=tk.NORMAL)
                    self.statementEntry.config(state=tk.NORMAL)
                else:
                    self.statementLabel.config(state=tk.DISABLED)
                    self.statementEntry.config(state=tk.DISABLED)
                    self.tlpLabel.config(state=tk.NORMAL)
                    self.tlpOption.config(state=tk.NORMAL)


            self.definition_typeLabel = tk.Label(self.mandatoryFrame, text="*Definition Type:", font=("OpenSans", 12))
            self.definition_typeLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            self.definition_typeVar = tk.StringVar()
            self.definition_typeVar.set("")
            self.definition_typeOption = tk.OptionMenu(self.mandatoryFrame, self.definition_typeVar, "statement", "tlp", command=markdef)
            self.definition_typeOption.grid(row=eRow, column=1, sticky=tk.W, pady=5)
            self.widget_list.append([self.definition_typeVar, "definition_type"])
            self.hover_labels_list.append(self.definition_typeLabel) #hover

            eRow += 1

            self.statementLabel = tk.Label(self.mandatoryFrame, text="**Statement:", font=("OpenSans", 12), bg=self.COLOR_1, state=tk.DISABLED)
            self.statementLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)

            self.statementEntry = tk.Entry(self.mandatoryFrame, font=("OpenSans", 12), state=tk.DISABLED, width=80)
            self.statementEntry.grid(row=eRow, column=1, sticky=tk.W, padx=5)
            #self.widget_list.append([self.statementEntry, "definition"])

            eRow += 1

            self.tlpLabel = tk.Label(self.mandatoryFrame, text="**TLP:", font=("OpenSans", 12), bg=self.COLOR_1, state=tk.DISABLED)
            self.tlpLabel.grid(row=eRow, column=0, sticky=tk.E, padx=5)
            self.tlpVar = tk.StringVar()
            self.tlpVar.set("")
            self.tlpOption = tk.OptionMenu(self.mandatoryFrame, self.tlpVar, "white", "green", "amber", "red")
            self.tlpOption.grid(row=eRow, column=1, sticky=tk.W, pady=5)
            self.tlpOption.config(state=tk.DISABLED)
            #self.widget_list.append([self.tlpVar, "definition"])

            eRow += 1

            self.markdefdesclaimerLabel=tk.Label(self.mandatoryFrame, text="**You can only choose one\n based on Definition Type",bg=self.COLOR_1, font=("OpenSans", 8))
            self.markdefdesclaimerLabel.grid(row=eRow,column=0, sticky=tk.E,padx=5)
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
        self.hover_labels_list.append(self.idLabel)  # hover

        afRow+=1

        self.createdLabel = tk.Label(self.afFrame, text="Created:", font=("OpenSans", 12), bg=self.COLOR_1)
        self.createdLabel.grid(row=afRow, column=0, sticky=tk.E, padx=5)
        self.createdEntry = tk.Entry(self.afFrame, font=("OpenSans", 12))
        self.createdEntry.grid(row=afRow, column=1, sticky=tk.W, pady=5)
        self.widget_list.append([self.createdEntry, "created"])
        self.hover_labels_list.append(self.createdLabel)  # hover

        afRow+=1

        if (object!="marking-definition"):
            self.modifiedLabel = tk.Label(self.afFrame, text="Modified:", font=("OpenSans", 12), bg=self.COLOR_1)
            self.modifiedLabel.grid(row=afRow, column=0, sticky=tk.E, padx=5)
            self.modifiedEntry = tk.Entry(self.afFrame, font=("OpenSans", 12))
            self.modifiedEntry.grid(row=afRow, column=1, sticky=tk.W, pady=5)
            self.widget_list.append([self.modifiedEntry, "modified"])
            self.hover_labels_list.append(self.modifiedLabel) #hover


            afRow+=1








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

        self.createdbyref = CreatedByRef(self.goFrame, goRow, self.COLOR_1)
        self.created_by_refButton = tk.Button(self.goFrame, font=("OpenSans", 12), text="Select Identity...", command= lambda : [self.createdbyref.pop(self.mandatoryFrame, self.goFrame)])
        self.created_by_refButton.grid(row=goRow, column=1, sticky=tk.W, pady=5)
        self.widget_list.append([self.createdbyref, "created_by_ref"])
        self.hover_labels_list.append(self.created_by_refLabel)  # hover

        goRow+=1

        if (object != "marking-definition"):
            self.revokedVar=tk.BooleanVar()
            self.revokedCheckButton=tk.Checkbutton(self.goFrame, text="Revoked?", font=("OpenSans", 12), bg=self.COLOR_1, variable=self.revokedVar)#Add revoked management
            self.revokedCheckButton.grid(row=goRow,column=0,sticky=tk.E, padx=5)
            self.widget_list.append([self.revokedVar,"revoked"])
            self.hover_labels_list.append(self.revokedCheckButton) #hover


            goRow+=1

        self.external_referencesLabel = tk.Label(self.goFrame, text="External References:", font=("OpenSans", 12), bg=self.COLOR_1)
        self.external_referencesLabel.grid(row=goRow, column=0, sticky=tk.E, padx=5)
        listitems=getExternalRefs()
        self.multiselect_external_references= Multiselect(self, self.goFrame, listitems, goRow, self.COLOR_1, self.COLOR_2, self.COLOR_3, flag="exref")
        self.external_referencesButton = tk.Button(self.goFrame, font = ("OpenSans", 12), text="Add...", command=lambda: [self.multiselect_external_references.place(x=Xsize, y=Ysize),
                                                        self.multiselect_external_references.lift(),
                                                        self.multiselect_external_references.grab_set()])
        self.external_referencesButton.grid(row=goRow, column=1, sticky=tk.W, pady=5)
        self.widget_list.append([self.multiselect_external_references, "external_references"])
        self.hover_labels_list.append(self.external_referencesLabel)  # hover

        goRow+=1

        self.object_marking_refsLabel = tk.Label(self.goFrame, text="Object Marking References:", font=("OpenSans", 12),
                                                 bg=self.COLOR_1)
        self.object_marking_refsLabel.grid(row=goRow, column=0, sticky=tk.E, padx=5)
        listitems = getFilesJson("marking-definition", 0)
        self.multiselect_object_marking_refs = Multiselect(self, self.goFrame, listitems, goRow, self.COLOR_1,
                                                           self.COLOR_2, self.COLOR_3)
        self.object_marking_refsButton = tk.Button(self.goFrame, font=("OpenSans", 12), text="Add...", command=lambda: [
            self.multiselect_object_marking_refs.place(x=Xsize, y=Ysize),
            self.multiselect_object_marking_refs.lift(),
            self.multiselect_object_marking_refs.grab_set()])
        self.object_marking_refsButton.grid(row=goRow, column=1, sticky=tk.W, pady=5)
        self.widget_list.append([self.multiselect_object_marking_refs, "object_marking_refs"])
        self.hover_labels_list.append(self.object_marking_refsLabel)  # hover

        goRow+=1

        self.granular_markingsLabel = tk.Label(self.goFrame, text="Granular Markings:", font=("OpenSans", 12),
                                                 bg=self.COLOR_1)
        self.granular_markingsLabel.grid(row=goRow, column=0, sticky=tk.E, padx=5)
        # listitems = getGranularMarks()
        self.multiselect_granular_markings = Multiselect(self, self.goFrame, listitems, goRow, self.COLOR_1,
                                                           self.COLOR_2, self.COLOR_3, flag="exref")
        self.granular_markingsButton = tk.Button(self.goFrame, font=("OpenSans", 12), text="Add...", command=lambda: [
            self.multiselect_granular_markings.place(x=Xsize, y=Ysize),
            self.multiselect_granular_markings.lift(),
            self.multiselect_granular_markings.grab_set()])
        self.granular_markingsButton.grid(row=goRow, column=1, sticky=tk.W, pady=5)
        self.widget_list.append([self.multiselect_granular_markings, "granular_markings"])
        self.hover_labels_list.append(self.granular_markingsLabel)  # hover

        self.granular_markingsButton.config(state=tk.DISABLED)

        goRow += 1


        #add markings, object_marking_refs and granualr markings


#----------HOVER bind manager
        self.hovermngr = HoverManager(object_class)
        i=0
        for item in self.hover_labels_list:
            item.bind("<Enter>", lambda evnt=None, val=self.widget_list[i][1] : self.hovermngr.show(evnt, val))
            i+=1

        for item in self.hover_labels_list:
            item.bind("<Leave>", lambda _: [object_class.selector(self.object), object_class.configure(cursor="")])
            item.configure(bg=self.COLOR_1)




        # OPEN EDITOR IN EDIT MODE
        if self.type_of_editor == 1:
            self.edit()



        #-----Frame Buttons----------------------
        self.buttonHolder = tk.Frame(self)
        self.buttonHolder.pack(side=tk.BOTTOM, fill=tk.X)
        self.backButton = tk.Button(self.buttonHolder, text="Previous Page", highlightthickness=0, font=("OpenSans", 12, "bold"), fg="white", bg=self.COLOR_3, command=lambda : self.switch_page("left"), relief=tk.FLAT)
        self.backButton.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.backButton.configure(state=tk.DISABLED)
        self.submitButton = tk.Button(self.buttonHolder, text="Submit", font=("OpenSans", 12, "bold"), fg="white", bg="#03AC13", relief=tk.FLAT, highlightthickness=0, command = lambda : [self.callback(object_class)])
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



#-----------------------------------------------------EDIT---------------------------------------------------------------------


    def edit(self):
        if self.object!="sighting" and self.object!="marking-definition":
            name = self.full_list[self.listbox.curselection()[0]]
            name = name.split(".:. ")
            stix2object = filestoarr2obj4edit(name[0], name[1])
            keys = getkeys(stix2object)
        else:
            name = self.full_list[self.listbox.curselection()[0]]
            name = name.split(".:. ")
            stix2object = filetoitem(os.path.join(name[0], name[1])+".json")
            keys = getkeys(stix2object)

        for item in self.widget_list:
            if item[1] in keys: #keys
                try:
                    try:
                        item[0].insert("1.0", stix2object[item[1]])
                    except:
                        item[0].insert(tk.END, stix2object[item[1]])

                except:
                    item[0].set(stix2object[item[1]])

        if "definition" in keys:
            temp = stix2object["definition"]
            temp = json.loads(str(temp))
            try:
                self.statementEntry.configure(state=tk.NORMAL)
                self.statementLabel.configure(state=tk.NORMAL)
                self.statementEntry.insert(tk.END, temp["statement"])
                self.tlpOption.configure(state=tk.DISABLED)
                self.tlpLabel.configure(state=tk.DISABLED)
            except:
                self.tlpOption.configure(state=tk.NORMAL)
                self.tlpLabel.configure(state=tk.NORMAL)
                self.tlpVar.set(temp["tlp"])
                self.statementEntry.configure(state=tk.DISABLED)
                self.statementLabel.configure(state=tk.DISABLED)



        self.editmode=True
        if self.object!="sighting" and self.object!="marking-definition":
            self.oname=self.nameEntry.get()
        else:
            self.oname=stix2object.get("id")
#-----------------------------------------------------EDIT-END-----------------------------------------------------------------



    #This gets called upon frame submit---
    def callback(self, object_class):
        object = self.object
        object_class.selector(object)


        dict = {}
        if object=="marking-definition":
            dict2 = {}
            if (self.definition_typeVar.get()=="statement"):
                dict2.update({self.definition_typeVar.get() : self.statementEntry.get()})
                dict.update({"definition" : dict2})
            else:
                dict2.update({self.definition_typeVar.get() : self.tlpVar.get()})
                dict.update({"definition": dict2})
        for item in self.widget_list:
            if isinstance(item[0], tk.Text):
                temp = item[0].get("1.0", "end-1c")
            else:
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
            try:
                check = self.oname!=self.nameEntry.get()
                changedvar="name"
            except:
                check = self.oname!=self.idEntry.get()
                changedvar="id"

            if (check):
                ans=tk.messagebox.askyesno("Warning", "You have modified the name/id of the object. As a result, all data will be stored into another object and not into the current one. Would you like to revert the property back to default?", parent=self)
                if(ans):
                    if(changedvar=="name"):
                        self.nameEntry.delete(0,tk.END)
                        self.nameEntry.insert(0, self.oname)
                    else:
                        self.idEntry.delete(0, tk.END)
                        self.idEntry.insert(0, self.oname)
                else:
                    ans2=tk.messagebox.askyesno("Replication", "Would you like to create a new object with the current properties?", parent=self)
                    if(ans2):
                        flag, debug = getattr(sys.modules[__name__], "%s_maker" % object.replace("-", "_"))(**dict)
                        print(debug)
                        if(changedvar=="name"):
                            tk.messagebox.showinfo("Object Replication Successfull!",
                                                       object + " " + self.nameEntry.get() + " was created seccessfully, while "+ self.oname + " was left intact.",
                                                       parent=self)
                        else:
                            tk.messagebox.showinfo("Object Replication Successfull!",
                                                   object + " " + self.idEntry.get() + " was created seccessfully, while " + self.oname + " was left intact.",
                                                   parent=self)
                        self.editmode=False
                        pass
                        self.destroy()
            else:
                try:
                    flag, debug = getattr(sys.modules[__name__], "%s_maker" % object.replace("-", "_"))(**dict)
                    print(debug)
                except Exception as e:
                    tk.messagebox.showerror("Error", str(e), parent=self)
                    return
                if flag == "True":
                    if self.object!="sighting" and self.object!="marking-definition":
                        msg=object + " " + self.nameEntry.get() + " was edited seccessfully!"
                    else:
                        msg=object + " " + self.idEntry.get() + " was edited seccessfully!"
                    tk.messagebox.showinfo("Object Edit Successfull!", msg, parent=self)
                    self.editmode=False
                    pass
                self.destroy()

        object_class.packer(0)
        object_class.updatelist(self.object)




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