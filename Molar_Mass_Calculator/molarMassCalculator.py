"""
Create by Jonathan Keane
Milwaukee School Of Engineering 
November 3, 2020

Purpose: 
	Read a JSON of periodic tables to create a molar mass calculator in a GUI through tkinter

How To Use GUI:
	1) Type in case sensitive formula with polyatomics delimited by '()' (example 'H4(SO4)2')
	2) Either press the 'Calculate' button or return
	3) Read the molar mass that appears above the 'Calculate' button

"""
import json
from tkinter import *

file_text = open("PeriodicTableJSON.json", encoding = "utf8").read()
periodic_table_json = json.loads(file_text)
atomic_mass_dict = {}

for element in periodic_table_json["elements"]:
	atomic_mass_dict[element["symbol"]] = round(element["atomic_mass"], 2)

def molar_mass_of_molecule(molecule):
	element_count_dict = {}
	current_element = ""
	count = ""
	working_on_polyatomic = False
	finished_polyatomic = False
	polyatomic_count_dict = {}
	for char in molecule:
		if char.isupper() or char == ")" or char == "(":
			if char == "(":
				working_on_polyatomic = True
			elif char == ")":
				working_on_polyatomic = False
				finished_polyatomic = True
				if current_element in polyatomic_count_dict.keys():
					polyatomic_count_dict[current_element] += int(count) if count != "" else 1
				else:
					polyatomic_count_dict[current_element] = int(count) if count != "" else 1
			elif finished_polyatomic == True:
				for poly_element in polyatomic_count_dict:
					# print(poly_element, polyatomic_count_dict[poly_element] * (int(count) - 1))
					if poly_element in element_count_dict.keys():
						element_count_dict[poly_element] += polyatomic_count_dict[poly_element] * (int(count) - 1) # added because program already added this one time
					else:
						element_count_dict[poly_element] = polyatomic_count_dict[poly_element] * (int(count) - 1) # added because program already added this one time
				# print(polyatomic_count_dict, f"({count})")
				polyatomic_count_dict.clear()
				finished_polyatomic = False
			if current_element != "":
				if working_on_polyatomic == True and char != "(":
					if current_element in polyatomic_count_dict.keys():
						polyatomic_count_dict[current_element] += int(count) if count != "" else 1
					else:
						polyatomic_count_dict[current_element] = int(count) if count != "" else 1
				if current_element in element_count_dict.keys():
					element_count_dict[current_element] += int(count) if count != "" else 1
				else:
					element_count_dict[current_element] = int(count) if count != "" else 1
				# print(current_element, f"+{count}")
			if char.isupper():
				current_element = char
			else:
				current_element = ""
			count = ""
		elif char.islower():
			current_element += char
		elif char.isnumeric():
			count += char
		# print(working_on_polyatomic, finished_polyatomic)
		# elif char == ")":
		# 	finished_polyatomic = True
			# if current_element in element_count_dict.keys():
			# 	element_count_dict[current_element] += count
			# else:
			# 	element_count_dict[current_element] = count

	# if current_element != "":
	# 	if current_element in element_count_dict.keys():
	# 		element_count_dict[current_element] += int(count) if count != "" else 1
	# 	else:
	# 		element_count_dict[current_element] = int(count) if count != "" else 1
	# print(current_element, finished_polyatomic)
	if finished_polyatomic:
		for poly_element in polyatomic_count_dict:
			if poly_element in element_count_dict.keys():
				element_count_dict[poly_element] += polyatomic_count_dict[poly_element] * (int(count) - 1) # added because program already added this one time
			else:
				element_count_dict[poly_element] = polyatomic_count_dict[poly_element] * (int(count) - 1) # added because program already added this one time
	elif current_element != "":
		if current_element in element_count_dict.keys():
			element_count_dict[current_element] += int(count) if count != "" else 1
		else:
			element_count_dict[current_element] = int(count) if count != "" else 1
	"""
	things to do tomorrow:
		1) address polyatomics
		2) address element counts >10 (multi-character) -> DONE
		3) put this into a GUI to make this quicker when I want to use it
	"""
	print(element_count_dict)
	molar_mass = 0.0
	for element in element_count_dict:
		molar_mass += atomic_mass_dict[element] * element_count_dict[element]
	return round(molar_mass, 2)

# print(f"The molar mass of {test} is {molar_mass_of_molecule(test)} g")

class LabelPairedEntry():
	def __init__(self, parent_element, text, entry_type, pady = (0, 10), entry_width = 50):
		self.base_frame = Frame(parent_element, background = "#3CBF54")
		self.base_frame.pack(padx = 10, pady = pady)
		# label
		self.label = Label(self.base_frame,
						   text       = text,
						   background = "#3CBF54",
						   fg         = "black")
		self.label.pack(side = LEFT, 
					    padx = 10, 
						pady = (0, 10))
		# entry
		self.entry_text_variable = entry_type
		self.entry_text_variable = Entry(self.base_frame, 
									  width        = entry_width,
									  textvariable = self.entry_text_variable)
		self.entry_text_variable.pack(side = RIGHT, 
								   padx = 10, 
								   pady = (0,10))
	def get(self):
		return self.entry_text_variable.get()

def main():
	root = Tk()
	root.geometry("500x500")
	root.configure(background = "#3CBF54")
	root.title("Molar Mass Calculator")
	molecule = LabelPairedEntry(root, "Molecule:", StringVar())
	molar_mass_label = Label(root, text = "", background = "#3CBF54")
	molar_mass_label.pack(padx = (0, 10), pady = (0, 10))
	calculate = Button(root, text       = "Calculate", 
						     command    = lambda: molar_mass_label.configure(text = str(molar_mass_of_molecule(molecule.get())) + " g"),
							 background = "white")
	calculate.pack(padx = (0, 10), 
				   pady = (0, 10))
	canvas = Canvas(root, width = 300, height = 350, background = "#3CBF54", borderwidth=0, highlightthickness=0)      
	canvas.pack() 
	def calculate_molar_mass(event):
		molar_mass_label.configure(text = str(molar_mass_of_molecule(molecule.get())) + " g")
	root.bind('<Return>', calculate_molar_mass)
	img = PhotoImage(file = "TransparentBeaker.png")      
	canvas.create_image(20,20, anchor = NW, image = img)
	root.mainloop()


if __name__ == "__main__":
	main()

