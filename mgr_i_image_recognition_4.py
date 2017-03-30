# -*- coding: utf-8 -*-
from scipy import misc
from scipy.ndimage.filters import gaussian_filter
import numpy as np
from matplotlib import pyplot as plt
import matplotlib
from noise import snoise2
import cv2

def findRegions(img):
    result=[]
    t=np.nonzero(regs)
    t=set(zip(t[0],t[1]))
    while(len(t)>0):
        temp=t.pop()
        res=[]
        grow(temp,t,res)
        result.append(res)
    return result
    
def grow(obj, li, res):
    
    curent=(obj[0]+1,obj[1]);
    if( curent in li ):
        li.remove(curent)
        res.append(curent)
        grow(curent,li,res)
    
    curent=(obj[0]-1,obj[1]);
    if( curent in li ):
        li.remove(curent)
        res.append(curent)
        grow(curent,li,res)

    curent=(obj[0],obj[1]+1);
    if( curent in li ):
        li.remove(curent)
        res.append(curent)
        grow(curent,li,res)
        
    curent=(obj[0],obj[1]-1);
    if( curent in li ):
        li.remove(curent)
        res.append(curent)
        grow(curent,li,res)
        
#READ FILE
image = misc.imread(r"C:\Users\Iza\Desktop\Telefony1.2.bmp")
data=np.array(image)
data=np.array(image)
o_data=data=data[:,:,0]

#NOISE GENERATION
o_data=data = gaussian_filter(data, sigma=1)

a=np.zeros(( len(data),len(data[0]) ))
for y in xrange(len(data[0])):
        for x in xrange(len(data)):
            v = snoise2(x, y , 8)
            if v < 0: v *= -1
            a[x][y] = int(v * 100.) #przesadziłam?

data = data+a
o_data= data = np.uint8( (data/data.max())*255. )

#EDGES IMPROVEMENT
edges = cv2.Canny(data,50,150)
data=data-edges*0.5
data[data<0]=0

#THRESHOLD
ret,data = cv2.threshold(data,100,255,cv2.THRESH_BINARY)

#MORPHOLOGY
kernel = np.ones((3,3),np.uint8)
kernel[[0,0,2,2],[0,2,0,2]]=0
data = cv2.dilate(data,kernel,iterations = 1)

#REGION DETECTION
regs=data<124
regions = findRegions(regs)
regions = [ x for x in regions if len(x)>8 ]
border=2
rectangles=[]
for i in range(len(regions)):
    down=max(regions[i],key=lambda item:item[1])[1] +1 +border
    down=down if down<len(o_data[0]) else len(o_data[0])
    up=min(regions[i],key=lambda item:item[1])[1] -border 
    up=up if up>0 else 0
    right=max(regions[i],key=lambda item:item[0])[0] +1 +border
    right=right if right<len(o_data) else len(o_data)
    left=min(regions[i],key=lambda item:item[0])[0] -border
    left=left if left>0 else 0
    print left,right,up,down
    
    rectangles.append(o_data[left:right,up:down])
    
plt.imshow(regs,interpolation='none',cmap=matplotlib.cm.get_cmap('rainbow', 256))
plt.show()

