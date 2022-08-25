from re import S
from configmain import *
'''
Return 1 If Test Is Passed

Return 0 If Test Is Failed
'''

warnings.filterwarnings('ignore')


def variance_of_laplacian(image):
    '''
    Returns The Variance Of Laplcian Score Of The Image
    '''
    return cv2.Laplacian(image, cv2.CV_64F).var()


def Image_Not_Blur(image):
    '''
    If Image Not Blur Returns 1
    If Image Blur Returns 0
    '''
    THRESHOLD_BLUR = LAP_THRESHOLD_BLUR
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    fm = variance_of_laplacian(gray)
    if fm < THRESHOLD_BLUR:
        # THRESHOLD_BLUR is below 150 so blur , return 1 -fail
        return 0
    else:
        # THRESHOLD_BLUR is above 150,not blur , return 1 -pass
        return 1


def Image_Has_No_Noise(img):
    '''
    If No Noise In Image Returns 1 = pass
    If Noise In Image Return 0 = fail
    '''
    # Convert image to HSV color space
    image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # Calculate histogram of saturation channel
    s = cv2.calcHist([image], [1], None, [256], [0, 256])
    # Calculate percentage of pixels with saturation >= p
    p = NOISE_SAT_THRESHOLD_PCT
    s_perc = np.sum(s[int(p * 255):-1]) / np.prod(image.shape[0:2])
    # Percentage threshold; above: valid image, below: noise
    s_thr = NOISE_SAT_THRESHOLD  # generally 0.5 used
    #print(s_perc)
    #print(s_thr)
    if s_perc > s_thr:
        return 0  # noise present
    else:
        return 1  # no noise present


def Image_Not_Scrolled(img):
    '''
    If Image Not Scrolled Returns 1
    If Image Scrolled Returns 0
    '''
    img = cv2.resize(img, (100, 100))
    img_blur = cv2.GaussianBlur(img, (3, 3), 0)
    edges = cv2.Canny(image=img_blur, threshold1=100, threshold2=200)
    white_pix = 0
    white_pix = np.sum(edges == 255)

    #print('Number of white pixels:', white_pix)
    if white_pix > (SCROLL_COLORCNT_PCT/100)*(IMG_WIDTH*IMG_HEIGHT):
        return 1  # not scrolled
    else:
        return 0  # scrolled


def MSE(imageA, imageB):
    '''
    Returns Mse(Mean Square Error) Of ImageS And ImageB
    '''
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    return err


def isaligned(test_img, perfect_img):
    imageA = cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)
    # test_img = cv2.flip(test_img, 0)
    imageB = cv2.cvtColor(perfect_img, cv2.COLOR_BGR2GRAY)
    # score = ssim_score(test_img, perfect_img)
    # print(score)
    # if score > 0.96:
    #     return "inverted"
    # elif score < 0.4:
    #     return "no issue with alignment"
    # elif score == 0 or (score > 0 and score <= 0.4):
    #     return "perfect"
    # else:
    #     return 1
    m = MSE(imageA, imageB)
    s = ssim(imageA, imageB)

    # return f'm:{m} s:{s}'
    return "aligned 0(pass)"


def checkscale(test_img):
    '''

    '''
    img_shape = test_img.shape
    w = img_shape[0]
    h = img_shape[1]

    hsv = cv2.cvtColor(test_img, cv2.COLOR_BGR2HSV)

    red_low = np.array([0, 1, 1])
    red_up = np.array([10, 255, 255])
    red_mask1 = cv2.inRange(hsv, red_low, red_up)
    red_low = np.array([170, 1, 1])
    red_up = np.array([179, 255, 255])
    red_mask2 = cv2.inRange(hsv, red_low, red_up)
    red_mask = red_mask1 + red_mask2
    redpix = cv2.countNonZero(red_mask)

    green_low = np.array([40, 1, 1])
    green_up = np.array([70, 255, 255])
    green_mask = cv2.inRange(hsv, green_low, green_up)
    greenpix = cv2.countNonZero(green_mask)

    blue_low = np.array([105, 1, 1])
    blue_high = np.array([130, 255, 255])
    blue_mask = cv2.inRange(hsv, blue_low, blue_high)
    bluepix = cv2.countNonZero(blue_mask)

    if redpix > (w * h * 0.6):
        return "Red Tint Present"
    elif redpix != 0 and greenpix < (w * h * 0.05) and bluepix < (w * h * 0.05):
        return "Red Tint Present"
    elif greenpix > (w * h * 0.6):
        return "Green Tint Present"
    elif greenpix != 0 and redpix < (w * h * 0.05) and bluepix < (w * h * 0.05):
        return "Green Tint Present"
    elif bluepix > (w * h * 0.6):
        return "Blue Tint Present"
    elif bluepix != 0 and redpix < (w * h * 0.05) and greenpix < (w * h * 0.05):
        return "Blue Tint Present"
    elif redpix == 0 and greenpix == 0 and bluepix == 0:
        return "Image Is Grayscale"
    elif redpix < (w * h * 0.05) and greenpix < (w * h * 0.05) and bluepix < (w * h * 0.05):
        return "Image Is Grayscale"
    else:
        return "Image Is Rgb Scale."


def blackspots(path):
    '''
    Returns The Number Of Blackspots In The Image
    '''
    gray = cv2.imread(path, 0)
# threshold
    th, threshed = cv2.threshold(gray, 100, 255,
                                 cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    # findcontours
    cnts = cv2.findContours(threshed, cv2.RETR_LIST,
                            cv2.CHAIN_APPROX_SIMPLE)[-2]
    s1 = 8
    s2 = 20
    xcnts = []
    for cnt in cnts:
        if s1 < cv2.contourArea(cnt) < s2:
            xcnts.append(cnt)
    return len(xcnts)


def Image_Has_No_STATIC_LINES(test_img):
    '''
    If Static Lines Present Returns 0
    If Static Lines Not Present Returns 1
    '''
    rows = test_img.shape[0]
    cols = test_img.shape[1]
    imgray = cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(imgray, (3, 3), 0)
    edges = cv2.Canny(image=img_blur, threshold1=STATIC_LINES_THRESHOLD_1,
                      threshold2=STATIC_LINES_THRESHOLD_2)
    lines = cv2.HoughLinesP(edges, threshold=STATIC_LINES_THRESHOLD_0, minLineLength=STATIC_LINES_MIN_LINE_LEN,
                            maxLineGap=STATIC_LINES_MAX_LINE_GAP, rho=STATIC_LINES_RHO, theta=np.pi / 180)
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(test_img, (x1, y1), (x2, y2), (0, 255, 0), 3)
    hsv = cv2.cvtColor(test_img, cv2.COLOR_BGR2HSV)
    green_low = np.array([40, 255, 255])
    green_up = np.array([70, 255, 255])
    green_mask = cv2.inRange(hsv, green_low, green_up)
    greenpix = cv2.countNonZero(green_mask)
    test_img = cv2.bitwise_and(test_img, test_img, mask=green_mask)
    if greenpix > (rows * cols * STATIC_LINES_THRESHOLD):
        return 0  # Static Lines Present
    else:
        return 1  # Static Lines Not Present


def detect_obj(img):
    # this is fixed for accurate object detction
    '''
    Returns Coordinates Of Object If Present In Image
    '''
    img = cv2.resize(img, (600, 400))
    objDetected = False
    bbox = cascade.detectMultiScale(img,
                                    scaleFactor=OBJ_SCALE_FACTOR,
                                    minNeighbors=OBJ_MIN_NEIGHBORS,
                                    minSize=OBJ_MIN_SIZE,
                                    maxSize=OBJ_MAX_SIZE
                                    )
    for (x, y, w, h) in bbox:
        objDetected = True
        return (x, y, w, h)
    if not objDetected:
        return (0, 0, 0, 0)


def isshifted(test_img, perfect_img):
    '''
    if img shifted: returns false 1
    else: true 0
    '''
    perfect_img_coords = detect_obj(perfect_img)
    test_img_coords = detect_obj(test_img)
    returnStr = ""
    (x1, y1, w1, h1) = perfect_img_coords
    (x2, y2, w2, h2) = test_img_coords
    horizontalShift = x1 - x2
    verticalShift = y1 - y2
    perfectArea = w1 * h1
    testArea = w2 * h2
    areaDiff = perfectArea - testArea
    if areaDiff < SHIFT_AREA_THRESHOLD_PER:
        if horizontalShift > LEFT_SHIFT_THRESHOLD_PER * 600 / 100:
            returnStr += f" {int(horizontalShift*100/600)}%-left"
        elif horizontalShift == 0:
            pass
        elif horizontalShift < -RIGHT_SHIFT_THRESHOLD_PER * 600 / 100:
            returnStr += f" {-int(horizontalShift*100/600)}%-right"
        if verticalShift > TOP_SHIFT_THRESHOLD_PER * 400 / 100:
            returnStr += f" {int(verticalShift*100/400)}%-top"
        elif verticalShift == 0:
            pass
        elif verticalShift < -BOTTOM_SHIFT_THRESOLD_PER * 400 / 100:
            returnStr += f" {-int(verticalShift*100/600)}%-bottom"
        pass
        if returnStr == "":
            returnStr = "No shift 0(pass)"
            return returnStr
        else:
            returnStr += " shift 1(fail)"
            returnStr = returnStr.strip().title()
            return returnStr
    else:
        return "Image not clear "

# Arun: 25 Aug 2022 -this code below is the backup code. it works  P703 and not for J73

def Image_Not_Rotated_old(test_img):
    '''
    If Image Not Rotated Returns 1
    If Image Rotated Returns 0
    '''
    #try:
    img_gray = cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)
    img_edges = cv2.Canny(img_gray, 100, 100, apertureSize=3)
    lines = cv2.HoughLinesP(img_edges, 1, math.pi / 180.0,
                                100, minLineLength=100, maxLineGap=5)
    angles = []
    for x1, y1, x2, y2 in lines[0]:
        angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
        angles.append(angle)
        median_angle = np.median(angles)
        rotated_angle = abs(round(median_angle))
    #except:
        #return 0  # image rotated
    if rotated_angle > ROTATION_ANGLE_THRESHOLD_DEG:
            #return 0  # image is rotated > than threshold
        return {'rotated_test': 0, 'rotated_degree': rotated_angle}
    else:
            #return 1  # image is not rotated > than threshold
        return {'rotated_test': 1, 'rotated_degree': rotated_angle}

#added by Govinda,Sayali,Amey
def Image_Not_Rotated(test_img , perfect_img):
    
    '''
    If Image Not Rotated Returns 1
    If Image Rotated Returns 0
    '''
     
    def drawAxis(img, p_, q_, color, scale):
            p = list(p_)
            q = list(q_)


          ## [visualization1]
            angle = atan2(p[1] - q[1], p[0] - q[0]) # angle in radians
            hypotenuse = sqrt((p[1] - q[1]) * (p[1] - q[1]) + (p[0] - q[0]) * (p[0] - q[0]))

          # Here we lengthen the arrow by a factor of scale
            q[0] = p[0] - scale * hypotenuse * cos(angle)
            q[1] = p[1] - scale * hypotenuse * sin(angle)
            cv2.line(img, (int(p[0]), int(p[1])), (int(q[0]), int(q[1])), color, 3, cv2.LINE_AA)

          # create the arrow hooks
            p[0] = q[0] + 9 * cos(angle + pi / 4)
            p[1] = q[1] + 9 * sin(angle + pi / 4)
            cv2.line(img, (int(p[0]), int(p[1])), (int(q[0]), int(q[1])), color, 3, cv2.LINE_AA)

            p[0] = q[0] + 9 * cos(angle - pi / 4)
            p[1] = q[1] + 9 * sin(angle - pi / 4)
            cv2.line(img, (int(p[0]), int(p[1])), (int(q[0]), int(q[1])), color, 3, cv2.LINE_AA)
          ## [visualization1]

    def getOrientation(pts, img):
          ## [pca]
          # Construct a buffer used by the pca analysis
            sz = len(pts)
            data_pts = np.empty((sz, 2), dtype=np.float64)
            for i in range(data_pts.shape[0]):
                data_pts[i,0] = pts[i,0,0]
                data_pts[i,1] = pts[i,0,1]

          # Perform PCA analysis
            mean = np.empty((0))
            mean, eigenvectors, eigenvalues = cv2.PCACompute2(data_pts, mean)

          # Store the center of the object
            cntr = (int(mean[0,0]), int(mean[0,1]))
          ## [pca]

          ## [visualization]
          # Draw the principal components
            cv2.circle(img, cntr, 3, (255, 0, 255), 2)
            p1 = (cntr[0] + 0.02 * eigenvectors[0,0] * eigenvalues[0,0], cntr[1] + 0.02 * eigenvectors[0,1] * eigenvalues[0,0])
            p2 = (cntr[0] - 0.02 * eigenvectors[1,0] * eigenvalues[1,0], cntr[1] - 0.02 * eigenvectors[1,1] * eigenvalues[1,0])
            drawAxis(img, cntr, p1, (255, 255, 0), 1)
            drawAxis(img, cntr, p2, (0, 0, 255), 5)

            angle = atan2(eigenvectors[0,1], eigenvectors[0,0]) # orientation in radians
          ## [visualization]

          # Label with the rotation angle
            label = "  Rotation Angle: " + str(90-int(np.rad2deg(angle)) - 90) + " degrees"
            textbox = cv2.rectangle(img, (cntr[0], cntr[1]-25), (cntr[0] + 250, cntr[1] + 10), (255,255,255), -1)
            cv2.putText(img, label, (cntr[0], cntr[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)

            #print(int(np.rad2deg(angle)))
            return angle

    def runForLoop(img):

            # Was the image there?
            if img is None:
                print("Error: File not found")
                exit(0)
            #cv.imshow('Input Image', img)

             #Convert image to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Convert image to binary
            _, bw = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

            # Find all the contours in the thresholded image
            contours, _ = cv2.findContours(bw, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

            for i, c in enumerate(contours):


                # Calculate the area of each contour

                area = cv2.contourArea(c)

                # Ignore contours that are too small or too large
                if area < 3700 or 100000 < area:
                    continue

              # Draw each contour only for visualisation purposes
                #R G B values
                cv2.drawContours(img, contours, i, (0, 255, 0), 2)

              # Find the orientation of each shape
                cv2.imwrite("output_img1.png", img)
                angleOfImage = getOrientation(c, img)
                angleOfImageDeg=(int(np.rad2deg(angleOfImage)))
                return angleOfImageDeg
        
        
    perfect_img_angle=runForLoop(perfect_img)
    test_img_angle=runForLoop(test_img)

    rotated_angle=abs(round(test_img_angle-perfect_img_angle) )
    
    #except:
        #return 0  # image rotated
    if rotated_angle > ROTATION_ANGLE_THRESHOLD_DEG:
            #return 0  # image is rotated > than threshold
        return {'rotated_test': 0, 'rotated_degree': rotated_angle}
    else:
            #return 1  # image is not rotated > than threshold
        return {'rotated_test': 1, 'rotated_degree': rotated_angle}
    





def Image_Horizontal_Shift(test_img, perfect_img):
    '''
    If Img Shifted: Returns 1 - (Arun 0, fail)
    Else: True 0 (Arun 1, Pass)
    '''
    test_img_coords = detect_obj(test_img)
    perfect_img_coords = detect_obj(perfect_img)
    (x1, y1, w1, h1) = perfect_img_coords
    (x2, y2, w2, h2) = test_img_coords
    horizontalShift = x1 - x2
    perfectArea = w1 * h1
    testArea = w2 * h2
    areaDiff = perfectArea - testArea
    if areaDiff < SHIFT_AREA_THRESHOLD_PER:
        """ if horizontalShift > LEFT_SHIFT_THRESHOLD_PER * 600 / 100:
            #return 1
            return {'horizontal_shift': 1, 'horizontal_shift_direction': horizontalShift,'horizontal_shift_percent': horizontalShift}
        elif horizontalShift < -RIGHT_SHIFT_THRESHOLD_PER * 600 / 100:
            #return 1
            return {'horizontal_shift': 1, 'horizontal_shift_percent': horizontalShift}"""
        #return 1
        #return {'horizontal_shift_test': 1, 'horizontal_shift_direction': 'noshift','horizontal_shift_percent': horizontalShift}
        return {'horizontal_shift_test': 1, 'horizontal_shift_percent': horizontalShift}
    else:
        #return 0
        if horizontalShift > LEFT_SHIFT_THRESHOLD_PER * 600 / 100:
            #return 1
            #return {'horizontal_shift_test': 0, 'horizontal_shift_direction': 'moved_left','horizontal_shift_percent': horizontalShift}
            return {'horizontal_shift_test': 0, 'horizontal_shift_percent': horizontalShift}
        elif horizontalShift < -RIGHT_SHIFT_THRESHOLD_PER * 600 / 100:
            #return 1
            #return {'horizontal_shift_test': 0, 'horizontal_shift_direction': 'moved_right', 'horizontal_shift_percent': horizontalShift}
            return {'horizontal_shift_test': 0, 'horizontal_shift_percent': horizontalShift}

        

def Image_Vertical_Shift(test_img, perfect_img):
    '''
    If Img Shifted: Returns 1 - (Arun 0, fail)
    Else: True 0 - (Arun 1, Pass)
    '''
    perfect_img_coords = detect_obj(perfect_img)
    test_img_coords = detect_obj(test_img)
    (x1, y1, w1, h1) = perfect_img_coords
    (x2, y2, w2, h2) = test_img_coords
    vertical_shift = y1 - y2
    perfectArea = w1 * h1
    testArea = w2 * h2
    areaDiff = perfectArea - testArea
    if areaDiff < SHIFT_AREA_THRESHOLD_PER:
        #return {'vertical_shift_test': 1, 'vertical_shift_direction': 'noshift','vertical_shift_percent': vertical_shift}
        return {'vertical_shift_test': 1, 'vertical_shift_percent': vertical_shift}
    else:
        if vertical_shift > TOP_SHIFT_THRESHOLD_PER * 400 / 100:
            #return {'vertical_shift_test': 0, 'vertical_shift_direction': 'moved_top','vertical_shift_percent': vertical_shift}
            return {'vertical_shift_test': 0,'vertical_shift_percent': vertical_shift}
        elif vertical_shift < -BOTTOM_SHIFT_THRESOLD_PER * 400 / 100:
            #return {'vertical_shift_test': 0, 'vertical_shift_direction': 'moved_bottom','vertical_shift_percent': vertical_shift}
            return {'vertical_shift_test': 0, 'vertical_shift_percent': vertical_shift}

def Image_Not_Inverted(test_img, perfect_img):
    '''
    If Image Inverted Returns 0
    If Image Not Inverted Returns 1'''
    test_img = cv2.rotate(test_img, cv2.ROTATE_180)
    test_img = cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)
    perfect_img = cv2.cvtColor(perfect_img, cv2.COLOR_BGR2GRAY)
    ssimscore = round(ssim(test_img, perfect_img))
    #check these values-ARun
    #if ssimscore == 1
    #if ssimscore > SSIM_SCORE_THRESHOLD_PCT:
    #if ssimscore > SSIM_SCORE_THRESHOLD_PCT
    if ssimscore > .90: 
        return 0  # inverted
    else:
        return 1  # not inverted


def Image_Not_Mirrored(test_img, perfect_img):
    '''
    If Image Not Mirrored: Returns 1
    If Image Mirrored: Returns 0
    '''
    try:
        test_img = cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)
        perfect_img = cv2.cvtColor(perfect_img, cv2.COLOR_BGR2GRAY)
        test_img = cv2.flip(test_img, 1)
        score = ssim(test_img, perfect_img)
        #if score >= MIRROR_THRESHOLD:
        if score >= MIRROR_THRESHOLD:
            return 0
        else:
            return 1
    except:
        return "IMAGE SIZES DIFFERENCE"


def Image_Not_Cropped_In_ROI(test_img, perfect_img):
    '''
    There Is Trim In The ROI Region, Image Is Not Cropped = 1(Arun 0, fail)
    There Is No Trim In the ROI Region, Image Is Cropped = 0(Arun 1, Pass)
    '''
    test_img_HSV = cv2.cvtColor(test_img, cv2.COLOR_BGR2HSV)
    perfect_img_HSV = cv2.cvtColor(perfect_img, cv2.COLOR_BGR2HSV)
    black_low = np.array([0, 0, 0])
    black_high = np.array([180, 255, 20])
    test_img_black_pix_mask = cv2.inRange(test_img_HSV, black_low, black_high)
    perfect_img_black_pix_mask = cv2.inRange(
        perfect_img_HSV, black_low, black_high)
    test_img_black_pix_cnt = cv2.countNonZero(test_img_black_pix_mask)
    perfect_img_black_pix_cnt = cv2.countNonZero(perfect_img_black_pix_mask)
    if test_img_black_pix_cnt > perfect_img_black_pix_cnt:
        diff = test_img_black_pix_cnt-perfect_img_black_pix_cnt
        threshold = (NOT_CROPPED_IN_ROI_THRESHOLD_PCT/100) * \
            perfect_img_black_pix_cnt
        if diff > threshold:
            return 1  # there is trim in the ROI region, image is not cropped = fail(Arun 1, Pass)
        else:
            return 0  # there is no trim in the ROI region, image is cropped = pass(Arun 0, Fail)
    else:
        return 0  # there is no trim in the ROI region, image is cropped = pass


def Image_Has_No_Noise_Staticlines_Scrolling_Blur(test_img, test_img_scrolled):
    '''
    If No Noise, Staticlines, Scrolling Present: Returns 1
    Else: Returns 0
    '''
    No_Noise = Image_Has_No_Noise(test_img)
    No_Staticlines = Image_Has_No_STATIC_LINES(test_img)
    No_Scrolling = Image_Not_Scrolled(test_img_scrolled)
    No_Blur = Image_Not_Blur(test_img)
    if No_Noise and No_Staticlines and No_Scrolling and No_Blur:
        return 1
    else:
        return 0
    pass


def SSIM_score(test_img, perfect_img):
    '''
    Returns The SSIM Score Of Both Images
    '''
    ssimscore = ssim(test_img, perfect_img)
    ssimscore = (round(ssimscore, 2))
    return (ssimscore)


def BRISQUE_score(test_img_path):
    '''
    Returns The BRISQUE Score Of The Image
    '''
    test_img_brisquescore = brisque_obj.get_score(test_img_path)
    test_img_brisquescore = round(test_img_brisquescore)
    return test_img_brisquescore
