#MenuTitle: Print STAT axes values
# -*- coding: utf-8 -*-
# Code by Olli Meier, March 2022
__doc__="""
Print STAT axes values.
"""

# add code here
from GlyphsApp import *
fonts = Glyphs.fonts

def get_family_name(instance):
	# allgemeine funktion für FamilyName
	if instance.preferredFamily is not None:
		return instance.preferredFamily
	if instance.styleMapFamilyName is not None:
		return instance.styleMapFamilyName
	if instance.familyName is not None:
		return instance.familyName

def get_subfamily_name(instance):
	# allgemeine funktion für SubFamilyName
	if instance.preferredSubfamilyName is not None:
		return instance.preferredSubfamilyName
	if instance.styleMapStyleName is not None:
		return instance.styleMapStyleName
	if instance.name is not None:
		return instance.name

def most_frequent(List):
	if not List:
		return ['']
		
	m = max(map(List.count, List))
	s = set(x for x in List if List.count(x) == m)
	if len(s) == 1:
		return list(s)
	else:
		return ['']

def get_axes_dict(fontObj):
	# Funktion zum sammeln der Achsen-Werte pro Achse
	axisDict = {}
	axes = fontObj.axes

	for axID, ax in enumerate(axes):
		axName = ax.name
		axTag = ax.axisTag
		axisDict[axID] = []
		for ins in fontObj.instances:
			if ins.type == 1 or not ins.active:
				# skip variable font instance.
				continue
			axValue = ins.axes[axID]
			matchValue = None
			if ins.customParameters['Axis Location']:
				axLocation = ins.customParameters['Axis Location']
				matchValue = float(axLocation[axID]['Location'])
			else:
				print("WARNING Missing custom parameter 'Axis Location' for instance: %s"%ins)

			if (axValue, matchValue) not in axisDict[axID]:
				axisDict[axID].append((axValue, matchValue))

	return axisDict

for font_obj in fonts:
	axes = []
	hasItalics = False

	axes_dict = get_axes_dict(font_obj)
	for axID in axes_dict:
		ax = font_obj.axes[axID]
		axes_values = dict(
			tag=ax.axisTag,
			name=ax.name,
			ordering=axID,
			values=[],
		)
		print(axes_values)
		
		axs_dict = sorted(axes_dict[axID])
		hasRegularValue = False
		hasBoldValue = False
		for i, item in enumerate(axs_dict):
			pre_i = i - 1
			next_i = i + 1
			if pre_i < 0:
				pre_i = i
			if next_i == len(axs_dict):
				next_i = i

			axis_value, axis_value_mapping = item
			collect_names = []
			for instance in font_obj.instances:
				if instance.type == 1 or not instance.active:
					# skip variable font instance.
					continue
				if axis_value == instance.axes[axID]:
					name_parts = f"{get_family_name(instance)} {get_subfamily_name(instance)}".replace(font_obj.familyName, '').strip().split()
					for name_part in name_parts:
						if name_part.lower() == 'italic':
							#skip to add this.
							hasItalics = True
							continue
						collect_names.append(name_part)

			axis_value_name = most_frequent(collect_names)[0]
			axis_value = axis_value_mapping if axis_value_mapping is not None else axis_value
			
			axis_value_pre, axis_value_mapping_pre = axs_dict[pre_i]
			axis_value_pre = axis_value_mapping_pre if axis_value_mapping_pre is not None else axis_value_pre
			
			axis_value_next, axis_value_mapping_next = axs_dict[next_i]
			axis_value_next = axis_value_mapping_next if axis_value_mapping_next is not None else axis_value_next
			
			nominal_value = axis_value
			min_value = axis_value if i == 0 else (axis_value + axis_value_pre) / 2
			max_value = axis_value if i == next_i else (axis_value + axis_value_next) / 2
			
			# special cases Optical Size:
			if ax.axisTag == 'opsz' and i == 0:
				min_value = '-infinty'  # fixedToFloat(-0x80000000, 16)
			if ax.axisTag == 'opsz' and i == next_i:
				max_value = '+infinty'  # fixedToFloat(0x7FFFFFFF, 16)
			
			if axis_value_name == '':
				if ax.axisTag == 'wght':
					axis_value_name = 'Regular'
				else:
					axis_value_name = 'Normal'
			
			axis_value = dict(nominalValue=axis_value, rangeMinValue=min_value, rangeMaxValue=max_value, name=axis_value_name)
			if axis_value_name in ('', 'Regular', 'Normal'):
				axis_value['flags'] = 0x2

			axes_values['values'].append(axis_value)
			print('axis_value: ', axis_value)
			
			if ax.axisTag == 'wght':
				if axis_value_name == 'Bold':
					hasBoldValue = nominal_value
				if axis_value_name in ('', 'Regular', 'Normal'):
					hasRegularValue = nominal_value
			
		if ax.axisTag == 'wght':
			if hasRegularValue and hasBoldValue:
				axis_value = dict(value=hasRegularValue, linkedValue=hasBoldValue, name="Regular", flags=0x2)
				axes_values['values'].append(axis_value)
				print('axis_value: ', axis_value)
		axes.append(axes_values)

	ital_values = dict(
		tag='ital',
		name='Italic',
		ordering=len(axes),
		values=[],
		)
		
	if not hasItalics:
		# is upright font
		axis_value = dict(value=0, linkedValue=1, name="Regular", flags=0x2, )
	else:
		# is italic font
		axis_value = dict(value=1, name="Italic")
	print('axis_value: ', axis_value)
	ital_values['values'].append(axis_value)
		
	axes.append(ital_values)
	#print('axes: ', axes)
