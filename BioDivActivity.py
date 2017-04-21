# -*- coding: utf-8 -*-
# BioDiv   BioDiv is a programme focused on biodiversity
# Copyright (C) 2012 Team Kabelsalat
# This program is free software; you can redistribute it
# and/or modify it under the terms of the GNU General
# Public License as published by the Free Software
# Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will
# be useful, but WITHOUT ANY WARRANTY; without even
# the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public
# License for more details.
#"You fight like a dairy farmer" - The Swordmaster
#"How appropriate, you fight like a cow" - Guybrush Threepwood
# You should have received a copy of the GNU General
# Public License along with this program; if not, write
# to the Free Software Foundation, Inc., 51 Franklin
# St, Fifth Floor, Boston, MA 02110-1301  USA

import gobject
import pygtk
import gtk
import time
import xml.dom.minidom as dom
import random
from sugar.activity import activity
from sugar.graphics import style
SIZE_X = gtk.gdk.screen_width()
SIZE_Y = gtk.gdk.screen_height()

class BioDivActivity(activity.Activity):
    def __init__(self,handle):
        activity.Activity.__init__(self,handle)

        # Standard-Toolbar
        toolbox = activity.ActivityToolbox(self)
        activity_toolbar = toolbox.get_activity_toolbar()
        activity_toolbar.keep.props.visible = False
        activity_toolbar.share.props.visible = False
        self.set_toolbox(toolbox)
        toolbox.show()

         #Assign self._top_canvas_box to be the top level widget on the canvas
        self._top_canvas_box = gtk.VBox()


        self.startv = StartView()
        self.startv.hauptbox.show()
        
        #Zuweisen der Hauptbox auf der Canvas (vergleichbar mit toplevel-Window
        self._top_canvas_box = self.startv.hauptbox

        #Setzen der Canvas (Hauptbildschirm der Activity)
        self.set_canvas(self._top_canvas_box)

    def refreshmain(box):
        self._top_canvas_box = box
        #Setzen der Canvas (Hauptbildschirm der Activity)
        self.set_canvas(self._top_canvas_box)

class Highscore():
    label = gtk.Label()
    vbox = gtk.VBox()
    
    def __init__(self):
        self.aufbau()
    
    def aufbau(self):
        button = gtk.Button("Zurück")
        self.auslesen()
        self.vbox.pack_start(self.label)
        self.vbox.pack_start(button)
        self.label.set_text(self.strzahlen)
        button.connect("clicked", self.buttonstart)
        self.label.show()
        button.show()
    
    def auslesen(self):
        fobj = open("highscore.txt", "r") 
        self.zahlen = fobj.readlines()
        self.zahlen.sort(reverse=True)
        self.strzahlen = self.zahlen[0] + self.zahlen[1] + self.zahlen[2] + self.zahlen[3] + self.zahlen[4]
        fobj.close()
    
    def buttonstart(self, widget):
        self.vbox.destroy()
        instanz = StartView()

# Klasse Tier: Datenstruktur eines Tier-Elements
class Tier():
    name = ""
    bild = ""
    merkmale = []
    def setzufall(self, data=None):
        global zufall
        zufall = random.randrange(0, len(viecher) -1, 1)
        return zufall
    def zufallasi(self):
        global zufallasi
        zufallasi = random.randrange(0, 32, 1)
        return zufallasi
    def zufallaust(self):
        global zufallaust
        zufallaust = random.randrange(0, 13,1)
        return zufallaust
    def zufallafr(self):
        global zufallafr
        zufallafr = random.randrange(0, 22, 1)
        return zufallafr
    def zufalleur(self):
        global zufalleur
        zufalleur = random.randrange(0, 37, 1)
        return zufalleur
    def zufallamer(self):
        global zufallamer
        zufallamer = random.randrange(0, 32, 1)
        return zufallamer
    def zufallmeer(self):
        global zufallmeer
        zufallmeer = random.randrange(0, 14, 1)
        return zufallmeer

# Klasse xmlauslesen: Packt die Auslesemethoden der XML-Datei zusammen.
class xmlauslesen():
    def _knoten_auslesen(knoten): 
        return eval("%s('%s')" % (knoten.getAttribute("typ"), 
                                  knoten.firstChild.data.strip()))
                              
    def lade_dict(dateiname): 
        tiere = []
        baum = dom.parse(dateiname)
        for eintrag in baum.firstChild.childNodes: 
            if eintrag.nodeName == "Tier": 
                tier = Tier()
                tier.merkmale = []
                for knoten in eintrag.childNodes: 
                    if knoten.nodeName == "name":
                        tier.name = knoten.firstChild.nodeValue 
                    elif knoten.nodeName == "bild":
                        tier.bild = None
                    elif knoten.nodeName == "merkmale":
                       for merkmal in knoten.childNodes: 
                           if merkmal.nodeName == "merkmal":
                               tier.merkmale.append(merkmal.firstChild.nodeValue)

                tiere.append(tier) 
        return tiere
    # Zentraler Auslesebefehl
    global viecher
    viecher = lade_dict("BIODIV_daten_debugged_dom.xml")
    global afrika
    afrika = lade_dict("BIODIV_daten_debugged_dom_afrika.xml")
    global asien
    asien = lade_dict("BIODIV_daten_debugged_dom_asien.xml")
    global europa
    europa = lade_dict("BIODIV_daten_debugged_dom_europa.xml")
    global nordamerika
    nordamerika = lade_dict("BIODIV_daten_debugged_dom_amerika.xml")
    global suedamerika
    suedamerika = lade_dict("BIODIV_daten_debugged_dom_meere.xml")
    global australien
    australien = lade_dict("BIODIV_daten_debugged_dom_australien.xml")

class quizfrage():
    Tier = Tier()
    stralleinfo = ""
    stralleinfoafr = ""
    stralleinfoeur = ""
    stralleinfonordamer = ""
    stralleinfosuedamer = ""
    stralleinfoasi = ""
    stralleinfoaus = ""
    stralleinfosuche = ""
    rantwort = []
    fantwort = []
    strantwort = ""
    strrantwort = ""
    strfantwort = ""
    strfantwort2 = ""
    strfantwort3 = ""
    stralleinfosuche = ""

    def setsringssuche(self, data=None):
        info = []
        self.current = viecher[suchtier]
        info.append(self.current.merkmale)
        info.append(self.current.name)
        #hier die Strings fuer die Info
        strinfo = info[0][0]
        strinfo2 = info[0][1]
        strinfo3 = info[0][2]
        strinfo4 = info[0][3]
        strinfo5 = info[0][4]
        strinfo6 = info[0][5]
        strname = info[1]
        self.stralleinfosuche = strname + '.\n' + strinfo + '.\n' + strinfo2 + '.\n' + strinfo3 + '.\n' + strinfo4 + '.\n' + strinfo5 + '.\n' + strinfo6 + '.'

    def setstringsafr(self, data=None):
        self.Tier.zufallafr()
        info = []
        self.current = afrika[zufallafr]
        info.append(self.current.merkmale)
        info.append(self.current.name)
        #hier die Strings fuer die Info
        strinfo = info[0][0]
        strinfo2 = info[0][1]
        strinfo3 = info[0][2]
        strinfo4 = info[0][3]
        strinfo5 = info[0][4]
        strinfo6 = info[0][5]
        strname = info[1]

        self.stralleinfoafr = strname + '.\n' + strinfo + '.\n' + strinfo2 + '.\n' + strinfo3 + '.\n' + strinfo4 + '.\n' + strinfo5 + '.\n' + strinfo6 + '.'
    
    
    def setstringssuedamer(self, data=None):
        self.Tier.zufallmeer()
        info = []
        self.current = suedamerika[zufallmeer]
        info.append(self.current.merkmale)
        info.append(self.current.name)
        #hier die Strings fuer die Info
        strinfo = info[0][0]
        strinfo2 = info[0][1]
        strinfo3 = info[0][2]
        strinfo4 = info[0][3]
        strinfo5 = info[0][4]
        strinfo6 = info[0][5]
        strname = info[1]
        self.stralleinfosuedamer = strname + '.\n' + strinfo + '.\n' + strinfo2 + '.\n' + strinfo3 + '.\n' + strinfo4 + '.\n' + strinfo5 + '.\n' + strinfo6 + '.'

    
    def setstringsnordamer(self, data=None):
        self.Tier.zufallamer()
        info = []
        self.current = nordamerika[zufallamer]
        info.append(self.current.merkmale)
        info.append(self.current.name)
        #hier die Strings fuer die Info
        strinfo = info[0][0]
        strinfo2 = info[0][1]
        strinfo3 = info[0][2]
        strinfo4 = info[0][3]
        strinfo5 = info[0][4]
        strinfo6 = info[0][5]
        strname = info[1]
        self.stralleinfonordamer = strname + '.\n' + strinfo + '.\n' + strinfo2 + '.\n' + strinfo3 + '.\n' + strinfo4 + '.\n' + strinfo5 + '.\n' + strinfo6 + '.'
    
    
    def setstringsaus(self, data=None):
        self.Tier.zufallaust()
        info = []
        self.current = australien[zufallaust]
        info.append(self.current.merkmale)
        info.append(self.current.name)
        #hier die Strings fuer die Info
        strinfo = info[0][0]
        strinfo2 = info[0][1]
        strinfo3 = info[0][2]
        strinfo4 = info[0][3]
        strinfo5 = info[0][4]
        strinfo6 = info[0][5]
        strname = info[1]
        self.stralleinfoaus = strname + '.\n' + strinfo + '.\n' + strinfo2 + '.\n' + strinfo3 + '.\n' + strinfo4 + '.\n' + strinfo5 + '.\n' + strinfo6 + '.'
    
        
    def setstringsasi(self, data=None):
        self.Tier.zufallasi()
        info = []
        self.current = asien[zufallasi]
        info.append(self.current.merkmale)
        info.append(self.current.name)
        #hier die Strings fuer die Info
        strinfo = info[0][0]
        strinfo2 = info[0][1]
        strinfo3 = info[0][2]
        strinfo4 = info[0][3]
        strinfo5 = info[0][4]
        strinfo6 = info[0][5]
        strname = info[1]
        self.stralleinfoasi = strname + '.\n' + strinfo + '.\n' + strinfo2 + '.\n' + strinfo3 + '.\n' + strinfo4 + '.\n' + strinfo5 + '.\n' + strinfo6 + '.'
    

    def setstringseur(self, data=None):
        self.Tier.zufalleur()
        info = []
        self.current = europa[zufalleur]
        info.append(self.current.merkmale)
        info.append(self.current.name)
        #hier die Strings fuer die Info
        strinfo = info[0][0]
        strinfo2 = info[0][1]
        strinfo3 = info[0][2]
        strinfo4 = info[0][3]
        strinfo5 = info[0][4]
        strinfo6 = info[0][5]
        strname = info[1]
        self.stralleinfoeur = strname + '.\n' + strinfo + '.\n' + strinfo2 + '.\n' + strinfo3 + '.\n' + strinfo4 + '.\n' + strinfo5 + '.\n' + strinfo6 + '.'
    
    
    def setstringsent(self, data=None):
        self.Tier.setzufall()
        info = []
        self.current = viecher[zufall]
        info.append(self.current.merkmale)
        info.append(self.current.name)
        #hier die Strings fuer die Info
        strinfo = info[0][0]
        strinfo2 = info[0][1]
        strinfo3 = info[0][2]
        strinfo4 = info[0][3]
        strinfo5 = info[0][4]
        strinfo6 = info[0][5]
        strname = info[1]
        self.stralleinfo = strname + '.\n' + strinfo + '.\n' + strinfo2 + '.\n' + strinfo3 + '.\n' + strinfo4 + '.\n' + strinfo5 + '.\n' + strinfo6 + '.'

    def setstrings(self, data=None):
        self.Tier.setzufall()
        info = []
        self.current = viecher[zufall]
        info.append(self.current.merkmale)
        #hier die Strings fuer die Info
        strinfo = info[0][0]
        strinfo2 = info[0][1]
        strinfo3 = info[0][2]
        strinfo4 = info[0][3]
        strinfo5 = info[0][4]
        strinfo6 = info[0][5]
        self.stralleinfo = strinfo + '.\n' + strinfo2 + '.\n' + strinfo3 + '.\n' + strinfo4 + '.\n' + strinfo5 + '.\n' + strinfo6 + '.'
        #hier der string aus der richtigen Antwort
        self.strrantwort = self.current.name
        #hier die Schleife fuer die falschen Antworten
        fantwort = []
        for aktuellesTier in viecher:
            self.fantwort.append(aktuellesTier.name)
        #hier die Strings aus fantwort
        zufallfantwort = random.randrange(0, len(self.fantwort) -1, 1)
        self.strfantwort = self.fantwort[zufallfantwort]
        self.fantwort.remove(self.fantwort[zufallfantwort])
        zufallfantwort = random.randrange(0, len(self.fantwort) -1, 1)
        self.strfantwort2 = self.fantwort[zufallfantwort]
        self.fantwort.remove(self.fantwort[zufallfantwort])
        zufallfantwort = random.randrange(0, len(self.fantwort) -1, 1)
        self.strfantwort3 = self.fantwort[zufallfantwort]
        self.fantwort.remove(self.fantwort[zufallfantwort])   

class TiereDerUmg():
    hbox1 = gtk.HBox(True, 1)
    vbox1 = gtk.VBox(True, 1)
    thauptbox = gtk.VBox(True, 1)
    buttoneuropa = gtk.Button("Europa")
    buttonasien = gtk.Button("Asien")
    buttonnordamer = gtk.Button("Amerika")
    buttonsuedamer = gtk.Button("Meere")
    buttonaust = gtk.Button("Australien")
    buttonafrika = gtk.Button("Afrika")
    label = gtk.Label("Waehle deine Region!")
    
    def set_label(self):
        self.buttoneuropa.set_label("Europa")
        self.buttonasien.set_label("Asien")
        self.buttonnordamer.set_label("Amerika")
        self.buttonsuedamer.set_label("Meere")
        self.buttonaust.set_label("Australien")
        self.buttonafrika.set_label("Afrika")
    
    def __init__(self):
        self.bildschirmFuellentier()
        
    def bildschirmFuellentier(self, data=None):
        #packen der boxen
        self.thauptbox.pack_start(self.vbox1)
        
        #hier der text
        label = gtk.Label("Waehle deinen Kontinent!")
        self.vbox1.pack_start(self.label) 
        #definieren der buttons
        self.hbox1.pack_start(self.buttoneuropa)
        
        self.hbox1.pack_start(self.buttonasien)
        
        self.hbox1.pack_start(self.buttonnordamer)
        
        self.hbox1.pack_start(self.buttonsuedamer)
        
        self.hbox1.pack_start(self.buttonaust)
        
        self.hbox1.pack_start(self.buttonafrika)
        
        self.vbox1.pack_start(self.hbox1)
        #zuweisen der funkts
        self.buttoneuropa.connect("clicked", self.europa)
        self.buttonasien.connect("clicked", self.asien)
        self.buttonnordamer.connect("clicked", self.nordamerika)
        self.buttonsuedamer.connect("clicked", self.suedamerika)
        self.buttonafrika.connect("clicked", self.afrika)
        self.buttonaust.connect("clicked", self.australien)
        #showen der objekte
        self.vbox1.show()
        self.hbox1.show()
        self.thauptbox.show()
        self.buttoneuropa.show()
        self.buttonasien.show()
        self.buttonnordamer.show()
        self.buttonsuedamer.show()
        self.buttonafrika.show()
        self.buttonaust.show()
        self.label.show()
        #Buttontext
        
        
    def europa(self, data=None):
        self.vbox1.destroy()
        self.hbox1.destroy()
        eur = kleuropa()
        
        eur.ehauptbox.show()

        self.thauptbox.pack_start(eur.ehauptbox)
        self.thauptbox.show()
        self.set_label()
        
    def asien(self, data=None):
        self.vbox1.destroy()
        self.hbox1.destroy()
        asi = klasien()
        
        asi.ehauptbox.show()
        
        self.thauptbox.pack_start(asi.ehauptbox)
        self.thauptbox.show()
        self.set_label()
        
    def australien(self, data=None):
        self.vbox1.destroy()
        self.hbox1.destroy()
        aus = klaustralien()
        self.thauptbox.pack_start(aus.ehauptbox)
        self.thauptbox.show()
        aus.ehauptbox.show()
        self.set_label()
    
    def nordamerika(self, data=None):
        self.vbox1.destroy()
        self.hbox1.destroy()
        nordamer = klnordamer()
        self.thauptbox.pack_start(nordamer.ehauptbox)
        self.thauptbox.show()
        nordamer.ehauptbox.show()
        self.set_label()
    
    def suedamerika(self, data=None):
        self.vbox1.destroy()
        self.hbox1.destroy()
        suedamer = klsuedamer()
        self.thauptbox.pack_start(suedamer.ehauptbox)
        self.thauptbox.show()
        suedamer.ehauptbox.show()
        self.set_label()
        
    def afrika(self, data=None):
        self.vbox1.destroy()
        self.hbox1.destroy()
        afr = klafrika()
        self.thauptbox.pack_start(afr.ehauptbox)
        self.thauptbox.show()
        afr.ehauptbox.show()
        self.set_label()
        
class klsuedamer():
    hbox1 = gtk.HBox()
    vbox1 = gtk.VBox()
    vbox2 = gtk.VBox(True, 1)
    ehauptbox = gtk.VBox(True, 1)
    beschriebenestier = quizfrage()
    Tier = Tier()
    tdu = TiereDerUmg()
    
    def __init__(self):
        self.beschriebenestier.setstringssuedamer()
        self.refreshanzeige()
 
    def refreshanzeige(self, data=None):
        #boxes
        self.ehauptbox.pack_start(self.vbox1)
        self.vbox1.show()
        self.hbox1.show()
        self.vbox2.show()
        #image 1
        self.image1 = gtk.Image()
        imagevar3 = 'tierbildermeer/' + str(zufallmeer) + '.jpg'
        self.image1.set_from_file(imagevar3)
        self.image1.show()
        self.vbox1.pack_start(self.image1)
        self.vbox1.pack_start(self.hbox1)
        #textbuf1
        hinweise_buffer = gtk.TextBuffer()
        hinweise_buffer.set_text(self.beschriebenestier.stralleinfosuedamer)
        hinweise_tag = gtk.TextTag()
        hinweise_tag.set_property("font", "Sans 10")
        hinweise_tag.set_property("wrap_mode", gtk.WRAP_WORD)
        hinweise_tag.set_property("pixels-above-lines",5)
        hinweise_tag.set_property("left-margin",5)
        start = hinweise_buffer.get_start_iter()
        end = hinweise_buffer.get_end_iter()
        hinweise_buffer.get_tag_table().add(hinweise_tag)
        hinweise_buffer.apply_tag(hinweise_tag, start, end)
        self.hinweisfeld = gtk.TextView(hinweise_buffer)
        self.hinweisfeld.set_editable(False)
        self.hinweisfeld.set_size_request(int(SIZE_X*0.8), int(SIZE_Y*0.25))
        self.hinweisfeld.show()
        self.hbox1.pack_start(self.hinweisfeld)
        self.hbox1.pack_start(self.vbox2)
        #button 1
        self.button1 = gtk.Button('Naechstes Tier')
        self.button1.connect("clicked", self.button_clicked)
        self.button1.show()
        self.vbox2.pack_start(self.button1)
        #button 2
        self.button2 = gtk.Button('Zurueck zum Startbildschirm')
        self.button2.connect("clicked", self.startbild)
        self.button2.show()
        self.vbox2.pack_start(self.button2)

  
    def button_clicked(self, data=None):
        self.vbox2.remove(self.button1)
        self.vbox2.remove(self.button2)
        self.hbox1.remove(self.hinweisfeld)
        self.hbox1.remove(self.vbox2)
        self.vbox1.remove(self.image1)
        self.vbox1.remove(self.hbox1)
        self.ehauptbox.remove(self.vbox1)
        self.beschriebenestier.setstringssuedamer()
        self.refreshanzeige()

 
    def startbild(self, data=None):
        self.ehauptbox.destroy()
        self.tdu.thauptbox.destroy()
        instanz = StartView()
 
    def destroy(self, data=None):
        self.window.destroy()
class klnordamer():
    hbox1 = gtk.HBox()
    vbox1 = gtk.VBox()
    vbox2 = gtk.VBox(True, 1)
    ehauptbox = gtk.VBox(True, 1)
    beschriebenestier = quizfrage()
    Tier = Tier()
    tdu = TiereDerUmg()
    
    def __init__(self):
        self.beschriebenestier.setstringsnordamer()
        self.refreshanzeige()
 
    def refreshanzeige(self, data=None):
        #boxes
        self.ehauptbox.pack_start(self.vbox1)
        self.vbox1.show()
        self.hbox1.show()
        self.vbox2.show()
        #image 1
        self.image1 = gtk.Image()
        imagevar3 = 'tierbilderamer/' + str(zufallamer) + '.jpg'
        self.image1.set_from_file(imagevar3)
        self.image1.show()
        self.vbox1.pack_start(self.image1)
        self.vbox1.pack_start(self.hbox1)
        #textbuf1
        hinweise_buffer = gtk.TextBuffer()
        hinweise_buffer.set_text(self.beschriebenestier.stralleinfonordamer)
        hinweise_tag = gtk.TextTag()
        hinweise_tag.set_property("font", "Sans 10")
        hinweise_tag.set_property("wrap_mode", gtk.WRAP_WORD)
        hinweise_tag.set_property("pixels-above-lines",5)
        hinweise_tag.set_property("left-margin",5)
        start = hinweise_buffer.get_start_iter()
        end = hinweise_buffer.get_end_iter()
        hinweise_buffer.get_tag_table().add(hinweise_tag)
        hinweise_buffer.apply_tag(hinweise_tag, start, end)
        self.hinweisfeld = gtk.TextView(hinweise_buffer)
        self.hinweisfeld.set_size_request(int(SIZE_X*0.8), int(SIZE_Y*0.25))
        self.hinweisfeld.set_editable(False)
        self.hinweisfeld.show()
        self.hbox1.pack_start(self.hinweisfeld)
        self.hbox1.pack_start(self.vbox2)
        #button 1
        self.button1 = gtk.Button('Naechstes Tier')
        self.button1.connect("clicked", self.button_clicked)
        self.button1.show()
        self.vbox2.pack_start(self.button1)
        #button 2
        self.button2 = gtk.Button('Zurueck zum Startbildschirm')
        self.button2.connect("clicked", self.startbild)
        self.button2.show()
        self.vbox2.pack_start(self.button2)

  
    def button_clicked(self, data=None):
        self.vbox2.remove(self.button1)
        self.vbox2.remove(self.button2)
        self.hbox1.remove(self.hinweisfeld)
        self.hbox1.remove(self.vbox2)
        self.vbox1.remove(self.image1)
        self.vbox1.remove(self.hbox1)
        self.ehauptbox.remove(self.vbox1)
        self.beschriebenestier.setstringsnordamer()
        self.refreshanzeige()

 
    def startbild(self, data=None):
        self.ehauptbox.destroy()
        self.tdu.thauptbox.destroy()
        instanz = StartView()
 
    def destroy(self, data=None):
        self.window.destroy()


        
class klaustralien():
    hbox1 = gtk.HBox()
    vbox1 = gtk.VBox()
    vbox2 = gtk.VBox(True, 1)
    ehauptbox = gtk.VBox(True, 1)
    beschriebenestier = quizfrage()
    Tier = Tier()
    tdu = TiereDerUmg()
    
    def __init__(self):
        self.beschriebenestier.setstringsaus()
        self.refreshanzeige()
 
    def refreshanzeige(self, data=None):
        #boxes
        self.ehauptbox.pack_start(self.vbox1)
        self.vbox1.show()
        self.hbox1.show()
        self.vbox2.show()
        #image 1
        self.image1 = gtk.Image()
        imagevar3 = 'tierbilderaust/' + str(zufallaust) + '.jpg'
        self.image1.set_from_file(imagevar3)
        self.image1.show()
        self.vbox1.pack_start(self.image1)
        self.vbox1.pack_start(self.hbox1)
        #textbuf1
        hinweise_buffer = gtk.TextBuffer()
        hinweise_buffer.set_text(self.beschriebenestier.stralleinfoaus)
        hinweise_tag = gtk.TextTag()
        hinweise_tag.set_property("font", "Sans 10")
        hinweise_tag.set_property("wrap_mode", gtk.WRAP_WORD)
        hinweise_tag.set_property("pixels-above-lines",5)
        hinweise_tag.set_property("left-margin",5)
        start = hinweise_buffer.get_start_iter()
        end = hinweise_buffer.get_end_iter()
        hinweise_buffer.get_tag_table().add(hinweise_tag)
        hinweise_buffer.apply_tag(hinweise_tag, start, end)
        self.hinweisfeld = gtk.TextView(hinweise_buffer)
        self.hinweisfeld.set_editable(False)
        self.hinweisfeld.show()
        self.hinweisfeld.set_size_request(int(SIZE_X*0.8), int(SIZE_Y*0.25))
        self.hbox1.pack_start(self.hinweisfeld)
        self.hbox1.pack_start(self.vbox2)
        #button 1
        self.button1 = gtk.Button('Naechstes Tier')
        self.button1.connect("clicked", self.button_clicked)
        self.button1.show()
        self.vbox2.pack_start(self.button1)
        #button 2
        self.button2 = gtk.Button('Zurueck zum Startbildschirm')
        self.button2.connect("clicked", self.startbild)
        self.button2.show()
        self.vbox2.pack_start(self.button2)

  
    def button_clicked(self, data=None):
        self.vbox2.remove(self.button1)
        self.vbox2.remove(self.button2)
        self.hbox1.remove(self.hinweisfeld)
        self.hbox1.remove(self.vbox2)
        self.vbox1.remove(self.image1)
        self.vbox1.remove(self.hbox1)
        self.ehauptbox.remove(self.vbox1)
        self.beschriebenestier.setstringsaus()
        self.refreshanzeige()

 
    def startbild(self, data=None):
        self.ehauptbox.destroy()
        self.tdu.thauptbox.destroy()
        instanz = StartView()
 
    def destroy(self, data=None):
        self.window.destroy()


        
class klasien():
    hbox1 = gtk.HBox()
    vbox1 = gtk.VBox()
    vbox2 = gtk.VBox(True, 1)
    ehauptbox = gtk.VBox(True, 1)
    beschriebenestier = quizfrage()
    Tier = Tier()
    tdu = TiereDerUmg()
    
    def __init__(self):
        self.beschriebenestier.setstringsasi()
        self.refreshanzeige()
 
    def refreshanzeige(self, data=None):
        #boxes
        self.ehauptbox.pack_start(self.vbox1)
        self.vbox1.show()
        self.hbox1.show()
        self.vbox2.show()
        #image 1
        self.image1 = gtk.Image()
        imagevar3 = 'tierbilderasi/' + str(zufallasi) + '.jpg'
        self.image1.set_from_file(imagevar3)
        self.image1.show()
        self.vbox1.pack_start(self.image1)
        self.vbox1.pack_start(self.hbox1)
        #textbuf1
        hinweise_buffer = gtk.TextBuffer()
        hinweise_buffer.set_text(self.beschriebenestier.stralleinfoasi)
        hinweise_tag = gtk.TextTag()
        hinweise_tag.set_property("font", "Sans 10")
        hinweise_tag.set_property("wrap_mode", gtk.WRAP_WORD)
        hinweise_tag.set_property("pixels-above-lines",5)
        hinweise_tag.set_property("left-margin",5)
        start = hinweise_buffer.get_start_iter()
        end = hinweise_buffer.get_end_iter()
        hinweise_buffer.get_tag_table().add(hinweise_tag)
        hinweise_buffer.apply_tag(hinweise_tag, start, end)
        self.hinweisfeld = gtk.TextView(hinweise_buffer)
        self.hinweisfeld.set_editable(False)
        self.hinweisfeld.show()
        self.hinweisfeld.set_size_request(int(SIZE_X*0.8), int(SIZE_Y*0.25))
        self.hbox1.pack_start(self.hinweisfeld)
        self.hbox1.pack_start(self.vbox2)
        #button 1
        self.button1 = gtk.Button('Naechstes Tier')
        self.button1.connect("clicked", self.button_clicked)
        self.button1.show()
        self.vbox2.pack_start(self.button1)
        #button 2
        self.button2 = gtk.Button('Zurueck zum Startbildschirm')
        self.button2.connect("clicked", self.startbild)
        self.button2.show()
        self.vbox2.pack_start(self.button2)

  
    def button_clicked(self, data=None):
        self.vbox2.remove(self.button1)
        self.vbox2.remove(self.button2)
        self.hbox1.remove(self.hinweisfeld)
        self.hbox1.remove(self.vbox2)
        self.vbox1.remove(self.image1)
        self.vbox1.remove(self.hbox1)
        self.ehauptbox.remove(self.vbox1)
        self.beschriebenestier.setstringsasi()
        self.refreshanzeige()

 
    def startbild(self, data=None):
        self.ehauptbox.destroy()
        self.tdu.thauptbox.destroy()
        instanz = StartView()
 
    def destroy(self, data=None):
        self.window.destroy()


        
class klafrika():
    hbox1 = gtk.HBox()
    vbox1 = gtk.VBox()
    vbox2 = gtk.VBox(True, 1)
    ehauptbox = gtk.VBox(True, 1)
    beschriebenestier = quizfrage()
    Tier = Tier()
    tdu = TiereDerUmg()
    
    def __init__(self):
        self.beschriebenestier.setstringsafr()
        self.refreshanzeige()
 
    def refreshanzeige(self, data=None):
        #boxes
        self.ehauptbox.pack_start(self.vbox1)
        self.vbox1.show()
        self.hbox1.show()
        self.vbox2.show()
        #image 1
        self.image1 = gtk.Image()
        imagevar3 = 'tierbilderafr/' + str(zufallafr) + '.jpg'
        self.image1.set_from_file(imagevar3)
        self.image1.show()
        self.vbox1.pack_start(self.image1)
        self.vbox1.pack_start(self.hbox1)
        #textbuf1
        hinweise_buffer = gtk.TextBuffer()
        hinweise_buffer.set_text(self.beschriebenestier.stralleinfoafr)
        hinweise_tag = gtk.TextTag()
        hinweise_tag.set_property("font", "Sans 10")
        hinweise_tag.set_property("wrap_mode", gtk.WRAP_WORD)
        hinweise_tag.set_property("pixels-above-lines",5)
        hinweise_tag.set_property("left-margin",5)
        start = hinweise_buffer.get_start_iter()
        end = hinweise_buffer.get_end_iter()
        hinweise_buffer.get_tag_table().add(hinweise_tag)
        hinweise_buffer.apply_tag(hinweise_tag, start, end)
        self.hinweisfeld = gtk.TextView(hinweise_buffer)
        self.hinweisfeld.set_editable(False)
        self.hinweisfeld.show()
        self.hbox1.pack_start(self.hinweisfeld)
        self.hbox1.pack_start(self.vbox2)
        self.hinweisfeld.set_size_request(int(SIZE_X*0.8), int(SIZE_Y*0.25))
        #button 1
        self.button1 = gtk.Button('Naechstes Tier')
        self.button1.connect("clicked", self.button_clicked)
        self.button1.show()
        self.vbox2.pack_start(self.button1)
        #button 2# -*- coding: utf-8 -*-
        self.button2 = gtk.Button('Zurueck zum Startbildschirm')
        self.button2.connect("clicked", self.startbild)
        self.button2.show()
        self.vbox2.pack_start(self.button2)

  
    def button_clicked(self, data=None):
        self.vbox2.remove(self.button1)
        self.vbox2.remove(self.button2)
        self.hbox1.remove(self.hinweisfeld)
        self.hbox1.remove(self.vbox2)
        self.vbox1.remove(self.image1)
        self.vbox1.remove(self.hbox1)
        self.ehauptbox.remove(self.vbox1)
        self.beschriebenestier.setstringsafr()
        self.refreshanzeige()

 
    def startbild(self, data=None):
        self.ehauptbox.destroy()
        self.tdu.thauptbox.destroy()
        instanz = StartView()
 
    def destroy(self, data=None):
        self.window.destroy()

class kleuropa():
    hbox1 = gtk.HBox()
    vbox1 = gtk.VBox()
    vbox2 = gtk.VBox(True, 1)
    ehauptbox = gtk.VBox(True, 1)
    beschriebenestier = quizfrage()
    Tier = Tier()
    tdu = TiereDerUmg()
    
    def __init__(self):
        self.beschriebenestier.setstringseur()
        self.refreshanzeige()
 
    def refreshanzeige(self, data=None):
        #boxes
        self.ehauptbox.pack_start(self.vbox1)
        self.vbox1.show()
        self.hbox1.show()
        self.vbox2.show()
        #image 1
        self.image1 = gtk.Image()
        imagevar3 = 'tierbildereur/' + str(zufalleur) + '.jpg'
        self.image1.set_from_file(imagevar3)
        self.image1.show()
        self.vbox1.pack_start(self.image1)
        self.vbox1.pack_start(self.hbox1)
        #textbuf1
        hinweise_buffer = gtk.TextBuffer()
        hinweise_buffer.set_text(self.beschriebenestier.stralleinfoeur)
        hinweise_tag = gtk.TextTag()
        hinweise_tag.set_property("font", "Sans 10")
        hinweise_tag.set_property("wrap_mode", gtk.WRAP_WORD)
        hinweise_tag.set_property("pixels-above-lines",5)
        hinweise_tag.set_property("left-margin",5)
        start = hinweise_buffer.get_start_iter()
        end = hinweise_buffer.get_end_iter()
        hinweise_buffer.get_tag_table().add(hinweise_tag)
        hinweise_buffer.apply_tag(hinweise_tag, start, end)
        self.hinweisfeld = gtk.TextView(hinweise_buffer)
        self.hinweisfeld.set_editable(False)
        self.hinweisfeld.set_size_request(int(SIZE_X*0.8), int(SIZE_Y*0.25))
        self.hinweisfeld.show()
        self.hbox1.pack_start(self.hinweisfeld)
        self.hbox1.pack_start(self.vbox2)
        #button 1
        self.button1 = gtk.Button('Naechstes Tier')
        self.button1.connect("clicked", self.button_clicked)
        self.button1.show()
        self.vbox2.pack_start(self.button1)
        #button 2
        self.button2 = gtk.Button('Zurueck zum Startbildschirm')
        self.button2.connect("clicked", self.startbild)
        self.button2.show()
        self.vbox2.pack_start(self.button2)

  
    def button_clicked(self, data=None):
        self.vbox2.remove(self.button1)
        self.vbox2.remove(self.button2)
        self.hbox1.remove(self.hinweisfeld)
        self.hbox1.remove(self.vbox2)
        self.vbox1.remove(self.image1)
        self.vbox1.remove(self.hbox1)
        self.ehauptbox.remove(self.vbox1)
        self.beschriebenestier.setstringseur()
        self.refreshanzeige()

 
    def startbild(self, data=None):
        self.ehauptbox.destroy()
        self.tdu.thauptbox.destroy()
        instanz = StartView()
 
    def destroy(self, data=None):
        self.window.destroy()

class quizView():
    aktuellequizfrage = quizfrage()
    Tier = Tier()
    #Elemente des Views "Quiz"
    qhauptbox = gtk.HBox(True, 1)
    hbox1 = gtk.HBox(True, 1)
    hbox2 = gtk.HBox(True, 1)
    hbox3 = gtk.HBox(True, 1)
    hbox4 = gtk.HBox(True, 1)
    vbox1 = gtk.VBox(True, 1)
    vbox2 = gtk.VBox(True, 1)
    vbox3 = gtk.VBox(False, 1)
    vbox4 = gtk.VBox(True, 1)
    score = 0
    time = time.asctime()
    
    
    def __init__(self,parent):
        self.parent = parent        
        self.Tier.setzufall()
        self.aktuellequizfrage.setstrings()
        self.refreshanzeige()
        
    
    def destroy(self, data=None):
        self.qhauptbox.destroy()
            
    def buttonfalsch(self, data=None):
        self.r_f_image.set_from_file("Falsch.png")
        self.button6 = gtk.Button("Leider Falsch, zurück zum Startbildschirm")
        self.button6.show()
        self.button1.hide()
        self.button2.hide()
        self.button3.hide()
        self.button4.hide()
        
    def buttonrichtig(self, data=None):
        self.score = self.score + 1
        self.r_f_image.set_from_file("Richtig.png")
        self.button5.show()
        self.button6.show()
        self.button1.hide()
        self.button2.hide()
        self.button3.hide()
        self.button4.hide()

    def buttonstartbild(self, data=None):
        fobj = open("highscore.txt", "a") 
        print >> fobj, 'Dein Score:  ' + str(self.score) + '  am  ' + self.time 
        fobj.close()
        self.qhauptbox.destroy()
        instanz = StartView()

    def buttonnaechst(self, data=None):
        self.Tier.setzufall()
        self.aktuellequizfrage.setstrings()
        self.vbox3.remove(self.button6)
        self.vbox3.remove(self.button5)
        self.vbox3.remove(self.labelsc)
        self.hbox4.remove(self.vbox3)
        self.hbox4.remove(self.r_f_image)
        self.vbox2.remove(self.hbox4)
        self.hbox1.remove(self.vbox2)
        self.hbox3.remove(self.button4)
        self.hbox3.remove(self.button3)
        self.vbox4.remove(self.hbox3)
        self.hbox2.remove(self.button2)
        self.hbox2.remove(self.button1)
        self.vbox4.remove(self.hbox2)
        self.vbox1.remove(self.vbox4)
        self.vbox1.remove(self.hinweisfeld)
        self.hbox1.remove(self.vbox1)
        self.qhauptbox.remove(self.hbox1)
        self.hbox1.destroy()
        self.refreshanzeige()

            
    def refreshanzeige(self, data=None):
        self.hbox1.show()
        self.hbox2.show()
        self.hbox3.show()
        self.hbox4.show()
        self.vbox1.show()
        self.vbox2.show()
        self.vbox3.show()
        self.vbox4.show()
        # das Hinweis-TextView
        hinweise_buffer = gtk.TextBuffer()
        hinweise_buffer.set_text(self.aktuellequizfrage.stralleinfo)
        hinweise_tag = gtk.TextTag()
        
        hinweise_tag.set_property("font", "Sans 12")
        hinweise_tag.set_property("wrap_mode", gtk.WRAP_WORD)
        hinweise_tag.set_property("pixels-above-lines",10)
        hinweise_tag.set_property("left-margin",10)
        start = hinweise_buffer.get_start_iter()
        end = hinweise_buffer.get_end_iter()
        hinweise_buffer.get_tag_table().add(hinweise_tag)
        hinweise_buffer.apply_tag(hinweise_tag, start, end)

        self.hinweisfeld = gtk.TextView(hinweise_buffer)
        self.hinweisfeld.set_editable(False)
        self.hinweisfeld.show()
        
        
        #hier der erste Button in der 2. self.vbox
        self.button1 = gtk.Button(self.aktuellequizfrage.strfantwort)
        self.button1.connect("clicked", self.buttonfalsch)
        self.button1.show()
        #hier der 2. button in der 2. self.vbox
        self.button2 = gtk.Button(self.aktuellequizfrage.strfantwort2)
        self.button2.connect("clicked", self.buttonfalsch)
        self.button2.show()
        #hier der 3. button in der 3.self.vbox
        self.button3 = gtk.Button(self.aktuellequizfrage.strfantwort3)
        self.button3.connect("clicked", self.buttonfalsch)
        self.button3.show()
        #hier der 4.button in der 3. self.vbox
        self.button4 = gtk.Button(self.aktuellequizfrage.strrantwort)
        self.button4.connect("clicked", self.buttonrichtig)
        self.button4.show()
        #hier der 5. button in der 5.self.vbox --> rechte Seite oben oben
        self.button5 = gtk.Button('Nächste Frage!')
        self.button5.connect("clicked", self.buttonnaechst)
        #hier der 6.button in der 5. self.vbox --> rechte Seite oben unten
        self.button6 = gtk.Button('Zurück zum Startbildschirm')
        self.button6.connect("clicked", self.buttonstartbild)
        self.button6.show()
        #hier das Feld, das "Richtig" oder "Falsch" anzeigt in vbox6image = gtk.Image()
        self.r_f_image = gtk.Image()
        self.r_f_image.show()
        
        self.qhauptbox.pack_start(self.hbox1)
        self.hbox1.pack_start(self.vbox1)
        self.vbox1.pack_start(self.hinweisfeld)
        self.vbox1.pack_start(self.vbox4)
        self.vbox4.pack_start(self.hbox2)
        buttonarray = [self.button1, self.button2, self.button3, self.button4]
        zufallszahl1 = random.randrange(0, len(buttonarray), 1)
        self.hbox2.pack_start(buttonarray[zufallszahl1])
        buttonarray.remove(buttonarray[zufallszahl1])
        zufallszahl2 = random.randrange(0, len(buttonarray), 1)
        self.hbox2.pack_start(buttonarray[zufallszahl2])
        buttonarray.remove(buttonarray[zufallszahl2])
        self.vbox4.pack_start(self.hbox3)
        zufallszahl3 = random.randrange(0, len(buttonarray), 1)
        self.hbox3.pack_start(buttonarray[zufallszahl3])
        buttonarray.remove(buttonarray[zufallszahl3])
        zufallszahl4 = random.randrange(0, len(buttonarray), 1)
        self.hbox3.pack_start(buttonarray[zufallszahl4])
        buttonarray.remove(buttonarray[zufallszahl4])
        
        self.labelsc = gtk.Label()
        inputLabelsc = '<span size="25000">'+ 'Dein aktueller Score: ' + str(self.score) + '</span>'
        self.labelsc.set_markup(inputLabelsc)
        self.labelsc.show()
        
        self.hbox1.pack_start(self.vbox3)
        self.vbox3.pack_start(self.labelsc)
        #~ self.vbox3.pack_start(tierbild)
        self.vbox3.pack_start(self.r_f_image)
        self.vbox3.pack_start(self.hbox4)
        self.hbox4.pack_start(self.button5)
        self.hbox4.pack_start(self.button6)
        
class Entdecken():
    hbox1 = gtk.HBox(False)
    vbox1 = gtk.VBox(False)
    vbox2 = gtk.VBox(True, 1)
    ehauptbox = gtk.VBox(False)
    beschriebenestier = quizfrage()
    Tier = Tier()
 
    def __init__(self):
        self.beschriebenestier.setstringsent()
        self.refreshanzeige()
        self.addbox()
        
    def addbox(self, data=None):
        self.ehauptbox.pack_start(self.vbox1)
        self.vbox1.pack_start(self.hbox1)
        self.vbox1.show()
        self.hbox1.show()
        self.vbox2.show()
 
    def refreshanzeige(self, data=None):
        #textbuf1
        hinweise_buffer = gtk.TextBuffer()
        hinweise_buffer.set_text(self.beschriebenestier.stralleinfo)
        hinweise_tag = gtk.TextTag()
        hinweise_tag.set_property("font", "Sans 10")
        hinweise_tag.set_property("wrap_mode", gtk.WRAP_WORD)
        hinweise_tag.set_property("pixels-above-lines",5)
        hinweise_tag.set_property("left-margin",5)
        start = hinweise_buffer.get_start_iter()
        end = hinweise_buffer.get_end_iter()
        hinweise_buffer.get_tag_table().add(hinweise_tag)
        hinweise_buffer.apply_tag(hinweise_tag, start, end)
        self.hinweisfeld = gtk.TextView(hinweise_buffer)
        self.hinweisfeld.set_editable(False)
        self.hinweisfeld.set_size_request(int(SIZE_X*0.8), int(SIZE_Y*0.25))
        self.hinweisfeld.show()
        self.hbox1.pack_start(self.hinweisfeld)
        #vbox2
        self.hbox1.pack_start(self.vbox2)
        #button 1
        self.button1 = gtk.Button('Naechstes Tier')
        self.button1.connect("clicked", self.button_clicked)
        self.button1.show()
        self.vbox2.pack_start(self.button1)
        #button 2
        self.button2 = gtk.Button('Zurueck zum Startbildschirm')
        self.button2.connect("clicked", self.startbild)
        self.button2.show()
        self.vbox2.pack_start(self.button2)
        #image 1
        self.image1 = gtk.Image()
        imagevar3 = 'tierbilder/' + str(zufall) + '.jpg'
        self.image1.set_from_file(imagevar3)
        self.image1.show()
        self.vbox1.pack_start(self.image1)
  
    def button_clicked(self, data=None):
        self.vbox1.remove(self.hbox1)
        self.vbox1.remove(self.image1)
        self.hbox1.remove(self.hinweisfeld)
        #~ self.hbox1.remove(self.label2)
        self.hbox1.remove(self.vbox2)
        self.vbox2.remove(self.button1)
        self.vbox2.remove(self.button2)
        
        self.beschriebenestier.setstringsent()
        self.refreshanzeige()
        self.addbox()
 
    def startbild(self, data=None):
        self.ehauptbox.destroy()
        instanz = StartView()
 
    def destroy(self, data=None):
        self.window.destroy()

class Suche():
    entry = gtk.Entry()
    dicti = {"giraffe" : 0, "feldhase" : 1, "hauskatze" : 2, "hund" : 3, "elefant" : 4, "huhn" : 5, "tiger" : 6, "loewe" : 7, "nilpferd" : 8, "nashorn" : 9, "kuh" : 10, "eichhoernchen" :11, "feldmaus" :12, "delfin" : 13, "streifenhoernchen" : 14, "ameisenbaer" : 15, "braunbaer" : 16, "lama" : 17, "emu" : 18, "strauss" : 19, "orca" : 20, "lachs" : 21, "oktopus" : 22, "seepferdchen" : 23, "schwertfisch" : 24, "regenwurm" : 25, "natter" : 26, "luchs" : 27, "leopard" : 28, "hai" : 29, "hummer" : 30, "kakerlake" : 31, "biber" : 32, "otter" : 33, "pferd" : 34, "meerschweinchen" : 35, "blauwal" : 36, "kaenguru" : 37, "esel" : 38, "fuchs" : 39, "wolf" : 40, "schwein" : 41, "wildschwein" : 42, "maulwurf" : 43, "koala" : 44, "panda" : 45, "gepard" : 46, "gecko" : 47, "salamander" : 48, "chamaeleon" : 49, "kroete" : 50, "clownfisch" : 51, "guerteltier" : 52, "murmeltier" : 53, "kobra" : 54, "nasenbaer" : 55, "goldfisch" : 56, "eisbaer" : 57, "zebra" : 58, "pelikan" : 59, "schmetterling" : 60, "biene" : 61, "storch" : 62, "schildkroete" : 63, "eule" : 64, "frosch" : 65, "bueffel" : 66, "stinkwanze" : 67, "ente" : 68, "kolibri" : 69, "vogelspinne" : 70, "viper" : 71, "klapperschlange" : 72, "hummel" : 73, "kiwi" : 74, "pinguin" : 75, "piranha" : 76}
    image1 = gtk.Image()
    daten = quizfrage()
    ehauptbox = gtk.HBox()
    hbox = gtk.HBox(False, 5)
    hbox1 = gtk.HBox(True, 1)
    hbox2 = gtk.HBox()
    hbox3 = gtk.HBox()
    vbox = gtk.VBox(False , 0)
    vbox1 = gtk.VBox()
    vbox2 = gtk.VBox()
    fixed = gtk.Fixed()
    biodivhase = gtk.Image()
    
    
    def __init__(self):
        self.refreshanzeige()
     
    def setstringssuche(self, data=None):
        info = []
        self.current = viecher[suchtier]
        info.append(self.current.merkmale)
        info.append(self.current.name)
        #hier die Strings fuer die Info
        strinfo = info[0][0]
        strinfo2 = info[0][1]
        strinfo3 = info[0][2]
        strinfo4 = info[0][3]
        strinfo5 = info[0][4]
        strinfo6 = info[0][5]
        strname = info[1]
        self.stralleinfosuche = strname + '.\n' + strinfo + '.\n' + strinfo2 + '.\n' + strinfo3 + '.\n' + strinfo4 + '.\n' + strinfo5 + '.\n' + strinfo6 + '.'
        
    def searchbuttonclicked(self, data=None):
        self.text = self.entry.get_text()
        textLow = self.text.lower()
        
        if textLow in self.dicti:
            self.suche()
        else:
            self.abbaufromsearch()
            self.refreshanzeige()
       
    def refreshanzeige(self):
        self.schriftbio = gtk.Image()
        self.ehauptbox.pack_start(self.vbox1)
        self.vbox1.pack_start(self.hbox3)
        self.hbox3.pack_start(self.entry)
        self.hbox3.pack_start(self.schriftbio)
        self.button = gtk.Button('Suche')
        self.button.connect("clicked", self.searchbuttonclicked)
        self.button.show()
        self.button2 = gtk.Button("Zurueck zum Startbildschirm")
        self.button2.connect("clicked", self.startbild)
        self.button2.show()
        self.vbox1.pack_start(self.hbox1)
        self.hbox1.pack_start(self.button)
        self.biodivhase.set_from_file('BioDivColour.png')
        self.biodivhase.show()
        self.pixbuf = gtk.gdk.pixbuf_new_from_file_at_size('bioheadernew.png', 100, 100)
        self.schriftbio.set_from_pixbuf(self.pixbuf)
        self.schriftbio.show()
        self.hbox1.pack_start(self.biodivhase)
        self.hbox1.pack_start(self.button2)
        self.hbox1.show()
        self.vbox1.show()
        self.hbox3.show()
        self.entry.show()
        self.entry.set_size_request(int(SIZE_X*0.72), 40)
        self.ehauptbox.show()

    def startbild(self, data=None):
        self.ehauptbox.destroy()
        instanz = StartView()
    
    def suche(self, data=None):
        self.abbaufromsearch()     
        self.entry.show()        
        global suchtier
        textLow = self.text.lower()
        if textLow in self.dicti:
            suchtier = self.dicti[textLow]
            self.setstringssuche()
            self.text = self.entry.get_text()
            self.hinweise_buffer = gtk.TextBuffer()
            self.hinweise_buffer.set_text(self.stralleinfosuche)
            self.hinweise_tag = gtk.TextTag()
            self.hinweise_tag.set_property("font", "Sans 11")
            self.hinweise_tag.set_property("wrap_mode", gtk.WRAP_WORD)
            self.hinweise_tag.set_property("pixels-above-lines",10)
            self.hinweise_tag.set_property("left-margin",10)
            self.start = self.hinweise_buffer.get_start_iter()
            self.end =self.hinweise_buffer.get_end_iter()
            self.hinweise_buffer.get_tag_table().add(self.hinweise_tag)
            self.hinweise_buffer.apply_tag(self.hinweise_tag, self.start, self.end)
            self.hinweisfeld = gtk.TextView(self.hinweise_buffer)
            self.hinweisfeld.set_editable(False)
            self.hinweisfeld.set_size_request(int(SIZE_X*0.28), int(SIZE_Y*0.7))
            self.hinweisfeld.show()
            self.imagevar = "tierbilder/" + str(suchtier) + ".jpg"
            self.pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(self.imagevar, int(SIZE_Y*0.87), int(SIZE_Y*0.87))
            self.image1.set_from_pixbuf(self.pixbuf)
            self.image1.show()
            self.backButton = gtk.Button("Zurueck zum Homebildschrim")
            self.backButton.show()
            self.backButton.connect("clicked", self.home)
            self.backButton.set_size_request(220, 40)
            self.searchButton = gtk.Button('Suche')
            self.searchButton.connect("clicked", self.suche2)
            self.searchButton.show()
            self.searchButton.set_size_request(80, 40)
        
            self.fixed.put(self.entry, 20, 20)
            self.fixed.put(self.searchButton, int(SIZE_X*0.76), 22)
            self.fixed.put(self.image1, int(SIZE_X*0.03), 95)
            self.fixed.put(self.hinweisfeld, int(SIZE_X*0.70), 95)
            self.fixed.put(self.backButton, 20, int(SIZE_Y*0.82))
            self.fixed.show()
            self.ehauptbox.pack_start(self.fixed)
            
        else:
            self.abbaufromergebnis()
            self.fixed.remove(self.entry)
            self.fixed.remove(self.entry)
            self.ehauptbox.remove(self.fixed)
            self.refreshanzeige()

        
    def suche2(self, data=None):
        self.abbaufromergebnis()
        self.entry.show()
        global suchtier
        self.text = self.entry.get_text()
        textLow = self.text.lower()
        
        if textLow in self.dicti:
            suchtier = self.dicti[textLow]
            self.setstringssuche()
            self.text = self.entry.get_text()
            self.hinweise_buffer = gtk.TextBuffer()
            self.hinweise_buffer.set_text(self.stralleinfosuche)
            self.hinweise_tag = gtk.TextTag()
            self.hinweise_tag.set_property("font", "Sans 11")
            self.hinweise_tag.set_property("wrap_mode", gtk.WRAP_WORD)
            self.hinweise_tag.set_property("pixels-above-lines",10)
            self.hinweise_tag.set_property("left-margin",10)
            self.start = self.hinweise_buffer.get_start_iter()
            self.end =self.hinweise_buffer.get_end_iter()
            self.hinweise_buffer.get_tag_table().add(self.hinweise_tag)
            self.hinweise_buffer.apply_tag(self.hinweise_tag, self.start, self.end)
            self.hinweisfeld = gtk.TextView(self.hinweise_buffer)
            self.hinweisfeld.set_editable(False)
            self.hinweisfeld.set_size_request(int(SIZE_X*0.28), int(SIZE_Y*0.7))
            self.hinweisfeld.show()
            self.imagevar = "tierbilder/" + str(suchtier) + ".jpg"
            self.pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(self.imagevar, int(SIZE_Y*0.87), int(SIZE_Y*0.87))
            self.image1.set_from_pixbuf(self.pixbuf)
            self.image1.show()
            self.backButton = gtk.Button("Zurueck zum Homebildschrim")
            self.backButton.show()
            self.backButton.connect("clicked", self.home)
            self.backButton.set_size_request(220, 40)
            self.searchButton = gtk.Button('Suche')
            self.searchButton.connect("clicked", self.suche2)
            self.searchButton.show()
            self.searchButton.set_size_request(80, 40)
        
            self.fixed.put(self.image1, int(SIZE_X*0.03), 95)
            self.fixed.put(self.hinweisfeld, int(SIZE_X*0.70), 95)
            self.fixed.put(self.backButton, 20, int(SIZE_Y*0.82))
            self.fixed.show()
            
        else:
            self.abbaufromergebnis()
            self.fixed.remove(self.entry)
            self.fixed.remove(self.entry)
            self.ehauptbox.remove(self.fixed)
            self.refreshanzeige()



    def abbaufromsearch(self, data=None):
        self.hbox3.remove(self.entry)
        self.hbox3.remove(self.schriftbio)
        self.vbox1.remove(self.hbox3)
        self.hbox1.remove(self.button)
        self.hbox1.remove(self.button2)
        self.hbox1.remove(self.biodivhase)
        self.vbox1.remove(self.hbox1)
        self.ehauptbox.remove(self.vbox1)
        
        
    def abbaufromergebnis(self, data=None):
        self.fixed.remove(self.backButton)
        self.fixed.remove(self.image1)
        self.fixed.remove(self.hinweisfeld)



    def home(self, data=None):
        self.fixed.remove(self.entry)
        self.fixed.remove(self.searchButton)
        self.fixed.remove(self.image1)
        self.fixed.remove(self.backButton)
        self.fixed.remove(self.hinweisfeld)
        self.ehauptbox.remove(self.fixed)
        self.ehauptbox.destroy
        self.startbild()


# Klasse StartView
class StartView():
    hauptbox = gtk.VBox(True, 1)
    hbox = gtk.HBox(True,1)
    vbox = gtk.VBox(False)
    vbox2 = gtk.VBox(False)
    
    def quizstart(self, widget, data=None):
        self.hbox.destroy()
        self.vbox2.destroy()
        self.vbox.destroy()
        quiz = quizView(StartView)
        quiz.qhauptbox.show()
        self.hauptbox.pack_start(quiz.qhauptbox)
        self.hauptbox.show()
    
    def histart(self, widget):
        self.hbox.destroy()
        self.vbox2.destroy()
        self.vbox.destroy()
        
        ent = Highscore()
        Highscore.vbox.show()
        
        self.hauptbox.pack_start(ent.vbox)
        self.hauptbox.show()
    
        
    def entstart(self, widget, date=None):
        self.hbox.destroy()
        self.vbox.destroy()
        
        ent = Entdecken()
        Entdecken.ehauptbox.show()
        
        self.hauptbox.pack_start(ent.ehauptbox)
        self.hauptbox.show
        
    def tierstart(self, widget, date=None):
        self.hbox.destroy()
        self.vbox2.destroy()
        self.vbox.destroy()
        
        tdu = TiereDerUmg()
        
        self.hauptbox.pack_start(tdu.thauptbox)
        self.hauptbox.show()
        
    def suchestart(self, widget):
        self.hbox.destroy()
        self.vbox2.destroy()
        self.vbox.destroy()
        
        suche = Suche()
        
        self.hauptbox.pack_start(suche.ehauptbox)
        self.hauptbox.show()        

    def destroy(self, widget, data=None):
        self.hauptbox.destroy()

    def bildschirmFuellen(self):


        bioheader = gtk.Image()
        
        tiereumgebungbild = gtk.Image()
        
        entdeckenbild = gtk.Image()
        
        spielbild = gtk.Image()
        
        findenbild = gtk.Image()
      
        labelleer1 = gtk.Label(' ')
        labelleer1.show()
        
        labelleer2 = gtk.Label(' ')
        labelleer2.show()
        
        tiereumgebungbutton = gtk.Button()
        tiereumgebungbutton.set_image(tiereumgebungbild)
        tiereumgebungbutton.get_image()
        
        hibutton = gtk.Button("Highscores")
        hibutton.connect("clicked", self.histart)
        hibutton.show()
        
        entdeckenbutton = gtk.Button()
        entdeckenbutton.set_image(entdeckenbild)
        entdeckenbutton.get_image()
        
        spielbutton = gtk.Button()
        spielbutton.set_image(spielbild)
        spielbutton.get_image()
        
        findenbutton = gtk.Button()
        findenbutton.set_image(findenbild)
        findenbutton.get_image()
        
        self.hbox.pack_start(self.vbox)
        im = gtk.Image()
        spielbild.set_from_file('puzzle.png')
        spielbild.show()
                
        spielbutton.connect("clicked", self.quizstart)
        spielbutton.show()
        self.vbox.pack_start(spielbutton)
        
        
        self.vbox.pack_start(labelleer1)
                
        tiereumgebungbild.set_from_file('erde.png')
        tiereumgebungbild.show()
        
        tiereumgebungbutton.connect("clicked", self.tierstart)
        tiereumgebungbutton.show()
        self.vbox.pack_start(tiereumgebungbutton)
        
        
        #~ bioheader.set_from_file('BioDiv.png')
        #~ bioheader.show()
        self.hbox.pack_start(hibutton)
        self.hbox.pack_start(self.vbox2)
        
        entdeckenbild.set_from_file('Suche.png')
        entdeckenbild.show()

    
        entdeckenbutton.connect("clicked", self.entstart)
        entdeckenbutton.show()
        self.vbox2.pack_start(entdeckenbutton)
        
        self.vbox2.pack_start(labelleer2)
        
        findenbild.set_from_file('Zeichnung.png')
        findenbild.show()

        
        findenbutton.connect("clicked", self.suchestart)
        findenbutton.show()
        self.vbox2.pack_start(findenbutton)
        
        #hier werden die boxen zum window geaddet
        self.hauptbox.pack_start(self.hbox)
        self.hauptbox.pack_start(self.vbox)
        self.hauptbox.pack_start(self.vbox2)

        #hier werden die boxen geshowed 
        self.vbox.show()
        self.hbox.show()
        self.vbox2.show()
    
    def __init__(self):
        self.bildschirmFuellen()


