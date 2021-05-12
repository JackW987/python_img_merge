import cv2 as cv
import os
import numpy as np
#超参数
PATH = 'img'
#获取文件列表 
file_list = os.listdir(PATH)
#定义空字典保存最后结果，索引值和文件名一一对应
dic = {}
#找到最左边的碎图片，根据图片信息，最左侧一列像素为白色即可
for files in file_list:
    img = cv.imread(PATH+'/'+files)
    ret,img_thre = cv.threshold(img,127,255,cv.THRESH_BINARY)
    if img_thre[:,0,0].sum() == 504900:
        dic['0'] = files
#求图片距离
now = 0
sum_m = 0
num  = 0
min_val = {}
for i in range(18):
    # 读取当前需要进行匹配的图片，将当前图片最右侧列找到定义为right_block
    img = cv.imread(PATH+'/'+dic[str(now)])
    ret,img_thre = cv.threshold(img,127,255,cv.THRESH_BINARY)
    right_block = img_thre[:,-1,0]
    # 搜索除本身之外的图片
    for files in file_list:
        if files != dic[str(now)]:
            # 每一张图片读取进来之后找到其最左侧的列
            img_find = cv.imread(PATH+'/'+files)
            ret,img_find_thre = cv.threshold(img_find,127,255,cv.THRESH_BINARY)
            left_block = img_find_thre[:,0,0]
            # 两列之间进行对比，找到欧式距离最小的匹配项
            for i in range(1980):
                num = abs(int(right_block[i])-int(left_block[i]))
                sum_m += num
            # 将每一张图片对应的欧式距离以键值对的形式存入字典
            min_val[sum_m] = files
        sum_m = 0
    now += 1
    # 找到最近距离的匹配项存入最终结果字典
    dic[str(now)]= min_val[min(min_val)] 
    min_val = {}
index = 0
result = cv.imread(PATH+'/'+dic[str(index)])
index += 1
# 根据结果字典的索引值找到对应图片名，进行拼接
for i in range(18):
    mid_img = cv.imread(PATH+'/'+dic[str(index)])
    result = np.concatenate((result,mid_img),axis = 1 )
    index += 1
# 保存最终结果
cv.imwrite('results/1.jpg',result)
cv.imshow('result',result)
cv.waitKey()


