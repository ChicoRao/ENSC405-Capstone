import cv2
import numpy as np



def motion_detector(img):
  status = 'free'
  frame_count = 0
  previous_frame = None
  
  while True:
    frame_count += 1

    # 1. Load image; convert to RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)   

    if ((frame_count % 2) == 0):

      # 2. Prepare image; grayscale and blur
      prepared_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
      prepared_frame = cv2.GaussianBlur(src=prepared_frame, ksize=(5,5), sigmaX=0)

    if (previous_frame is None):
  # First frame; there is no previous one yet
        previous_frame = prepared_frame
        continue
  
# calculate difference and update previous frame
    diff_frame = cv2.absdiff(src1=previous_frame, src2=prepared_frame)
    previous_frame = prepared_frame

    # 4. Dilute the image a bit to make differences more seeable; more suitable for contour detection
    kernel = np.ones((5, 5))
    diff_frame = cv2.dilate(diff_frame, kernel, 1)

    # 5. Only take different areas that are different enough (>20 / 255)
    thresh_frame = cv2.threshold(src=diff_frame, thresh=20, maxval=255, type=cv2.THRESH_BINARY)[1]
    contours, _ = cv2.findContours(image=thresh_frame, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(image=img, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)

    contours, _ = cv2.findContours(image=thresh_frame, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour) < 50:
        # too small: skip!
            continue
        status = 'Occupied'
    return status


