# only live feed showing , capture Image (c), start video recording (v), pause video recording (p)
# resume video recording (r), stop video recording (b), exit program (q)
# to stop recording and exit (q)
import cv2
from datetime import datetime
import threading

cap = cv2.VideoCapture(0)
cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
recordControl = 0
# recordControl = 0 : video is being captured (recorded)
# recordControl = 1 : video recording is paused
# recordControl = 2 : video recording is finished (to stop recording)
# we will record video and show current feed parallely using thread


class recordVideo(threading.Thread):  # thread class to record video
	def run(self):
		now = datetime.now()
		time = datetime.time(now)
		name = "capture_V_" + now.strftime("%y%m%d") + time.strftime("%H%M%S") + ".avi"

		fourcc = cv2.VideoWriter_fourcc(*'XVID')
		out = cv2.VideoWriter(name, fourcc, 30.0, (640, 480))

		while True:
			ret, frame = cap.read()
			frame = cv2.flip(frame, 1)
			if recordControl == 0:
				out.write(frame)
			elif recordControl == 2:
				break
		out.release()


def show_video():
	global recordControl
	m = 0  # it will be used to create new thread
	lock = False  # it makes sure that we are only recording one video at a time (only one file is being written on disk at a time)
	while True:
		now = datetime.now()
		time = datetime.time(now)
		name = "capture_" + now.strftime("%y%m%d") + time.strftime("%H%M%S") + ".jpg"

		ret, frame = cap.read()
		if ret is True:
			frame = cv2.flip(frame, 1)   # 1 = vertical , 0 = horizontal

			cv2.imshow('frame', frame)

			k = cv2.waitKey(1) & 0Xff
			if k == ord('v'):  # start video recording
				if lock is False:
					recordControl = 0
					m = m + 1
					threadName = 'recordThread' + str(m)  # everytime find new name
					threadObj = recordVideo(name=threadName)
					threadObj.start()
					lock = True
			elif k == ord('q'):  # Quit program and recording
				if recordControl != 2:  # make sure that out child process is complet
					recordControl = 2
				threadObj.join()
				break
			elif k == ord('c'):  # capture Image
				cv2.imwrite(name, frame)
			elif k == ord('b'):  # stop recording
				recordControl = 2
				threadObj.join()
				lock = False
			elif k == ord('p'):  # pause recording
				recordControl = 1
			elif k == ord('r'):  # resume recording
				recordControl = 0
		else:
			break


if (cap.isOpened()):
	show_video()
else:
	cap.open()
	show_video()

cap.release()
cv2.destroyAllWindows()
