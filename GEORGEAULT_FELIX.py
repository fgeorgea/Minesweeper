### -------------------------------------------- ###
### This code was written by Felix Georgeault
### Date: 15/11/2023
### Little minesweeper game
### -------------------------------------------- ###

### Import section
import random

### Macros
BOMB_FILE = "bombes.txt"
DEFAULT = 0
EASY = 1
HARD = 2

### Print functions
def	print_round_informations(round_number, spots_to_discover, difficulty):
	print("\n-- Round ", round_number, " --", sep="")
	print("--> You still have ", spots_to_discover, " spots to discover\n", sep="")
	if difficulty == HARD and round_number != 1:
		print("!!! Bombs have been swapped !!!\n")

def	print_welcome_message():
	print("---")
	print("Welcome to Felix's minesweeper game")
	print("Find all hidden spots without landing on bombs, good luck !")
	print("---\n")

def	print_number_bombs(difficulty, grid_size, bomb_spots):
	nbr_bombs = (grid_size ** 2) // 5
	if difficulty == DEFAULT:
		difficulty_str = "default grid"
		nbr_bombs = len(bomb_spots)
	elif difficulty == EASY:
		difficulty_str = "easy"
	else:
		difficulty_str = "hard"
	print("You are playing in", difficulty_str, "mode, there is/are", nbr_bombs, "hidden bomb(s).\n")

def	print_first_row(size):
	print(" " * 3, end="")
	for i in range(size):
		if i + 1 < 10:
			print(" " * 3, i + 1, " " * 2, sep="", end="")
		else:
			print(" " * 3, i + 1, " ", sep="", end="")
	print(" ", end="")

def	print_row_separator(size):
	print()
	print(" " * 3, end="")
	for i in range(size):
		print("-" * 6, end="")
	print("-")

def	print_row(size, letter, empty_spots):
	print(" ", chr(letter), " ", sep="", end="")
	for i in range(size):
		print("|  ", end="")
		tmp_coord = (letter - ord('A'), i)
		if tmp_coord in empty_spots:
			print(empty_spots[tmp_coord], end="")
		else:
			print("*", end="")
		print("  ", end="")
	print("|", end="")

def	print_grid(size, empty_spots):
	print_first_row(size)
	for i in range(size):
		print_row_separator(size)
		print_row(size, ord('A') + i, empty_spots)
	print_row_separator(size)

def	print_endgame_message(is_dead, nbr_bombs):
	if is_dead:
		print("BOOM BADABOOM ! Maybe you'll have more luck next time...")
	else:
		if difficulty == DEFAULT:
			difficulty_str = "default grid"
		elif difficulty == EASY:
			difficulty_str = "easy"
		else:
			difficulty_str = "hard"
		if nbr_bombs == 0:
			print("Well of course you won, there was no bomb...haha got you :p")
		else:
			print("Well done, you beat the game in", difficulty_str, "difficulty! You can start the game again and maybe try another one")

### Boolean functions (useful to use in conditions)
def	has_adjecent_bomb(coord, bombs):
	has_adjecent_bomb = False
	if (coord[0], coord[1] - 1) in bombs or (coord[0] - 1, coord[1]) in bombs or (coord[0], coord[1] + 1) in bombs or (coord[0] + 1, coord[1]) in bombs:
		has_adjecent_bomb = True
	return has_adjecent_bomb

def	is_corner(coord, grid_size):
	is_corner = False
	if coord == (0, 0) or coord == (0, grid_size - 1) or coord == (grid_size - 1, 0) or coord == (grid_size - 1, grid_size - 1):
		is_corner = True
	return is_corner

### Read or random generation functions
def	read_bombs_from_file(grid_size):
	bombs_positions = {}
	try:
		bomb_file = open(BOMB_FILE)
		lines = bomb_file.readlines()
		for line in lines:
			tmp = line.split(",")
			x = int(tmp[0])
			y = int(tmp[1][:1]) # Here we get rid of the '\n'
			if not is_corner((x, y), grid_size):
				bombs_positions[(x, y)] = 'B'
	except:
		print("\nNo file 'bombes.txt' was found, bombs will be randomly generated\n")
		bombs_positions = generate_bomb_spots(grid_size)
	return bombs_positions

def	generate_random_coord(grid_size):
	x = random.randint(0, grid_size - 1)
	y = random.randint(0, grid_size - 1)
	return x, y

def	generate_bomb_spots(grid_size):
	bomb_spots = {}
	max = grid_size - 1
	nbr_bombs = (grid_size ** 2) // 5
	while nbr_bombs != len(bomb_spots):
		tmp_coord = generate_random_coord(grid_size)
		if not tmp_coord in bomb_spots and not is_corner(tmp_coord, grid_size):
			bomb_spots[tmp_coord] = 'B'
	return bomb_spots

def	regenerate_bomb_spots(bomb_spots, empty_spots, grid_size):
	nbr_bombs = len(bomb_spots)
	for bomb in bomb_spots:
		empty_spots[bomb] = "*"
	bomb_spots.clear()
	while len(bomb_spots) != nbr_bombs:
		tmp_coord = generate_random_coord(grid_size)
		if (tmp_coord in empty_spots) and (not is_corner(tmp_coord, grid_size)) and (empty_spots[tmp_coord] == "*"):
			bomb_spots[tmp_coord] = 'B'
			del empty_spots[tmp_coord]

def	update_discovered_spots(bomb_spots, empty_spots):
	for spot in empty_spots:
		if empty_spots[spot] != "*":
			if count_adjacent_bombs(spot, bomb_spots) > 0:
				empty_spots[spot] = count_adjacent_bombs(spot, bomb_spots)
			else:
				empty_spots[spot] = " "

### Functions that require player's input
def	try_input(is_int):
	input_value = -1
	try:
		if is_int:
			input_value = int(input())
		else:
			input_value = ord(input())
	except:
		print("\n--- Numeric argument required ---\n")
	return input_value

def	choose_difficulty():
	difficuly_choice = -1
	while difficuly_choice < DEFAULT or difficuly_choice > HARD:
		print("To choose your difficulty:\n\n- Enter 0 (default grid)\n\n- Enter 1 (easy)\n\n- Enter 2 (hard)\n\nYour choice: ", end="")
		difficuly_choice = try_input(True)
	return difficuly_choice

def	choose_grid_size():
	grid_size = 0
	while grid_size < 1 or grid_size > 26:
		print("\nChoose the grid's size by entering a number between 1 and 26: ", end="")
		grid_size = try_input(True)
	return grid_size

def	choose_coordinates(size):
	y = -1
	while y < 1 or y > size:
		print("Choose column (between 1 and ", size, "): ", sep="", end="")
		y = try_input(True)
	x = -1
	while x < ord('A') or x > (ord('A') + size - 1):
		print("Choose row (between A and ", chr(ord('A') + size - 1), "): ", sep="", end="")
		x = try_input(False)
	return x - ord('A'), y - 1

### Count functions
def	count_adjacent_bombs(coord, bombs):
	adjacent_bombs = 0
	if (coord[0], coord[1] - 1) in bombs:
		adjacent_bombs += 1
	if (coord[0] - 1, coord[1]) in bombs:
		adjacent_bombs += 1
	if (coord[0], coord[1] + 1) in bombs:
		adjacent_bombs += 1
	if (coord[0] + 1, coord[1]) in bombs:
		adjacent_bombs += 1
	return adjacent_bombs

def	count_spot_to_discover(empty_spots):
	spots_to_discover = 0
	for spot in empty_spots:
		if empty_spots[spot] == "*":
			spots_to_discover += 1
	return spots_to_discover

### Creates a new dictionnary with all the (non bombs) spots initalized with the value *
def	save_empty_spots(size, bombs):
	empty_spots = {}
	for i in range(size):
		for j in range(size):
			if not (i, j) in bombs:
				empty_spots[(i, j)] = '*'
	return empty_spots

def	change_neighboring_spots(coord, empty_spots, bomb_spots):
	for i in range(3):
		for j in range(3):
			tmp_coord = coord[0] - 1 + i, coord[1] - 1 + j
			if tmp_coord in empty_spots and count_adjacent_bombs(tmp_coord, bomb_spots) > 0:
				empty_spots[tmp_coord] = count_adjacent_bombs(tmp_coord, bomb_spots)
			elif tmp_coord in empty_spots and count_adjacent_bombs(tmp_coord, bomb_spots) <= 0:
				empty_spots[tmp_coord] = " "

# Initializing settings and main variables
print_welcome_message()
difficulty = choose_difficulty()
if difficulty == DEFAULT:
	grid_size = 9
	bomb_spots = read_bombs_from_file(grid_size)
else:
	grid_size = choose_grid_size()
	bomb_spots = generate_bomb_spots(grid_size)
print_number_bombs(difficulty, grid_size, bomb_spots)
empty_spots = save_empty_spots(grid_size, bomb_spots)
spots_to_discover = count_spot_to_discover(empty_spots)
is_dead = False
round_number = 1

### Main game loop
while is_dead == False and spots_to_discover > 0:
	print_grid(grid_size, empty_spots)
	print_round_informations(round_number, spots_to_discover, difficulty)
	x, y = choose_coordinates(grid_size)
	if (x, y) in bomb_spots:
		is_dead = True
	if has_adjecent_bomb((x, y), bomb_spots):
		empty_spots[(x, y)] = count_adjacent_bombs((x, y), bomb_spots)
	else:
		change_neighboring_spots((x, y), empty_spots, bomb_spots)
	if difficulty == HARD:
		regenerate_bomb_spots(bomb_spots, empty_spots, grid_size)
		update_discovered_spots(bomb_spots, empty_spots)
	spots_to_discover = count_spot_to_discover(empty_spots)
	round_number += 1

### End message
print_endgame_message(is_dead, (grid_size**2)//5)