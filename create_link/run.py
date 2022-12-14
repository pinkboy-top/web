# gun.py
import multiprocessing

# 协程需要此补丁
# form gevent import monkey
# monkey.patch_all()
# 其他非uvicorn需打开此配置 
# worker_class = "gevent"

# ip + port
bind = "0.0.0.0:9696"
# 超时时间
timeout = 40

# 并行工作进程数
workers = multiprocessing.cpu_count() * 2 + 1
# 每个进程开启的线程数
threads = 2
#服务器中在pending状态的最大连接数 (建议 64-2048)
backlog = 2048


# sync(同步, eventlet(并发), gevent（协程, tornado, gthread，此处使用
worker_class = "uvicorn.workers.UvicornWorker"

# 客户端同时最大连接数，适用于 gevent eventlet
worker_connections = 1000

# 以守护进程形式运行：后台运行
daemon = True

loglevel = 'debug'
pidfile = 'log/gunicorn.pid'
accesslog = 'log/gun-access.log'
errorlog = 'log/gun-error.log'

# reload=true 自动重启
# chdir = '/path/' 指定它的工作路径