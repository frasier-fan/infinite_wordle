from tkinter import *
import random

## Wordle has a list of valid answers and valid guesses (which does NOT include
## answers; it's just valid guesses that will never be the answer).  
## The following lines compile a list of guesses and a list of answers from 
## accompanying txt files. 

with open('guess_list.txt', 'r') as f:
  guess_list = f.read().split("\n")

with open('answer_list.txt', 'r') as f:
  answer_list = f.read().split("\n")

## Choose word from answer list

answer = list(random.choice(answer_list))

## Create list of alphabetical letters, used to to confirm button/key presses 
## are letters suitable to go on Wordle grid

alphabet = "abcdefghijklmnopqrstuvwxyz"
alphabet = list(alphabet)

## Establish initial GUI frame

root = Tk()
frame_wordle_grid = Frame(root, bg="black", padx = 20, pady = 30)
frame_keyboard_q_row = Frame(root, bg="black", padx = 41)
frame_keyboard_a_row = Frame(root, bg="black", padx = 52)
frame_keyboard_ent_row = Frame(root, bg="black", padx = 28)
bottom_blank_frame = Frame(root, bg="black", height = 100, width = 265)
bottom_blank_frame.grid_propagate(False)
bottom_blank_frame.grid_columnconfigure(0, weight = 5)
bottom_blank_frame.grid_rowconfigure(10, weight = 4)
bottom_blank_text = Label(bottom_blank_frame, text = " ",
			bg='black', fg='green')
bottom_blank_text.grid(row=10, column = 0)

row = 0
column = 0

## Establish initial variables

current_guess = [] # List that holds the letters of the current guess
current_guess_labels = [] # Holds labels of current guess to change colors on submit
all_guess_labels = [] # Holds labels of all guesses, so they can be destroyed in event of restart
key_buttons = {} # Dictionary with letters as keys and button for such letter as value

def create_letter_button(letter, location):
	"""Makes a keyboard button; when pressed, letter added to wordle grid"""
	return Button(location, text=letter, activebackground = "cyan", 
		bg="black", fg="green", 
		command=lambda: [print_letter_pressed(letter, row, column),shift_pos()])

def create_clear_button(letter, location):
	"""Makes a keyboard button; when pressed, current guess cleared"""
	global curent_guess
	return Button(location, text=letter, activebackground = "cyan", 
		bg="black", fg="green", 
		command=lambda: [clear_guess()])

def create_enter_button(letter, location):
	"""Makes a keyboard button; when pressed, current guess submitted for review"""
	return Button(location, text=letter, activebackground = "cyan", 
		bg="black", fg="green", 
		command=lambda: [submit_guess(current_guess, answer, 
			current_guess_labels)])

def create_restart_button(location):
	"""Makes a button after game over to restart"""
	return Button(location, text="Play again?", bg='grey', fg='black',
		command=lambda: [restart()])

def print_letter_pressed(letter, row, column):
	"""Prints letter on Wordle grid upon press of QWERTY board button"""
	global current_guess
	global current_guess_labels
	if letter.lower() in alphabet and len(current_guess) < 5:
		e = Label(frame_wordle_grid, text = letter, width=5, bg = "black", 
					fg = "green", justify="center", relief="ridge")
		e.grid(row=row, column=column)
		current_guess.append(letter.lower())
		current_guess_labels.append(e)
		all_guess_labels.append(e)
	else:
		pass

def print_letter_typed(event):
	"""For manual typing; prints letter on Wordle grid after typed, if it's"""
	"""in alphabet"""
	global column
	global row
	shift_flag = False
	if event.keysym.lower() in alphabet and len(current_guess) < 5:
		e = Label(frame_wordle_grid, text = event.keysym.upper(), 
					width=5, bg = "black", fg = "green",
					justify="center", relief="ridge")
		e.grid(row=row, column=column)
		shift_flag = True
		current_guess.append(event.keysym.lower())
		current_guess_labels.append(e)
		all_guess_labels.append(e)
	else:
		pass
	if shift_flag == True:
		shift_pos()

def shift_pos():
	"""Shifts to next cell in Wordle grid"""
	global column
	if column == 4:
		pass
	else:
		column += 1

def clear_guess():
	"""Clears out current guess, both on-screen and the letter & label lists"""
	global current_guess
	global current_guess_labels
	global column
	current_guess = []
	for label in current_guess_labels:
		label.destroy()
	current_guess_labels = []
	column = 0

def submit_guess(guess, answer, guess_labels):
	"""Checks if guess matches correct answer; if not, (1) presents as green"""
	"""each letter that is in correct spot and (2) presents as yellow each"""
	"""letter that is in word but not in correct spot"""
	global row
	global column
	global current_guess
	global current_guess_labels
	global restart_button
	if len(guess) < 5 or ("".join(guess) not in guess_list and 
		"".join(guess) not in answer_list):
		bottom_blank_text.config(text = "Invalid Answer")
		bottom_blank_text.grid(row=10, column = 0)
		clear_guess()
	if len(guess) == 5 and ("".join(guess) in guess_list or 
		"".join(guess) in answer_list):
		bottom_blank_text.config(text = " ")
		for x in range(5):
			if guess[x] == answer[x]:
				guess_labels[x].config(bg='green', fg='black')
				key_buttons[guess[x]].config(bg='green', fg='black')
			elif guess[x] != answer[x] and guess[x] in answer:
				guess_labels[x].config(bg='yellow', fg='black')
				key_buttons[guess[x]].config(bg='yellow')
			else:
				guess_labels[x].config(bg='gray', fg='black')
				key_buttons[guess[x]].config(bg='gray', fg='black')
		if guess == answer:
			bottom_blank_text.config(text = "WORDLE! SPLENDID!")
			restart_button = create_restart_button(bottom_blank_frame)
			restart_button.grid(row=11, column=0)
		else:
			if row == 6:
				printed_answer = "".join(answer)
				bottom_blank_text.config(text = f"Game Over :( \n Answer: {printed_answer}")
			else:
				row += 1
				column = 0
				current_guess = []
				current_guess_labels = []

def submit_guess_typed(event):
	submit_guess(current_guess, answer, current_guess_labels)

def clear_guess_typed(event):
	clear_guess()

def restart():
	"""Restarts game"""
	global all_guess_labels
	global answer
	global row
	global column
	global all_guess_labels
	global restart_button
	global bottom_blank_text
	for item in all_guess_labels:
		item.destroy()
	all_guess_labels = []
	clear_guess()
	for letter in qwerty_board:
		if letter != 'ENTER' and letter != 'DEL':
			key_buttons[letter.lower()].config(bg='black', fg='green')
	answer = list(random.choice(answer_list))
	row = 1
	column = 0
	bottom_blank_text.config(text="")
	restart_button.destroy()


## Create title header

title_label = Label(frame_wordle_grid,
	text="Wordle",
	font=("playbill", 32),
	bd = 16,
	background="black",
	foreground="white")

title_label.grid(row=0, column=0, columnspan=5)

## Create wordle grid

for row in range(1, 7):
	for column in range (0, 5):
		e = Label(frame_wordle_grid, width=5, bg="black", 
			relief="ridge")
		e.grid_configure(padx=2, pady=2)
		e.grid(row=row, column=column)

row = 7
column = 0
current_row = frame_keyboard_q_row 

## Create QWERTY keyboard in second, southern window

qwerty_board = ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P",
	"A", "S", "D", "F", "G", "H", "J", "K", "L", "ENTER",
	"Z", "X", "C", "V", "B", "N", "M", "DEL"]
for letter in qwerty_board:
	if letter == "A":
		current_row = frame_keyboard_a_row
	if letter == "ENTER":
		current_row = frame_keyboard_ent_row
	if letter == "DEL":
		letter_button = create_clear_button(letter, current_row)
	elif letter == "ENTER":
		letter_button = create_enter_button(letter, current_row)
	else:
		letter_button = create_letter_button(letter, current_row)
		key_buttons[letter.lower()] = letter_button
	if letter == "A":
		row += 1
		column = 0
	if letter == "ENTER":
		row += 1
		column = 0
	letter_button.grid(row=row, column=column)
	column += 1

row = 1
column = 0

root.bind('<Key>', print_letter_typed)
root.bind('<Return>', submit_guess_typed)
root.bind('<BackSpace>', clear_guess_typed)

frame_wordle_grid.pack()
frame_keyboard_q_row.pack()
frame_keyboard_a_row.pack()
frame_keyboard_ent_row.pack()
bottom_blank_frame.pack()

root.mainloop()
