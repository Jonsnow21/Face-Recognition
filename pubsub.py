import redis
import time
from facenet import recognize

queue = redis.StrictRedis(host='localhost', port=6379, db=0)

p = queue.pubsub()

p.subscribe('test')

while True:
    message = p.get_message()
    if message:
        print(str(message['data']))
        if isinstance(message['data'], bytes):
            diff, person = recognize(message['data'].decode('utf-8'))

            if diff is None or diff > 0.7:
                queue.publish('result', 'ERR_NOT_FOUND_IN_DB')
            else:
                queue.publish('result', person)

        print(type(message['data']))
    time.sleep(1)
