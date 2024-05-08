# Tools for debugging and interacting with server
# Copyright (C) 2024  Brady Cason

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

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
