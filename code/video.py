import os
import cv2
import shutil
from ocr import Ocr
Video_FILE = "The_Detective_Dog.mp4"

def FrameCapture(path):
  
    dir = 'output'
    if not os.path.isdir(dir):
        os.makedirs(dir)
    else:
        shutil.rmtree(dir)
        os.makedirs(dir)

    # Path to video file
    vidObj = cv2.VideoCapture(path)
    fps = vidObj.get(cv2.CAP_PROP_FPS)
  
    # Used as counter variable
    count = 0
  
    # checks whether frames were extracted
    success = 1

    ocr = Ocr()
  
    while count < 120000:
        
        # vidObj object calls read
        # function extract frames
        success, image  = vidObj.read()
        millis = vidObj.get(cv2.CAP_PROP_POS_MSEC)
        if millis % 30000 == 0:
            # Saves the frames with frame-count
            img_path = os.path.join("output","frame%d.jpg" % count)
            cv2.imwrite(os.path.join("output","frame%d.jpg" % count), image)
            text = ocr.get_text_from_image_path(img_path, language='eng')
            filename = "frame_" + str(count) + ".txt"
            output_file = open(os.path.join("output",filename),"a", encoding='utf-8')
            output_file.writelines(text)
        count += 1

FrameCapture(Video_FILE)

#vidObj = cv2.VideoCapture(Video_FILE)
#fps = vidObj.get(cv2.CAP_PROP_FPS)
#print(fps)