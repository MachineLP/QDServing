
## 服务器情况
### 线上服务器
```
.
├── model_serving             # gpu算法模块（gRPC服务）
│   ├── app
│   ├── docker
│   ├── docs
│   ├── log
│   ├── README.md
│   ├── run_client.py
│   ├── run_service.py
│   └── test.py
├── qd_serving                # 数据模块（gRPC服务）
│   ├── app
│   ├── docker
│   ├── docs
│   ├── log
│   ├── README.md
│   ├── run_client.py
│   ├── run_service.py
│   └── test.py


```

## 部署服务
```shell
docker-compose -f project_dir/start/docker-compose.yml up -d
or
docker-compose -f project_dir/docker/release/docker-compose.yml up -d
```
