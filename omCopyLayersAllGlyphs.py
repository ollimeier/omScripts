#MenuTitle: Make copy of layers for all glyphs
# encoding: utf-8
# code by Olli Meier
# 2022, Version 1.0

__doc__="""
Copy all masters and special layers for all glyphs and add 'orig' to the name.
"""

from GlyphsApp import *
f = Glyphs.font

def copyLayers(g):
	collection_newlayers = []
	for x, layer in enumerate(g.layers):
		if not (layer.isMasterLayer or layer.isSpecialLayer):
			continue
		
		newLayer = layer.copy()
		newLayer.name = f"{layer.name} orig"
		collection_newlayers.append(newLayer)
		
	if collection_newlayers:
		for l in collection_newlayers:
			g.layers.append(l)
		
for g in f.glyphs:
	copyLayers(g)

print ('Done')