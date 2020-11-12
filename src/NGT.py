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

import ngtpy
from six.moves import cPickle
import os
import cv2

from SQLite import SQLite
import time


d_type= 'Normalized Cosine'# L1 , L2, Angle ,Normalized Angle, Cosine, Normalized Cosine, Hamming,Jaccard
depth = 5
NGT_dir = 'NGT'
if not os.path.exists(NGT_dir):
      os.makedirs(NGT_dir)
linkInput='/home/dev/Desktop/using_ray/CBIR-master/src/test/test2.jpg'

# plt.figure()
# def showim(results):
#     i=1
#     samples = cPickle.load(open(os.path.join(NGT_dir, sample_cache), "rb", True))
#     for result in results:
#         i+=1
        
#         data = next(item for item in samples if item["index"] == result[0] )# get info result
#         tmp = data['link']
#         name = data['lable']
#         links = '/media/dev/Data/Doan/fashion-dataset/images/'+tmp
#         imgs = mpimg.imread(links)
#         plt.subplot(3,3,i)
#         plt.imshow(imgs)
#         plt.title(name)




class NGT(object):
    
    def __init__(self, db, f_class=None, d_type='L1'):
        self.NGT_dir = 'NGT_{}_{}'.format(f_class,d_type)
        self.NGT_path = b''
        self.fearure = f_class
        self.SQLdb = SQLite()

        if f_class == 'daisy':
            self.f_c = Daisy()
            self.NGT_path = b'NGT/NGT_daisy_'+d_type.encode()
        elif f_class == 'edge':
            self.f_c = Edge()
            self.NGT_path = b'NGT/NGT_edge_'+d_type.encode()
        elif f_class == 'hog':
            self.f_c = HOG()
            self.NGT_path = b'NGT/NGT_hog_'+d_type.encode()
        elif f_class == 'vgg':
            self.f_c = VGGNetFeat()
            self.NGT_path = b'NGT/NGT_vgg_'+d_type.encode()
        elif f_class == 'res':
            self.f_c = ResNetFeat()
            self.NGT_path = b'NGT/NGT_res_'+d_type.encode()
        if not os.path.exists(os.path.join(NGT_dir,self.NGT_dir)):
                samples = self.f_c.make_samples(db, verbose=False)
                dim = 0
                try: 
                    dim = samples[0]['hist'].shape[0]
                except:
                    pass
                images= []
                objects = []
                for i, row in enumerate(samples):
                    vector  = row['hist']
                    link    = row['img']
                    lable   = row['cls']
                    data = {'index':i,'link':link,'lable':lable}
                    images.append(data)
                    objects.append(vector)
                self.SQLdb.updateMuti(f_class,images)

                # cPickle.dump(images, open(os.path.join(NGT_dir, sample_cache), "wb", True))
                ngtpy.create(path=self.NGT_path, dimension=dim, distance_type=d_type)
                self.index = ngtpy.Index(self.NGT_path)
                self.index.batch_insert(objects)
                self.index.save()

        self.index  = ngtpy.Index(self.NGT_path) 


        
        
    
    def search (self, link ,depth=5):
        query=self.f_c.get_featInput(link)
        r = self.index.search(query, depth)# result[index,square]
        results = []
        for item in r :
            id = item[0]
            results.append(self.SQLdb.select(self.fearure,id))
        return results
    
    def add (self, objects):
        index = self.index
        ids = index.insert(objects)
        index.build_index()
        index.save()
        index.close()
        return ids

    def remove (self, id):
        index = self.index
        index.remove(id)
        index.save()
        index.close()
        return 0


def search4flask(link,f_class='res',d_type='L2',depth=5):
    db = Database()
    ngt = NGT(db=db,f_class=f_class,d_type=d_type)
    result = ngt.search(link = link,depth=depth)
    return result



    








if __name__ == '__main__':
    #example
    db = Database()
    ngt = NGT(db=db,f_class='res',d_type='L1')



    # result = search4flask(linkInput,'edge','L2',5)
    # print(result)