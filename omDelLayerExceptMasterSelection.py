#MenuTitle: Delete layers from Selection
# encoding: utf-8
# code by Olli Meier
# 2017 July 15, Version 1.0

__doc__="""
Deletes all layers except masters for all selected glyphs.
"""

from GlyphsApp import *
f = Glyphs.font

masterName = []
for master in f.masters:
	masterName.append(master.name)

def delLayers(g):
	delList = []
	for x, layer in enumerate(g.layers):
		if layer.name not in masterName:
			delList.append(x)

	for l in reversed(delList): #need to start with the highest value
		print ('del layer: %s' %g.layers[l])
		del(g.layers[l])

	if not delList:
		print ('There are just masters, no other layers to delete.')

for g in f.selection:
	delLayers(g)

print ('Done')