#MenuTitle: Change too long Production Names
# -*- coding: utf-8 -*-
# Code by Olli Meier, January 2016
__doc__="""
If a nice name is longer than 29 characters and it has an extention, it changes the production name based on base glyph unicode.
"""


font = Glyphs.font

for g in font.glyphs:
	if len(g.name) > 29:
		if not g.unicode:
			glyphname = g.name
			if '.' in glyphname:
				glyphNameEnding = glyphname.split('.')[-1]
				baseName = glyphname.replace('.' + glyphNameEnding, '')
				try:
					productionName = 'uni%s.%s'%(font.glyphs[baseName].unicode, glyphNameEnding)
					g.productionName = productionName
					g.storeProductionName = True
					print ('%s base glyph is %s'%(glyphname, baseName))
					print ('Added production name: %s'%productionName)
				except:
					print ('Something get wrong.')
			