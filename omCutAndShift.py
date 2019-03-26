#MenuTitle: Cut and Shift
# -*- coding: utf-8 -*-
# Code by Olli Meier (Github: moontypespace, Instagram: tyyyyypo)

__doc__="""
Cut a glyph and shift the top part to the right for just a selection of glyphs or for all glyphs in a font.
"""

import GlyphsApp
from Foundation import *

try:
	from vanilla import *
	vanilla = True
except:
	vanilla = False

	
font = Glyphs.font


def cut(font, glyph, x, y, z):
	g = glyph
	for master in font.masters:
		mID = master.id
		masterlayer = font.glyphs[g.name].layers[mID]

		#for component in masterlayer.components:
		#	print ('component: ', component)
		
		masterlayer.removeOverlap() # remove overlaping
		masterlayer.cutBetweenPoints(NSPoint(y, x), NSPoint(masterlayer.width, x )) #cut paths
	
		masterlayercut = font.glyphs[g.name].layers[mID]
		
		for path in masterlayercut.paths:
			cut = False
			for node in path.nodes: #if one node of path is higher than the cut, turn to true
				if node.position.y > (x+1): #plus one, cause some rounding mistakes
					cut = True
					pass

			if cut: #if cut is true, shift all nodes
				for node in path.nodes:
					node.position = NSPoint(node.position.x + z, node.position.y)
				
	

if vanilla:
	y = 0 #rotation
	class WindowCutShift(object):
		
		def __init__(self):
			a = 200
			b = a-40
			self.w = Window((a, b), "Cut and Shift")

			self.w.textcut = TextBox((10, 13, -10, 17), "cut")
			self.w.textEditor_cut = EditText((a/2, 10, -10, 22))
			
			self.w.textshift = TextBox((10, 43, -10, 17), "shift")
			self.w.textEditor_shift = EditText((a/2, 40, -10, 22))
			
			self.w.textGlyphs = TextBox((10, 70, -10, 40), "glyphs")
			self.w.selector = RadioGroup((a/2, 70, -10, 40),["selected", "all"])
			self.w.selector.set(0)
			
			self.w.Button = Button((10, 110, -10, -10), "process", callback = self.Button)

			self.w.open()

			
		def Button(self, sender): #open text file documentation
			x = int(self.w.textEditor_cut.get())
			z = int(self.w.textEditor_shift.get())
			if x is not '' and z is not '':
				if self.w.selector.get() == 0: #just selected glyphs
					for glyph in font.selection:
						cut(font, glyph, x, y, z)
				if self.w.selector.get() == 1: #just selected glyphs
					for glyph in font.glyphs:
						cut(font, glyph, x, y, z)
			else:
				print 'Values are missing.'

	WindowCutShift()

if not vanilla: #default values
	x = 300 #cut height
	y = 0 #rotation
	z = 100 #shift
	for glyph in font.selection:
		cut(font, glyph, x, y, z)
