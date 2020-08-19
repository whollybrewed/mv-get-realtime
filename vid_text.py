import re
import cv2
cap = cv2.VideoCapture('output.mp4')  
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output_stat.mp4', fourcc, fps, (width, height))
while(True):  
    ret, frame = cap.read() 
    fr = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
    print('FRAME: ' + str(fr), end="\r", flush=True)
    pattern = "fr=" + str(fr)
    font = cv2.FONT_HERSHEY_SIMPLEX 
    with open('stat_all.txt', 'r') as f1, open('stat_inter.txt', 'r') as f2, open('stat_intra.txt', 'r') as f3 :
        lines1 = f1.readlines()
        for line1 in lines1:
            if re.search(r"\b" + pattern + r"\b", line1):
                    cv2.putText(frame, line1.rstrip('\n'), (50, 50), font, 0.5, (255, 255, 255)) 
        lines2 = f2.readlines()
        for line2 in lines2:
            if re.search(r"\b" + pattern + r"\b", line2):
                    cv2.putText(frame, line2.rstrip('\n'), (50, 70), font, 0.5, (0, 0, 255))
        lines3 = f3.readlines()
        for line3 in lines3:
            if re.search(r"\b" + pattern + r"\b", line3):
                    cv2.putText(frame, line3.rstrip('\n'), (50, 90), font, 0.5, (255, 0, 0))

        out.write(frame)
        cv2.imshow('video', frame) 
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break
cap.release() 
out.release()
cv2.destroyAllWindows() 