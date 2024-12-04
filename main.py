from tkinter import *
import pandas
import random
import os

BACKGROUND_COLOR = "#B1DDC6"


QA = {}
dict_data = {}

try:
    data = pandas.read_csv(r"flash_card\flash-card-project-start\data\update_QA.csv")
except FileNotFoundError:
    original_data  = pandas.read_csv(r"flash_card\flash-card-project-start\data\c_prg.csv")
    dict_data = original_data.to_dict(orient="records")
else:
    dict_data = data.to_dict(orient="records")
    

def next_card():
    global QA
    global flip_timer
    
    if len(dict_data) == 0:  
        canvas.itemconfig(title, text="No Cards Left", fill="black")
        canvas.itemconfig(card, text="You reviewed all cards!", fill="black")
        canvas.itemconfig(back_gr, image=front_img)
        return  

    window.after_cancel(flip_timer)
    QA = random.choice(dict_data)
    canvas.itemconfig(title, text="QUESTION", fill="black")
    canvas.itemconfig(card, text=QA["Question"], fill="black")
    canvas.itemconfig(back_gr, image=front_img)
    flip_timer = window.after(4000, flip_card)

def is_know():
    global dict_data
    if len(dict_data) == 0:  
        canvas.itemconfig(title, text="No Cards Left", fill="black")
        canvas.itemconfig(card, text="You reviewed all cards!", fill="black")
        canvas.itemconfig(back_gr, image=front_img)
        try:
            os.remove(r"flash_card\flash-card-project-start\data\update_QA.csv")
        except FileNotFoundError:
            pass 
        return

    dict_data.remove(QA)
    print(len(dict_data))
    data = pandas.DataFrame(dict_data)
    data.to_csv(r"flash_card\flash-card-project-start\data\update_QA.csv", index=False)
    
    next_card()
 
    
def flip_card():
    canvas.itemconfig(title, text="ANSWER")
    canvas.itemconfig(card, text=QA["Answer"])
    canvas.itemconfig(back_gr, image=back_img)
    


window = Tk()

window.title("CODIFY")
window.config(padx = 50, pady=50, bg = BACKGROUND_COLOR)

canvas = Canvas(width=800, height=526)
front_img = PhotoImage(file=r"flash_card\flash-card-project-start\images\card_front.png")
back_img = PhotoImage(file=r"flash_card\flash-card-project-start\images\card_back.png")

back_gr = canvas.create_image(400, 263, image=front_img)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
title = canvas.create_text(400, 150, text="", font=("arial",20,"italic"))
card = canvas.create_text(400, 263, text="", font=("arial",30,"bold"))
canvas.grid(row=0, column=0, columnspan=2)

cross_img = PhotoImage(file=r"flash_card\flash-card-project-start\images\wrong.png")
cross_button = Button(image=cross_img, highlightthickness=0, command=next_card)
cross_button.grid(row=1, column=0)

tick_img = PhotoImage(file=r"flash_card\flash-card-project-start\images\right.png")
tick_button = Button(image=tick_img, highlightthickness=0, command=is_know)
tick_button.grid(row=1, column=1)

flip_timer = window.after(4000, flip_card)
next_card()

window.mainloop()




