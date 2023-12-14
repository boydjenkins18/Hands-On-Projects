from tkinter import *
import bcrypt

root = Tk()
canvas = Canvas(root,width=400,height=300)
canvas.pack()

title_label = Label(root,text="Enter a valid password",fg="white",font=("Arial",20))
canvas.create_window(200,100,window=title_label)

password_entry = Entry(show="*")
canvas.create_window(200,140,window=password_entry)

button = Button(text="validate",command=lambda:validate(password_entry.get()))
canvas.create_window(200,170,window=button)


def validate(password):

    my_password = b"password"
    hash = bcrypt.hashpw(my_password,bcrypt.gensalt())

    #print(hash) #to check hashed password

    password = bytes(password,encoding="utf-8")

    if bcrypt.checkpw(password,hash):
        valid_label = Label(root, text="Password is valid", fg="green", font=("Arial", 20))
        canvas.create_window(200, 210, window=valid_label)
    else:
        invalid_label = Label(root, text="Invalid password", fg="red", font=("Arial", 20))
        canvas.create_window(200, 210, window=invalid_label)

    password_entry.delete(0,END)

root.mainloop()