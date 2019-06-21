import json
import pika
import util
from pika import exceptions

class RabbitMQ:
  """Clase para establecer una conexion con RabbitMQ"""

  @classmethod
  def __init__(cls, **kwargs):
    """Method init"""
    keys = util.DICT2KEYS(kwargs, 'host', 'virtualhost', 'port', 'queue')
    cls.host, cls.virtualhost, cls.port, cls.queue = keys

  @classmethod
  def connect(cls):
    """Connect to RabbitMQ"""
    try:
      cls.connection = pika.BlockingConnection(pika.ConnectionParameters(cls.host, cls.port, cls.virtualhost))
      cls.channel = cls.connection.channel()
      cls.channel.queue_declare(queue=cls.queue)
      print('connection_established_rabbit')
      return True
    except exceptions.AMQPConnectionError as error:
      print('connection_established_not_rabbit', str(error))
      return False

  @classmethod
  def disconnect(cls):
    """Disconnect"""
    cls.connection.close()
