#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs 
import xml.etree.ElementTree as ET

def parseMain(main):
	xpath = ".//data"
	mainParts = main.findall(xpath)

	for part in mainParts:
		xpath = "./label"
		found = main.find(xpath)
		if found:
			mainPartName = found.text
			print mainPartName

#dom = parse('d:\\github\\mensappserver\speiseplan.xml') # parse an XML file by name

fileObj = codecs.open('d:\\github\\mensappserver\speiseplan.xml', "r", errors = "replace") 
encoded = fileObj.read() # Returns a Unicode string from the UTF-8 bytes in the file 
root = ET.fromstring(encoded)

date = "20151007"
mensaId = "1"

mensaSet = None
mensa = None

# Top-level elements
xpath = "./artikel[@date='{0}']".format(date)
mensa = root.find(xpath)

xpath = ".//standort[@id='standort-{0}']".format(mensaId)
place = mensa.find(xpath)

xpath = "./label"
mensaName = place.find(xpath).text
xpath = "./geschlossen"
isClosed = place.find(xpath).text == "1"

xpath = ".//theke"
menus = mensa.findall(xpath)

print "\n"
print mensaName
print "==="

for menu in menus:
	xpath = "./label"
	menuName = menu.find(xpath).text
	print "\n" + menuName
	
	xpath = "./geschlossen"
	isMenuClosed = menu.find(xpath).text == "1"
	
	if isMenuClosed:
		print "- Leider geschlossen -"
	
	xpath = ".//mahlzeit"
	foods = menu.findall(xpath)
	
	for food in foods:
		xpath = ".//price"
		prices = food.findall(xpath)		
		print "Student: {0}, Mitarbeiter: {1}, Gast: {2}".format(prices[0].get("data"), prices[1].get("data"), prices[2].get("data"))
		
		xpath = "./titel"
		foodName = food.find(xpath).text
		
		xpath = "./beschreibung"
		foodDescription = food.find(xpath).text
		
		print u"{0} - {1}".format(foodName, foodDescription)
		
		xpath = "./vorspeise"
		starter = food.find(xpath).text

		xpath = "./hauptkomponente"
		main = food.find(xpath)
		parseMain(main)
		
		xpath = "./beilage1"
		side1 = food.find(xpath)
		xpath = "./beilage2"
		side2 = food.find(xpath)
		
		sides = [side1, side2]
		for side in sides:
			parseMain(main)