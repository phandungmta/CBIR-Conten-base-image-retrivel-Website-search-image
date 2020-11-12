# -*- coding: utf-8 -*-

from __future__ import print_function

from evaluate import inferInput
from DB import Database




from color import Color
from daisy import Daisy
from edge import Edge
from gabor import Gabor
from HOG import HOG
from vggnet import VGGNetFeat
from resnet import ResNetFeat
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import cv2
import time



depth = 5
d_type = 'd1'
query_idx = 0
linkInput='/home/dev/Desktop/using_ray/CBIR-master/src/test/test2.jpg'

plt.figure()
def showim(result):
    i=1
    
    for item in result:
        i+=1
        

        tmp = item['img']
        name = item['cls']
        links = '/media/dev/Data/Doan/fashion-dataset/images/'+tmp
        imgs = mpimg.imread(links)
        plt.subplot(3,3,i)
        plt.imshow(imgs)
        plt.title(name)
    


    
    



if __name__ == '__main__':
    db = Database()

    img = cv2.imread(linkInput)
    plt.subplot(3,3,1)
    plt.imshow(img)
   

    # # retrieve by color
    # method = Color()
    # samples = method.make_samples(db)
    # query = samples[query_idx]
    # _, result = infer(query, samples=samples, depth=depth, d_type=d_type)
    # print(result)

    # # retrieve by daisy
    # method = Daisy()
    # samples = method.make_samples(db)
    # query = method.histogram(linkInput)
    # result = inferInput(query, samples=samples, depth=depth, d_type=d_type)
    # print(result)

    # # retrieve by edge
    # method = Edge()
    # samples = method.make_samples(db)
    # query = method.histogram(linkInput)
    # result = inferInput(query, samples=samples, depth=depth, d_type=d_type)
    # print(result)

    # # retrieve by gabor
    # method = Gabor()
    # samples = method.make_samples(db)
    # query = samples[query_idx]
    # _, result = infer(query, samples=samples, depth=depth, d_type=d_type)
    # print(result)

    # #retrieve by HOG
    method = HOG()
    samples = method.make_samples(db)
    query = method.get_featInput(img)
    start_time = time.time()

    result = inferInput(query, samples=samples, depth=depth, d_type=d_type)
    end_time = time.time()
    print ('total run-time: %f ms' % ((end_time - start_time) * 1000))
    print(result)

    # retrieve by VGG
    method = VGGNetFeat()
    samples = method.make_samples(db)
    query = method.get_featInput(img)
    start_time = time.time()

    result = inferInput(query, samples=samples, depth=depth, d_type=d_type)
    end_time = time.time()
    print ('total run-time: %f ms' % ((end_time - start_time) * 1000))


  
    
    

    # retrieve by resnet
    method = ResNetFeat()
    samples = method.make_samples(db)
    query = method.get_featInput(img)
    start_time = time.time()

    result = inferInput(query, samples=samples, depth=depth, d_type=d_type)
    end_time = time.time()
    print ('total run-time: %f ms' % ((end_time - start_time) * 1000))
    print(result)
    
    showim(result)
    plt.show()






