# oj backend

## dev 运行环境
> 需要环境 Python3.8, Redis, PostgreSQL  
> Redis 和 PostgresSQL 的安装可以使用oj-tools中的docker配置文件

安装依赖：`pip install -r requirements.txt`
## dev 更新数据库模型结构
```sh
python manage.py makemigrations
```
## dev 同步数据库模型结构到数据库
```sh
python manage.py migrate
```

## dev 执行命令
```sh
python manage.py runserver
```

## 创建一个管理员用户
```sh
python manage.py createsuperuser
```


---
## 推荐IDE
JetBrains PyCharm

## 静态代码检查
```shell script
flake8 --ignore=E722,W504 --exclude=venv,migrations,__pycache__ --max-line-length=120 .
```

## celery
```shell script
celery -A ddl worker --concurrency=1 -Q result
```

---
## deploy
```
docker-compose -f deploy.yaml build
docker-compose -f deploy.yaml up -d
```
## build with proxy
```
docker-compose -f deploy.yaml build --build-args HTTPS_PROXY=socks5://127.0.0.1:1080
```