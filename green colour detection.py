import cv2
import numpy as np

# we need to decide the range of hsv value for green

lowerbound = np.array([33,80,40])

upperbound = np.array([102,255,255])

font = cv2.FONT_HERSHEY_SIMPLEX


cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()

    if ret:
        # resize the video
        frame = cv2.resize( frame, (340,220))

        
        imghsv = cv2.cvtColor(frame , cv2.COLOR_BGR2HSV)


        # create a mask
        mask = cv2.inRange(imghsv , lowerbound, upperbound)

        # morphology

        kernelopen = np.ones((5,5))
        maskopen = cv2.morphologyEx(mask , cv2.MORPH_OPEN , kernelopen)

        kernelclose = np.ones((20,20))
        maskclose = cv2.morphologyEx(maskopen , cv2.MORPH_CLOSE , kernelclose)

        maskfinal = maskclose

        # finding contours

        conts, h = cv2.findContours(maskfinal.copy(), cv2.RETR_EXTERNAL ,cv2.CHAIN_APPROX_NONE)

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
