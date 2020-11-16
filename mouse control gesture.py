import cv2
import numpy as np

import tkinter as tk
from pynput.mouse import Button, Controller


# mouse controller

mouse = Controller()

# creating a window

root = tk.Tk()
# getting the size of the window
sx = root.winfo_screenwidth()

sy = root.winfo_screenheight()

(camx , camy) = (640,480)


# we need to decide the range of hsv value for green

lowerbound = np.array([170,120,150])

upperbound = np.array([190,255,255])

font = cv2.FONT_HERSHEY_SIMPLEX


kernelopen = np.ones((5,5))
        
kernelclose = np.ones((20,20))
        
# assigning the pinchflag L
pinchflag = 0


cap = cv2.VideoCapture(0)
cap.set(3,camx)
cap.set(4,camy)

while True:

    ret, frame = cap.read()

    if ret:
        # resize the video
        #frame = cv2.resize( frame, (340,220))

        
        imghsv = cv2.cvtColor(frame , cv2.COLOR_BGR2HSV)


        # create a mask
        mask = cv2.inRange(imghsv , lowerbound, upperbound)

        # morphology

        maskopen = cv2.morphologyEx(mask , cv2.MORPH_OPEN , kernelopen)

        maskclose = cv2.morphologyEx(maskopen , cv2.MORPH_CLOSE , kernelclose)

        maskfinal = maskclose

        # finding contours

        conts, h = cv2.findContours(maskfinal.copy(), cv2.RETR_EXTERNAL ,cv2.CHAIN_APPROX_NONE)
        


        # creating a mouse gesture

        if(len(conts)==2):
            if(pinchflag==1):

                pinchflag=0

                mouse.release(Button.left)

            x1, y1, w1, h1 = cv2.boundingRect(conts[0])
            x2, y2, w2, h2 = cv2.boundingRect(conts[1])

            cv2.rectangle( frame, (x1,y1), (x1+w1,y1+h1), (255,0,0) ,2)

            cv2.rectangle( frame, (x2,y2), (x2+w2,y2+h2), (255,0,0) ,2)

            cx1 = int(x1+w1/2)
            cy1 = int(y1+h1/2)

            cx2 = int(x2+w2/2)
            cy2 = int(y2+h2/2)

            cx = int((cx1+cx2)/2)
            cy = int((cy1+cy2)/2)

            cv2.line(frame, (cx1,cy1), (cx2,cy2), (255,0,0), 2)
            cv2.circle(frame, (cx,cy),2,(0,0,255), 2)

            mouseLoc = (sx - (cx*sx//camx) , cy*sy//camy)
            mouse.position = mouseLoc

            while mouse.position != mouseLoc:
                pass

        elif(len(conts)==1):
            x, y, w, h = cv2.boundingRect(conts[0])

            if(pinchflag==0):
                pinchflag = 1
                mouse.press(Button.left)
            cv2.rectangle(frame, (x,y),(x+w,y+h),(255,0,0),2)
            cx = int(x+w/2)
            cy = int(y+h/2)
            cv2.circle(frame, (cx,cy),(w+h)//4,(0,0,255),2)
            mouseLoc = (sx - (cx*sx//camx), cy*sy//camy)
            mouse.position = mouseLoc
            while mouse.position != mouseLoc:
                pass
        
 
        cv2.imshow("mouse move", frame)
        
        # draw contours
        

        cv2.drawContours( frame, conts, -1,( 255,0,0 ), 3)

        # using the contours
        for i in range(len(conts)):

            x, y, w, h = cv2.boundingRect(conts[i])
            cv2.rectangle( frame , (x,y), (x+w,y+h) , (0,0,255) ,3)
            cv2.putText(frame, str(i+1),(x,y+h),font,2,(0,255,255),2,cv2.LINE_AA)

        cv2.imshow("maskclose",maskclose)
        cv2.imshow("maskopen" ,maskopen)
        cv2.imshow(" mask ", mask)
        cv2.imshow(" cam ",frame)

        


        cv2.imshow("image",frame)


        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        
cap.release()

cv2.destroyAllWindows()        
