import cv2
import os
import urllib.request
import shutil
import argparse
import wget
from tqdm import tqdm
import patoolib
from zipfile import ZipFile

def unzip(path, dir):
    zf = ZipFile(path, 'r')
    if not os.path.exists(dir):
        os.makedirs(dir)
    zf.extractall(dir)
    zf.close()

def unrar(file, dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
    patoolib.extract_archive(file, outdir=dir)

def download(dataset):
    if dataset=='UCF-101':
        url='https://www.crcv.ucf.edu/data/UCF101/UCF101.rar'
        # out_file='ucf101.rar'
        # with urllib.request.urlopen(url) as resp, open(out_file, 'wb') as out:
        #     shutil.copyfileobj(resp, out)
        url='https://www.crcv.ucf.edu/data/UCF101/UCF101TrainTestSplits-DetectionTask.zip'
        out_file='UCF101_Action_detection_splits.zip'
        with urllib.request.urlopen(url) as resp, open(out_file, 'wb') as out:
            shutil.copyfileobj(resp, out)

    else:
        pass

def vid2img(videoDir, save_path):
    actions = os.listdir(videoDir)
    for action in actions:
        if not os.path.exists(save_path+action):
            os.mkdir(save_path+action)
        video_list = os.listdir(videoDir+action)
        for video in video_list:
            prefix = video.split('.')[0]
            if not os.path.exists(save_path+action+'/'+prefix):
                os.mkdir(save_path+action+'/'+prefix)
            save_name = save_path + action + '/' + prefix + '/'
            video_name = videoDir+action+'/'+video
            cap = cv2.VideoCapture(video_name)
            fps = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps_count = 0
            for i in range(fps):
                ret, frame = cap.read()
                if ret:
                    cv2.imwrite(save_name+str(10000+fps_count)+'.jpg',frame)
                    fps_count += 1

def checkEmptyDir(imageDir):
    dirs = os.listdir(imageDir)

    for allDir in dirs:
        child = os.path.join('%s%s' % (imageDir, allDir))
        vids = os.listdir(child)
        for filename in vids:
            file_path = child + '/' + filename
            s1 = allDir + '/' + filename
            files = os.listdir(file_path)
            for file in files:
                img = cv2.imread(file_path+'/'+file)
                if img is None:
                    print(file_path+'/'+file)
                    os.remove(file_path+'/'+file)

def label2text(trainFile,testFile, imageDir, trainList, testList):
    train_list = trainFile.readlines()
    test_list = testFile.readlines()

    clip_length = 16
    for line in train_list:
        name = line.split(' ')[0]
        image_path = imageDir+name
        label = line.split(' ')[-1]
        images = os.listdir(image_path)
        nb = len(images) // clip_length
        for i in range(nb):
            trainList.write(name+' '+ str(i*clip_length+1)+' '+label)


    for line in test_list:
        name = line.split(' ')[0]
        image_path = imageDir+name
        label = line.split(' ')[-1]
        images = os.listdir(image_path)
        nb = len(images) // clip_length
        for i in range(nb):
            testList.write(name+' '+ str(i*clip_length+1)+' '+label)

    trainFile.close()
    testFile.close()
    trainList.close()
    testList.close()