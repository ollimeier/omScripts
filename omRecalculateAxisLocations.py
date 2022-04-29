#MenuTitle: Recalculate Axes Locations
# -*- coding: utf-8 -*-
# Code by Olli Meier, March 2022
__doc__="""
Recalculate axes locations for master and instances. Only Print. Now change.
"""

from GlyphsApp import *

font_obj = Glyphs.font

def recalculate_axis_value(axis_value,
                           master_value_min, master_value_max,
                           master_value_min_preferred, master_value_max_preferred):

    if master_value_max-master_value_min != 0:
        axis_value_new = (((axis_value-master_value_min)/(master_value_max-master_value_min)) * (master_value_max_preferred-master_value_min_preferred)) + master_value_min_preferred
    else:
        axis_value_new = ((axis_value-master_value_min) * (master_value_max_preferred-master_value_min_preferred)) + master_value_min_preferred

    return axis_value_new


def get_axes_dict(fontObj):
	axisDict = {}
	axes = fontObj.axes

	for axID, ax in enumerate(axes):
		axName = ax.name
		axTag = ax.axisTag
		axisDict[axID] = []
		for m in fontObj.masters:
			axValue = m.axes[axID]
			matchValue = None
			if m.customParameters['Axis Location']:
				axLocation = m.customParameters['Axis Location']
				matchValue = float(axLocation[axID]['Location'])
			else:
				print("ERROR Missing custom parameter 'Axis Location' for master: %s"%m)
				return
			if axValue not in axisDict[axID]:
				axisDict[axID].append((axValue, matchValue))

	return axisDict

def recalculate_axes_locations(fontObj):
	axisDict = get_axes_dict(fontObj)
	
	axisMappingDict = {}
	calculationError = False
	for axID in axisDict:
		ax = fontObj.axes[axID]
		axName = ax.name
		axTag = ax.axisTag
		axisMappingDict[axID] = dict()
		for instance in fontObj.instances:
			if instance.type == INSTANCETYPEVARIABLE:
				continue
			if not instance.customParameters['Axis Location']:
				print("ERROR Missing custom parameter 'Axis Location' for instance: %s"%instance)
				return 

			if instance.active:
				minMaster = None
				maxMaster = None
				minMasterPrefered = None
				maxMasterPrefered = None
				axisValue = instance.axes[axID]

				for masterValue in axisDict[axID]:
					if masterValue[0] <= axisValue:
						minMaster = masterValue[0]
						minMasterPrefered = masterValue[1]
					if masterValue[0] >= axisValue:
						maxMaster = masterValue[0]
						maxMasterPrefered = masterValue[1]

					if minMaster and maxMaster:
						break

				newAxisValue = None
				if None not in (minMaster, maxMaster, minMasterPrefered, maxMasterPrefered):
					newAxisValue = recalculate_axis_value(axisValue, minMaster, maxMaster, minMasterPrefered, maxMasterPrefered)
				else:
					print('ERROR Might be that there is an extrapolation used. Cannot recalcuate this. Instance needs to be in between or be equal to masters.')
					print("\tIssues with instance '%s' axis '%s' value is '%s'."%(instance.name, axTag, axisValue))
					return

				axLocation = instance.customParameters['Axis Location']
				axisValueMapping = float(axLocation[axID]['Location'])

				if newAxisValue is None:
					print( 'instance.name: %s'%instance.name)
					print( 'minMaster: %s'%minMaster)
					print( 'maxMaster: %s'%maxMaster)
					print( 'minMasterPrefered: %s'%minMasterPrefered)
					print( 'maxMasterPrefered: %s'%maxMasterPrefered)
					print( 'newAxisValue: %s'%newAxisValue)
					return 
					
				if axisValueMapping not in axisMappingDict[axID]:
					axisMappingDict[axID][axisValueMapping] = dict()
					axisMappingDict[axID][axisValueMapping]['newAxisValue'] = newAxisValue
					axisMappingDict[axID][axisValueMapping]['currentAxisValue'] = axisValue
				else:
					if axisMappingDict[axID][axisValueMapping]['newAxisValue'] != newAxisValue:
						tempMappingName = '%s %s'%(instance.name, axisValueMapping)
						axisMappingDict[axID][tempMappingName] = dict()
						axisMappingDict[axID][tempMappingName]['newAxisValue'] = newAxisValue
						axisMappingDict[axID][tempMappingName]['currentAxisValue'] = axisValue
						print('Duplicate Mapping: %s'%tempMappingName)
						print("\taxisValueMapping: %s -> newAxisValue: %s, axisValue: %s"%(axisValueMapping, axisMappingDict[axID][axisValueMapping]['newAxisValue'], axisMappingDict[axID][axisValueMapping]['currentAxisValue']))
						print("\taxisValueMapping: %s -> newAxisValue: %s, axisValue: %s"%(axisValueMapping, newAxisValue, axisValue))
						calculationError = True

				minMaster = None
				maxMaster = None
				minMasterPrefered = None
				maxMasterPrefered = None

	if calculationError:
		print('Sorry, something went wrong. Did not change anything. Calculation error.')
		for axID in axisMappingDict:
			ax = fontObj.axes[axID]
			axName = ax.name
			axTag = ax.axisTag
			print("%s, %s "%(axName, axTag))
			for currentAxisValue in sorted(axisMappingDict[axID]):
				print("%s, %s "%(currentAxisValue, axisMappingDict[axID][currentAxisValue]))
		return
	else:
		for axID in axisMappingDict:
			ax = fontObj.axes[axID]
			axName = ax.name
			axTag = ax.axisTag
			print( "Axis '%s' = '%s':"%(axTag, axName, ))
			for currentAxisValue in sorted(axisMappingDict[axID]):
				origAV = axisMappingDict[axID][currentAxisValue]['currentAxisValue']
				recalculatedAV = axisMappingDict[axID][currentAxisValue]['newAxisValue']
				mappingAV = currentAxisValue
				print( "\tOriginal axis value '%s' -> recalculated '%s' -> mapped to '%s'"%(origAV, recalculatedAV, mappingAV))


		return axisMappingDict

print(recalculate_axes_locations(font_obj))
# Hierbei sind noch keine 'Special-Layer' überarbeitet. Das muss extra passieren, aber mit gleicher Logik.


