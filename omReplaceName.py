#MenuTitle: Replace Name in Masters and Exports
# -*- coding: utf-8 -*-
# Code by Olli Meier, January 2022
__doc__="""
Rename your font by replacing name parts in different locations like various custom parameters.
"""

from GlyphsApp import *

font_obj = Glyphs.font

old_name = 'Compact'
new_name = 'Compressed'

def replace_name(obj):
	if not isinstance(obj, str):
		return
	print('old object name: ', obj)
	new = obj.replace(old_name, new_name)
	print('new object name: ', new)
	return new

#change area 'Font'
r = replace_name(font_obj.familyName)
if r is not None:
	font_obj.familyName = r
r = replace_name(font_obj.compatibleFullName)
if r is not None:
	font_obj.compatibleFullName = r
r = replace_name(font_obj.description)
if r is not None:
	font_obj.description = r
r = replace_name(font_obj.trademark)
if r is not None:
	font_obj.trademark = r
r = replace_name(font_obj.copyright)
if r is not None:
	font_obj.copyright = r
r = replace_name(font_obj.license)
if r is not None:
	font_obj.license = r

for master in font_obj.masters:
	r = replace_name(master.name)
	if r is not None:
		master.name = r
	
for instance in font_obj.instances:
	r = replace_name(instance.name)
	if r is not None:
		instance.name = r
	r = replace_name(instance.styleMapStyleName)
	if r is not None:
		instance.styleMapStyleName = r
	r = replace_name(instance.styleMapFamilyName)
	if r is not None:
		instance.styleMapFamilyName = r
	r = replace_name(instance.familyName)
	if r is not None:
		instance.familyName = r
	
	r = replace_name(instance.preferredFamily)
	if r is not None:
		instance.preferredFamily = r
	#print('instance.fileName: ', instance.fileName())
	r = replace_name(instance.variableStyleName)
	if r is not None:
		instance.variableStyleName = r
	
	for CP in instance.customParameters:
		r = replace_name(CP.value)
		if r is not None:
			CP.value = r
