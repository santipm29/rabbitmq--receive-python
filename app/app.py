'''Module main'''
import json
from rabbitmq import RabbitMQ

class App:
    '''class Application'''

    @classmethod
    def __init__(cls):
        '''Method init'''
        cls.config = json.loads(open('config/config.json').read())
      

    @classmethod
    def callback(cls, channel, method, properties, body):
        '''Receive message '''
        del properties
        data = json.loads(body.decode('utf-8'))
        print(data)
        
        channel.basic_ack(delivery_tag=method.delivery_tag)

    @classmethod
    def main(cls):
        '''start application'''
        objqueue = RabbitMQ(**cls.config['source'])
        if not objqueue.connect():
            raise RuntimeError(['connection_not_established'])
        objqueue.channel.basic_consume(
            queue=cls.config['source']['queue'],
            on_message_callback=cls.callback,
            auto_ack=False
        )
        objqueue.channel.start_consuming()

if __name__ == '__main__':
    App().main()
