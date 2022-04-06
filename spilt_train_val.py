import os
import cv2
import random
from PIL import Image
# os.makedirs('labels_train')
# os.makedirs('labels_val')

img_train_path = 'd:/data/dolphin_version1/train/images/'  # 图片训练集保存路径，需要自己新建
img_val_path = 'd:/data/dolphin_version1/val/images/'     # 图片验证集保存路径   需要自己新建
labels_train_path = 'd:/data/dolphin_version1/train/labels/'       # 标签训练集保存路径   需要自己新建
labels_val_path = 'd:/data/dolphin_version1/val/labels/'           # 标签验证集保存路径   需要自己新建
dir_images = 'd:/data/dolphin_version1/dolphin/'                       # 数据集路径
dir_labels = 'd:/data/dolphin_version1/labels/'                  # 标签路径

images = os.listdir(dir_images)           # 把所有的图片名放入一个列表中
labels = os.listdir(dir_labels)           # labels的顺序和images的顺序不一定是一致的

random.seed(2021)                           # 设置一个随机种子，确保每次运行都按照既定的随机形式
random.shuffle(images)                      # 洗牌操作，打乱列表顺序

train_spilt_rate = 0.8       # 数据集划分比例，数据集较小可选0.8
a = int(len(images)*train_spilt_rate)   # 训练集数量
count = 0
num_train = 0
num_val = 0
for i, image in enumerate(images):   # 对图片进行划分
    image_path = dir_images + image
    img = Image.open(image_path)    # 读取图片
    if i < a:
        image = image.split('.')
        for label in labels:
            label = label.split('.')
            if label[0] ==image[0]:
                image = str.join('.',image)
                img.save(img_train_path + image)  # 保存训练集图像
                label = str.join('.',label)
                with open(dir_labels +label,'r') as f:
                    with open(labels_train_path + label , 'w') as s:    # 保存训练集标签
                        s.write(f.read())
                num_train += 1
            else:
                continue

    else:
        image = image.split('.')
        for label in labels:
            label = label.split('.')
            if label[0] == image[0]:
                image = str.join('.', image)
                img.save(img_val_path + image)  # 保存验证集
                label = str.join('.', label)
                with open(dir_labels + label, 'r') as f:
                    with open(labels_val_path + label, 'w') as s:  # 保存验证集
                        s.write(f.read())
                num_val+=1

            else:
                continue
    count+=1

print('图片总数量=====================', count)
print('训练集数量=====================', num_train)
print('验证集数量=====================', num_val)
