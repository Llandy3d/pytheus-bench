from redis import StrictRedis


connection = StrictRedis()
connection.flushall()
