#MenuTitle: rename anchors
# -*- coding: utf-8 -*-
# Code by Olli Meier, January 2016, Version 1.00
__doc__="""
Rename anchors for all master layers in selection.
"""

from GlyphsApp import *

try:
	from vanilla import *
except:
	Glyphs.displayDialog_(u'Vanilla for python is missing.')

font = Glyphs.font


def change_anchorName(font, glyph, x, y):
	for master in font.masters:
		mID = master.id
		masterlayer = font.glyphs[glyph.name].layers[mID]

		for anchor in masterlayer.anchors:
			if anchor.name == x:
				print anchor.name
				anchor.name = str(y)
				print anchor
				print anchor.name
				print ('Glyph: ' + glyph.name + ' change anchor from \'' + x + '\' to \'' + y + '\'' )
		


class WindowComb(object):
	
	def __init__(self):
		a = 400
		b = a/2 - 40
		
		self.w = Window((a, b), "Change naming of anchors")

		self.w.w_width = TextBox((10, 13, -10, 17), "Old name of anchor: ")
		self.w.textEditor_old = EditText((a*2/4, 10, -10, 22))
		self.w.textEditor_old.set('top')
		
		self.w.w_shift = TextBox((10, 43, -10, 17), "New name for anchor: ")
		self.w.textEditor_new = EditText((a*2/4, 40, -10, 22))
		self.w.textEditor_new.set('topCase')
		
		self.w.Button = Button((10, 110, -10, -10), "process", callback = self.Button)

		self.w.open()

		
	def Button(self, sender):
		
		x = self.w.textEditor_old.get() 
		y = self.w.textEditor_new.get()
		
		
		#### start: main part
		
		if y is not '' and x is not '': 
			glyphSelection = []

			for glyph in font.selection:
				change_anchorName(font, glyph, x, y)
			print "Done."
			self.w.close()

		else:
			if x is '' and y is not '':
				text = 'You forgot to define an anchor for changing.'
			if y is '' and x is not '':
				text = 'You forgot to define a new name for you anchors.'
			if y is '' and x is '':
				text = 'Please define a name for the old anchor and a new name for the old anchor name.'
				
			w = Window((200, 100), "Error")
			w.w_error_character = TextBox((10, 10, -10, -10), text)
			w.center()
			w.open()
			

				
		#### end: main part


WindowComb()

