#MenuTitle: Proof PDF Instances
# -*- coding: utf-8 -*-
# Code by Olli Meier, October 2017, Version 1.00

__doc__="""
It generates a PDF and saves it to your desktop.
"""

import sys
import os
import shutil
import datetime
now = datetime.datetime.now()

#import random
import math

from GlyphsApp import *

import drawBot as d

font = Glyphs.font

rows = 10
distance = 10
margin = 20 
pageX = 595
pageY = 842
savePath = '~/Desktop'
leftMargin = 100
rightMargin = leftMargin
topMargin = 30
bottomMargin = topMargin


interpolations = []


for i in font.instances:
    if i.active == True:
		interpolations.append(i.interpolatedFont)

#print interpolations

d.newDrawing()

def getMaxUPM(font):
    collectAscender = []
    collectDescender = []
    for master in font.masters:
        collectAscender.append(master.ascender)
        collectDescender.append(master.descender)
    maxHeight = max(collectAscender) - min(collectDescender)
    return maxHeight

def getMaxWidth():
    collectWidth = []
    for value, instance in enumerate(interpolations):
        for glyph in instance.glyphs:
            collectWidth.append(instance.glyphs[glyph.name].layers[0].width)
    return max(collectWidth)


def scale(rows, pageX, pageY, distance, leftMargin, rightMargin, topMargin, bottomMargin):
    height =  (pageY - ((rows+1)* distance)) / (rows + 1) # plus one to have more distance to the buttom
    #height = (((rows+1)* distance) + pageY) / rows
    PageLayoutWidth = pageX - leftMargin - rightMargin
    PageLayoutHight = pageY - topMargin - bottomMargin
    maxGlyphHeight = getMaxUPM(font)
    
    scale = height / maxGlyphHeight
    scaleUndo = getMaxUPM(font) / height
    
    maxGlyphWidth = getMaxWidth()
    if (len(interpolations) * maxGlyphWidth * scale) > PageLayoutWidth:
        scale = PageLayoutWidth / ((len(interpolations) * maxGlyphWidth))
        scaleUndo = (len(interpolations) * maxGlyphWidth) / PageLayoutWidth
        tempRows = int(PageLayoutHight / (maxGlyphHeight * scale)) #without distance
        listofRows = [x for x in range(tempRows)]
        for i in reversed(listofRows):
            calculateNewHeight = i * distance + i * (maxGlyphHeight * scale)
            if calculateNewHeight < PageLayoutHight:
                newRows = i
                break
    else:
        newRows = rows
    return scale, scaleUndo, newRows


def main(rows):
    #d.font("any FontName")    
    scaleFactor, scaleFactorUndo, newRows = scale(rows, pageX, pageY, distance, leftMargin, rightMargin, topMargin, bottomMargin)
    #scaleFactor = 0.02
    
    if rows < newRows:
        rows = newRows
    
    print (rows)

    height = getMaxUPM(font) * scaleFactor
    d.newpage (pageX, pageY) # first page
    headerStr = '%s by %s' %(font.familyName, font.designer)
    d.fontSize(6)
    d.textBox(headerStr , (margin, pageY - topMargin, pageX - margin * 2, margin), align="center") #Date + name
    moveByRow = []
    d.translate(leftMargin, pageY - topMargin)

    for i, glyph in enumerate(font.glyphs):
        i = i +1
        if (i % rows == 0):
            d.newpage (pageX, pageY)
            d.fontSize(6)
            d.textBox(headerStr, (margin, pageY - topMargin, pageX - margin * 2, margin), align="center") #Date + name
            d.textBox(str(d.pageCount()) , (margin, 0, pageX - margin * 2, margin), align="center") #page number + CopyRight
            d.fontSize(3)
            d.textBox( 'Script by Olli Meier' , (margin, 0, pageX - margin * 2, margin/2), align="center") #page number + CopyRight
            d.translate(leftMargin, pageY - topMargin)
            #d.translate(0, -(sum(moveByRow) + distance))
            moveByRow = []
            #
            
        moveByRow.append(height + distance)

        d.fontSize(6)
        d.translate(0, -(height + distance))
        getBaseline = d.textBoxBaselines('%s\n%s' %(glyph.name, glyph.unicode) , (-leftMargin + margin, 0, leftMargin - margin*1.5, height))
        moveToBaseline = getBaseline[0][1]
        d.textBox('%s\n%s' %(glyph.name, glyph.unicode) , (-leftMargin + margin , 0 - moveToBaseline, leftMargin - margin*1.5, height ), align="right") #page number + CopyRight
        #d.translate(0, -(50))
        gWidthsInst = []
        for value, instance in enumerate(interpolations):
            d.save()
            d.scale(scaleFactor)
    
            width_total_temp = sum(gWidthsInst)
            d.translate ( width_total_temp, 0)
    
            g = instance.glyphs[glyph.name]

            gwidth = (g.layers[0].width)
            gWidthsInst.append(gwidth)
    
            n = g.layers[0].bezierPath
            d.drawPath(n)
            layer = g.layers[0]
            for component in layer.components:
                Cmp = component.bezierPath
                d.drawPath(Cmp)
            d.stroke(0.7)
            d.line((0, 0), (layer.width, 0)) #underline
            d.restore()

    path = savePath + '/%s%s%s_%s%s_%s_proof.pdf' %(now.year, now.month, now.day, now.hour, now.minute, font.familyName)
    d.saveImage([path])


main(rows) 