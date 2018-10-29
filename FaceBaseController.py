import cv2
import os
import numpy as np
import FaceBaseModule as faceModule


def inputData():
    cam = cv2.VideoCapture(0)
    detector = cv2.CascadeClassifier('Lib/haarcascade_frontalface_default.xml')

    idUser = input('Enter your id : ')
    nameUser = input('Enter your name : ')

    faceModule.insertOrUpdate(idUser, nameUser)
    faceModule.createFolder('./DataSet/')
    sampleNumber = 0
    while True:
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + w), (255, 0, 0), 2)
            sampleNumber += 1
            cv2.imwrite("DataSet/User." + idUser + '.' + str(sampleNumber) + ".jpg",
                        gray[y:y + h, x:x + w])
            cv2.imshow('frame', img)

        if cv2.waitKey(100) & 0xFF == ord('q'):
            break
        elif sampleNumber > 30:
            break

    cam.release()
    cv2.destroyAllWindows()


# path ex path = 'DataSet'
def trainingData(path):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    Ids, faces = faceModule.getImagesAndLabel(path)
    recognizer.train(faces, np.array(Ids))
    print(Ids)

    recognizer.save('Recognizer/trainingData.yml')
    cv2.destroyAllWindows()


def detectorFace():
    faceDetect = cv2.CascadeClassifier('Lib/haarcascade_frontalface_default.xml')
    cam = cv2.VideoCapture(0)
    rec = cv2.face.LBPHFaceRecognizer_create()
    rec.read('Recognizer/trainingData.yml')

    # set text style
    fontFace = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 1
    fontColor = (203, 23, 252)

    while True:
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceDetect.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            idUser, conf = rec.predict(gray[y:y + h, x:x + w])
            profileUser = faceModule.getProfile(idUser)
            # set text to window
            if profileUser is not None:
                #cv2.PutText(cv2.fromarray(img), str(id), (x + y + h), fontFace, (0, 0, 255), 2);
                cv2.putText(img, "Name: " + str(profileUser[1]), (x, y + h + 30), fontFace, fontScale, fontColor, 2)
                cv2.putText(img, "Age: " + str(profileUser[2]), (x, y + h + 60), fontFace, fontScale, fontColor, 2)
                cv2.putText(img, "Gender: " + str(profileUser[3]), (x, y + h + 90), fontFace, fontScale, fontColor,
                            2)

            cv2.imshow('Face', img)
        if cv2.waitKey(1) == ord('q'):
            break
    cam.release()
    cv2.destroyAllWindows()
