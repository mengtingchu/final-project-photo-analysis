# USAGE
# python detect_faces.py --image rooster.jpg --prototxt deploy.prototxt.txt --model res10_300x300_ssd_iter_140000.caffemodel

# import the necessary packages
import numpy as np
import argparse
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=False,
	help="path to input image")
ap.add_argument("-p", "--prototxt", required=False,
	help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", required=False,
	help="path to Caffe pre-trained model")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
	help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

# input image name
args = { 'image' : 'img_1125.jpg',
		'prototxt' : 'deploy.prototxt.txt',
		'model' : 'res10_300x300_ssd_iter_140000.caffemodel',
 		'confidence': 0.1	}
print(args)

# load our serialized model from disk
# load AI model from the model file, net is the name of AI
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

# load the input image and construct an input blob for the image
# by resizing to a fixed 300x300 pixels and then normalizing it

# read image
image = cv2.imread(args["image"])

# resize the image to 300x300 pixels and put the result in the variable blob
(h, w) = image.shape[:2]
blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0,
	(300, 300), (104.0, 177.0, 123.0))

# pass the blob through the network and obtain the detections and
# predictions
print("[INFO] computing object detections...")
# set the blob to be the input of the AI
net.setInput(blob)
# run the AI, get all detected faces and put the data in a list called detections
detections = net.forward()

people_counter = 0
# loop over the detected faces (contained in the list 'detections')
for i in range(0, detections.shape[2]):
	# extract the confidence (i.e., probability) associated with the
	# prediction
	confidence = detections[0, 0, i, 2]

	# filter out weak detections by ensuring the `confidence` is
	# greater than the minimum confidence
	if confidence > args["confidence"]:
		people_counter += 1

		# compute the (x, y)-coordinates of the bounding box for the
		# object
		box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
		# startX, startY endX endY are the coordinates
		(startX, startY, endX, endY) = box.astype("int")

		# draw the bounding box of the face along with the associated
		# probability
		text = "{:.2f}%".format(confidence * 100)
		y = startY - 10 if startY - 10 > 10 else startY + 10

		# this line draz the bounding box
		cv2.rectangle(image, (startX, startY), (endX, endY),
			(0, 0, 255), 2)
		# This line zrite the confidence text on the image
		cv2.putText(image, text, (startX, y),
			cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

# show the output image
cv2.imshow("Output", image)
cv2.waitKey(0)
print('Our amazing sofware detected %s faces, hell yeah' % people_counter)
