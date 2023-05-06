import cv2
import glob
import time
from datetime import datetime
import os
import numpy as np

img_path = 'images/'
video_path = 'videos/'
file_name = datetime.now().strftime("%Y%m%d-%H%M%S")
camera_port = 0
ramp_frames = 30



def calculate_angle(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle 



def _get_image(camera):
    retval, im = camera.read()
    return im


def capture_a_single_image():
    camera = cv2.VideoCapture(camera_port)

    for i in range(ramp_frames):
        camera_capture = _get_image(camera)
        cv2.imwrite(file_name + '.jpg', camera_capture)
        # TODO: Load it to mongodb instead of local save
    camera = None


def load_images_from_path(path):
    return [cv2.imread(file) for file in glob.glob(f'{path}*.jpg')]


def capture_video():
    # The duration in seconds of the video captured
    capture_duration = 5
    video = cv2.VideoCapture(0)

    w = video.get(cv2.CAP_PROP_FRAME_WIDTH);
    h = video.get(cv2.CAP_PROP_FRAME_HEIGHT);
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    captured_name = file_name
    print(captured_name)
    out = cv2.VideoWriter(f'{video_path}{captured_name}.mp4', fourcc, 20.0, (int(w), int(h)))
    # TODO: Load it to mongodb instead of local save
    start_time = time.time()

    while int(time.time() - start_time) < capture_duration:
        ret, frame = video.read()
        if ret:
            frame = cv2.flip(frame, 180)
            out.write(frame)
            cv2.imshow('frame', frame)
        else:
            break

    video.release()
    out.release()
    cv2.destroyAllWindows()
    print(captured_name)
    return captured_name


def split_video_to_frames(path, video_name):
    frame_number = 0
    # Opens the Video file
    video = cv2.VideoCapture(f'{path}{video_name}.mp4')
    os.mkdir(video_path + video_name)

    while True:
        ret, frame = video.read()
        if not ret:
            break

        cv2.imwrite(f'{video_path}{video_name}/{video_name}_{frame_number}.jpg', frame)
        # TODO: Load it to mongodb instead of local save
        frame_number = frame_number + 1

    video.release()
    cv2.destroyAllWindows()


def main():
    # load_images_from_path(img_path)
    # capture_images()
    # import ipdb
    # ipdb.set_trace()
    captured_video = capture_video()
    split_video_to_frames(video_path, captured_video)


if __name__ == "__main__":
    main()




