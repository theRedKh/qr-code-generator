from tkinter import *
import tkinter.font as font
import qrcode
import os
from PIL import Image

#GUI/base window
root = Tk()
root.title("QR Code Generator v1.1")

#Fonts definition
f_Entry = font.Font(size= 17, family = 'Calibri')
f_Button = font.Font(size = 15, family = 'Calibri')
f_Labels = font.Font(size = 13, family = 'Calibri')
f_messages = font.Font(size = 13, family = 'Calibri', weight = 'bold')

#Generate QR code button function
def button_generate():
    webLink = dataEntry.get()
    if webLink == "":
        flag = "Error. No text"
    elif webLink == " ":
        flag = "Error. No text"
    else:
        flag = "Complete. Proceed to save."
    global qr
    qr = qrcode.QRCode(version = 1, box_size = 5, border = 5, )
    qr.add_data(webLink)
    qr.make()
    global complete
    complete = Label(root, text = flag, fg = 'green', bg = 'black')
    complete.grid(row = 3, column = 1, columnspan = 2)
    complete['font'] = f_messages


#label
helloLabel = Label(root, text = "Hello! Welcome to QR code generator.\n To start, Enter your website link in the box below:", fg = 'red')
helloLabel.grid(row = 0, column = 0, columnspan = 4,pady = 10)

#Input box
dataEntry = Entry(root, width = 50, bg = 'white',  )
dataEntry.grid(row = 1, column = 1, columnspan = 2)

#Buttons
gButton = Button(root, text = "Generate", foreground = 'white',background= 'purple' , activebackground= 'white', borderwidth = 0.2,  padx = 30, command = button_generate)
gButton.grid(row = 2, column = 1, pady = 20, columnspan = 2 )

#File Saving
newLabel = Label(root, text=" Enter a name for your file", fg = 'purple') #Instructions for user
newLabel.grid(row = 4, column= 1, columnspan = 2, pady= 5)
newEntry = Entry(root, background = 'white', fg = 'black',) #Data entry for user
newEntry.grid(row = 5, column = 1, columnspan = 2, pady = 10)

#Command for save file
def fN_click():
    global fileName
    global qr
    fileName = newEntry.get() + ".png"
    image = qr.make_image(fill_color = 'black', back_color = 'white')
    image.save(fileName) #To change path saved, add [directory + imagename.png or imagename.jpg] in quotes
    global completed
    completed = Label(root, text = "File Saved", fg = 'green')
    completed.grid(row = 7, column = 1, columnspan = 2)
    completed['font'] = f_messages
    image.show(fileName)

#Reset function - clear everything
def reset():
    newEntry.delete(0,END)
    dataEntry.delete(0,END)
    global complete
    complete.destroy()
    global completed
    completed.destroy()

#Save File
fNButton = Button(root, text = "Save QR", foreground = 'white', background= 'purple', activebackground= 'white', borderwidth = 0.2, padx= 40, command = fN_click)
fNButton.grid(row = 6, column = 1, columnspan = 2) 

#Reset button
clrAll = Button(root,text = "Reset",foreground = 'white', bg = '#008080', activebackground= 'blue', borderwidth= 0.2, padx= 30, pady= 3, command = reset)
clrAll.grid(row = 8, column = 1, columnspan = 2, pady = 10)

#Delete File Function
def deleteFile():
    global fileName
    os.remove(fileName)
    deletedMessage = Label(root, text= "File Deleted", font = f_messages, fg = 'red')
    deletedMessage.grid(row = 9,column =1, columnspan = 2, pady= 9)
    root.after(2500,deletedMessage.destroy)

#Delete file Button
delFile = Button(root, text = "Delete File", fg= 'white', bg = '#e46a53', activebackground= '#feb7a9', borderwidth= 0.2,pady = 3, command= deleteFile)
delFile.grid(row = 10, column = 1, columnspan = 2, pady = 9)

#Choose Color 
#Apply Fonts
dataEntry['font'] = f_Entry
newEntry['font'] = f_Entry
helloLabel['font'] = f_Labels
newLabel['font'] = f_Labels
gButton['font'] = f_Button
clrAll['font'] = font.Font(size = 10, family = 'Courier')

root.mainloop()