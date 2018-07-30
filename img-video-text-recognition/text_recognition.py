import os
import cv2
import pytesseract
import imageio

#####################################

class text_recognition():
    '''
    Tool to recognise text from the image. So far it supports jpeg, jpg, gif, mp4 file extensions.

    Usage:
    1. Create an instance - "tr = text_recognition.text_recognition(silent=True)"
    2. Recognise the text from image - tr.image_recognise("image_path")
    '''
    
    ######################################
    
    __instanceCount = 0
    __silent = True
    
    def __init__(self, silent=True):
        self.__instanceCount += 1
        self.__silent = silent
        self.__pprint("Creating an instance Nr.: " + str(self.__instanceCount) + " of text_recognition()")
        
    def __pprint(self, str_text):
        if not self.__silent:
            print(str_text)
            
    def img_recognise(self, path):
        "Usage: img_recognise(path). Compares strings created by __recogn_color, __recogn_black_and_white and returns longest result."
        try:
            str_color_img = self.__recogn_color(path)
        except Exception as ex:
            self.__pprint("Exception in __recogn_color(path) method: " + str(ex) + "\n" + "Path: " + str(path))
            str_color_img = ""
        try:
            str_b_w = self.__recogn_black_and_white(path)
        except Exception as ex:
            self.__pprint("Exception in __recogn_black_and_white(path) method: " + str(ex) + "\n" + "Path: " + str(path))
            str_b_w = ""

        if (len(str_color_img) > len(str_b_w)):
            return str_color_img
        else:
            return str_b_w
        
    def __recogn_color(self, file):
        filename, file_extension = os.path.splitext(file)
        text = ""
#         try:
        if file_extension.casefold() == ".gif":
            self.__pprint(".gif image detected. \nConverting...")
            gif = imageio.mimread(file)
            nums = len(gif)
            self.__pprint("Total {} frames in the gif!".format(nums))
            text = pytesseract.image_to_string(gif[int(nums / 2)])
        if file_extension.casefold() == ".mp4":
            vid = imageio.get_reader(file,  'ffmpeg')
            nums = len(vid)
            self.__pprint("Total {} frames in mp4 file!".format(nums))
            
            frames = []

            img0 = vid.get_data(0)
            text0 = pytesseract.image_to_string(img0)
            frames.append({"length": int(len(text0)), "content": text0})

            img1 = vid.get_data(int(nums / 4))
            text1 = pytesseract.image_to_string(img1)  
            frames.append({"length": int(len(text1)), "content": text1})

            img2 = vid.get_data(int(nums / 3))
            text2 = pytesseract.image_to_string(img2)
            frames.append({"length": int(len(text2)), "content": text2})

            img3 = vid.get_data(int(nums / 2))
            text3 = pytesseract.image_to_string(img3)    
            frames.append({"length": int(len(text3)), "content": text3})

            img4 = vid.get_data(int(nums - 1))
            text4 = pytesseract.image_to_string(img4)     
            frames.append({"length": int(len(text4)), "content": text4})

            text = sorted(frames, key=lambda k: k['length'], reverse=True)[0]["content"]
            
        if file_extension.casefold() == ".jpg" or file_extension.casefold() == ".jpeg" or file_extension.casefold() == ".png":
            img = cv2.imread(file)
            #image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            text = pytesseract.image_to_string(img) 

#         except Exception as Ex:
#             print("Exception in __recogn_color() \n" + str(Ex)) 

        return text


    def __recogn_black_and_white(self, file1):

        filename, file_extension = os.path.splitext(file1)
        text = ""
#         try:
        if file_extension.casefold() == ".gif":
            self.__pprint(".gif image detected. \nConverting...")
            gif = imageio.mimread(file1)
            nums = len(gif)
            self.__pprint("Total {} frames in the gif!".format(nums))
            text = pytesseract.image_to_string(gif[int(nums / 2)])
        if file_extension.casefold() == ".mp4":
            text = ""
        if file_extension.casefold() == ".jpg" or file_extension.casefold() == ".jpeg" or file_extension.casefold() == ".png":
            img = cv2.imread(file1)
            imag = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            imga = cv2.threshold(imag, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
            #image = cv2.medianBlur(imga, 3)
            text = pytesseract.image_to_string(imga)
#         except Exception as Ex:
#             print("Exception....\n" + str(Ex)) 

        return text
