#!C:\Users\Lenovo\anconda3\evns\evn3\python
# -*- coding: utf-8 -*-
'''
@Time    : 21/01/05 AM 11:01
@Author  : dafei
@User    : dafei
@FileName: __main__.py
@Software: PyCharm
'''

import yaml
import cv2
from pathlib import Path
import numpy as np
from matplotlib import pyplot as plt
from utils import Pbar,Wait



class MicEpil():
    '''
    统计视频中小鼠癫痫的运动速度
    返回小鼠在两帧的位置差值
    '''

    def __init__(self):
        '''魔法函数init'''
        #初始yaml中的类内全局变量_低负载的实例方法可以放在init函数中
        self._load_yaml()
        # 初始化视频信息_低负载的实例方法可以放在init函数中
        self._init_videoinfo()

        # 添加实例属性
        # 上一帧信息
        self.pre_frame=None
        # 帧差值
        self.res=[]
        # 保存路径
        self.res_saved_path=Path(self.cfg['output_dir'],'res.npy')
        self.hist_output_path=Path(self.cfg['output_dir'],'hist.png')
        self.txt_output_path=Path(self.cfg['output_dir'],'time_points.txt')

    # 添加实例方法：访问实例属性
    def _load_yaml(self):
        '''
        导入yaml文件中的参数
        '''
        if Path('config.yaml').exists():
            with open('config.yaml', encoding='utf-8') as f:
                cfg = yaml.safe_load(f)
            if not Path(cfg['video_path']).exists():
                print('路径[video_path]不存在!')
                exit()
            if not Path(cfg['output_dir']).exists():
                print('路径[output_dir]不存在!')
                exit()
        else:
            print('没有找到配置文件：config.yaml!')
            exit()
        self.cfg=cfg #类内实例属性

    # 添加实例方法：访问实例属性
    def _init_videoinfo(self):
        '''
        获取视频的基础信息
        '''
        #访问实例属性self.cap，self.fps，self.frame_num
        self.cap=cv2.VideoCapture(self.cfg['video_path'])#将yaml中的视频路径引入
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)#设置类内全局变量每秒的帧数
        self.frame_num=self.cap.get(cv2.CAP_PROP_FRAME_COUNT)##设置类内全局变量整个视频的帧数

    # 添加实例方法
    def _binary_dif(self,gray_lwpCV,th=20):
        '''
        将图像二值化并求帧间差值
        '''
        bin = gray_lwpCV < th #判定每帧图像像素是否小于阈值 ，小于阈值输出false，大于输出true
        if self.cfg['show']:
            bin_img = bin.astype(np.uint8) * 255 #将大于阈值的像素二值化
            cv2.imshow('bin_img', bin_img)
            cv2.waitKey(1)
        # 对于每个从背景之后读取的帧都会计算其与背景之间的差异，并得到一个差分图。
        diff = np.logical_xor(self.pre_frame, bin)#访问实例属性
        if self.cfg['show']:
            diff_img = diff.astype(np.uint8) * 255 #将有插值的额像素二值化
            cv2.imshow('diff_img', diff_img)
        self.res.append(np.sum(diff))#访问实例属性

    # 添加实例方法
    def cal_time_points(self):
        '''
        计算可能的癫痫发作时间点并保存
        '''
        das = np.array(self.res)#访问实例属性——将帧的差值存放为数组
        mean = np.mean(das) #求帧间差值的均值
        self.line_th=mean * self.cfg['f']#访问实例属性——帧间差值的均值*判定癫痫发作时间点的均值系数
        y = das > mean * self.cfg['f']#访问实例属性——判定帧的差值数组是否大于均值
        inds = np.argwhere(y == True)
        inds=inds.astype(np.float)
        inds/=(self.fps*60)#访问实例属性
        with open(self.txt_output_path,'w') as f:#访问实例属性
            for v in inds:
                f.write(str(v[0])+'\n')

    # 添加实例方法京脑
    def _save_npy(self):
        '''
        将数据保存到npy并读取
        '''
        np.save(self.res_saved_path, self.res)#访问实例属性

    # 添加实例方法
    def _hist(self):
        '''
        根据差值画出直方图
        '''
        plt.rcParams['figure.figsize'] = (self.cfg['hx'], self.cfg['hy'])#访问实例属性
        mins = self.frame_num/self.fps/60#访问实例属性
        xs = np.linspace(0,mins,len(self.res))#访问实例属性
        plt.plot(xs,self.res)#访问实例属性
        plt.xlabel('min')
        plt.ylabel('feture value')
        plt.title('Hist')
        plt.plot([0,mins],[self.line_th,self.line_th])#访问实例属性
        plt.savefig(self.hist_output_path)  # 存储图片

    # 添加实例方法
    def run(self):

        # 获取帧率和大小
        # fps = videoCapture.get(cv2.CAP_PROP_FPS)
        # get方法参数按顺序对应下表（从0开始编号，比如这里为了获取视频的总帧数，在下表是排第八个的 CV_CAP_PROP_FRAME_COUNT
        # frames_num = int(videoCapture.get(7))
        print(self.frame_num)

        # 测试用,查看视频size
        size = (int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),# 添加实例方法
                int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        print('size:' + repr(size))

        # es = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 4))
        pbar = Pbar(total=self.frame_num)# 添加实例方法self.frame_num，实现完成程度进度条
        while True:
            # 读取视频流
            pbar.update(1)
            grabbed, frame_lwpCV = self.cap.read() # 添加实例方法，读取视频，grabbed是一个布尔值，表示视频是否结束，只有最后才为false
            if grabbed:   #使用grabbed判断视频是否结束
                frame_lwpCV = cv2.resize(frame_lwpCV, None, fx=self.cfg['fx'], fy=self.cfg['fy'])# 添加实例方法
                if self.cfg['show']: #提供实时显示结果的开关，添加实例方法
                    cv2.imshow('src', frame_lwpCV)
                    cv2.waitKey(1)
                # 对帧进行预处理，转灰度图。
                gray_lwpCV = cv2.cvtColor(frame_lwpCV, cv2.COLOR_BGR2GRAY) #将每帧图片变成灰度图
                bin = gray_lwpCV < self.cfg['th']  #根据阈值判断亮度是否超过阈值
                if self.cfg['show']: #提供实时显示结果的开关，添加实例方法
                    bin_img = bin.astype(np.uint8) * 255  #超过阈值点亮化
                    cv2.imshow('bin_img', bin_img)
                    cv2.waitKey(1) #与cv2.imshow成对使用
                # 设置前一帧为后一帧的背景
                if self.pre_frame is None:
                    self.pre_frame = bin
                    continue
                diff = np.logical_xor(self.pre_frame, bin) #np.logical_xor逻辑异或判断：找到前一帧与当前帧取值不同的像素点
                self.pre_frame = bin #实时跟新前一帧
                if self.cfg['show']:
                    diff_img = diff.astype(np.uint8) * 255 #超过阈值点亮化
                    cv2.imshow('diff_img', diff_img)
                self.res.append(np.sum(diff))    #将每帧差值存入实例方法self.res的矩阵中
            else:
                break
        self._save_npy() #使用实例方法：将数据保存到npy并读取
        self.cal_time_points() #使用实例方法：计算可能的癫痫发作时间点并保存
        self._hist() #使用实例方法：画出直方图





if __name__ == '__main__':


    me = MicEpil()#创建对象
    me.run()#调用实例方法：跑大负载的实例属性
    # me.cal_time_points()
    # me._hist()
