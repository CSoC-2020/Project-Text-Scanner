from PyPDF2 import PdfFileReader,PdfFileWriter
import os
import cv2
from tkinter import *
from tkinter.filedialog import *
import pytesseract
from PIL import Image
from PIL import Image,ImageTk
from tkinter import font as tkFont
from tkinter import simpledialog

pytesseract.pytesseract.tesseract_cmd =r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def Import():
    a = askopenfilename(title="import")
    ext = os.path.splitext(a)[1]  # it split extension from file location
    # print(" hello ",ext)
    a_name = a.split("/")[::-1]
    a_name = a_name[0].split(".")

    # --- extracting from image---

    if ext == ".png" or ext == ".jpg":
        img = Image.open(a)
        txt = pytesseract.image_to_string(img)
        print(txt)
        b = f"extracted_txt\{a_name[0]}.txt"
        with open(b, "w") as f:
            f.write(txt)

    # ---extracting from video file

    elif ext == ".mp4" or ext == ".avi" or ext == ".mkv":
        cam = cv2.VideoCapture(a)

        try:

            # creating a folder named vid-frames
            if not os.path.exists('vid_frames'):
                os.makedirs('vid_frames')

            # if not created then raise error
        except OSError:
            print('Error: Creating directory of data')
        i = 0

        # counter for reducing no. of frames
        counter = 0
        frame_skip = 10
        txt = ''
        txt1 =''

        # frame
        while cam.isOpened():

            # reading from frame
            ret, frame = cam.read()

            if not ret:
                break
            if counter > frame_skip - 1:
                # if video is still left continue creating images
                name = './vid_frames/frame' + str(i) + '.jpg'
                print('Creating...' + name)
                cv2.imwrite(name, frame)
                img = Image.open(name)

                txt1 = pytesseract.image_to_string(img)
                if txt1 not in txt:
                    txt = txt + " \n " + txt1
                else:
                    pass
                # this counter will moniter no. of frames created
                i += 1

                counter = 0
                continue
            counter += 1
        print("text : ", txt)

        # Release all space and windows once done
        cam.release()
        cv2.destroyAllWindows()

        b = f"extracted_txt\{a_name[0]}.txt"
        with open(b, "w") as f:
            f.write(txt)



    # ----- extraction from pdf file

    elif ext == ".pdf":
        pdf = PdfFileReader(a)
        with open(f"{a_name[0]}.txt", "w") as f:
            for page_num in range(pdf.numPages):
                print(f"page : {page_num}")
                pageobj = pdf.getPage(page_num)

                try:
                    # extracting text from single page
                    txt = pageobj.extractText()
                    print(''.center(100, "-"))
                except:
                    pass
                else:
                    # page indexing
                    f.write(f"page {page_num + 1}\n")
                    f.write(" ".center(100, "-"))
                    f.write(txt)
            f.close()

    else:
        print("extraction of text cannot be performed of this extension")


def Picture():
    txt = ""
    cam = cv2.VideoCapture(0)

    cv2.namedWindow("Camera")

    counter = 0

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
            new_name = img_name.split(".")
            print(f"{new_name[0]} taken!")
            img = Image.open(img_name)
            txt = txt + pytesseract.image_to_string(img)
            counter += 1
    cam.release()
    cv2.destroyAllWindows()

    print(txt)
    b = f"extracted_txt\{new_name[0]}.txt"
    with open(b, "w") as f:
        f.write(txt)



def Video():
    # making directory for output video
    try:

        # creating a folder named vid_frames
        if not os.path.exists('captured_video'):
            os.makedirs('captured_video')

        # if not created then raise error
    except OSError:
        print('first create captured_video folder manullay')

   #recording video
    cam = cv2.VideoCapture(0)

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('captured_video\output.avi',fourcc, 20.0, (640,480))

    while(True):
        ret, frame = cam.read()
        out.write(frame)
        cv2.imshow('capture_video',frame)
        if cv2.waitKey(1) == 27:
            print("camera is closed")
            break
# Release everything if job is finished

    cam.release()
    out.release()
    cv2.destroyAllWindows()

# extracting text from video

    cam1 = cv2.VideoCapture("captured_video\output.avi")

    try:

        # creating a folder named vid_frames
        if not os.path.exists('vid_frames'):
            os.makedirs('vid_frames')

        # if not created then raise error
    except OSError:
        print('Error: Creating directory of data')
    i=0
    # frame
    counter = 0
    frame_skip=10
    txt=''
    txt1=''
    while cam1.isOpened():

        # reading from frame
        ret, frame = cam1.read()

        if not ret:
            break
        if counter > frame_skip - 1:
            # if video is still left continue creating images
            name = './vid_frames/frame' + str(i) + '.jpg'
            print('Creating...' + name)
            cv2.imwrite(name, frame)
            img = Image.open(name)

            txt1=pytesseract.image_to_string(img)
            if txt1 not in txt:
                txt=txt+" \n "+txt1
            else:
                pass
            # writing the extracted images
            i+=1
            counter=0
            continue
            # increasing counter so that it will
            # show how many frames are created
        counter += 1
    print("text : ",txt)

    # Release all space and windows once done
    cam1.release()
    cv2.destroyAllWindows()

    b = "extracted_txt\output.txt"
    with open(b, "w") as f:
        f.write(txt)




def Take():
    screen1 = Toplevel(screen)
    screen1.geometry("800x800")
    screen1.configure(bg="black")
    helv36 = tkFont.Font(family='Helvetica', size=10, weight='bold')
    #window icon
    screen.iconbitmap(r"C:\Users\Karmveer\Downloads\Hopstarter-Soft-Scraps-Document-Text.ico")
    #img = ImageTk.PhotoImage(Image.open(r"C:\Users\Karmveer\Downloads\doodle.jpg"))
    #Label(screen, image=img).place(relwidth=1, relheight=1)
    screen1.title("Take")
    Label(screen1,text="choose one ",font="times 18 bold", bg="grey12",fg="white").pack()
    Button(screen1,text="Picture",bg="grey",height="4",width="45",font=helv36,command=Picture).pack()
    Button(screen1,text="Video",bg="grey",height="4",width="45",font=helv36,command=Video).pack(expaand=YES)
    Label(screen1,text="Tips -- Press ESC button to exit and SPACE to take picture",font="helv36", bg="grey12",
        fg="white").pack()


def main_screen():
    # creating directory for text file
    try:

        # creating a folder named vid_frames
        if not os.path.exists('extracted_txt'):
            os.makedirs('extracted_txt')

        # if not created then raise error
    except OSError:
        print('Error: first create dir for text file extracted_txt manually')

    # making GUI
    global screen
    screen = Tk()
    screen.geometry("800x800")
    #window icon
    screen.iconbitmap(r"C:\Users\Karmveer\Downloads\Hopstarter-Soft-Scraps-Document-Text.ico")
    img = ImageTk.PhotoImage(Image.open(r"C:\Users\Karmveer\Downloads\doodle.jpg"))
    Label(screen, image=img).place(relwidth=1, relheight=1)
    helv36 = tkFont.Font(family='Helvetica', size=10, weight='bold')
    screen.title("TEXT SCANNER")
    Label(text="Pick your option",font="helv36", bg="grey12",fg="white").pack()
    Button(text="Import", bg="grey", height="4", width="45",font=helv36, command=Import).pack()
    Button(text="Take", bg="grey", height="4", width="45",font=helv36, command=Take).pack(expand=YES)
    screen.mainloop()

main_screen()

