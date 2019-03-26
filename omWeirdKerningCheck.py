#MenuTitle: Check Weird Kerning
# -*- coding: utf-8 -*-
# Code by Olli Meier, Mai 2016
__doc__="""
Check weird Kerning for selected master.
"""

from GlyphsApp import *

font = Glyphs.font

def weirdKerningCheck(font=None):
	kernGroup = 0
	totalKern = 0
	kernValues = []
	if font:
		for master in font.kerning:
			kernGroup += len(font.kerning[master])
			masterKern = font.kerning[master]
			for anyKernGroup in masterKern:
				totalKern += len(masterKern[anyKernGroup])
				singleKern = masterKern[anyKernGroup]
				for kernValue in singleKern:
					kernValues.append(singleKern[kernValue])

	
	return kernGroup, totalKern, kernValues

def getGlyphWidth(font=None):
	glyphWidth = {}
	if font:
		for anyG in font.glyphs:
			#glyphWidth.append(anyG.layers[font.selectedFontMaster.id].width)
			glyphWidth[anyG.name] = anyG.layers[font.selectedFontMaster.id].width

	return glyphWidth
	

if __name__ == "__main__":
	
	kernGroup, totalKern, kernValues = weirdKerningCheck(font)
	glyphWidth = getGlyphWidth(font)
	content = ('Kerning groups: ' + str(kernGroup) + '\n' + 'Number of kerning pairs: ' + str(totalKern) + '\n' + 'Min kerning: ' + str(min(kernValues)) + '\n' + 'Max kerning: ' + str(max(kernValues)))
	
	generalGlyphwidth = []
	for anyG in glyphWidth:
		generalGlyphwidth.append(glyphWidth[anyG])
	
	if (min(kernValues) * -1) >= (max(generalGlyphwidth) / 2):
		content += '\nWarning: There is a kerning larger than half of the biggest glyph width.'
	
	Glyphs.displayDialog_(str(content))
