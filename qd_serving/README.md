
```
flask服务:
nohup /home/di/anaconda3/bin/gunicorn -w 16 -b 0.0.0.0:9969 flask_run:app > flask_run.log 2>&1 &
flask服务测试:
curl -i -H "Content-Type: application/json" -X POST -d '
{
"content":"你好啊"
}' 127.0.0.1:9959/infer
```

```
grpc服务:
nohup /home/di/anaconda3/bin/python grpc_run.py > grpc_run.log 2>&1 &
grpc服务测试:
python grpc_run_client.py
```

## 支持docker部署
