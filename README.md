# 营养膳食餐盘
## 项目需求
1. 注册人脸（省略）
2. 当餐盘出现重量时，通过摄像头1（CAM1）识别人脸，调用人脸识别。
3. 对于每一次称重，都调用提前录入的营养类型与质量计算乘积。将乘积+用户id记录至表中。
4. 从小程序中需要能够访问数据库，支持趋势线、单次记录访问。（省略）
## 实现方式
数据库采用在线形式，能够与服务器交互（demo中为离线数据库）
### 一、数据表设计
  1. user（id,faceToken,sex）
  2. record(id,date,typenum,weight)
  3. nutrition(typenum,typename,protein,heat,fat)
### 二、后端逻辑
面部注册（可以不实现）：
  1. 调用人脸管理模块，设置id为user表中即将添加的id，获取含有facetoken的json文件
  2. 在user表中添加记录。
面部
机器应用：
  1. 随时对重量传感器进行检测
  2. 当重量传感器发生较大变化的时候，认定为有目标出现，调用CAM1进行人脸识别
  3. 调用CAM2配合opencv获取图像
  4. 对捕获的图像利用多主体识别端口定位
  5. 将定位数据乘上比例系数k，得到在测重仪器上的坐标
  6. 对每一区域解力系方程进行计算。
  过程：
  7. 连接数据库（在线访问）
  8. 在record表中增添记录
### 三、手机端设计
### 四、GPIO口文档
## 进展与说明
### 2021.5.26 21:30
1. 完成了音响的配置与测试。需要注意出厂将右声道的正负极已经连接，因而需要连接红线。同时，要将树莓派的config中audio设置成从耳机孔输出。杜邦线过短，可能需要更换。
2. 完成了称重传感器的安装。膨胀螺丝是用来当底座的。需要注意有两个垫片，上下都要垫，不要使白色部分受力过度而造成损坏。尚未进行测试。
3. 完成了多主体端口调用的配置与测试、人脸识别的配置（但尚未测试）
4. 完成了摄像头的配置与测试。
5. opencv用pip安装的命令应为 pip install opencv-python
6. 不要让一台电脑有两个python版本，会导致pip爆炸。如果两个版本为2.x和3.x，则可以选择调用pip3/pip2，这样两个版本可以并存。
7. 先在百度平台建立新应用程序，接下来调用ai时需要先鉴权，具体实现：
```python
# client_id 为官网获取的AK， client_secret 为官网获取的SK
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id='+client_id+'&client_secret='+client_secret
response = requests.get(host)
if response:
    t = response.json()
    access_token = t['access_token']
```
值得注意的是，每一套token有效时长为30天，因而建议每次使用时调用新的token
8. 借用工具箱一套、显示器一台、键盘一个、焊台一台、拖线板一个。其中最大的箱子是用于装焊台的，需要注意保存。别的纸箱都可以给隔壁组。
9. 树莓派购买失误：micro-HDMI接口；没有散热片；没有SD卡；没有镜像……
