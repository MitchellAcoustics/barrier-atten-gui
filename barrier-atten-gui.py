# A GUI to calculate the acoustic attenuation due to a barrier

"""
ADD:
Checkboxes with options for SWL or SPL, type of directivity
Based on that, if statements for distance correction

Indicator of whether or not line of site was broken

A limit option for the barrier attenuation.

"""

from tkinter import *
from math import sqrt, log, exp
import numpy as np

class Application(Frame):
	def __init__(self, master):
		"""Initialize the frame """
		Frame.__init__(self, master)
		self.grid()
		self.create_octave_input_widgets()
		self.create_para_input_widgets()
		self.create_para_output_widgets()
		self.create_barrier_calc_widgets()
		self.create_results_widgets()


	
	def create_octave_input_widgets(self): # ADD: Shorten this by creating an array with octave band or 3rd octave values and a for loop which automatically generates the widgets. Will need to include if statement which creates second and third rows when doing third octave inputs
		# Create labels and entry widgets for entering octave band noise data 
		octave_bands = [63, 125, 250, 500, 1000, 2000, 4000, 8000]

		#Create 63 Hz Label
		self.hz63_lbl = Label(self, text = str(octave_bands[0]) + " Hz")
		self.hz63_lbl.grid(row = 0, column = 0)
		#Create 63 Hz entry
		self.hz63_ent = Entry(self, bg = "yellow", justify = CENTER)
		self.hz63_ent.grid(row = 1, column = 0) 

		#Create 125 Hz Label
		self.hz125_lbl = Label(self, text = "125 Hz")
		self.hz125_lbl.grid(row = 0, column = 1)
		#Create 125 Hz entry
		self.hz125_ent = Entry(self, bg = "yellow", justify = CENTER)
		self.hz125_ent.grid(row = 1, column = 1)

		#Create 250 Hz Label
		self.hz250_lbl = Label(self, text = "250 Hz")
		self.hz250_lbl.grid(row = 0, column = 2)
		#Create 250 Hz entry
		self.hz250_ent = Entry(self, bg = "yellow", justify = CENTER)
		self.hz250_ent.grid(row = 1, column = 2)		

		#Create 500 Hz Label
		self.hz500_lbl = Label(self, text = "500 Hz")
		self.hz500_lbl.grid(row = 0, column = 3)
		#Create 500 Hz entry
		self.hz500_ent = Entry(self, bg = "yellow", justify = CENTER)
		self.hz500_ent.grid(row = 1, column = 3)
	
		#Create 1000 Hz Label
		self.hz1000_lbl = Label(self, text = "1000 Hz")
		self.hz1000_lbl.grid(row = 0, column = 4)
		#Create 1000 Hz entry
		self.hz1000_ent = Entry(self, bg = "yellow", justify = CENTER)
		self.hz1000_ent.grid(row = 1, column = 4)

		#Create 2000 Hz Label
		self.hz2000_lbl = Label(self, text = "2000 Hz")
		self.hz2000_lbl.grid(row = 0, column = 5)
		#Create 2000 Hz entry
		self.hz2000_ent = Entry(self, bg = "yellow", justify = CENTER)
		self.hz2000_ent.grid(row = 1, column = 5)
		
		#Create 4000 Hz Label
		self.hz4000_lbl = Label(self, text = "4000 Hz")
		self.hz4000_lbl.grid(row = 0, column = 6)
		#Create 4000 Hz entry
		self.hz4000_ent = Entry(self, bg = "yellow", justify = CENTER)
		self.hz4000_ent.grid(row = 1, column = 6)

		#Create 8000 Hz Label
		self.hz8000_lbl = Label(self, text = "8000 Hz")
		self.hz8000_lbl.grid(row = 0, column = 7)
		#Create 8000 Hz entry
		self.hz8000_ent = Entry(self, bg = "yellow", justify = CENTER)
		self.hz8000_ent.grid(row = 1, column = 7)

	
	def create_para_input_widgets(self):
		# Create label and entry widgets with inputs for barrier calc measurements
		# ADD: Need to better arrange these. Would like an empty row between noise data input and parameter inputs

		# Create Barrier Height Label
		self.barrier_ht_lbl = Label(self, text = "Barrier Height (Bh): ")
		self.barrier_ht_lbl.grid(row = 2, column = 0)
		# Create Barrier Height Entry
		self.barrier_ht_ent = Entry(self, bg = "yellow", justify = CENTER)
		self.barrier_ht_ent.grid(row = 2, column = 1)

		# Create Source Height Label
		self.source_ht_lbl = Label(self, text = "Source Height (Sh): ")
		self.source_ht_lbl.grid(row = 2, column = 3)
		# Create Source Height Entry
		self.source_ht_ent = Entry(self, bg = "yellow", justify = CENTER)
		self.source_ht_ent.grid(row = 2, column = 4)

		# Create Receiver height label
		self.receive_ht_lbl = Label(self, text = "Receiver Height (Rh): ")
		self.receive_ht_lbl.grid(row = 2, column = 6)
		# Create Receiver height entry
		self.receive_ht_ent = Entry(self, bg = "yellow", justify = CENTER)
		self.receive_ht_ent.grid(row = 2, column = 7)

		# Create D1 Label
		self.d1_lbl = Label(self, text = "Receiver to Source Distance (D1): ")
		self.d1_lbl.grid(row = 3, column = 2, columnspan = 2, sticky = E)
		# Create D1 entry
		self.d1_ent = Entry(self, bg = "yellow", justify = CENTER)
		self.d1_ent.grid(row = 3, column = 4)

		# Create D2 label
		self.d2_lbl = Label(self, text = "Source to Barrier Distance (D2): ")
		self.d2_lbl.grid(row = 3, column = 5, columnspan = 2, sticky = E)
		# Create D2 entry
		self.d2_ent = Entry(self, bg = "yellow", justify = CENTER)
		self.d2_ent.grid(row = 3, column = 7)

		# Create Button to calculate remaining parameters
		self.calc_paras_bttn = Button(self, text = "Calculate Remaining Parameters", command = self.calc_paras)
		self.calc_paras_bttn.grid(row = 4, column = 0, columnspan = 8)

	def create_para_output_widgets(self):
		#Create label and entry widgets which will be filled with the calculated parameters

		#Create D3 Label
		self.d3_lbl = Label(self, text = "Reciever to Barrier Dist (D3): ")
		self.d3_lbl.grid(row = 5, column = 0, sticky = E)
		#Create D3 entry
		self.d3_ent = Entry(self, justify = CENTER)
		self.d3_ent.grid(row = 5, column = 1)

		#Create D4 Label
		self.d4_lbl = Label(self, text = "Direct Line Distance (D4): ")
		self.d4_lbl.grid(row = 5, column = 2, sticky = E)
		#Create D4 entry
		self.d4_ent = Entry(self, justify = CENTER)
		self.d4_ent.grid(row = 5, column = 3)

		#Create D5 Label
		self.d5_lbl = Label(self, text = "D5: ")
		self.d5_lbl.grid(row = 5, column = 4, sticky = E)
		#Create D5 entry
		self.d5_ent = Entry(self, justify = CENTER)
		self.d5_ent.grid(row = 5, column = 5)

		#Create D6 Label
		self.d6_lbl = Label(self, text = "D6: ")
		self.d6_lbl.grid(row = 5, column = 6, sticky = E)
		#Create D6 entry
		self.d6_ent = Entry(self, justify = CENTER)
		self.d6_ent.grid(row = 5, column = 7)

	def calc_paras(self):
		#Retrieve the barrier parameters defined above and calculate the missing parameters
		# Retrieve parameters
		barrier_ht = float(self.barrier_ht_ent.get())
		source_ht = float(self.source_ht_ent.get())
		receive_ht = float(self.receive_ht_ent.get())
		d1 = float(self.d1_ent.get())
		d2 = float(self.d2_ent.get())

		#calculate remaining parameters
		d3 = d1 - d2
		d4 = sqrt( d1**2 + (source_ht - receive_ht)**2 )
		d5 = sqrt( d3**2 + (barrier_ht - receive_ht)**2 )
		d6 = sqrt( d2**2 + (barrier_ht - source_ht)**2 )

		# Fill the remaining parameters entry widgets with the calculated parameters
		# Fill D3
		self.d3_ent.delete(0, END)
		self.d3_ent.insert(0, round(d3, 2))
		# Fill D4
		self.d4_ent.delete(0, END)
		self.d4_ent.insert(0, round(d4, 2))		
		# Fill D5
		self.d5_ent.delete(0, END)
		self.d5_ent.insert(0, round(d5, 2))
		# Fill D6
		self.d6_ent.delete(0, END)
		self.d6_ent.insert(0, round(d6, 2))	

		return barrier_ht, source_ht, receive_ht, d1, d2, d3, d4, d5, d6

	def create_barrier_calc_widgets(self):
		# Create label and entry widgets to be filled with the calculated attenuation factors, corrected spectrum, and a-weighted corrected spectrum. Also create a button for initiating the calculation.
		#Create calculation button
		self.calc_atten_bttn = Button(self, text = "Calculate Barrier Attenuation", command = self.calc_atten)
		self.calc_atten_bttn.grid(row = 6, column = 0, columnspan = 8)

		# Create labels and entry widgets for octave band attenuation 
		#Create 63 Hz Label
		self.atten_63_lbl = Label(self, text = "63 Hz")
		self.atten_63_lbl.grid(row = 7, column = 0)
		#Create 63 Hz entry
		self.atten_63_ent = Entry(self, justify = CENTER)
		self.atten_63_ent.grid(row = 8, column = 0)

		#Create 125 Hz Label
		self.atten_125_lbl = Label(self, text = "125 Hz")
		self.atten_125_lbl.grid(row = 7, column = 1)
		#Create 125 Hz entry
		self.atten_125_ent = Entry(self, justify = CENTER)
		self.atten_125_ent.grid(row = 8, column = 1)

		#Create 250 Hz Label
		self.atten_250_lbl = Label(self, text = "250 Hz")
		self.atten_250_lbl.grid(row = 7, column = 2)
		#Create 250 Hz entry
		self.atten_250_ent = Entry(self, justify = CENTER)
		self.atten_250_ent.grid(row = 8, column = 2)		

		#Create 500 Hz Label
		self.atten_500_lbl = Label(self, text = "500 Hz")
		self.atten_500_lbl.grid(row = 7, column = 3)
		#Create 500 Hz entry
		self.atten_500_ent = Entry(self, justify = CENTER)
		self.atten_500_ent.grid(row = 8, column = 3)
	
		#Create 1000 Hz Label
		self.atten_1000_lbl = Label(self, text = "1000 Hz")
		self.atten_1000_lbl.grid(row = 7, column = 4)
		#Create 1000 Hz entry
		self.atten_1000_ent = Entry(self, justify = CENTER)
		self.atten_1000_ent.grid(row = 8, column = 4)

		#Create 2000 Hz Label
		self.atten_2000_lbl = Label(self, text = "2000 Hz")
		self.atten_2000_lbl.grid(row = 7, column = 5)
		#Create 2000 Hz entry
		self.atten_2000_ent = Entry(self, justify = CENTER)
		self.atten_2000_ent.grid(row = 8, column = 5)
		
		#Create 4000 Hz Label
		self.atten_4000_lbl = Label(self, text = "4000 Hz")
		self.atten_4000_lbl.grid(row = 7, column = 6)
		#Create 4000 Hz entry
		self.atten_4000_ent = Entry(self, justify = CENTER)
		self.atten_4000_ent.grid(row = 8, column = 6)

		#Create 8000 Hz Label
		self.atten_8000_lbl = Label(self, text = "8000 Hz")
		self.atten_8000_lbl.grid(row = 7, column = 7)
		#Create 8000 Hz entry
		self.atten_8000_ent = Entry(self, justify = CENTER)
		self.atten_8000_ent.grid(row = 8, column = 7)

	def create_results_widgets(self):
		# Create entry widgets for the octave band corrected linear results
		#Create 63 Hz entry
		self.hz63_res_ent = Entry(self, justify = CENTER)
		self.hz63_res_ent.grid(row = 9, column = 0)

		#Create 125 Hz entry
		self.hz125_res_ent = Entry(self, justify = CENTER)
		self.hz125_res_ent.grid(row = 9, column = 1)

		#Create 250 Hz entry
		self.hz250_res_ent = Entry(self, justify = CENTER)
		self.hz250_res_ent.grid(row = 9, column = 2)

		#Create 500 Hz entry
		self.hz500_res_ent = Entry(self, justify = CENTER)
		self.hz500_res_ent.grid(row = 9, column = 3)

		#Create 1000 Hz entry
		self.hz1000_res_ent = Entry(self, justify = CENTER)
		self.hz1000_res_ent.grid(row = 9, column = 4)

		#Create 2000 Hz entry
		self.hz2000_res_ent = Entry(self, justify = CENTER)
		self.hz2000_res_ent.grid(row = 9, column = 5)

		#Create 4000 Hz entry
		self.hz4000_res_ent = Entry(self, justify = CENTER)
		self.hz4000_res_ent.grid(row = 9, column = 6)

		#Create 8000 Hz entry
		self.hz8000_res_ent = Entry(self, justify = CENTER)
		self.hz8000_res_ent.grid(row = 9, column = 7)

		# Create A- weighted results widgets
		#Create 63 Hz entry
		self.hz63_ares_ent = Entry(self, justify = CENTER)
		self.hz63_ares_ent.grid(row = 10, column = 0)

		#Create 125 Hz entry
		self.hz125_ares_ent = Entry(self, justify = CENTER)
		self.hz125_ares_ent.grid(row = 10, column = 1)

		#Create 250 Hz entry
		self.hz250_ares_ent = Entry(self, justify = CENTER)
		self.hz250_ares_ent.grid(row = 10, column = 2)

		#Create 500 Hz entry
		self.hz500_ares_ent = Entry(self, justify = CENTER)
		self.hz500_ares_ent.grid(row = 10, column = 3)

		#Create 1000 Hz entry
		self.hz1000_ares_ent = Entry(self, justify = CENTER)
		self.hz1000_ares_ent.grid(row = 10, column = 4)

		#Create 2000 Hz entry
		self.hz2000_ares_ent = Entry(self, justify = CENTER)
		self.hz2000_ares_ent.grid(row = 10, column = 5)

		#Create 4000 Hz entry
		self.hz4000_ares_ent = Entry(self, justify = CENTER)
		self.hz4000_ares_ent.grid(row = 10, column = 6)

		#Create 8000 Hz entry
		self.hz8000_ares_ent = Entry(self, justify = CENTER)
		self.hz8000_ares_ent.grid(row = 10, column = 7)

		#Create total A-weighted level entry
		self.total_a_weight_ent = Entry(self, justify = CENTER)
		self.total_a_weight_ent.grid(row = 10, column = 8)


	def calc_atten(self):
		# Calculate the octave band total attenuation

		# Recall values calculated in the calc_paras function
		barrier_ht, source_ht, receive_ht, d1, d2, d3, d4, d5, d6 = self.calc_paras()
		
		# Calculate distance correction
		dist_corr = -20 * log(d4 * 0.3048, 10) - 8 		#NOTE: Hemispherical and SWL only. ADD options and if statements for other directivity and SPL

		# Calculate octave band barrier attenuation
		c_sound = 1125
		PLD = (d5 + d6) - d4 		#PLD == Path Length Difference

		#Calculat Fresnel numbers for each octave band
		wavelength_63 = c_sound / 63
		fresnel_63 = (2 / wavelength_63) * PLD
		
		wavelength_125 = c_sound / 125
		fresnel_125 = (2 / wavelength_125) * PLD
		
		wavelength_250 = c_sound / 250
		fresnel_250 = (2 / wavelength_250) * PLD
		
		wavelength_500 = c_sound / 500
		fresnel_500 = (2 / wavelength_500) * PLD
		
		wavelength_1000 = c_sound / 1000
		fresnel_1000 = (2 / wavelength_1000) * PLD
		
		wavelength_2000 = c_sound / 2000
		fresnel_2000 = (2 / wavelength_2000) * PLD
		
		wavelength_4000 = c_sound / 4000
		fresnel_4000 = (2 / wavelength_4000) * PLD
		
		wavelength_8000 = c_sound / 8000
		fresnel_8000 = (2 / wavelength_8000) * PLD

		# Calculate Barrier Attenuation using Harris  method
		# k_met = exp( - (1 / 2000) * sqrt( (d5 * d6) / (2 * PLD)) ) 	# Correction for favourable conditions from ISO 9613
		k_met = 1

		atten_63 = 10 * log(3 + (10 * fresnel_63 * k_met), 10)
		total_atten_63 = dist_corr - atten_63

		atten_125 = 10 * log( 3 + (10 * fresnel_125 * k_met), 10 )
		total_atten_125 = dist_corr - atten_125

		atten_250 = 10 * log( 3 + (10 * fresnel_250 * k_met), 10 )
		total_atten_250 = dist_corr - atten_250

		atten_500 = 10 * log( 3 + (10 * fresnel_500 * k_met), 10 )
		total_atten_500 = dist_corr - atten_500

		atten_1000 = 10 * log( 3 + (10 * fresnel_1000 * k_met), 10 )
		total_atten_1000 = dist_corr - atten_1000

		atten_2000 = 10 * log( 3 + (10 * fresnel_2000 * k_met), 10 )
		total_atten_2000 = dist_corr - atten_2000

		atten_4000 = 10 * log( 3 + (10 * fresnel_4000 * k_met), 10 )
		total_atten_4000 = dist_corr - atten_4000		

		atten_8000 = 10 * log( 3 + (10 * fresnel_8000 * k_met), 10 )
		total_atten_8000 = dist_corr - atten_8000													


		# Insert into the waiting entry widgets
		self.atten_63_ent.delete(0, END)
		self.atten_63_ent.insert(0, round(total_atten_63, 2))

		self.atten_125_ent.delete(0, END)
		self.atten_125_ent.insert(0, round(total_atten_125, 2))

		self.atten_250_ent.delete(0, END)
		self.atten_250_ent.insert(0, round(total_atten_250, 2))

		self.atten_500_ent.delete(0, END)
		self.atten_500_ent.insert(0, round(total_atten_500, 2))

		self.atten_1000_ent.delete(0, END)
		self.atten_1000_ent.insert(0, round(total_atten_1000, 2))

		self.atten_2000_ent.delete(0, END)
		self.atten_2000_ent.insert(0, round(total_atten_2000, 2))

		self.atten_4000_ent.delete(0, END)
		self.atten_4000_ent.insert(0, round(total_atten_4000, 2))

		self.atten_8000_ent.delete(0, END)
		self.atten_8000_ent.insert(0, round(total_atten_8000, 2))

		#Calculate linear results and insert into waiting widgets
		source_63 = float(self.hz63_ent.get())
		lin_res_63 = source_63 + total_atten_63
		self.hz63_res_ent.delete(0, END)
		self.hz63_res_ent.insert(0, round(lin_res_63, 2))

		source_125 = float(self.hz125_ent.get())
		lin_res_125 = source_125 + total_atten_125
		self.hz125_res_ent.delete(0, END)
		self.hz125_res_ent.insert(0, round(lin_res_125, 2))

		source_250 = float(self.hz250_ent.get())
		lin_res_250 = source_250 + total_atten_250
		self.hz250_res_ent.delete(0, END)
		self.hz250_res_ent.insert(0, round(lin_res_250, 2))

		source_500 = float(self.hz500_ent.get())
		lin_res_500 = source_500 + total_atten_500
		self.hz500_res_ent.delete(0, END)		
		self.hz500_res_ent.insert(0, round(lin_res_500, 2))

		source_1000 = float(self.hz1000_ent.get())
		lin_res_1000 = source_1000 + total_atten_1000
		self.hz1000_res_ent.delete(0, END)
		self.hz1000_res_ent.insert(0, round(lin_res_1000, 2))

		source_2000 = float(self.hz2000_ent.get())
		lin_res_2000 = source_2000 + total_atten_2000
		self.hz2000_res_ent.delete(0, END)
		self.hz2000_res_ent.insert(0, round(lin_res_2000, 2))

		source_4000 = float(self.hz4000_ent.get())
		lin_res_4000 = source_4000 + total_atten_4000
		self.hz4000_res_ent.delete(0, END)
		self.hz4000_res_ent.insert(0, round(lin_res_4000, 2))

		source_8000 = float(self.hz8000_ent.get())
		lin_res_8000 = source_8000 + total_atten_8000
		self.hz8000_res_ent.delete(0, END)
		self.hz8000_res_ent.insert(0, round(lin_res_8000, 2))

		# Apply A-weighting
		a_weighting = [26.2, 16.1, 8.6, 3.2, 0, -1.2, -1, 1.1]
		
		ares_63 = lin_res_63 - a_weighting[0]
		self.hz63_ares_ent.delete(0, END)
		self.hz63_ares_ent.insert(0, round(ares_63, 2))

		ares_125 = lin_res_125 - a_weighting[1]
		self.hz125_ares_ent.delete(0, END)
		self.hz125_ares_ent.insert(0, round(ares_125, 2))		

		ares_250 = lin_res_250 - a_weighting[2]
		self.hz250_ares_ent.delete(0, END)
		self.hz250_ares_ent.insert(0, round(ares_250, 2))		

		ares_500 = lin_res_500 - a_weighting[3]
		self.hz500_ares_ent.delete(0, END)
		self.hz500_ares_ent.insert(0, round(ares_500, 2))		

		ares_1000 = lin_res_1000 - a_weighting[4]
		self.hz1000_ares_ent.delete(0, END)
		self.hz1000_ares_ent.insert(0, round(ares_1000, 2))		

		ares_2000 = lin_res_2000 - a_weighting[5]
		self.hz2000_ares_ent.delete(0, END)
		self.hz2000_ares_ent.insert(0, round(ares_2000, 2))		

		ares_4000 = lin_res_4000 - a_weighting[6]
		self.hz4000_ares_ent.delete(0, END)
		self.hz4000_ares_ent.insert(0, round(ares_4000, 2))		

		ares_8000 = lin_res_8000 - a_weighting[7]
		self.hz8000_ares_ent.delete(0, END)
		self.hz8000_ares_ent.insert(0, round(ares_8000, 2))		

		#Calculate total, a-weighted level
		total_a_weight = 10 * log( 10**(ares_63/10) + 10**(ares_125/10) + 10**(ares_250/10) + 10**(ares_500/10) + 10**(ares_1000/10) + 10**(ares_2000/10) + 10**(ares_4000/10) + 10**(ares_8000/10), 10)
		self.total_a_weight_ent.delete(0, END)
		self.total_a_weight_ent.insert(0, round(total_a_weight, 2))

#main
root = Tk()
root.title("Barrier Attenuation")

app = Application(root)

root.mainloop()
