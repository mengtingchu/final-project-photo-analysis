import os
import numpy as np
import cv2
import pandas as pd
import datetime
import matplotlib.pyplot as plt

def get_ppl_number(image_name, verbose = False):
    args = { 'image' : image_name,
            'prototxt' : 'deploy.prototxt.txt',
            'model' : 'res10_300x300_ssd_iter_140000.caffemodel',
            'confidence': 0.5	}
    tic = datetime.datetime.now()
    net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])
    toc = datetime.datetime.now()
    image = cv2.imread(args["image"])
    
    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0,
        (300, 300), (104.0, 177.0, 123.0))
    net.setInput(blob)
  
    detections = net.forward()
    people_counter = 0
 
    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > args["confidence"]:
            people_counter += 1
    if verbose:        
        print('Our amazing sofware detected %s faces, hell yeah' % people_counter)
    return people_counter

def get_folder_stats(image_name_list):
   
    list_photo_analysis = []

    for image_name in image_name_list:
        if image_name != None:
            nbr_ppl = get_ppl_number(image_name)
            list_photo_analysis.append(nbr_ppl)
    return pd.Series(list_photo_analysis)



cwd = os.getcwd()
dir_list = os.listdir(cwd)

folder_list = [element for element in dir_list if os.path.isdir(element)]

df = pd.DataFrame()

for folder in folder_list:

    image_list = os.listdir(cwd + '\\' + folder)

    image_name_list = [folder + '\\' + file_ if file_[:3] == 'img' else None for file_ in image_list]
   
    df[folder] = get_folder_stats(image_name_list)
    print('Folder %s Done %s images analysed' % (folder, len(image_name_list)))

df.to_csv('analysis_results.csv')

