import os
os.environ['KMP_DUPLICATE_LIB_OK'] = "TRUE"
import streamlit as st
import pandas as pd
import numpy as np
import torch
import CNN.cnn as cnn
from torchvision import datasets, transforms
import torch.utils.data as Data
from PIL import Image
from main2 import cal,fill,S

def cut_image(image):
    width, height = image.size
    item_width = int(width / 9)
    box_list = []
    # (left, upper, right, lower)
    for i in range(0,9):
        for j in range(0,9):
            #print((i*item_width,j*item_width,(i+1)*item_width,(j+1)*item_width))
            box = (j*item_width,i*item_width,(j+1)*item_width,(i+1)*item_width)
            box_list.append(box)
    image_list = [image.crop(box) for box in box_list]
    return image_list

class TestDataset(Data.Dataset):
    def __init__(self,path) -> None:
        
        #img = Image.open(path).convert("L").resize((28*9,28*9))
        img = Image.open(st.session_state.img).convert("L").resize((28*9,28*9))
        #c1.image(img)
        self.image = cut_image(img)
        self.data_tf = transforms.Compose(
            [transforms.ToTensor(),
            transforms.Normalize([0.5], [0.5])
            ])

    def __len__(self):
        return len(self.image)

    def __getitem__(self, index):
        return self.data_tf(self.image[index])

model = cnn.CNN()
model.load_state_dict(torch.load(os.path.join('CNN/model_sd.pkl'),map_location = 'cpu'))
uploaded_file = st.file_uploader("上传一张图片", type="png")
button = st.button('Solve')
numm = []
for i in range(1,10):
    img = Image.open('num/'+str(i)+'.png').convert("RGB").resize((28,28))
    img = (np.asarray(img))
    numm.append(img)
c1,c2 = st.columns([0.5,0.5])

if uploaded_file is not None:
    # 将传入的文件转为Opencv格式
    st.session_state.img = uploaded_file

    raw = Image.open(st.session_state.img).convert("L").resize((28*9,28*9))
    c1.image(raw)
    
    
if button :
    test_dataset = TestDataset('CNN/T2.png')
    test_loader = Data.DataLoader(test_dataset, batch_size= 3, shuffle=False)
    A = []
    with torch.no_grad():
        acc = num = 0
        for idx,(img) in enumerate(test_loader):
            pred = model(img)
            
            with torch.no_grad():
            
                _, pred = torch.max(pred, 1)
                num += len(img)
                A = A+(pred.cpu().tolist())
    n = 9
    sn = 3
    A = np.array(A).reshape(9,9)
    p = np.zeros((n,n,n+1))
    v = np.zeros((n,n))
    v[A>0] = 1
    p[A>0] = 1 
    for i in range(n):
        for j in range(n):
            if A[i][j]>0 :
                p[:,j,A[i][j]] = 1
                p[i,:,A[i][j]] = 1
                l = i // sn
                h = j // sn
                p[l*sn:(l+1)*sn,h*sn:(h+1)*sn,A[i][j]] = 1
    print('input')
    print(A)
    show = np.zeros((9*28,9*28,3))
    S.clear()
    cal(A,p,0,n)
    for idx,i in enumerate(S):
        print('result:',idx+1)
        for j in range(n):
            s = ''
            s1 = ''
            for k in range(n):
                s1 = s1 + str(i[j,k])
                fv = numm[i[j,k]-1].copy()
                print(fv.shape)
                
                if v[j,k] == 0:
                    s = s+'\033[1;31m %d\033[0m'%i[j,k]
                else: 
                    s = s+'\033[1;37m %d\033[0m'%i[j,k]
                    fv[:,:,1] = 0
                    fv[:,:,2] = 0
                show[j*28:j*28+28,k*28:k*28+28,:] = fv
            print(s)

        
        show = Image.fromarray(np.uint8(show))
        show = show.convert('RGB')

        c2.image(show)
        break
            #st.write(s1)
