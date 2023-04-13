from tkinter import *
import pandas
import random
BACKGROUND_COLOR = "#B1DDC6"
random_pick ={}
word_list = {}

#_________________ Initialize Pandas, Read CSV file & Convert it to a list of dicitionaries __________________________

try:
  data = pandas.read_csv('data/word_toLearn.csv')
except FileNotFoundError:
  origina_data = pandas.read_csv('data\french_words.csv')
  word_list = origina_data.to_dict(orient='records')
# word_list = [{row['French']: row['English']} for index, row in data.iterrows()]
else:
  word_list = data.to_dict(orient="records")


#__________________ Randomly Choose a dicitionary __________________

def random_choice():
  global random_pick, flip_timer
  window.after_cancel(flip_timer)
  random_pick = random.choice(word_list)
  
  french = list(random_pick.keys())[0]
  word = random_pick[french]
  
  canvas.itemconfig(language, text= f'{french}', fill= 'black')
  canvas.itemconfig(translation, text= f'{word}', fill= 'black')
  canvas.itemconfig(card_background, image= white_card)
  flip_timer = window.after(3000, func=flip_card)
  
  
#________________________________________________________

def flip_card():
  canvas.itemconfig(language, text= 'English', fill= 'white')
  canvas.itemconfig(translation, text= random_pick['English'], fill= 'white')
  canvas.itemconfig(card_background, image= green_card)
  
def is_known():
  word_list.remove(random_pick)
  data = pandas.DataFrame(word_list)
  data.to_csv('data/word_toLearn.csv', index= False)
  random_choice()

# _________________ GUI SETUP __________________________________

window = Tk()
window.title('Flash Card')
window.minsize(600, 400)
window.config(background= BACKGROUND_COLOR, padx=50, pady=50)



flip_timer = window.after(3000, func=flip_card)

white_card = PhotoImage(file='images\card_front.png')
green_card = PhotoImage(file='images\card_back.png')
unchecked_button = PhotoImage(file='images\wrong.png')
checked_button = PhotoImage(file='images/right.png')

# Canvas
canvas = Canvas(width=800, height=526, background= BACKGROUND_COLOR, highlightthickness=0)
card_background = canvas.create_image(410, 276, image= white_card)
language = canvas.create_text(420, 150, text= 'Title', fill='black', font=('arial', 25, 'bold'))
translation = canvas.create_text(420, 300, text= 'Word', fill='black', font=('arial', 35, 'bold'))
timer = canvas.create_text(420,50, text= '00', fill='black', font=('arial', 15, 'bold'))
canvas.grid(column=0, row=0, columnspan=2)

#Button
incorrect_answer = Button(image=unchecked_button, highlightthickness=0, command= random_choice)
incorrect_answer.grid(row=1, column= 0 )
incorrect_answer.config(borderwidth=0)

correct_answer = Button(image=checked_button, highlightthickness=0, command= is_known)
correct_answer.grid(row=1, column= 1 )
correct_answer.config(borderwidth=0)

random_choice()

window.mainloop()