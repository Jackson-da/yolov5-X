import glob
import xml.etree.ElementTree as ET
import os
import shutil

train_anns = glob.glob('tmp/讯飞研究院-X光安检图像检测挑战赛2022公开数据/训练集/*/XML/*.xml')
train_paths = glob.glob('tmp/讯飞研究院-X光安检图像检测挑战赛2022公开数据/训练集/*/*.jpg')

sets = ['domain1', 'domain2', 'domain3']

classes = ["knife", 'scissors', 'lighter', 'USBFlashDisk', 'pressure', 'plasticBottleWithaNozzle', 'seal',
           'battery']  # 改成自己的类别
abs_path = os.getcwd()
print(abs_path)


def convert(size, box):
    dw = 1. / (size[0])
    dh = 1. / (size[1])
    x = (box[0] + box[1]) / 2.0 - 1
    y = (box[2] + box[3]) / 2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return x, y, w, h


def convert_annotation(in_path, out_path):
    in_file = open(in_path, encoding='UTF-8')
    out_file = open(out_path, 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    for obj in root.iter('object'):
        cls = obj.find('name').text
        if cls not in classes:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))
        b1, b2, b3, b4 = b
        # 标注越界修正
        if b2 > w:
            b2 = w
        if b4 > h:
            b4 = h
        b = (b1, b2, b3, b4)
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')


# for data_set in sets:
#
#     # 处理xml
#     if not os.path.exists('tmp/讯飞研究院-X光安检图像检测挑战赛2022公开数据/训练集/%s/labels' % data_set):
#         os.makedirs('tmp/讯飞研究院-X光安检图像检测挑战赛2022公开数据/训练集/%s/labels' % data_set)
#
#     anns_paths = glob.glob('tmp/讯飞研究院-X光安检图像检测挑战赛2022公开数据/训练集/%s/XML/*.xml' % data_set)
#     for in_path in anns_paths:
#         out_path = 'tmp/讯飞研究院-X光安检图像检测挑战赛2022公开数据/训练集/%s/labels/%s_%s.txt' % (
#             data_set, data_set, in_path.split('\\')[-1].split('.')[0])
#         convert_annotation(in_path, out_path)
#
#     # 处理image
#     if not os.path.exists('tmp/讯飞研究院-X光安检图像检测挑战赛2022公开数据/训练集/%s/images' % data_set):
#         os.makedirs('tmp/讯飞研究院-X光安检图像检测挑战赛2022公开数据/训练集/%s/images' % data_set)
#
#     image_paths = glob.glob('tmp/讯飞研究院-X光安检图像检测挑战赛2022公开数据/训练集/%s/*.jpg' % data_set)
#
#     for image_path in image_paths:
#         out_path = 'tmp/讯飞研究院-X光安检图像检测挑战赛2022公开数据/训练集/%s/images/%s_%s.jpg' % (
#             data_set, data_set, image_path.split('\\')[-1].split('.')[0])
#         shutil.copy(image_path, out_path)


wd = os.getcwd()
data_base_dir = os.path.join(wd, "tmp/讯飞研究院-X光安检图像检测挑战赛2022公开数据/训练集/merge\\")
if not os.path.isdir(data_base_dir):
    os.mkdir(data_base_dir)
img_dir = os.path.join(data_base_dir, "images\\")
if not os.path.isdir(img_dir):
    os.mkdir(img_dir)
img_train_dir = os.path.join(img_dir, "train\\")
if not os.path.isdir(img_train_dir):
    os.mkdir(img_train_dir)
img_val_dir = os.path.join(img_dir, "val\\")
if not os.path.isdir(img_val_dir):
    os.mkdir(img_val_dir)
label_dir = os.path.join(data_base_dir, "labels\\")
if not os.path.isdir(label_dir):
    os.mkdir(label_dir)
label_train_dir = os.path.join(label_dir, "train\\")
if not os.path.isdir(label_train_dir):
    os.mkdir(label_train_dir)
label_val_dir = os.path.join(label_dir, "val\\")
if not os.path.isdir(label_val_dir):
    os.mkdir(label_val_dir)

images_str = 'tmp/讯飞研究院-X光安检图像检测挑战赛2022公开数据/训练集/{}/images'
labels_str = 'tmp/讯飞研究院-X光安检图像检测挑战赛2022公开数据/训练集/{}/labels'

# 训练集
for data_set in sets[:2]:
    image_names = os.listdir(images_str.format(data_set))
    label_names = os.listdir(labels_str.format(data_set))

    for image_name, label_name in zip(image_names, label_names):
        # 复制图片
        source_path = images_str.format(data_set) + '/' + image_name
        target_path = images_str.format('merge') + '/train/' + image_name
        shutil.copy(source_path, target_path)

        # 复制标签
        source_path = labels_str.format(data_set) + '/' + label_name
        target_path = labels_str.format('merge') + '/train/' + label_name
        shutil.copy(source_path, target_path)

# 验证集
for data_set in sets[2:]:
    image_names = os.listdir(images_str.format(data_set))
    label_names = os.listdir(labels_str.format(data_set))

    for image_name, label_name in zip(image_names, label_names):
        # 复制图片
        source_path = images_str.format(data_set) + '/' + image_name
        target_path = images_str.format('merge') + '/val/' + image_name
        shutil.copy(source_path, target_path)

        # 复制标签
        source_path = labels_str.format(data_set) + '/' + label_name
        target_path = labels_str.format('merge') + '/val/' + label_name
        shutil.copy(source_path, target_path)