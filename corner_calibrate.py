'''
sudo apt-get install python-tk
sudo apt-get install python-imaging
sudo apt-get install python-imaging-tk
pip install Pillow
'''

from Tkinter import *
from tkFileDialog import askopenfilename
from PIL import Image, ImageTk
import sys

if __name__ == "__main__":
    counter = 0

    root = Tk()

    corners_file = file('corners.txt', 'w')
    corners_string = ''

    #fn = '/home/vctr/Dropbox/_UNSW/Robocup/vctr_field_transform/testphotosat1340.JPG'
    # fn = '/Users/Martin/Github/RSA-Major-Project-2016/field_image_colour_cal_2.JPG'
    fn = '/home/rsa/RSA-Major-Project-2016/calibrationphoto.jpg'
    # fn = './' + sys.argv[1]
    size = Image.open(fn).size

    #setting up a tkinter canvas with scrollbars
    frame = Frame(root, bd=2, relief=SUNKEN)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    xscroll = Scrollbar(frame, orient=HORIZONTAL)
    xscroll.grid(row=1, column=0, sticky=E+W)
    yscroll = Scrollbar(frame)
    yscroll.grid(row=0, column=1, sticky=N+S)
    canvas = Canvas(frame, width=size[0], height=size[1], bd=0, xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
    canvas.grid(row=0, column=0, sticky=N+S+E+W)
    xscroll.config(command=canvas.xview)
    yscroll.config(command=canvas.yview)
    frame.pack(fill=BOTH,expand=1)

    #adding the image
    #File = askopenfilename(parent=root, initialdir="C:/",title='Choose an image.')
    img = ImageTk.PhotoImage(Image.open(fn))
    canvas.create_image(0,0,image=img,anchor="nw")
    canvas.config(scrollregion=canvas.bbox(ALL))

    #function to be called when mouse is clicked
    def printcoords(event):
        #outputting x and y coords to console
        global counter
        global corners_string

        corners_string += str(event.x) + ',' + str(event.y) + '|'
        counter += 1
        if counter == 4:
            corners_file.write(corners_string[:-1])
            root.destroy()

    #mouseclick event
    canvas.bind("<Button 1>",printcoords)

    root.mainloop()
