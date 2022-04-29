#MenuTitle: Create Axis Locations
# -*- coding: utf-8 -*-
# Code by Olli Meier, February 2022
__doc__="""
Add Axis Locations to Masters and Instances.
"""

from GlyphsApp import *
from GlyphsApp import objcObject

axis_location_dict = {
	'wght': {
		130: 300,
		176: 400,
		230: 500,
		270: 600,
		310: 700,
	},
	'ital': {
		0: 0,
		1: 14,
	},
	'XTDR': {
		0: 0,
		30: 30,
	},
	'INKT': {
		0: 0,
		1: 1,
	},
	'APRT': {
		0: 0,
		100: 100,
	},
	'SPAC': {
		0: 0,
		40: 40,
		60: 60,
	},
	'SS01': {
		0: 0,
		1: 1,
	},
	'SS02': {
		0: 0,
		1: 1,
	},
	'SS03': {
		0: 0,
		1: 1,
	},
}


def create_CP(obj, param, value, overwrite=False):
	'''
	create custom parameter:
	param: 'Axis Location'
	value: Content
	obj: font, master or instance
	'''

	if obj.customParameters[param]:
		if overwrite:
			obj.customParameters[param] = value
			print(f"{obj.name}: overwrote CustomParameter '{param}'.")
		else:
			print(f"{obj.name}: CustomParameter '{param}'' exists already, won't do anything.")
	else:
		obj.customParameters[param] = value
		print(f"New CustomParameter '{param}'' created.")


def create_axis_location(obj):
	'''
	obj: master or instance.
	'''
	values = []
	for ax_i, ax in enumerate(obj.axes):
		v = obj.axes[ax_i]
		if v in axis_location_dict[ax.axisTag]:
			location_value = axis_location_dict[ax.axisTag][v]
			values.append({"Axis": ax.name, "Location": location_value})
		else:
			print(f'Error: Could not find {v} in in given axis_location_dict. Please check: {obj.name}')
			values = None
			break

	print('values: ', values)
	if values is not None:
		create_CP(obj, objcObject('Axis Location'), objcObject(values), overwrite=True)


def create_axis_locations(font_obj, axis_location_dict=axis_location_dict):

	for obj in font_obj.masters:
		m = font_obj.masters[obj.id]
		create_axis_location(m)

	for obj in font_obj.instances:
		create_axis_location(obj)

def get_axis_location_dict():
	'''
	TODO: automation.
	'''
	return axis_location_dict


def main():
	axis_location_dict = get_axis_location_dict()
	for font_obj in Glyphs.fonts:
		create_axis_locations(font_obj, axis_location_dict=axis_location_dict)


if __name__ == '__main__':
	main()

