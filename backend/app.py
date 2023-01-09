from flask import Flask, request, Response, jsonify
# import db_init from the db.py file
from db import db_init, db
# secure filename for images
from werkzeug.utils import secure_filename
# models contains our database setup
from model import Img


import cv2
import numpy as np


def getRandomColor():
    return (np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255))


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///img.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_init(app)


@app.route('/')
def hello():
    return 'Home Page'


@app.route('/upload', methods=['POST'])
def upload():

    pic = request.files['pic']
    #cmonth = request.files['currentMonth']
    #currentMonth = pic.name

    if not pic:
        return "NO PICTURE ADDED", 400

    filename = secure_filename(pic.filename)
    print(filename)
    mimetype = pic.mimetype
    img = Img(img=pic.read(), mimetype=mimetype, name=filename)
    currentMonth = pic.filename

    '''# get rid of all existing files with given month name
    itemDel = db.session.query(Img).filter(Img.month == currentMonth)
    db.session.delete(itemDel)
    db.session.commit()'''


# BOX DETECTION SCRIPT HERE----BOX DETECTION SCRIPT HERE----BOX DETECTION SCRIPT HERE--BOX DETECTION SCRIPT HERE----BOX DETECTION SCRIPT HERE--BOX DETECTION SCRIPT HERE
# BOX DETECTION SCRIPT HERE----BOX DETECTION SCRIPT HERE----BOX DETECTION SCRIPT HERE--BOX DETECTION SCRIPT HERE----BOX DETECTION SCRIPT HERE--BOX DETECTION SCRIPT HERE
    # convert the byte image to
    file_bytes = np.asarray(bytearray(img.img), dtype=np.uint8)
    imageIn = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    original = cv2.rotate(imageIn, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)
    # this will display the image dimensions
    print(imageIn.shape)
    width = int(original.shape[1])
    height = int(original.shape[0])

    print(f"Width: {width} Height: {height}")

    imageIn = cv2.resize(original, (width//4, height//4),
                         interpolation=cv2.INTER_AREA)

    '''
    gray = cv2.cvtColor(imageIn, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 1)
    thresh = cv2.Canny(blur, 200, 50)
    kernel = np.ones((5, 5))
    dilation = cv2.dilate(thresh, kernel, iterations=3)
    erosion = cv2.erode(dilation, kernel, iterations=1)
    
    allContours, hierarchy = cv2.findContours(
        dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    maxArea = 0
    maxContour = allContours[0]

    for contour in allContours:
        area = cv2.contourArea(contour)
        if area > maxArea:
            maxArea = area
            maxContour = contour
    x, y, w, h = cv2.boundingRect(maxContour)
    imageCropped = imageIn[y:y+h, x:x+w]
    '''

    gray = cv2.cvtColor(imageIn, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 2)
    contours = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    # expand the contours for the calendar lines by drawing over the contours in the thresh image
    for c in contours:
        area = cv2.contourArea(c)
        if 1000 < area < 50000:
            # thicken the contours that are detected
            cv2.drawContours(thresh, [c], -1, (255, 255, 255), 4)

    # vertical and horizontal thresholds using morphological transformations
    thresh = cv2.bitwise_not(thresh)
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 4))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE,
                              vertical_kernel, iterations=1)

    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 1))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE,
                              horizontal_kernel, iterations=1)
    thresh = cv2.bitwise_not(thresh)

    # get rid of background noise in image
    thresh = cv2.erode(thresh, (1, 1), iterations=3)
    # END - vertical and horizontal thresholds using morphological transformations
    # obtain contours once more on the cleaner thresh image
    contours = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    # (contoursC, _) = contours.sort_contours(contoursC, method="top-to-bottom")
    avgW = 0
    avgH = 0
    avgArea = 0
    counter = 0
    for contour in contours:
        area = cv2.contourArea(contour)
        if 1000 < area < 25000:
            x, y, w, h = cv2.boundingRect(contour)
            avgArea += area
            avgW += w
            avgH += h
            counter += 1

    avgW = (avgW / counter)
    avgArea = (avgArea / counter)
    avgH = (avgH / counter)

    imgCounter = 35
    for contour in contours:
        area = cv2.contourArea(contour)
        if (avgArea - (avgArea * .4)) < area < (avgArea + (avgArea * .4)):
            x, y, w, h = cv2.boundingRect(contour)
            x -= 20
            if (avgW - (avgW * .4)) < w < (avgW + (avgW * .4)) and (avgH - (avgH * .4)) < h < (avgH + (avgH * .4)):
                x *= 4
                y *= 4
                w *= 4
                h *= 4
                save = original[y:y+h, x:x+w]

                # encode the image to byte data so that the database can store it properly
                output_string = cv2.imencode('.jpg', save)[1].tostring()

                # the metro bundler stops running after executing this piece of code, but I plan on using it
                # to replace any existing image in the database
                # modify this code to only run/replace if an image with the given id already exists

                dbInfo = Img.query.filter_by(
                    id=imgCounter - 1, month=currentMonth).first()
                dbInfo = Img.query.get(imgCounter)
                # change the data inside of dbInfo.img to the new output_string
                dbInfo.img = output_string

                # this code is essential for initially filling the database
                # for now, it has been commented out in order to allow for modifications
                # to be made to existing images in db

                temp = Img(img=output_string, mimetype=mimetype,
                           name=f"{imgCounter}", month=currentMonth)

                # db.session.add(temp)
                db.session.commit()

                imgCounter -= 1

                cv2.drawContours(
                    imageIn, [contour], -1, getRandomColor(), 2)

                # imageCropped = cv2.resize(imageCropped, (2000, 3000),
                #                          interpolation = cv2.INTER_AREA)

                # cv2.imshow("Original Image", original)

                # cv2.waitKey(0)
                # cv2.destroyAllWindows()

                # BOX DETECTION SCRIPT HERE----BOX DETECTION SCRIPT HERE----BOX DETECTION SCRIPT HERE--BOX DETECTION SCRIPT HERE----BOX DETECTION SCRIPT HERE--BOX DETECTION SCRIPT HERE
                # BOX DETECTION SCRIPT HERE----BOX DETECTION SCRIPT HERE----BOX DETECTION SCRIPT HERE--BOX DETECTION SCRIPT HERE----BOX DETECTION SCRIPT HERE--BOX DETECTION SCRIPT HERE

    cv2.imshow("img", imageIn)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return jsonify({"Done!": "The file has been uploaded."})


@ app.route('/<int:id>')
def get_img(id):
    img = Img.query.filter_by(id=id).first()

    if not img:
        return 'No image found', 404

    return Response(img.img, mimetype=img.mimetype)


@ app.route('/<month>/<name>')
def get_imgWithMonth(name, month):
    img = Img.query.filter_by(month=month, name=name).first()

    if not img:
        return 'No image found', 404

    return Response(img.img, mimetype=img.mimetype)
