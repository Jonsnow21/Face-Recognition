from facenet import FaceNetClass

import redis
import json
import cv2
import ast


class Listener:
    def __init__(self, r, channels):
        self.redis = r
        self.pub_sub = self.redis.pubsub()
        self.pub_sub.subscribe(channels)
        self.faceNet = FaceNetClass()

    def work(self, item):
        print(item['channel'], ":", item['data'])
        print(self.pub_sub)

        if isinstance(item['channel'], bytes) and item['channel'].decode('utf-8') == 'train':
            print(item['channel'])
            print(str(item['data']))
            if isinstance(item['data'], bytes):
                json_str = item['data'].decode('utf-8')
                print(json_str)
                data = ast.literal_eval(json.loads(json_str))
                print(data)
                print(type(data))
                self.faceNet.one_shot_train(data)
                print('After train')
                self.redis.publish('result', 'SUCCESS')
        elif isinstance(item['channel'], bytes) and item['channel'].decode('utf-8') == 'test':
            print(str(item['data']))
            if isinstance(item['data'], bytes):
                file = item['data'].decode('utf-8')
                print(file)
                data = self.faceNet.recognize(file)
                print(data)
                if data is None:
                    self.redis.publish('result', 'PERSON_NOT_FOUND_IN_DB')
                else:
                    diff, person = data
                    self.redis.publish('result', person)

            print(type(item['data']))

    def run(self):
        for item in self.pub_sub.listen():
            print(item)
            if item['data'] == "KILL":
                self.pub_sub.unsubscribe()
                print(self, "unSubscribed and finished")
                break
            else:
                self.work(item)


if __name__ == "__main__":
    redis = redis.StrictRedis(host='localhost', port=6379, db=0)
    client = Listener(redis, ['test', 'train'])
    client.run()
