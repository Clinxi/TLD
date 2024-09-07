# TLD项目后端使用及部署说明

---
[TOC]

## Python环境配置
本算法使用的是python, 因此需要配置对应的python环境
### Anaconda下载安装
#### Linux环境 非root用户安装
1. 在以下地址进行下载:
```
https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/
```
2. cd到anaconda安装包目录下，安装anaconda:
```shell
bash Anaconda3-5.0.1-Linux-x86_64.sh
```
3. 按enter浏览完协议以后，输入yes同意协议（注意再选择安装路径的时候，按enter即可安装在默认目录下
4. 将conda加入环境变量
```shell
echo 'export PATH="path/to/anaconda3/bin:$PATH"'>>~/.bashrc
source ~/.bashrc
```
#### Window环境 下载安装

1. 在以下地址进行下载:
```
https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/
```
2. 根据所运行的windows架构对应下载 conda 安装包并进行安装，安装路径采用默认路径。
![image](https://github.com/user-attachments/assets/8c25095b-153a-4c58-a6f5-fca6b1dcaf34)
![image](https://github.com/user-attachments/assets/886582ae-69ff-41c3-93fb-3a01cc15846e)
![image](https://github.com/user-attachments/assets/d693bbf8-427b-4abc-bbcf-467a463c66a7)

4. 添加环境变量(可在安装时配置，勾选框中图片即可).

![image](https://github.com/user-attachments/assets/2b746b42-40d6-45aa-a7f4-27aca25be0a7)

### 根据系统环境选择项目主目录下的 .yml 文件
#### linux环境——配置
1. 进入项目目录后创建需要的python环境
```shell
cd path/to/TLD
conda env create -f linux_environment.yml
```
2. 启动python环境
```shell
conda activate defect_detect
```
3. 添加yolo环境包
```shell
cd path/to/TLD/src/main/algorithm/yolov10
pip install -e .
```
#### windows环境——配置
1. 进入项目目录后创建需要的 python 环境
```shell
cd path/to/TLD
conda env create -n 环境名 python=3.9 -f windows_environment.yml
```
2. 启动python环境
```shell
conda activate 环境名
```
3. 添加yolo环境包
```shell
cd path/to/TLD/src/main/algorithm/yolov10
pip install -e .
```

## 后端

### Jave+Maven

#### Linux环境 非root用户安装
**java:**
1. 去oracle官网下载jdk文件
2. 上传服务器然后解压
```shell
 tar -zxvf (jdk-11.0.20_linux-x64_bin.tar.gz) -C /destination
```
3. 添加环境变量
```shell
vim ~/.bashrc //更改坏境变量,.profile⽂件也可以
在任意空⽩处添加：
# Java（注释）
export JAVA_HOME=/nfs/DamDetection/apps/jdk1.8.0_201
export PATH=.:$JAVA_HOME/bin:$PATH
export CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
```

**maven:**
1. 使用wget相应的maven包即可
```shell
wget --no-check-certificate https://dlcdn.apache.org/maven/maven-3/3.9.5/binaries/apache-maven-3.9.5-bin.tar.gz
```
2. tar -zxvf解压
3. 配置环境变量
```shell
export MAVEN_HOME=path/to/apache-maven-3.9.5
export PATH=${MAVEN_HOME}/bin:$PATH
```
#### Window环境 下载安装
**java:**
1. 去oracle官网下载jdk文件
 [jdk1.8下载地址](https://www.oracle.com/java/technologies/downloads/?er=221886#java8-windows)  
2. 下载安装完毕后设置环境变量

 ![image](https://github.com/user-attachments/assets/f5b3fbb8-4463-4384-b6c3-7e1f7588af1f)

 添加JAVA_HOME系统变量 ：变量值即是jdk的安装路径，本文安装在D:\Java\jdk-1.8，根据自己的安装路径修改即可.

 ![image](https://github.com/user-attachments/assets/e7721cef-b7ad-4d22-9d15-3c539f9ffb57)
 
 添加CLASSPATH系统变量，变量值为：
 ```
 .;%JAVA_HOME%\lib\dt.jar;%JAVA_HOME%\lib\tools.jar
 ```
 
 ![image](https://github.com/user-attachments/assets/90457ad0-90d6-470a-921d-69ec5f9ec776)

 ![image](https://github.com/user-attachments/assets/573eeeff-7a0d-4ea3-a3a6-961b4bc0c6eb)
 
 在系统变量Path中新建增加下述两个变量
 ```
 %JAVA_HOME%\bin 
 %JAVA_HOME%\jre\bin
 ```
 设置完成后打开cmd检查是否成功

![image](https://github.com/user-attachments/assets/b344f4a6-44f9-4202-928e-1784727eef91)

**maven:**

1.下载软件包

 [maven3.9.5下载地址](https://dlcdn.apache.org/maven/maven-3/3.9.5/binaries/) 
 
2.解压安装包，修改setting文件
 ![image](https://github.com/user-attachments/assets/be789ab2-4c56-455d-881c-0b413e40dca8)
 
 搜索localRepository，添加maven仓库的位置。本文是在D盘下的.m文件夹下，创建的repository文件夹充当maven仓库。读者可以在非驱动盘外的任意位置创建maven仓库，将仓库路径按图示添入settings配置文件即可。
 
 ![image](https://github.com/user-attachments/assets/699532d5-fe68-409d-810b-9f97f2e0b4ab)

 保存即可
 
3.编辑环境变量
 
 ![image](https://github.com/user-attachments/assets/49d8bf94-6393-4ff2-8980-74b1b6f67961)

 ![image](https://github.com/user-attachments/assets/7c9d33d2-44a8-485e-be4f-928ec3345837)

 新建增加下述变量
 ```
 %MAVEN_HOME%\bin
 ```

 ![image](https://github.com/user-attachments/assets/ec3e6549-68c4-42f9-895b-185fee01468c)

 最后打开cmd输入mvn -version检查

 ![image](https://github.com/user-attachments/assets/bb6e7584-b01d-4abe-aad7-e5c154ff4db5)

 

### 运行后端
进入项目目录并运行后端
```shell
cd path/to/TLD
mvn spring-boot:run
```

## 输入端要求
可以根据以下目录下的具体例子来明确要求:
```sh
TLD/src/main/java/org/zjuvipa/util/Client.java
```

根据要求, 传给后端的应该是一个APhotoWithStandards对象的list, APhotoWithStandards代码在
```sh
TLD/src/main/java/org/zjuvipa/entity/APhotoWithStandards.java
```
与其相关的成员变量的类分别有DetectOriginalPhoto和ProjectStandard, 分别如下所示
```sh
TLD/src/main/java/org/zjuvipa/entity/DetectOriginalPhoto.java
TLD/src/main/java/org/zjuvipa/entity/ProjectStandard.java
```
## 后端添加字段处理方式
配置java后需要更改OrignalPhotoInfor.py下的class DetectOriginalPhoto和class ProjectStandard这两个类__init__函数
注意定义顺序和变量名称需要跟接受到的JSON内的字段顺序和名称相一致。

### 示例图如下

Json文件下配置
You can view the test case file [here](./src/main/algorithm/test/case4/test.json).

class DetectOriginalPhoto类设置
![img_1](https://github.com/user-attachments/assets/b8f56ec0-8278-408b-8985-f53e48b76a61)

class ProjectStandard类设置
![img_2](https://github.com/user-attachments/assets/296f704b-58b3-4413-85c5-7f18272c016c)

## 测试案例

