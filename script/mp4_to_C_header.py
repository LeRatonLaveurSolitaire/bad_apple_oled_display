import cv2 as cv
import time

# Output vid paramerters

HEIGHT = 64
WIDTH = 128
FPS = 15
output_path = "video.h"

# Input video path

video_path = "bad_apple!!.mp4"


def main() -> None:

    vid = cv.VideoCapture(video_path)
    ret, frame = vid.read()
    cv.imshow("Frame", frame)
    time.sleep(1)

    if vid.isOpened() == False:
        print("Error opening video file")

    while vid.isOpened():

        # Capture frame-by-frame
        ret, frame = vid.read()
        # ret, frame = vid.read()

        if ret == True:
            # Display the resulting frame
            cv.imshow("Frame", frame)
            # time.sleep(1 / 15)
            # Press Q on keyboard to exit
            if cv.waitKey(25) & 0xFF == ord("q"):
                break

        # Break the loop
        else:
            break

        # When everything done, release
        # the video capture object
    vid.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()
