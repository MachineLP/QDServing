> 本工程依赖 python 3.6



## 消息处理模块 

### 表信息
作品：gaodingx.contents
gaodingx.user_templets
模板：caishichang.contents
caishichang.templets


## 部署位置

服务器： 47.96.120.55

开发目录：/data_ext/docker_deploy/python/auto-nested-template
开发使用的docker： 9dd16e924af2   0.0.0.0:41000->41000/tcp,  0.0.0.0:41005->22/tcp  gpu_auto_nested_template


## 开放端口

50000-50049




## 

## 依赖


### python 依赖

```shell

pip install Flask
pip install Flask-SQLAlchemy
pip install opencv-python 

## 或者
pip install opencv-python==3.2.0.8


pip install Flask-Script
pip install Flask-Migrate
pip install pymysql


```


### 依赖库

```shell

apt-get install libsm6
apt-get install libxrender1
apt-get install libxext-dev

```



## 运行流程

### 建立数据库

```mysql
mysql> create DATABASE shoe;

```



### 迁移数据库

```shell

python manage.py db migrate
python manage.py db upgrade

```





## 运行

```python

python instance.py

```


## 测试新建模型

```python

cd test
python post_load_model.py

```


## 请求网页

```


```



## 速度测试参考

```
单条请求（均含20张图）：
1.导入模板，用时：16-20s
2.新增套图，用时：9-15s
```



