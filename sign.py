import mediapipe as mp
import time as time
import cv2
import handTrackingModule as hm
def check_dictionary(dict_to_check, keys_with_one):
    if(len(keys_with_one)>0):
        for key, value in dict_to_check.items():
                if key in keys_with_one:
                    if value != 1:
                        return False
                else:
                    if value != 0:
                        return False
    else:
        for key, value in dict_to_check.items():
            if value !=0:
                return False
    return True

cap = cv2.VideoCapture(0)
detector = hm.HandDetector()
fingers = ['Thumb','Index','Middle','Ring','Pinky']
tipID = [4,8,12,16,20]
final_msg = ""
delay = 2.0
last_time = time.time()
while True:
    msg = ""
    success, img = cap.read()
    img = detector.findHands(img)
    img = cv2.flip(img,1)
    lmlist = detector.findPosition(img,allHands=True,draw = False)
    # if(len(lmlist)>0):
    #     print(lmlist)
    dict_finger = {}
    if(len(lmlist)!=0):
        if(lmlist[4][2]<lmlist[3][2]):
            dict_finger['Thumb'] = 1
        else :
            dict_finger['Thumb'] = 0
        for i in range(1,5):
            if (lmlist[tipID[i]][3]<=lmlist[tipID[i]-2][3]):
                dict_finger[fingers[i]]=1
            else: 
                dict_finger[fingers[i]]=0

    #A
        keys_with_one = {'Thumb'}
        if(check_dictionary(dict_finger,keys_with_one) and abs(lmlist[8][2]-lmlist[5][2])<=10):
            msg+="A"
    #B
        keys_with_one={"Index","Middle","Ring","Pinky"}
        if(check_dictionary(dict_finger,keys_with_one)):
            msg+="B"
        
    #D
        keys_with_one= {"Index"}
        if(check_dictionary(dict_finger,keys_with_one)):
            msg+="D"
        
    #E 
        keys_with_one = {None}
        if(check_dictionary(dict_finger,keys_with_one) and abs(lmlist[4][3]-lmlist[12][3])<20):
            msg+="E"
    #M
        elif(check_dictionary(dict_finger,keys_with_one) and abs(lmlist[4][3]-lmlist[12][3])>50):
            msg+="M"
        
        elif(check_dictionary(dict_finger,keys_with_one) and abs(lmlist[4][3]-lmlist[12][3])>22 and abs(lmlist[4][3]-lmlist[12][3])<50):
            msg+="S"
        # else:
        #     msg+="S"

    #F
        keys_with_one = {"Middle","Ring","Pinky"}
        if(check_dictionary(dict_finger,keys_with_one)):
            msg+="F"
    
    #I
        keys_with_one = {"Pinky"}
        if(check_dictionary(dict_finger,keys_with_one)):
            msg+="I"

    #W
        keys_with_one = {"Index","Middle","Ring"}
        if(check_dictionary(dict_finger,keys_with_one)):
            msg+="W"
    
    #U 
        keys_with_one = {"Index","Middle"}
        if(check_dictionary(dict_finger,keys_with_one) and abs(lmlist[8][2]-lmlist[12][2])<=32 and abs(lmlist[6][2]-lmlist[10][2])<=42):
            msg+="U"
    #V
        if(check_dictionary(dict_finger,keys_with_one) and abs(lmlist[8][2]-lmlist[12][2])>32 and abs(lmlist[6][2]-lmlist[10][2])>42):
            msg+="V"
    
    #L
        keys_with_one = {"Thumb","Index"}
        if(check_dictionary(dict_finger,keys_with_one)):
            msg+="L"
    
    # #C
        # keys_with_one = {"Thumb"}
        # if(check_dictionary(dict_finger,keys_with_one) and (abs(lmlist[8][2]-lmlist[5][2]))>10 and (abs(lmlist[4][3]-lmlist[12][3]))>15):
        #     msg+="C"
    # #O
    #     if(check_dictionary(dict_finger,keys_with_one) and abs(lmlist[8][2]-lmlist[5][2])>10 and abs(lmlist[4][3]-lmlist[12][3])<=15 ):
    #         msg+="O"
    #     print(msg)
    
    current_time = time.time()
    if(current_time - last_time)>=delay:
        if(len(lmlist)>0):
            keys_with_one = {None}
            print("...",check_dictionary(dict_finger,keys_with_one))
            print("M  ",abs(lmlist[4][3]),"  ",abs(lmlist[8][4]))
            # print("E(<25)  ",abs(lmlist[4][3]-lmlist[12][3]))
        final_msg+=msg
        last_time = current_time
    cv2.putText(img,str('Timer:'+str(int(current_time - last_time))),(250,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),3)
    cv2.putText(img,str(final_msg),(200,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)