"""
Decoder module. This code was found in this stackoverflow post:
https://stackoverflow.com/questions/23256932/redis-py-and-hgetall-behavior.
The decoder is used to decode the response from redis.
"""

def decode_redis(src):
    if isinstance(src, list):
        rv = list()
        for key in src:
            rv.append(decode_redis(key))
        return rv
    elif isinstance(src, dict):
        rv = dict()
        for key in src:
            rv[key.decode()] = decode_redis(src[key])
        return rv
    elif isinstance(src, bytes):
        return src.decode()
    else:
        raise Exception("type not handled: " +type(src))

