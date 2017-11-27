#MenuTitle: Delete Anchors
# -*- coding: utf-8 -*-
# Code by Olli Meier, January 2016
__doc__="""
Delete all anchors.
"""

from GlyphsApp import *

font = Glyphs.font


for glyph in font.glyphs:
    for layer in glyph.layers:
        layer.anchors = ()