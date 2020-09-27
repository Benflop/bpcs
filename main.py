import tkinter as tk
from PIL import ImageTk, Image
# To get the dialog box to open when required
from tkinter import filedialog

from bpcs.bpcs_steg_encode import *

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.btn = tk.Button(self.master, text='Browse', command=self.open_img).pack()

        self.btn = tk.Button(self.master, text='Encode', command=self.encode_image).pack()

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def open_img(self):
        # Select the Image Name from a folder
        x = self.openfilename()

        # opens the image
        img = Image.open(x)

        # resize the image and apply a high-quality down sampling filter
        img = img.resize((250, 250), Image.ANTIALIAS)

        # PhotoImage class is used to add image to widgets, icons etc
        img = ImageTk.PhotoImage(img)

        # create a label
        panel = tk.Label(root, image=img)

        # set the image as img
        panel.image = img

        panel.pack(side="left")

    def openfilename(self):
        # open file dialog box to select image
        # The dialogue box has a title "Open"
        filename = filedialog.askopenfilename(title='"pen')
        return filename

    def encode_image(self):
        #encode(x, self, self, self)
        print("Done")

root = tk.Tk()
x = ""
app = Application(master=root)
app.mainloop()