import os
import cv2
import pytesseract
import numpy as np
from datetime import datetime
from PIL import Image, ImageEnhance, ImageFilter

class Ocr:

    def get_text_from_image_path(self, img_file_path, language='por'):
        return pytesseract.image_to_string(Image.open(img_file_path), lang='eng',
                        config='--psm 10')

    def get_text_from_image(self, img, language='por'):
        h, w, c = img.shape
        
        #Preprocessing image
        #https://tesseract-ocr.github.io/tessdoc/ImproveQuality

        #Read and prepare image
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (7, 7), 0)

        # Binarization appling adaptive thresholding
        #mask = cv2.adaptiveThreshold(blurred, 255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 21, 10)                
        #mask = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 10)
        mask = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 31, 10)
        
        #Dilation and Erosion
        kernel = np.ones((2,2),np.uint8)
        processed_img = cv2.erode(mask, kernel, iterations = 1)
        processed_img = cv2.dilate(processed_img, kernel, iterations = 1)

        exec_date = datetime.now()
        exec_date_str = exec_date.strftime("%Y-%m-%d-%H%M%S")

        '''
        #try to erase images from context 
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # transform to grayscale
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]  # perform OTSU threhold
        cv2.rectangle(thresh, (0, 0), (w, h), (0, 0, 0), 2)
        contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0]  # search for contours
        max_cnt = max(contours, key=cv2.contourArea)  # select biggest one
        mask = np.zeros((h, w), dtype=np.uint8)  # create a black mask
        cv2.drawContours(mask, [max_cnt], -1, (255, 255, 255), -1)  # draw biggest contour on the mask
        kernel = np.ones((15, 15), dtype=np.uint8)  # make a kernel with appropriate values - in both cases (resized and original) 15 is ok
        erosion = cv2.erode(mask, kernel, iterations=1)  # erode the mask with given kernel

        reverse = cv2.bitwise_not(img.copy())  # reversed image of the actual image 0 becomes 255 and 255 becomes 0
        processed_img = cv2.bitwise_and(reverse, reverse, mask=erosion)  # per-element bit-wise conjunction of the actual image and eroded mask (erosion)
        processed_img = cv2.bitwise_not(processed_img) 
        '''

        mask = img.filter(ImageFilter.MedianFilter())
        enhancer = ImageEnhance.Contrast(mask)
        processed_img = enhancer.enhance(2)
        

        cv2.imwrite(os.path.join("output",exec_date_str + "_1.jpg"), processed_img)

        processed_img = processed_img.convert('1')
        cv2.imwrite(os.path.join("output",exec_date_str + "_2.jpg"), processed_img)
        
        #[+more details] 
        # https://pyimagesearch.com/2021/05/12/adaptive-thresholding-with-opencv-cv2-adaptivethreshold/ 
        # https://towardsdatascience.com/pre-processing-in-ocr-fc231c6035a7

        #To install Tesseract
        #choco install tesseract
        #If the package is not installed in the C:\Program Files\Tesseract-OCR folder please check the folder C:\ProgramData\chocolatey\lib\tesseract\tools
        #Extract the file tesseract-ocr-w64-setup-v5.3.0.20221214.exe as a zip file and copy them to your local applications folder
        #Add this folder to your PATH environment variables
        #In the end get the portuguese language model from here https://github.com/tesseract-ocr/tessdata find by por.traineddata and save in your application folder C:\Applics\tesseract-ocr-w64-setup-v5.3.0.20221214\tessdata

        #ocr_dict = pytesseract.image_to_data(pil_im, lang='por', output_type=Output.DICT)
        # ocr_dict now holds all the OCR info including text and location on the image
        #text = " ".join(ocr_dict['text'])

        text = pytesseract.image_to_string(processed_img, lang=language)
        #filename = "file_" + str(pg) + ".txt"
        #output_file = open(os.path.join(self.HOME_PATH, filename),"a", encoding='utf-8')
        return text