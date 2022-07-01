import json
import os

with open('tmp/提交示例.json', 'r') as f:
    data_sl = json.load(f)
    pass


with open('tmp/sx.txt', 'r') as f:
    image_list = list(map(lambda x: x.replace('\n', '').replace('.jpg', ''), f.readlines()))

label_path = {'domain1': 'runs/detect/exp/labels_2',
              'domain2': 'runs/detect/exp2/labels_2',
              'domain3': 'runs/detect/exp3/labels_2'}

label_dict = dict()
label_list = []
for k, v in label_path.items():
    label_list = os.listdir(v)
    label_dict.update(dict(list(map(lambda x: (k + '/' + x.replace('.txt', ''), v + '/' + x), label_list))))

data = []
for img_name in image_list:
    single_data = []
    cate1 = []
    cate2 = []
    cate3 = []
    cate4 = []
    cate5 = []
    cate6 = []
    cate7 = []
    cate8 = []
    label_path = label_dict.get(img_name, '')
    if label_path:
        with open(label_path, 'r') as f:
            for line in f.readlines():
                line_split = line.replace('\n', '').split(' ')
                line_split = list(map(float, line_split))
                cate, xmin, ymin, xmax, ymax, conf = line_split
                if int(cate) + 1 == 1:
                    cate1.append([xmin, ymin, xmax, ymax, conf])
                elif int(cate) + 1 == 2:
                    cate2.append([xmin, ymin, xmax, ymax, conf])
                elif int(cate) + 1 == 3:
                    cate3.append([xmin, ymin, xmax, ymax, conf])
                elif int(cate) + 1 == 4:
                    cate4.append([xmin, ymin, xmax, ymax, conf])
                elif int(cate) + 1 == 5:
                    cate5.append([xmin, ymin, xmax, ymax, conf])
                elif int(cate) + 1 == 6:
                    cate6.append([xmin, ymin, xmax, ymax, conf])
                elif int(cate) + 1 == 7:
                    cate7.append([xmin, ymin, xmax, ymax, conf])
                elif int(cate) + 1 == 8:
                    cate8.append([xmin, ymin, xmax, ymax, conf])

    single_data.append(cate1)
    single_data.append(cate2)
    single_data.append(cate3)
    single_data.append(cate4)
    single_data.append(cate5)
    single_data.append(cate6)
    single_data.append(cate7)
    single_data.append(cate8)
    data.append(single_data)

with open('tmp/result/1.txt', 'w') as f:
    f.write(str(data))
