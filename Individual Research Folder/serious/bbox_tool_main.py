import cv2
from process_unit import process_unit
import json

all_boxes = {}
refPt = []
mouse_clicked = False
loaded = False

def load_boxes_from_json():
    global all_boxes, loaded
    try:
        with open('./boxes.json') as f:
            dictdumnp = json.loads(f.read())
        all_boxes = dictdumnp
        loaded = True
    except:
        print('no local json detected')

def mouse_event(event, x, y, flags, param):
    global refPt, mouse_clicked
    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being
    # performed
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        mouse_clicked = True

    # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates and indicate that
        # the cropping operation is finished
        refPt.append((x, y))
        if curr_path not in all_boxes:
            all_boxes[curr_path] = []
        all_boxes[curr_path].append(refPt)
        mouse_clicked = False
        # draw a rectangle around the region of interest
        box = cv2.rectangle(curr_image, refPt[0], refPt[1], (255, 0, 0), 1)
        index = all_boxes[curr_path].__len__()-1
        cv2.putText(box, str(index), refPt[0], cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 255, 100), 2)
        cv2.imshow("image", curr_image)
        refPt = []

    elif event == cv2.EVENT_MOUSEMOVE:
        if mouse_clicked:
            orig = curr_image.copy()
            cv2.rectangle(orig, refPt[0], (x, y), (255, 0, 0), 1)
            cv2.imshow("image", orig)


if __name__ == '__main__':
    # initialize
    pu = process_unit()
    pu.read_frames()
    frames = pu.frames
    outer = True
    frame_index = 0

    # load local json file if there is one
    load_boxes_from_json()
    while frame_index < frames.__len__():
        if (frame_index < 0):
            frame_index = 0
        frame = frames[frame_index]
        if not outer:
            break
        while True:
            curr_path = frame
            print(curr_path)
            curr_image = cv2.imread(curr_path)
            initial = curr_image.copy()
            if loaded:
                if curr_path in all_boxes:
                    prebounds = all_boxes[curr_path]
                    box_index = 0
                    for bound in prebounds:
                        x = bound[0]
                        y = bound[1]
                        box = cv2.rectangle(curr_image, (x[0], x[1]), (y[0], y[1]), (0, 0, 255), 2)
                        cv2.putText(box, str(box_index), (x[0], x[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100,255,100), 2)
                        box_index+=1
                cv2.imshow("image", curr_image)
            else:
                all_boxes[frame] = []
                cv2.imshow('image', curr_image)
            cv2.setMouseCallback('image', mouse_event)

            #key strokes
            k = cv2.waitKey(0)
            #next frame
            if '.' == chr(k & 255):
                frame_index+=1
                break
            #previous frame
            elif ',' == chr(k & 255):
                frame_index -= 1
                break
            #save bounding boxes
            elif 's' == chr(k & 255):
                with open('boxes.json', 'w') as f:
                    json.dump(all_boxes, f)

            #refresh current frame
            elif 'r' == chr(k & 255):
                all_boxes[frame] = []
                cv2.imshow('image', initial)

            #delete single bounding box from this frame
            elif 'd' == chr(k & 255):
                bi = input("Enter Number Of Bounding Box you want to delete: ")
                curr_box = all_boxes[frame]
                del curr_box[int(bi)]
                all_boxes[frame] = curr_box
                prebounds = all_boxes[frame]
                box_index = 0
                for bound in prebounds:
                    x = bound[0]
                    y = bound[1]
                    box = cv2.rectangle(curr_image, (x[0], x[1]), (y[0], y[1]), (0, 0, 255), 2)
                    cv2.putText(box, str(box_index), (x[0], x[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 255, 100), 2)
                    box_index += 1
                cv2.imshow('image', initial)

            #refresh all frames
            elif 'f' == chr(k & 255):
                all_boxes = {}
                cv2.imshow('image', initial)

            #quit program
            elif 'q' == chr(k & 255):
                cv2.destroyAllWindows()
                outer = False
                break


