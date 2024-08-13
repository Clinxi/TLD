# TLD项目后端使用及部署说明

---
[toc]

## python环境配置
本算法使用的是python, 因此需要配置对应的python环境
### anaconda

#### 非root用户安装
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
#### 配置环境
1. 进入项目目录后创建需要的python环境
```shell
cd path/to/TLD
conda env create -f environment.yml
```
2. 启动python环境
```shell
conda activate defect_detect
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

