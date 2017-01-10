#MenuTitle: delete anchors
# -*- coding: utf-8 -*-
# Code by Olli Meier, January 2016
__doc__="""
delete all anchors in all masters of your selection.
"""

from GlyphsApp import *

font = Glyphs.font

for glyph in font.selection:
	for master in font.masters:
		mID = master.id
		masterlayer = font.glyphs[glyph.name].layers[mID]
		
		masterlayer.anchors = ()