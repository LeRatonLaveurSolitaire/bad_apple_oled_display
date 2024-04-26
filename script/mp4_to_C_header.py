import cv2 as cv
import time
import numpy as np

# Output vid paramerters

HEIGHT = 64
WIDTH = 128
OUTPUT_FPS = 15
output_file = "include/video.h"
max_nbr_img = OUTPUT_FPS * 60 * 2

# Input video path

video_path = "bad_apple!!.mp4"


def reshape(frame) -> np.ndarray:
    output_frame = np.zeros((HEIGHT, WIDTH, 3))
    init_height = np.shape(frame)[0]
    init_width = np.shape(frame)[1]

    height_ratio = init_height / HEIGHT
    width_ratio = init_width / WIDTH
    ratio = min(height_ratio, width_ratio)
    center = (init_height // 2, init_width // 2)

    for h in range(HEIGHT):
        for w in range(WIDTH):
            if (round((h - HEIGHT // 2) * ratio) == (h - HEIGHT // 2) * ratio) and (
                round((w - WIDTH // 2) * ratio) == (w - WIDTH // 2) * ratio
            ):
                scaled_h = center[0] + round((h - HEIGHT // 2) * ratio)
                scaled_w = center[1] + round((w - WIDTH // 2) * ratio)
                output_frame[h, w] = frame[scaled_h, scaled_w]
            else:
                scaled_h = center[0] + int((h - HEIGHT // 2) * ratio)
                scaled_w = center[1] + int((w - WIDTH // 2) * ratio)
                output_frame[h, w] = (
                    frame[scaled_h, scaled_w]
                    + frame[scaled_h, scaled_w + 1]
                    + frame[scaled_h + 1, scaled_w]
                    + frame[scaled_h + 1, scaled_w + 1]
                )

            if output_frame[h, w, 0] > 75:
                output_frame[h, w] = np.array([255, 255, 255])
            else:
                output_frame[h, w] = np.array([0, 0, 0])
    return output_frame


def add_frame_to_array(frame, array):
    byte = ""
    for h in range(HEIGHT):
        for w in range(WIDTH):
            if frame[h, w, 0] > 127:
                byte += "1"
            else:
                byte += "0"
            if len(byte) == 8:
                array.append(
                    int(byte[::-1], 2)
                )  # [::-1] because of U8G2 requires reverse bit order
                byte = ""


def main() -> None:
    output_array = []
    nbr_img = 0
    vid = cv.VideoCapture(video_path)
    ret, frame = vid.read()
    add_frame_to_array(reshape(frame), output_array)
    nbr_img += 1
    if vid.isOpened() == False:
        print("Error opening video file")

    while vid.isOpened() and nbr_img < max_nbr_img:

        ret, frame = vid.read()
        ret, frame = vid.read()

        if ret == True:

            # cv.imshow("Original frame", frame)
            # cv.imshow("Reshaped frame", reshape(frame))
            add_frame_to_array(reshape(frame), output_array)
            nbr_img += 1
            print(f"Picture {len(output_array) // 1024}/{max_nbr_img}")

            # Press Q on keyboard to exit
            # if cv.waitKey(25) & 0xFF == ord("q"):
            #    break

        else:
            break

    vid.release()
    cv.destroyAllWindows()
    with open(output_file, "w") as file:
        file.write("#include <stdint.h>\n\n\nconst uint8_t images[] = {")
        for i in range(0, len(output_array), 16):
            if i == 0:
                file.write(
                    f"\n\t0x{output_array[i]:02x},0x{output_array[i+1]:02x},0x{output_array[i+2]:02x},0x{output_array[i+3]:02x},0x{output_array[i+4]:02x},0x{output_array[i+5]:02x},0x{output_array[i+6]:02x},0x{output_array[i+7]:02x},0x{output_array[i+8]:02x},0x{output_array[i+9]:02x},0x{output_array[i+10]:02x},0x{output_array[i+11]:02x},0x{output_array[i+12]:02x},0x{output_array[i+13]:02x},0x{output_array[i+14]:02x},0x{output_array[i+15]:02x}"
                )
            else:
                file.write(
                    f",\n\t0x{output_array[i]:02x},0x{output_array[i+1]:02x},0x{output_array[i+2]:02x},0x{output_array[i+3]:02x},0x{output_array[i+4]:02x},0x{output_array[i+5]:02x},0x{output_array[i+6]:02x},0x{output_array[i+7]:02x},0x{output_array[i+8]:02x},0x{output_array[i+9]:02x},0x{output_array[i+10]:02x},0x{output_array[i+11]:02x},0x{output_array[i+12]:02x},0x{output_array[i+13]:02x},0x{output_array[i+14]:02x},0x{output_array[i+15]:02x}"
                )

        file.write("};")
        file.write(f"\n\nuint32_t images_len = {len(output_array)};")
        file.write(f"\n\nuint32_t nbr_img = {len(output_array)//1024};")


if __name__ == "__main__":
    main()
