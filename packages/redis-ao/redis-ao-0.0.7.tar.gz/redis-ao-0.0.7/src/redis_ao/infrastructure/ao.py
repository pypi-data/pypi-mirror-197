from typing import Any, Optional
import redis, pickle
from ddd_objects.lib import get_random_string
from .do import RedisData


class RedisAccessOperator:
    """Redis访问接口类。
    """
    def __init__(self, ip: str, port: int, token: str) -> None:
        self.client = redis.StrictRedis(host=ip, port=port, password=token)


    def send_request(self, domain:str, key:str, request:Any, request_id=None)->str:
        """发送请求到请求队列。
        Args:
            domain (str): 请求队列所属的领域。
            key (str): 请求队列名称。
            request (Any): 请求体。
        Returns:
            返回请求id。
        """
        if request_id is None:
            request_id = get_random_string(10)
        key = f'{domain}:{key}'
        obj = RedisData(id=request_id, obj=request)
        obj = pickle.dumps(obj)
        self.client.lpush(key, obj)
        return request_id


    def get_request(self, domain:str, key:str)->Optional[Any]:
        """从请求队列中取一个请求出来。
        Args:
            domain (str): 请求队列所属的领域。
            key (str): 请求队列名称。
        Returns:
            如果存在返回一个请求体，否则返回None
        """
        key = f'{domain}:{key}'
        obj = self.client.lpop(key)
        if obj:
            return pickle.loads(obj)
        return None

    
    def get_queue_length(self, domain:str, key:str)->int:
        """获取队列长度。
        Args:
            domain (str): 请求队列所属的领域。
            key (str): 请求队列名称。
        Returns:
            返回长度，不存在返回0
        """
        key = f'{domain}:{key}'
        return self.client.llen(key)


    def set_response(self, domain:str, request_id:str, response:Any, timeout:int=300)->bool:
        """保存一个回复体到redis。
        Args:
            domain (str): 请求队列所属的领域。
            request_id (str): 对应请求的id。
            response (Any): 回复体。
            timeout (int): 回复体在redis中存在的时间。
        Returns:
            返回是否保存成功。
        """
        obj = pickle.dumps(response)
        key = f'{domain}:{request_id}'
        succeed = self.client.setex(key, timeout, obj)
        return succeed


    def get_response(self, domain:str, request_id)->Optional[Any]:
        """从redis中获取一个回复体。
        Args:
            domain (str): 请求队列所属的领域。
            request_id (str): 对应请求的id。
        Returns:
            如果成功返回请求体，否则返回None
        """
        key = f'{domain}:{request_id}'
        obj = self.client.get(key)
        if obj:
            return pickle.loads(obj)
        return None



