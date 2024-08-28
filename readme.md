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
3. 添加环境变量（可在安装时配置，勾选框中图片即可）![image](https://github.com/user-attachments/assets/6ce25ad6-286d-4105-8cd0-de804fbd15ba)

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
conda create -n 环境名 python=3.9 -f windows_environment.yml
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

#### 非root用户安装
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

## 测试案例

