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



class Relationship(tk.Frame):
    def __init__(self, object_class, parent):
        tk.Frame.__init__(self, parent)
        self.grid_propagate(0)
        self.pack_propagate(0)
        object_class.packer(1)
        self.infoLabel = object_class.infoLabel
        self.topLabel = object_class.topLabel
        self.COLOR_1 = object_class.COLOR_1
        self.COLOR_2 = object_class.COLOR_2
        self.COLOR_3 = object_class.COLOR_3
        self.object = object_class.object

        self.configure(bg=self.COLOR_3)

        PADX = 20
        PADY = 10

        self.rel_type_var = tk.StringVar()
        self.entryFlag = False
        self.radio_buttons = []

        self.infoLabel.configure(
            text="Relationship: Used to link two SDOs and to describe how they are related to each other.")
        self.topLabel.config(text="Select an Object from the left list to relate it")


        self.radioFrame = tk.Frame(self, bg=self.COLOR_3)

        self.listboxLeft = tk.Listbox(self, exportselection=0, font=("OpenSans", 10, "bold"), bd=0,
                                      width=30, height=23, relief=tk.FLAT, highlightthickness=0, bg=self.COLOR_1,
                                      fg=self.COLOR_3)
        self.listboxLeft.pack(side=tk.LEFT, padx=PADX, fill=tk.BOTH, expand=True)
        self.listboxLeft.bind('<<ListboxSelect>>', self.constructRelation)

        # ----List All in Left List-------
        # -----------LISTING FOR RELATIONSHIP TAB-----------------------------

        for itemname in filestoarr2("alph"):
            if itemname.get("type") != "relationship" and itemname.get("type") != "marking-definition" and itemname.get("type") != "sighting":
                self.listboxLeft.insert(tk.END, itemname.get("type") + ": " + itemname.get("name"))
            # stix2obj.get("type") + "-> " + stix2obj.get("name")

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
            self.relationshipRadio = tk.Radiobutton(self.radioFrame, command=lambda: self.completeRelation(), text=text,
                                                    variable=self.rel_type_var, value=mode, indicator=0,
                                                    font=("OpenSans", 12, "bold"), fg="white", width=15, bg="#A37F6F",
                                                    relief=tk.FLAT, highlightthickness=0, height=1, pady=5,
                                                    selectcolor="#E09873")
            self.relationshipRadio.pack(pady=3)
            self.radio_buttons.append(self.relationshipRadio)

        self.relationshipEntry = tk.Entry(self.radioFrame, width=15, font=("OpenSans", 12, "bold"),
                                          highlightthickness=2, highlightcolor="#E09873")
        self.relationshipEntry.pack(pady=3)
        self.relationshipEntry.insert(tk.END, "User custom")
        self.relationshipEntry.bind("<1>", lambda _: [self.rel_type_var.set("custom"), self.completeRelation()])
        self.relationshipEntry.bind('<KeyPress>', self.keyPress)

        # disable radio button by default
        for radio_button in self.radio_buttons:
            radio_button.configure(state=tk.DISABLED)
        self.relationshipEntry.configure(stat=tk.DISABLED)

        self.radioFrame.pack(side=tk.LEFT)

        self.listboxRight = tk.Listbox(self, exportselection=0, font=("OpenSans", 10, "bold"), bd=0,
                                       width=30, height=23, relief=tk.FLAT, highlightthickness=0, bg=self.COLOR_1,
                                       fg=self.COLOR_3, highlightcolor="red")
        self.listboxRight.pack(side=tk.LEFT, padx=PADX, fill=tk.BOTH, expand=True)
        self.listboxRight.bind('<<ListboxSelect>>', lambda _: self.ok_button.configure(
            state=tk.NORMAL) if self.rel_type_var.get() != "null" else self.ok_button.configure(state=tk.DISABLED))

        self.ok_button = tk.Button(self.radioFrame, text="Relate", font=("OpenSans", 12, "bold"), fg="white", width=5,
                                   bg="#03AC13", relief=tk.FLAT, highlightthickness=0, height=1,
                                   command=lambda: [self.createRelationship(), self.grab_release(),
                                                    self.destroy(), object_class.packer(0),
                                                    object_class.selector(self.object)])
        self.ok_button.pack(side=tk.LEFT, pady=20, padx=5)

        self.cancel_button = tk.Button(self.radioFrame, text="Abort", font=("OpenSans", 12, "bold"), fg="white",
                                       width=5, bg="#FF3B30", relief=tk.FLAT, highlightthickness=0, height=1,
                                       command=lambda: [self.grab_release(),
                                                        self.destroy(), object_class.packer(0),
                                                        object_class.selector(self.object)])
        self.cancel_button.pack(side=tk.LEFT, pady=20, padx=5)

        self.ok_button.configure(state=tk.DISABLED)



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
            tk.messagebox.showinfo(parent=self, title="Success!",
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
            tk.messagebox.showinfo(parent=self, title="Success!",
                                   message="Relationship: \n" + self.listboxLeft.get(
                                       self.listboxLeft.curselection()) + " ➜ " + self.relationshipEntry.get() + " ➜ " + self.listboxRight.get(
                                       self.listboxRight.curselection()) + "\ncreated successfully!")

            #---Call the Rel Maker with proper args (user custom value)
            debug = relationship_maker(filetoitemfromlist(self.listboxLeft.get(self.listboxLeft.curselection())), self.relationshipEntry.get(), filetoitemfromlist(self.listboxRight.get(self.listboxRight.curselection())))
            print(debug)
        else:
            tk.messagebox.showwarning(parent=self, title="Warning!", message="Please insert a custom value!")


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


