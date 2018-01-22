from random import randint
from math import floor
from graphics import *

canvas_height = 400
canvas_width = 400
window = GraphWin("Minesweeper", canvas_height+1, canvas_width+1)

rows = 16
cols = 16
s = canvas_height / rows
cells = []

def game_over():
	for i in range(0, cols):
		for j in range(0, rows):
			if cells[i][j].mine == True:
				p1 = Point(cells[i][j].i * s, cells[i][j].j * s)
				p2 = Point(cells[i][j].i * s + s, cells[i][j].j * s + s)
				rect = Rectangle(p1, p2)
				rect.setFill('pink')
				rect.draw(window)
				
				center = Point(cells[i][j].i * s + s / 2, cells[i][j].j * s + s / 2)
				radius = s / 4
				circle = Circle(center, radius)
				circle.setFill('black')
				circle.draw(window)

class Cell(object):
	
	def __init__(self, i, j):
		self.i = i
		self.j = j
		self.mine = False
		self.revealed = False
		self.neighbours = 0
		
	def print_info(self):
		print "MINE(%r, %r), mine = %r" % (self.i, self.j, self.mine)
		
	def show(self):
		p1 = Point(self.i * s, self.j * s)
		p2 = Point(self.i * s + s, self.j * s + s)
		rect = Rectangle(p1, p2)
		if self.revealed == True:
			rect.setFill('grey')
		rect.draw(window)
		if self.revealed == True:
			center = Point(self.i * s + s / 2, self.j * s + s / 2)
			if self.mine == True:
				radius = s / 4
				circle = Circle(center, radius)
				circle.setFill('black')
				circle.draw(window)
				game_over()
				window.getMouse()
				window.close()
			elif self.neighbours != 0:
				string = str(self.neighbours)
				text = Text(center, string)
				text.draw(window)
				
	def check_neighbours_bombs(self):
		for i in range(-1, 2):
			for j in range(-1, 2):
				if self.i + i >= 0 and self.i + i < cols and self.j + j >= 0 and self.j + j < rows:
					if cells[self.i + i][self.j + j].mine == True:
						self.neighbours += 1
						
	def check_neighbours_zeros(self):
		for i in range(-1, 2):
			for j in range(-1, 2):
				if self.i + i >= 0 and self.i + i < cols and self.j + j >= 0 and self.j + j < rows:# and i != 0 and j != 0:
					if cells[self.i + i][self.j + j].mine == False and self.neighbours == 0 and cells[self.i + i][self.j + j].revealed == False:
						cells[self.i + i][self.j + j].revealed = True
						cells[self.i + i][self.j + j].show()
						cells[self.i + i][self.j + j].check_neighbours_zeros()
						
		
def setup_cells():

	# create a 2D array of cell objects and show them
	for i in range(0, cols):
		row = []
		for j in range(0, rows):
			new_cell = Cell(i, j)
			row.append(new_cell)
			mine_chance = randint(1,100)
			if mine_chance <= 10:
				new_cell.mine = True
			new_cell.show()
		cells.append(row)
		
	# tally each cell's neighbours that are mines
	for i in range(0, cols):
		for j in range(0, rows):
			cells[i][j].check_neighbours_bombs()
		
# Return the i and j of a cell that was clicked on
def convert_click(click_point):
	click_point_x = floor(click_point.getX() / s)
	click_point_y = floor(click_point.getY() / s)
	return int(click_point_x), int(click_point_y)
	
def check_if_won():
	flag = False
	for i in range(0, cols):
		for j in range(0, rows):
			if cells[i][j].mine == False and cells[i][j].revealed == True:
				pass
			else:
				flag == True
	if flag == False:
		print "YOU WIN"
		window.getMouse()
		window.close()
		
def main():
	setup_cells()
	
	while True:
		click_point = window.getMouse()
		clicked_i, clicked_j = convert_click(click_point)
		cells[clicked_i][clicked_j].revealed = True
		cells[clicked_i][clicked_j].show()
		if cells[clicked_i][clicked_j].neighbours == 0:
			temp = cells[clicked_i][clicked_j].check_neighbours_zeros()
		#check_if_won()
		
	
	
main()