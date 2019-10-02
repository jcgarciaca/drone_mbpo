import cv2
import os

root_path = '/home/JulioCesar/drone_videos'
videos_folder = os.path.join(root_path, 'videos')

target_folder = os.path.join(root_path, 'frames')

video_name = 'GX016808'
video_path = os.path.join(videos_folder, video_name + '.MP4')

if not os.path.exists(os.path.join(target_folder, video_name)):
	os.makedirs(os.path.join(target_folder, video_name))

cap = cv2.VideoCapture(video_path)
length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print('length:', length)


if (cap.isOpened()== False):
	print("Error opening video stream or file")
counter = 0
while(cap.isOpened()):
	ret, frame = cap.read()	
	if ret == True:
		print('Processing frame #: {}'.format(counter))
		cv2.imwrite(os.path.join(target_folder, video_name, 'img_' + str(counter) + '.jpg'), frame)
		counter += 1
	if counter >= length - 1:
		break

