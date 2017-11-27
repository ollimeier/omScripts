#MenuTitle: Copy Hinting from one Layer to Another
# -*- coding: utf-8 -*-
# Code by Olli Meier, July 2017
# Version 1.0
__doc__="""
Copy PS and TT hinting for each glyph from one layer to another.
"""

from GlyphsApp import *

font = Glyphs.font
import copy


for g in font.glyphs:
	hintedLayer = ''
	for layer in g.layers:
		if layer.hints:
			hintedLayer = layer
			break
	if hintedLayer:
		for layer in g.layers:
			if layer != hintedLayer and not layer.hints:
				layer.hints = copy.copy(hintedLayer.hints)
				print 'Glyph: %s, copied hinting from %s to %s.' %(g.name, hintedLayer, layer)
