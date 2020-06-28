

README...

Once python 3 is installed


INSTALLS::

pip install pandas
pip install pulp
pip install matplotlib
pip install ast?



from inside this folder run the following script but for the appropriate seat map file

run ::
 python seat_optimizer.py "hurricanes_xy_coordinates.csv" 36 [2] [1] "section" 500 "not_normal"

* python - to run it in python
* seat_optimizer.py - seat_optimizer (program)
* "hurricanes_xy_coordinates.csv" - original seat map with 'section_label', 'row_label', 'seat_num', 'seat_center_x', 'seat_center_y', 'venuesid', 'seatsid' 
					- seatsid = concatenation of venue, section, row, seat number
					
* 36 - threshold (36 units based on KORE map is about 6 feet)
* [2] - array of seat cluster sizes, without more compute, one size should be chosen
* [1] - array of seat cluster percentages, 100% if one size chosen
* "section" - algorithm breakdown, optimized based on section is the preferred way
* 500 - time limit for optimization, less time will only produce a feasible seat selection if optimization is too difficult (gap set to .01)
* "not_normal" - seat ordering, not_normal is typical, but some seats are ordered correctly in each row with no gaps




while running:
  
- the algorithm first creates an appropriate seat map by breaking up rows where there are gaps 
	- (this new map is saved under Row Adjusted Arena)
- then the algorithm creates clusters within rows (requiring only people who adjacent to sit next to each other, instead of in front of or behind)
	- if there are 3 seats in a row, 1, 2, and 3...and clusters are 2 people, then there are two clusters created from that row either 1-2 or 2-3
	- (these clusters are saved per section in Seating Segments)
- the program then creates distances to and from each seat cluster
	- (these distances are saved in Distances)
- then the program optimizes each section
	- (an optimization program output file is saved in LP Files, could be output to optimization server if necessary for larger sections (or in MPS format))
- then these files are aggregated as indicated seats
	- (the progress file and final files are saved in Final Seat Map)
- then a map is printed (for Windows, dpi = 300 is set, but larger can be used for mac, from experience)
	- (this map is found in Images)




to do maybe::
		
		
	add list of already designated seats?

if any questions feel free to reach out to christopherm@carolinahurricanes.com
