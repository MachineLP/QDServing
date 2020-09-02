> 本工程依赖 python 3.6

# 套模板-获取图片特征服务（gRPC）


## 概述
```shell
    此工程以gRPC服务的形式对外提供获取图片特征值，此服务在gpu下运行，依赖于tensorflow-gpu， 该服务以docker形式启动，可根据业务场景进行复用和扩容。
```


## 代码结构

```shell
.
├── app                                         # 代码路径
│   ├── config                                  # 配置文件  
│   ├── exts                                    # 外部依赖
│   ├── grpc                                    # grpc相关
│   └── template_core                           # gpu算法相关
├── docker                                      # docker相关
│   ├── debug
│   ├── dev
│   └── release
├── docs                                        # 文档目录
├── log                                         # 日志
│   └── log.log
├── README.md
├── run_client.py                               # grpc客户端
├── run_service.py                              # grpc服务端
└── test.py                                     # 测试脚本


```


## 服务器情况
### 线上服务器
```
```
### 开发服务器
```shell
服务器：麒麟
docker镜像：py36_tf_flask_sql_grpc:1.0

```
## 部署服务
```shell
docker-compose -f project_dir/start/docker-compose.yml up -d
or
docker-compose -f project_dir/docker/release/docker-compose.yml up -d
```

## 运行
```shell
1. 进入容器
2. 运行指令：python run_service.py
```

## 测试
```shell
1. 进入容器
2. 运行指令：python run_client.py
```

## 附录
```shell
- 仓库地址：git@git.huanleguang.com:ai-applications/ai-grpc-ant.git
```

