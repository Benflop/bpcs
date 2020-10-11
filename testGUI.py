import tkinter as tk
import os

from tkinter import filedialog, PhotoImage, Image, messagebox
from PIL import ImageTk, Image
from bpcs.bpcs_steg_encode import *
from bpcs.bpcs_steg_decode import *


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
        self.root.resizable(width=False, height=False)

        self.lblProgramName = tk.Label(text="Steganographier", font=("Helvetica", 32), bg="white")
        self.lblProgramName.place(relwidth=0.6, relheight=0.08, relx=0.2, rely=0.2)

        self.encryptPhoto = PhotoImage(file=r"resources\lock.PNG")
        self.encryptPhotoImage = self.encryptPhoto.subsample(3, 3)
        self.btnEncrypt = tk.Button(self.root, image=self.encryptPhotoImage, bg="#D3D3D3",
                               command = lambda: self.encryptFunction())

        self.btnEncrypt.place(relwidth=0.3, relheight=0.3, relx=0.15, rely=0.4)

        self.decryptphoto = PhotoImage(file=r"resources\unlock.PNG")
        self.decrypPhotoimage = self.decryptphoto.subsample(6, 6)
        self.btnDecrypt = tk.Button(self.root, image=self.decrypPhotoimage, bg="#D3D3D3",
                                    command = lambda: self.decryptFunction())
        self.btnDecrypt.place(relwidth=0.3, relheight=0.3, relx=0.55, rely=0.4)

        self.lblDecryptText = tk.Label(text="Decrypt Image", font=("Helvetica", 16), bg="white")
        self.lblDecryptText.place(relwidth=0.2, relheight=0.08, relx=0.6, rely=0.7)

        self.lblEncryptText = tk.Label(text="Encrypt Image", font=("Helvetica", 16), bg="white")
        self.lblEncryptText.place(relwidth=0.2, relheight=0.08, relx=0.2, rely=0.7)


        self.lblSelectText = tk.Label(text="Select image to encrypt:", font=("Helvetica", 16), bg="white")
        self.lblSelectText.place(relwidth=0.35, relheight=0.08, relx=0.17, rely=0.3)
        self.lblSelectText.lower(self.frame)


        self.btnFileSelect = tk.Button(self.root, text='Browse', font=("Helvetica", 16),bg="white", command = lambda: self.set_Image())
        self.btnFileSelect.place(relwidth=0.12, relheight=0.05, relx=0.52, rely=0.31)
        self.btnFileSelect.lower(self.frame)

        self.btnFileSelectInput = tk.Button(self.root, text='Browse input', font=("Helvetica", 16),bg="white", command=lambda: self.set_Input())
        self.btnFileSelectInput.place(relwidth=0.25, relheight=0.05, relx=0.52, rely=0.31)
        self.btnFileSelectInput.lower(self.frame)

        self.lblShowSelectInput = tk.Label( text='Something',font=("Helvetica", 16), bg="white")
        self.lblShowSelectInput.place(relwidth=0.2, relheight=0.05, relx=0.52, rely=0.31)
        self.lblShowSelectInput.lower(self.frame)

        self.btnNextProcess = tk.Button(self.root, text='Next', bg="white",font=("Helvetica", 16), command=lambda: self.processing())
        self.btnNextProcess.place(relwidth=0.12, relheight=0.05, relx=0.45, rely=0.82)
        self.btnNextProcess.lower(self.frame)

        self.lblOutputFileName=tk.Label(text="Enter new file name:", font=("Helvetica", 16), bg="white")
        self.lblOutputFileName.place(relwidth=0.35, relheight=0.08, relx=0.18, rely=0.4)
        self.lblOutputFileName.lower(self.frame)

        self.textOutputFileName = tk.Entry(self.root)
        self.textOutputFileName.place(relwidth=0.25, relheight=0.04, relx=0.51, rely=0.42)
        self.textOutputFileName.lower(self.frame)


        self.fileLocation = ""
        self.outputFileName = ""
        self.encodeData = ""
        self.thirdPage = False # false is at the 2nd page, true is at 3rd page
        self.selectedFunction = 0 # 0 is encrypt, 1 is decrypt

        self.lblShowPanel=None

        self.lblShowOriginal = None
        self.lblShowEncrypted = None
        self.lblEncryptedText = None
        self.lblOriginalText = None

        self.btnHome = tk.Button(self.root, text='Home', font=("Helvetica", 16), bg="white", command=lambda: self.reset())
        self.btnHome.place(relwidth=0.12, relheight=0.05, relx=0.44, rely=0.75)
        self.btnHome.lower(self.frame)



        self.root.mainloop()


    def encryptFunction(self):
        self.lblProgramName['text'] = "Encryption Selected"
        # self.btnBack.lift(self.frame)
        self.lblSelectText.lift(self.frame)
        self.btnFileSelect.lift(self.frame)
        self.btnDecrypt.lower(self.frame)
        self.btnEncrypt.lower(self.frame)
        self.lblDecryptText.lower(self.frame)
        self.lblEncryptText.lower(self.frame)

    def decryptFunction(self):
        self.selectedFunction = 1
        self.lblProgramName['text'] = "Decryption Selected"
        self.lblSelectText['text'] = "Select image to decrypt:"
        self.lblSelectText.lift(self.frame)
        self.btnFileSelect.lift(self.frame)
        self.btnDecrypt.lower(self.frame)
        self.btnEncrypt.lower(self.frame)
        self.lblDecryptText.lower(self.frame)
        self.lblEncryptText.lower(self.frame)

    def set_Image(self):
        self.fileLocation = self.open_file()
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
            self.btnNextProcess.lift(self.frame)
            self.btnFileSelectInput.lower(self.frame)

    def set_Input(self):
        self.encodeData=self.open_file()
        if self.encodeData:
            self.btnFileSelectInput.lower(self.frame)
            base = os.path.basename(self.encodeData)
            self.lblShowSelectInput['text']=base
            self.lblShowSelectInput.lift(self.frame)

    def open_file(self):
        return filedialog.askopenfilename(initialdir="\\", title="Select File", filetypes=(
        ("png", ".png"), ("txt", ".txt"), ("all files", ".")))


    def encoding(self):
        encode(self.fileLocation, self.encodeData, self.outputFileName)

        messagebox.showinfo("Complete", 'Steganographier have encrypted the image successfully! The file is located at  \n'
                                           +self.outputFileName)

        self.lblProgramName['text'] = "Encryption Completed"
        self.lblSelectText.lower(self.frame)
        self.lblOutputFileName.lower(self.frame)
        self.lblShowSelectInput.lower(self.frame)
        self.btnNextProcess.lower(self.frame)
        self.textOutputFileName.lower(self.frame)

        originalImg = Image.open(self.fileLocation)
        # resize the image and apply a high-quality down sampling filter
        originalImg = originalImg.resize((210, 210), Image.ANTIALIAS)
        # PhotoImage class is used to add image to widgets, icons etc
        originalImg = ImageTk.PhotoImage(originalImg)
        self.lblShowOriginal = tk.Label(self.root, image=originalImg, bg="white")
        self.lblShowOriginal.image = originalImg
        self.lblShowOriginal.place(relwidth=0.3, relheight=0.3, relx=0.15, rely=0.35)

        # opens the image
        encryptImg = Image.open(self.outputFileName)
        # resize the image and apply a high-quality down sampling filter
        encryptImg = encryptImg.resize((210, 210), Image.ANTIALIAS)
        # PhotoImage class is used to add image to widgets, icons etc
        encryptImg = ImageTk.PhotoImage(encryptImg)
        self.lblShowEncrypted = tk.Label(self.root, image=encryptImg, bg="white")
        self.lblShowEncrypted.image = encryptImg
        self.lblShowEncrypted.place(relwidth=0.3, relheight=0.3, relx=0.55, rely=0.35)

        self.lblOriginalText = tk.Label(text="Original Photo", font=("Helvetica", 16), bg="white")
        self.lblOriginalText.place(relwidth=0.3, relheight=0.08, relx=0.15, rely=0.65)
        self.lblEncryptedText = tk.Label(text="Encrypted Photo", font=("Helvetica", 16), bg="white")
        self.lblEncryptedText.place(relwidth=0.3, relheight=0.08, relx=0.55, rely=0.65)
        self.btnHome.lift(self.frame)


    def decoding(self):
        decode(self.fileLocation, self.outputFileName)
        MsgBox = tk.messagebox.askquestion('Complete',
                                           'Steganographier have decrypted the image successfully! The file is located at  \n'
                                           + self.outputFileName + '\nDo you want to open the file?')

        if MsgBox == 'yes':
            os.system('cmd /c "' + self.outputFileName + '"')
            self.reset()
        else:
            self.reset()

    def processing(self):
        if self.thirdPage: #check which page it is
            if self.selectedFunction == 0:  # 0 is encrypt
                if self.encodeData:  # check whether the .txt file is selected
                    if (self.textOutputFileName.get()):  # check whether the NEW file is entered
                        extension = os.path.splitext(self.fileLocation)[1]
                        self.outputFileName = os.path.dirname(
                            self.fileLocation) + "/Encoded_" + self.textOutputFileName.get() + extension
                        self.encoding()
                    else:
                        messagebox.showerror("Error", "Please enter a file name.")
                else:
                    messagebox.showerror("Error", "Please select the encode data file")
            else:# 1 is decrypt
                if (self.textOutputFileName.get()):  # check whether the NEW file is entered
                    self.outputFileName = os.path.dirname(
                        self.fileLocation) + "/Encoded_" + self.textOutputFileName.get() + ".txt"
                    self.decoding()
                else:
                    messagebox.showerror("Error", "Please enter a file name.")
        else:
            if self.selectedFunction == 0:  # 0 is encrypt
                self.lblProgramName['text'] = "Encryption Selected"
                self.btnFileSelect.lower(self.frame)
                self.lblShowPanel.lower(self.frame)
                self.lblSelectText['text'] = "Select Input file: "
                self.lblSelectText.lift(self.frame)
                self.btnFileSelectInput.lift(self.frame)
                self.thirdPage=True
                self.textOutputFileName.lift(self.frame)
                self.lblOutputFileName.lift(self.frame)
            else:
                self.lblProgramName['text'] = "Decryption Selected"
                self.btnFileSelect.lower(self.frame)
                self.lblShowPanel.lower(self.frame)
                self.lblOutputFileName['text'] = "Enter decrypted name:"
                self.thirdPage = True
                self.textOutputFileName.lift(self.frame)
                self.lblOutputFileName.lift(self.frame)



    def reset(self):
        self.lblProgramName['text'] = "Steganographier"
        self.lblProgramName.lift(self.frame)
        self.btnEncrypt.lift(self.frame)
        self.btnDecrypt.lift(self.frame)
        self.lblDecryptText.lift(self.frame)
        self.lblEncryptText.lift(self.frame)

        self.lblShowPanel.lower(self.frame)
        self.lblSelectText.lower(self.frame)
        self.btnFileSelect.lower(self.frame)
        self.btnFileSelectInput.lower(self.frame)
        self.lblShowSelectInput.lower(self.frame)
        self.btnNextProcess.lower(self.frame)
        self.lblOutputFileName.lower(self.frame)
        self.textOutputFileName.lower(self.frame)
        self.textOutputFileName.delete(0, 'end')

        self.fileLocation = ""
        self.outputFileName = ""
        self.encodeData = ""
        self.lblSelectText['text'] = "Select image to encrypt:"
        self.lblOutputFileName['text'] = "Enter new file name:"
        self.thirdPage = False

        self.lblShowOriginal.lower(self.frame)
        self.lblShowEncrypted.lower(self.frame)
        self.lblEncryptedText.lower(self.frame)
        self.lblOriginalText.lower(self.frame)
        self.btnHome.lower(self.frame)

app=TestGUI()