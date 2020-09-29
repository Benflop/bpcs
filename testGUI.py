import tkinter as tk
from tkinter import filedialog, Text, PhotoImage, Image, messagebox
from PIL import ImageTk, Image
import os, threading
from bpcs.bpcs_steg_encode import *
from tkinter.ttk import Progressbar


class TestGUI():
    def __init__(self):
        self.root = tk.Tk()

        self.photo = PhotoImage(file='resources/security.png')
        self.root.iconphoto(False, self.photo)
        self.root.title('Steganographier')

        self.canvas = tk.Canvas(self.root, height=700, width=700, bg="#263D42")
        self.canvas.pack()

        self.frame = tk.Frame(self.root, bg="white")
        self.frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

        self.lblProgramName = tk.Label(text="Steganographier", font=("Helvetica", 32), bg="white")
        self.lblProgramName.place(relwidth=0.6, relheight=0.08, relx=0.2, rely=0.2)

        self.encryptPhoto = PhotoImage(file=r"resources\lock.PNG")
        self.encryptPhotoImage = self.encryptPhoto.subsample(3, 3)
        self.btnEncrypt = tk.Button(self.root, image=self.encryptPhotoImage, bg="#D3D3D3",
                               command = lambda: self.encryptFunction())

        self.btnEncrypt.place(relwidth=0.3, relheight=0.3, relx=0.15, rely=0.4)

        self.decryptphoto = PhotoImage(file=r"resources\unlock.PNG")
        self.decrypPhotoimage = self.decryptphoto.subsample(6, 6)
        self.btnDecrypt = tk.Button(self.root, image=self.decrypPhotoimage, bg="#D3D3D3")
        self.btnDecrypt.place(relwidth=0.3, relheight=0.3, relx=0.55, rely=0.4)

        self.lblDecryptText = tk.Label(text="Decrypt Image", font=("Helvetica", 16), bg="white")
        self.lblDecryptText.place(relwidth=0.2, relheight=0.08, relx=0.6, rely=0.7)

        self.lblEncryptText = tk.Label(text="Encrypt Image", font=("Helvetica", 16), bg="white")
        self.lblEncryptText.place(relwidth=0.2, relheight=0.08, relx=0.2, rely=0.7)

        self.photo = PhotoImage(file=r"resources\back.png")
        self.photoimage = self.photo.subsample(10, 10)
        self.btnBack = tk.Button(self.root, image=self.photoimage, bg="white", command = lambda: self.backFunction())
        self.btnBack.place(relwidth=0.1, relheight=0.1, relx=0.1, rely=0.1)
        self.btnBack.lower(self.frame) #make it invisible

        self.lblSelectText = tk.Label(text="Select image to encrypt:", font=("Helvetica", 16), bg="white")
        self.lblSelectText.place(relwidth=0.35, relheight=0.08, relx=0.17, rely=0.3)
        self.lblSelectText.lower(self.frame)


        self.btnFileSelect = tk.Button(self.root, text='Browse', bg="white", command = lambda: self.set_Image())
        self.btnFileSelect.place(relwidth=0.12, relheight=0.05, relx=0.52, rely=0.31)
        self.btnFileSelect.lower(self.frame)

        self.btnFileSelectInput = tk.Button(self.root, text='Browse input', bg="white", command=lambda: self.set_Input())
        self.btnFileSelectInput.place(relwidth=0.12, relheight=0.05, relx=0.52, rely=0.31)
        self.btnFileSelectInput.lower(self.frame)

        self.lblShowSelectInput = tk.Label(text="dsahjdghajs.txt", font=("Helvetica", 16), bg="white")
        self.lblShowSelectInput.place(relwidth=0.2, relheight=0.05, relx=0.52, rely=0.31)
        self.lblShowSelectInput.lower(self.frame)

        self.btnNextProcess = tk.Button(self.root, text='Next', bg="white", command = lambda: self.processing())
        self.btnNextProcess.place(relwidth=0.12, relheight=0.05, relx=0.45, rely=0.82)
        self.btnNextProcess.lower(self.frame)



        self.lblOutputFileName=tk.Label(text="Enter new file name:", font=("Helvetica", 16), bg="white")
        self.lblOutputFileName.place(relwidth=0.35, relheight=0.08, relx=0.19, rely=0.4)
        self.lblOutputFileName.lower(self.frame)

        self.textOutputFileName = tk.Entry(self.root)
        self.textOutputFileName.place(relwidth=0.25, relheight=0.04, relx=0.51, rely=0.42)
        self.textOutputFileName.lower(self.frame)
        # self.textOutputFileName.pack()
        # self.textOutputFileName.grid(row=0, column=1)

        self.fileLocation = ""
        self.outputFileName = ""
        self.encodeData = ""
        self.encrypt_state = False

        self.lblShowPanel=None
        # self.progress = Progressbar(self.root, orient="horizontal", length=100, mode='indeterminate')


        self.root.mainloop()


    def set_Input(self):
        self.encodeData=self.open_file()
        self.btnFileSelectInput.lower(self.frame)
        base = os.path.basename(self.encodeData)
        self.lblShowSelectInput['text']=base
        self.lblShowSelectInput.lift(self.frame)


    def open_file(self):
        return filedialog.askopenfilename(initialdir="/", title="Select File", filetypes=(
        ("JPEG", ".jpg"), ("png", ".png"), ("txt", ".txt"), ("all files", ".")))

    def set_Image(self):
        self.fileLocation=self.open_file()
        if self.fileLocation:
            # opens the image
            img = Image.open(self.fileLocation)
            # resize the image and apply a high-quality down sampling filter
            img = img.resize((400, 400), Image.ANTIALIAS)
            # PhotoImage class is used to add image to widgets, icons etc
            img = ImageTk.PhotoImage(img)
            # create a label
            self.lblShowPanel = tk.Label(self.root, image=img, bg="white")
            self.lblShowPanel.image = img
            self.lblShowPanel.place(relwidth=0.6, relheight=0.5, relx=0.2, rely=0.3)
            self.lblProgramName['text'] = "Photo Selected"
            self.lblSelectText.lower(self.frame)
            # self.btnFileSelect.lower(self.frame)
            self.btnNextProcess.lift(self.frame)
            self.btnFileSelectInput.lower(self.frame)

    def encoding(self):
        encode(self.fileLocation, self.encodeData, self.outputFileName)

    def processing(self):

        if self.encrypt_state:
            if self.encodeData:
                print("Well Done")
                if(self.textOutputFileName.get()):
                    # fileType=os.path(self.fileLocation).suffixes()
                    extension = os.path.splitext(self.fileLocation)[1]
                    self.outputFileName = os.path.dirname(self.fileLocation)+"/Encoded_"+self.textOutputFileName.get()+extension
                    self.encoding()
                else:
                    messagebox.showerror("Error", "Please enter a file name.")
            else:
                messagebox.showerror("Error", "Please select the encode data file")
        else:
            print("OOps")
            self.lblProgramName['text'] = "Encryption Selected"
            self.btnFileSelect.lower(self.frame)
            self.lblShowPanel.lower(self.frame)
            self.lblSelectText['text'] = "Select Input file: "
            self.lblSelectText.lift(self.frame)
            # self.btnNextProcess.lower(self.frame)
            self.btnFileSelectInput.lift(self.frame)
            self.encrypt_state=True
            self.textOutputFileName.lift(self.frame)
            self.lblOutputFileName.lift(self.frame)


    def encryptFunction(self):
        self.lblProgramName['text'] = "Encryption Selected"
        # self.btnBack.lift(self.frame)
        self.lblSelectText.lift(self.frame)
        self.btnFileSelect.lift(self.frame)
        self.btnDecrypt.lower(self.frame)
        self.btnEncrypt.lower(self.frame)
        self.lblDecryptText.lower(self.frame)
        self.lblEncryptText.lower(self.frame)




    def homeDefault(self):
        self.lblProgramName['text'] = "Steganographier"
        self.btnBack.lower(self.frame)
        self.btnDecrypt.lift(self.frame)
        self.btnEncrypt.lift(self.frame)
        self.lblDecryptText.lift(self.frame)
        self.lblEncryptText.lift(self.frame)

app=TestGUI()