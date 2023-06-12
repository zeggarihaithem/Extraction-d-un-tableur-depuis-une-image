import cv2
import os
import sys
import numpy as np
import pandas as pd
import helpers as hlp
import pytesseract
from pytesseract import Output

def showimage(img, title):
    if hlp.debug:
        cv2.imshow(title, img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def isImageRotated(img):
    """
    Takes an image as parameter and returns True if it seems rotated, False otherwise.
    """
    im = img.copy()
    # showimage(im, "original")

    blur = cv2.GaussianBlur(im, (7, 7), 0)
    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 7)
    # showimage(thresh, "thresh")

    kernel = np.ones((21, 1), np.uint8)
    morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    # showimage(morph, "morph")

    edges = cv2.Canny(morph, 50, 150, apertureSize=3)
    # showimage(edges, "edges")

    kernel = np.ones((15, 3), np.uint8)
    dilated = cv2.dilate(edges, kernel, iterations=1)
    # showimage(dilated, "dilated")

    lines = cv2.HoughLinesP(dilated, 1, np.pi / 180, 100, minLineLength=100, maxLineGap=10)

    # Get the longest line
    line = lines[0][0]
    for x1, y1, x2, y2 in lines[0]:
        if x2 - x1 > line[2] - line[0]:
            line = [x1, y1, x2, y2]

    # Draw the longest line
    cv2.line(im, (line[0], line[1]), (line[2], line[3]), (0, 255, 0), 2)
    # showimage(im, "lines")

    # Get angle of line
    angle = np.arctan2(line[3] - line[1], line[2] - line[0])
    angle = np.degrees(angle)

    print("Angle of the original image: " + str(int(angle)))

    if not (90 <= abs(angle) < 91 or 0 <= abs(angle) < 1 or 180 <= abs(angle) < 181 or 270 <= abs(angle) < 271):
        hlp.log('Image seems to be rotated')
        return True, angle
    hlp.log('Image seems to be straight')
    return False, angle


def cropToTable(img):
    """
    Takes an image as parameter and returns the image cropped to the table inside (can be not straight).
    Some code from https://stackoverflow.com/questions/59363937/opencv-detecting-an-object-and-its-rotation
    """
    im = img.copy()
    # showimage(im, "original")

    # As usual
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (7, 7), 0)
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 17, 11)
    # showimage(thresh, "thresh")

    # Find the contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    areas = [(cv2.contourArea(cnt), cnt) for cnt in contours]
    areas.sort(key=lambda x: x[0], reverse=True)
    im = cv2.drawContours(im, [areas[0][1]], -1, (0, 255, 0), 1)
    # showimage(im, "contours")

    # Remove the biggest contour (the image)
    areas.pop(0) # Error for rotated script table
    x, y, w, h = cv2.boundingRect(areas[0][1])
    im = cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Crop the image to the table
    crop = im[y : y + h, x : x + w]

    #showimage(crop, "crop")
    return crop


def rotateImage(img, angle):
    """
        Rotate the image so the table is straight.
    """
    (h, w) = img.shape[:2]
    center = (w // 2, h // 2)
    if angle > 0:
        angle = 270 + angle
    else :
        angle = 90 + angle
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    return rotated


def perspective(img):
      # As usual
      im = img.copy()
      gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
      blur = cv2.GaussianBlur(gray, (7, 7), 0)
      thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 17, 11)
      # showimage(thresh, "thresh")

      # Find the 4 corners of the table
      contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
      areas = [(cv2.contourArea(cnt), cnt) for cnt in contours]
      areas.sort(key=lambda x: x[0], reverse=True)
      # im = cv2.drawContours(im, [areas[0][1]], -1, (0, 255, 0), 10)
      # showimage(im, "contours")
      # Get the contour's width and height
      x, y, w, h = cv2.boundingRect(areas[0][1])

      # Correct the perspective to fit the table only in the image
      peri = cv2.arcLength(areas[0][1], True)
      approx = cv2.approxPolyDP(areas[0][1], 0.02 * peri, True)

      # Take largest contour
      pts = np.float32(approx)
      screenpts = np.float32([[0, 0], [0, h], [w, h], [w, 0]])
      
      # Get the perspective matrix with the same ratio
      matrix = cv2.getPerspectiveTransform(pts, screenpts)
      # Apply the perspective transformation
      result = cv2.warpPerspective(im, matrix, (w, h))

      return result


def removeDarkCells(image):
    """
    Remove the cells that have a dark background.
    """
    print("# Cleaning dark cells\t[...]")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Remove noise
    kernel = np.ones((8, 8), np.uint8)
    morph = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    morph = cv2.morphologyEx(morph, cv2.MORPH_CLOSE, kernel)
    showimage(morph, "morph")

    # Find contours
    contours = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]

    # Invert the color inside the cells
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        # image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        if w > 10 and h > 10:
            image[y : y + h, x : x + w] = 255 - image[y : y + h, x : x + w]

    showimage(image, "image with dark cells removed")

    hlp.clear()
    print(hlp.bcolors.OKGREEN + "# Dark cells cleaned\t[✔]" + hlp.bcolors.ENDC)

    return image


def redrawContours(img, rotated):
    print("# Finding contours\t[...]")
    cntsImg = img.copy()

    # showimage(cntsImg, "contours image")

    gray = cv2.cvtColor(rotated, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # Find contours
    contours, _ = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    contours.pop(0)
    if(len(contours) > 1):
        contours.pop(0)

    # Draw a rectangle around the contours
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w*h > 500: # Filter out small contours
            cv2.rectangle(cntsImg, (x, y), (x+w, y+h), (0, 0, 0), 1)

    showimage(cntsImg, "contours image")

    hlp.clear()
    print(hlp.bcolors.OKGREEN + "# Contours found\t[✔]" + hlp.bcolors.ENDC)

    return cntsImg, thresh


def preprocessImg(img):
    print("# Preprocessing image\t[...]")
    prep_img = img.copy()

    # showimage(prep_img, "original image")

    # Set to 300 dpi
    print(prep_img.shape)
    dpi = 300 if prep_img.shape[1] < 1000 else 150 if prep_img.shape[1] < 2400 else 100 if prep_img.shape[1] < 4000 else 50
    prep_img = cv2.resize(prep_img, (int(prep_img.shape[1] * dpi / 72), int(prep_img.shape[0] * dpi / 72)))

    # showimage(prep_img, "resized image")

    gray = cv2.cvtColor(prep_img, cv2.COLOR_BGR2GRAY)

    # showimage(gray, "gray image")

    blur = cv2.GaussianBlur(gray, (11, 11), 0)

    # showimage(blur, "blurred image")

    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 17, 12)

    # kernel = np.ones((3, 3), np.uint8)
    # morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    # morph = cv2.morphologyEx(morph, cv2.MORPH_OPEN, kernel)

    showimage(thresh, "preprocessed image")


    hlp.clear()
    print(hlp.bcolors.OKGREEN + "# Image preprocessed\t[✔]" + hlp.bcolors.ENDC)

    return thresh


def removeText(img):
    print("# Finding cells\t\t[...]")
    grid = img.copy()

    th = cv2.adaptiveThreshold(grid, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    blur = cv2.GaussianBlur(th, (3, 3), 0)

    kernel = np.ones((3, 3), np.uint8)
    morph = cv2.morphologyEx(blur, cv2.MORPH_CLOSE, kernel)
    morph = cv2.morphologyEx(morph, cv2.MORPH_OPEN, kernel)
    
    config = r"--oem 3 --psm 11 --dpi 300"

    details = pytesseract.image_to_data(morph, output_type=Output.DICT, config=config)

    totalWords = len(details['text'])

    for word in range(totalWords):
        if int(details['conf'][word]) > 30 and not details['text'][word].isspace():
            x, y, w, h = details['left'][word], details['top'][word], details['width'][word], details['height'][word]
            grid[y : y + h, x : x + w] = 255

    showimage(grid, "grid with text removed")
    showimage(morph, "grid with text removed")

    return grid, morph


def get_cells(grid):
    
    result = np.zeros((grid.shape[0], grid.shape[1], 3), np.uint8)

    edges = cv2.Canny(grid, 50, 150, apertureSize=3)

    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=100, maxLineGap=10)

    for line in lines:
        x1, y1, x2, y2 = line[0]
        # Draw horizontal and vertical lines and stretch them to the image size
        if x1 == x2:
            cv2.line(result, (x1, 0), (x1, grid.shape[0]), (255, 255, 255), 2)
        elif y1 == y2:
            cv2.line(result, (0, y1), (grid.shape[1], y1), (255, 255, 255), 2)

    kernel = np.ones((11, 11), np.uint8)
    d_im = cv2.dilate(result, kernel, iterations=1) # Dilate to connect lines
    e_im = cv2.erode(d_im, kernel, iterations=1)    # Erode to thin lines


    corners = np.zeros((grid.shape[0], grid.shape[1], 3), np.uint8)

    result = cv2.cvtColor(e_im, cv2.COLOR_BGR2GRAY)

    # We close if necessary the lines of the table
    result = cv2.morphologyEx(result, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))

    showimage(result, "grid")

    # List of the detected cells
    cells = []

    # We find the contours of the cells
    contours, _ = cv2.findContours(result, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    hlp.log("Number of contours: " + str(len(contours)))

    # For each contour
    for cnt in contours:
        (x, y, w, h) = cv2.boundingRect(cnt)
        if not any([x1 - 10 < x < x1 + 10 and y1 - 10 < y < y1 + 10 for (x1, y1, w1, h1) in cells]) and w < result.shape[1] - 10 and h < result.shape[0] - 10 and w > 10 and h > 10:
            hlp.log("x: " + str(x) + " y: " + str(y) + " w: " + str(w) + " h: " + str(h))
            cells.append((x, y, w, h))
            cv2.circle(corners, (x, y), 10, (255, 0, 0), -1)
            cv2.rectangle(corners, (x, y), (x+w, y+h), (255, 255, 255), 2)

    showimage(corners, "corners")

    hlp.clear()
    print(hlp.bcolors.OKGREEN + "# Cells found\t\t[✔]" + hlp.bcolors.ENDC)

    return cells


def makeCsv(imgPath, img, cellsCoordinates):
    """
    Read texts from cells and make a csv file
    """
    print("# Making csv\t\t[...]")
    cCoo = cellsCoordinates.copy()

    config = r"--oem 3 --psm 12 --dpi 300"

    cells = [[]]

    cCoo.reverse()
    hlp.log(cCoo)

    print("# Reading cells text\t[...]")

    hlp.printProgressBar(0, len(cellsCoordinates), suffix="Complete")

    hlp.log(cellsCoordinates)

    totalWords = 0
    totalConf = 0
    avgConf = 0

    lastLineCoo = 0

    for i, cellCoo in enumerate(cCoo):
        (x, y, w, h) = cellCoo

        cell = img[y : y + h, x : x + w]

        _, thresh = cv2.threshold(cell, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        blur = cv2.GaussianBlur(thresh, (7, 7), 0)

        # thin
        kernel = np.ones((3, 3), np.uint8)
        blur = cv2.morphologyEx(blur, cv2.MORPH_CLOSE, kernel)
        
        showimage(blur, "blurred image")

        data = pytesseract.image_to_data(blur, output_type=Output.DICT, config=config)

        hlp.log(data)

        data["text"] = [d for k, d in enumerate(data["text"]) if data["conf"][k] > 30]
        data["conf"] = [d for d in data["conf"] if d > 30]

        text = " ".join(data['text'])

        hlp.log(data["text"])
        hlp.log(data["conf"])

        hlp.log(
            "cell: "
            + str(i)
            + " of size : "
            + str(w)
            + "x"
            + str(h)
            + "\nHas text: "
            + text
            + " with confidence: "
            + str(data["conf"])
            + "\nAnd coordinates: "
            + str(x)
            + ", "
            + str(y)
        )

        hlp.log("i = " + str(i))
        hlp.log("Previous cells line coordinate is : " + str(cellsCoordinates[i - 1][1]))
        hlp.log("Current line coordinate is : " + str(y))

        # If cell is on the same line as the previous one
        if (i == 0 or lastLineCoo - 5 < y < lastLineCoo + 5):
            hlp.log(hlp.bcolors.WARNING + "APPEND SAME LINE\n" + hlp.bcolors.ENDC)
            cells[-1].append(text)
            lastLineCoo = y
        else:
            hlp.log(hlp.bcolors.OKGREEN + "APPEND NEW LINE\n" + hlp.bcolors.ENDC)
            cells.append([text])
            lastLineCoo = y

        hlp.log(cells)

        hlp.printProgressBar(i + 1, len(cellsCoordinates), suffix="Complete")

        for conf in data["conf"]:
            if conf > 30:
                totalWords += 1
                totalConf += int(conf)

    hlp.log(cells)

    avgConf = totalConf / totalWords

    hlp.clear()
    hlp.clear()
    hlp.clear()
    hlp.printProgressBar(i + 1, len(cellsCoordinates), suffix="Complete")

    print(hlp.bcolors.OKGREEN + "# Cells read\t\t[✔]" + hlp.bcolors.ENDC)
    print("# Creating DataFrame\t[...]")

    # Convert the list of lists into a pandas DataFrame
    df = pd.DataFrame(cells)
    hlp.clear()
    print(hlp.bcolors.OKGREEN + "# DataFrame created\t[✔]" + hlp.bcolors.ENDC)

    file_name = os.path.basename(imgPath).split(".")[0]
    file_name = file_name.split()[0]

    dir_name = os.path.basename(os.path.dirname(imgPath))

    if not os.path.exists("outputs/" + dir_name):
        os.makedirs("outputs/" + dir_name)

    print("outputs/" + dir_name + "/" + file_name + ".csv")
    print(imgPath)
    file_name = "outputs/" + dir_name + "/" + file_name + ".csv"

    csv = df.to_csv(file_name, index=False, header=False)
    
    print(hlp.bcolors.OKGREEN + "# CSV created\t\t[✔]" + hlp.bcolors.ENDC)
    print(
        "With an average confidence of : "
        + hlp.bcolors.OKCYAN
        + str(avgConf)
        + hlp.bcolors.ENDC
    )

    return csv


def getCsv(imgPath, isScanned):

    print(imgPath)
    image = cv2.imread(imgPath)
    print(hlp.bcolors.OKGREEN + "# Image loaded\t\t[✔]" + hlp.bcolors.ENDC)

    isRotated, angle = isImageRotated(image)
    # showimage(image, "original image")
    if(isRotated):
        # Rotate the image to have a straight table
        rotated = rotateImage(image, angle)
        # showimage(rotated, "rotated image")

        if(isImageRotated(rotated)[0]):
            rotated = perspective(rotated)
            # showimage(rotated, "rotated image")

    else:
        rotated = image

    if(str.lower(isScanned) == "true"):
        rotated = cropToTable(rotated)
    showimage(rotated, "rotated image")
    print(hlp.bcolors.OKGREEN + "# Image rotated\t\t[✔]" + hlp.bcolors.ENDC)

    im = removeDarkCells(rotated.copy())

    # If the image is mostly black, invert it
    if np.mean(im) < 127:
        im = 255 - im

    cntsImg, thresh = redrawContours(im, rotated)

    thresh = preprocessImg(cntsImg)

    grid, preprocessed_img = removeText(thresh)
    cells = get_cells(grid)

    return makeCsv(imgPath, preprocessed_img, cells)

if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("usage: python3 getCsv.py <image_path> <is image scanned>")
        exit()
    
    getCsv(sys.argv[1], sys.argv[2])
