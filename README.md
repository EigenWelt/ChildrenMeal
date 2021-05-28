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

端口号：BOARD
|变量名|端口号|类型|说明|
|---|---|---|---|
|SCK|29|GPIO.OUT|压力传感器时钟模块|
|DT|31|GPIO.IN|压力传感器数据模块|

### 五、文档
|函数|变量名|类型|说明|
|---|---|---|---|
|global|SCK|list|压力传感器时钟引脚|
|global|DT|list|数据引脚|
|global|APP_ID|string|appid|
|global|API_KEY|string|apikey|
|global|SECRET_KEY|string|secretkey|
|global|client||aipface对象|
|global|token|string|accesstoken|
|getToken|||获取百度云的accesstoken|
|**musicplay**|||播放音乐|
|**calweight**|||获取某一传感器的示数|
|calweight|**value**|int|示数|
|calweight|initWeight|int|去皮|
|calweight|nowWeight|int|称量值|
|calweight|flag|bool|是否首次测量|
|processWeight|||处理每一分餐盘的质量|
|**camerapos**|||摄像头定位餐品|
|camerapos|**res**|list|结果|
|camerapos|cap||摄像头读入图像|
|camerapos|rval|int|读入状态|
|camerapos|frame|image|读入图像|
|camerapos|img|image|旋转90°后的图像|
|camerapos|x1|int|截取矩形的左端点x|
|camerapos|x2|int|截取矩形的右端点x|
|camerapos|y1|int|截取矩形的上端点y|
|camerapos|y2|int|截取矩形的下断点y|
|camerapos|dst|image|截取的图像|
|camerapos|grey|image|灰度图|
|camerapos|element1|image|用于膨胀腐蚀的元素|
|camerapos|element2|image|用于二次膨胀的元素|
|camerapos|request_url|string|api|
|camerapos|f|file|文件读入数据流|
|camerapos|img|string|base64加密过的图片|
|camerapos|params|list|参量|
|camerapos|headers|string|headers|
|camerapos|response|module|request返回值|
|camerapos|raw|string|request原始文本|
|camerapos|json_data|json|raw形成的json文件|
|camerapos|top|int|返回的top|
|camerapos|height|int|返回的height|
|camerapos|width|int|返回的width|
|camerapos|left|int|返回的left|
|**faceSearch**|||人脸搜索|
|faceSearch|cap||摄像头读入图像|
|faceSearch|rval|int|读入状态|
|faceSearch|det|image|读入图像|
|faceSearch|det2|image|旋转90°后的图像|
|faceSearch|f|file|文件|
|faceSearch|pic||经过base64加密的图像|
|faceSearch|image|string|base64加密字符串|
|faceSearch|image_type|string|"BASE64"|
|faceSearch|group_id_list|string|组别|
|faceSearch|**response**||返回的response|
|**main**|||主函数|

### 临时文件
1. pospic.jpg 与菜品摄像头相对应的图像
2. SearchPic.jpg 与人像摄像头相对应的图片

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

### 2021.5.27 10:00

需要借用热缩管、万用表

称重传感器成为了现代工艺的残次品，需要用万用表测试虚焊/应变片损坏

推导力学方程，准备计算比例

需要用stm32测试力传感器

### 2021.5.28 12:00

人像识别完成了线上部署测试。

人像注册完成了线上测试。

正在开展压力传感器测试、摄像头距离测试

### 2021.5.28 17:00

除力传感器外，均已基本完成部署。项目文件已上传。

### 2021.5.28 21:00

已完成音响的部署，更新了appid便于可视化管理人脸库；

已完成人像识别、图像分割的检验。图像分割采用灰度图膨胀、腐蚀、再膨胀得到的图像。

摄像头与外壳已经组装完毕。

摄像头调参已完成。

缺少力传感器、以及关于力传感器的相应数据处理。目前已经测试成功放置3物品的情况。
