#MenuTitle: Delete layers from Selection
# encoding: utf-8
# code by Olli Meier
# 2017 July 15, Version 1.0

__doc__="""
Deletes all layers except masters for all selected glyphs.
"""

from GlyphsApp import *
f = Glyphs.font

# masterName = []
# for master in f.masters:
# 	masterName.append(master.name)

def delLayers(g):
	delList = []
	for x, layer in enumerate(g.layers):
		#if layer.name not in masterName:

		if not (layer.isMasterLayer() or layer.isBraceLayer() or layer.isSpecialLayer()):
			delList.append(x)
		'''
		 	print ('layer Master: ', layer.name)
		elif layer.isBraceLayer():
		 	print ('layer Brace: ', layer.name)
		elif layer.isSpecialLayer:
			print ('layer Special: ', layer.name)
		else:
			print ('layer.name to delete: ', layer.name)
			#delList.append(x)
		'''

	for l in reversed(delList): #need to start with the highest value
		print ('del layer: %s' %g.layers[l])
		del(g.layers[l])

	if not delList:
		print ('There are just masters, no other layers to delete.')

for g in f.selection:
	delLayers(g)

print ('Done')