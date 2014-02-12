#!/usr/bin/env python

"""
excel-to-rdf.py: converts an Excel workbook to triple statements in turtle syntax.
See example workbook "example_input_data.xlsx"for input data formatting. Workbook must contain 
two sheets. First sheet consists of triple statements where the first column lists 
each subject, the row headers are the predicates, and each column in a row is the 
object for that row's statement. The second sheet is two columns with each row containing 
a prefix and its full URI. The script will check for and skip empty cells. 
"""

import xlrd

# Change this to the actual path and filename of the spreadsheet to convert
spreadsheet = '/Users/melonbreath/Dropbox/Work/MIT-Fellowship/DCM Initiative/Data Model/data files/content_types.xlsx'
turtle = '/Users/melonbreath/Dropbox/Work/MIT-Fellowship/DCM Initiative/Data Model/data files/content_types_turtle.rdf'

# Open spreadsheet and file
book = xlrd.open_workbook(spreadsheet)
sh1 = book.sheet_by_index(0)
sh2 = book.sheet_by_index(1)
file = open(turtle, 'w')


for rowx in range(sh2.nrows):
	file.write("@prefix " + str(sh2.cell_value(rowx, 0)) + ": <" + str(sh2.cell_value(rowx, 1)) + "> .\n")
file.write("\n")
	
for rowx in range(2, sh1.nrows):
	for coly in range(1, sh1.ncols):
		# Check to make sure the object cell has data, otherwise skip it
		if sh1.cell_type(rowx, coly) != 0:
			# Creates a triple statement in turtle syntax with object as a string.
			if str(sh1.cell_value(1, coly)) == "string":
				file.write(str(sh1.cell_value(rowx, 0)) + " " + str(sh1.cell_value(0, coly)) + ' "' + str(sh1.cell_value(rowx, coly)) + '" .\n')
			# Creates a triple statement in turtle syntax with object as a number.
			elif str(sh1.cell_value(1, coly)) == "number":
				file.write(str(sh1.cell_value(rowx, 0)) + " " + str(sh1.cell_value(0, coly)) + " " + str(sh1.cell_value(rowx, coly)) + " .\n")
			# Creates a triple statement in turtle syntax.
			else:	
				file.write(str(sh1.cell_value(rowx, 0)) + " " + str(sh1.cell_value(0, coly)) + " " + str(sh1.cell_value(rowx, coly)) + " .\n")

file.close()