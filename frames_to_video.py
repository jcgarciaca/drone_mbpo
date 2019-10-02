import cv2
import numpy as np
import os

root_path = '/home/JulioCesar/drone_videos'
frames_folder = os.path.join(root_path, 'frames', 'GX016808')
num_frames = len(os.listdir(frames_folder))
dst_video = os.path.join(root_path, 'videos', 'GX016808_30FPS.mp4')

frame_array = []
fps = 8

for num in range(num_frames):
	print('Processing frame {}'.format(num))
	if num % fps == 0:
		filename = os.path.join(frames_folder, 'img_' + str(num) + '.jpg')
		img = cv2.imread(filename)
		
		# img = cv2.resize(img, (1280, 720), interpolation = cv2.INTER_AREA)
		
		height, width, layers = img.shape
		size = (width,height)
		frame_array.append(img)


out = cv2.VideoWriter(dst_video,cv2.VideoWriter_fourcc(*'DIVX'), (240 / fps), size)

for frame in frame_array:
	out.write(frame)
out.release()
