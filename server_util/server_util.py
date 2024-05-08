import redis
import json
import requests

def delete_all_subscriptions(conn):
    for sub in conn.smembers("subscriptions"):
        conn.srem("subscriptions", sub)

def print_all_subscriptions(conn):
    for sub in conn.smembers("subscriptions"):
        print(sub)

def print_all_watched_courses(conn):
    for course in conn.smembers("watched courses"):
        print(course)
        print()

if __name__ == "__main__":
    conn = redis.Redis(host='localhost', port=6379, db=0)
    
    # r.rpush("list", "Croatia")
    # r.rpush("list", "Bahamas")

    # while True:
    #     while notification := conn.lpop("notifications"):
    #         print("")
    #         print(notification)
    #         print("Subscriptions:")
    #         print(conn.smembers("subscriptions"))
    delete_all_subscriptions(conn)
