from PyPDF2 import PdfFileReader,PdfFileWriter
import os
import cv2
from tkinter import *
from tkinter.filedialog import *
import pytesseract
from PIL import Image
from tkinter import simpledialog

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"

def main_scan():
    a = askopenfilename(title="import")
    ext=os.path.splitext(a)[1]     # it split extension from file location
    #print(" hello ",ext)
    a_name = a.split("/")[::-1]
    a_name = a_name[0].split(".")

    #--- extracting from image---

    if ext==".png" or ext==".jpg":
        img = Image.open(a)
        txt = pytesseract.image_to_string(img)
        print(txt)
        b = f" {a_name[0]}.txt"
        with open(b, "w") as f:
            f.write(txt)

    #---extracting from PDF file

    elif ext==".pdf":
        pdf=PdfFileReader(a)
        with open(f"{a_name[0]}.txt", "w") as f:
            for page_num in range(pdf.numPages):
                print(f"page : {page_num}")
                pageobj = pdf.getPage(page_num)

                try:
                    txt = pageobj.extractText()
                    print(''.center(100, "-"))
                except:
                    pass
                else:
                    f.write(f"page {page_num + 1}\n")
                    f.write(" ".center(100, "-"))
                    f.write(txt)
            f.close()




def Take():
    txt=""
    cam = cv2.VideoCapture(0)

    cv2.namedWindow("Camera")

    counter= 0

    while True:
        ret, frame = cam.read()
        if not ret:
            print("unable to load camera")
            break
        cv2.imshow("Camera", frame)

        k = cv2.waitKey(1)
        if k == 27:
            # for stop press ESC
            break
        elif k == 32:
            # press SPACE to save
            img_name = f"picture{counter}.png"
            cv2.imwrite(img_name, frame)
            new_name=img_name.split(".")
            print(f"{new_name[0]} taken!")
            img = Image.open(img_name)
            txt = txt+pytesseract.image_to_string(img)
            counter += 1
    cam.release()
    cv2.destroyAllWindows()

    print(txt)
    b = f"{new_name[0]}.txt"
    with open(b, "w") as f:
        f.write(txt)




def main_screen():
    global screen
    screen = Tk()
    screen.geometry("600x600")
    screen.title("TEXT SCANNER")
    Label(text="Pick your option").pack()
    Label(text=8 * "\n ").pack()
    Button(text="Import",bg="grey", height="2", width="30", command=main_scan).pack()
    Label(text=" ").pack()
    Button(text="Take",bg="grey", height="2", width="30", command=Take).pack()
    Label(text=5* "\n").pack()
    Label(text="Tip : use SPACE BAR to take picture and ESC to close camera.").pack()
    screen.mainloop()

main_screen()
