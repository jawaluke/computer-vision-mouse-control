"""
    import cv2

    cap = cv2.VideoCapture(0)

    while True:

        ret, frame = cap.read()

        if ret:
        
        
        

        #a = random.randint(0,4)

        
            
            cv2.imshow("frame",frame)


        
            if cv2.waitKey(1) & 0xFF == ord("q"):
                cv2.imwrite("image1.jpg",frame)
                break

    cap.release()

    cv2.destroyAllWindows()        

"""

import cv2
import numpy as np

cap = cv2.VideoCapture(0)

# path for the image to loaded on background

back_path = r"C:\Users\movies\Desktop\python\new modules\opencv\image1.jpg"

back = cv2.imread(back_path)

while True:

    ret, frame = cap.read()

    if ret:
    
    
        
    
        

        # with a red color range

        red = np.uint8([[[0,0,255]]])

        hsv = cv2.cvtColor(frame ,cv2.COLOR_BGR2HSV)

        l_red = np.array([0, 120, 70])
        u_red = np.array([10 , 255, 255])

        mask1 = cv2.inRange(hsv , l_red, u_red)


        l_red = np.array([170, 120, 70])
        u_red = np.array([180 , 255, 255])

        mask2 = cv2.inRange(hsv , l_red, u_red)

        mask = mask1+mask2

        print(mask)

        
        
        mask1 = cv2.morphologyEx(mask , cv2.MORPH_OPEN, np.ones((3,3), np.uint8), iterations = 3)


        mask1 = cv2.morphologyEx(mask1 , cv2.MORPH_DILATE, np.ones((3,3), np.uint8), iterations = 5)

        part1 = cv2.bitwise_not(mask1)

        part2 = cv2.bitwise_and(back , back, mask = mask1)

        part3 = cv2.bitwise_and(frame, frame, mask =part1)


        # add weight

        final_out = cv2.addWeighted(part2,1,part3,1,0)

        
        

        
        cv2.imshow("part 1",part1)
        
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        
cap.release()

cv2.destroyAllWindows()        
