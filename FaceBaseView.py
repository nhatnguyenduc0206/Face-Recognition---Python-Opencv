import FaceBaseController as fController


def chooseInput():
    print('1. Input Data')
    print('2. Training Data')
    print('3. Detector Data')
    iChoose = input('Input your choose :')
    return int(iChoose)


def main():
    iChoose = chooseInput()
    while iChoose not in [1, 2, 3]:
        print('Incorrect.')
        iChoose = chooseInput()
    print('Correct')
    if iChoose == 1:
        fController.inputData()
    elif iChoose == 2:
        path = input('Input path training :')
        fController.trainingData(path)
    else:
        fController.detectorFace()


main()
