import time
import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
     retries = 5
     while True: # 檢查 try 運算式是否回傳 True
         try:
             return cache.incr('hits')
         except redis.exceptions.ConnectionError as exc: # 如果不是 True 就執行 except 程式碼, 將 redis.exceptions.ConnectionError 當作 exc 來看
             if retries == 0:
                 raise exc
             retries -= 1
             time.sleep(0.5)

@app.route('/')
def get_index():
     count = get_hit_count()
     return 'Yo! 你是第 {} 次瀏覽\n'.format(count)

if __name__ == "__main__":
     app.run(host="0.0.0.0", debug=True)
