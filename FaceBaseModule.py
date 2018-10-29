import cv2
import sqlite3
import os
from PIL import Image
import numpy as np


# Insert Or Update Database
def insertOrUpdate(IdUser, NameUser):
    conn = sqlite3.connect('Database/FaceBaseDatabase.db')
    cmd = "SELECT * FROM People WHERE ID=" + str(IdUser)
    curson = conn.execute(cmd)
    isRecordExit = 0

    for row in curson:
        isRecordExit = 1
    if isRecordExit == 1:
        cmd = "UPDATE People SET Name = \"" + str(NameUser) + "\" WHERE ID = " + str(IdUser)
    else:
        cmd = "INSERT INTO People(ID,Name) VALUES(" + str(IdUser) + ",'" + str(NameUser) + "')"
    conn.execute(cmd)
    conn.commit()
    conn.close()


# Get Images And Labels For Training
def getImagesAndLabel(pathFile):
    imagePaths = [os.path.join(pathFile, f) for f in os.listdir(pathFile)]
    faces = []
    IDs = []
    for imagePath in imagePaths:
        if imagePath == 'DataSet/.DS_Store':
            continue
        faceImg = Image.open(imagePath).convert('L')
        faceNp = np.array(faceImg, 'uint8')
        ID = int(os.path.split(imagePath)[-1].split('.')[1])
        faces.append(faceNp)
        print(ID)
        IDs.append(ID)
        cv2.imshow("training", faceNp)
        cv2.waitKey(10)
    return IDs, faces


# Get Data Profile User From Sqlite By IdUser
def getProfile(IdUser):
    conn = sqlite3.connect('Database/FaceBaseDatabase.db')
    cmd = "SELECT * FROM People WHERE ID=" + str(IdUser)
    cursor = conn.execute(cmd)
    profileUser = None
    for row in cursor:
        profileUser = row
    conn.close()
    return profileUser


# Create New Folder
def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)
