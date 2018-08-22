import cv2
import os
 
def extractFrames(pathIn, pathOut, video):
    os.mkdir(pathOut)
 
    cap = cv2.VideoCapture(pathIn)
    count = 0
 
    while (cap.isOpened()):
        ret, frame = cap.read()
 
        if ret == True:
            print('Read %d frame: ' % count, ret)
            cv2.imwrite(os.path.join(pathOut, video+"{:d}.jpg".format(count)), frame)  # save frame as JPEG file
            count += 1
        else:
            break
 
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
# 'E033M', 'E033V', 'E034M','E034V','E036M','E036V','E037M', 'E037V', 'E038M', 'E038V'
# 'E041M','E041V','E042M','E042V','E045M','E045V','E046V', 'E046M','E048M','E048V','E052V','E052M','E054M','E054V'

def main():
	videos = []
	for i in videos:
		videoName = i+'.mp4'
		folder = './'+i
		extractFrames(videoName, folder,i)


 
if __name__=="__main__":
    main()