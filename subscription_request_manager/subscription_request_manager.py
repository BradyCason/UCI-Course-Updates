# Manage incoming subscription requests from server
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

def valid_subscription(unsubscribe: bool, subscription):
    if subscription["type"] not in ["ALL", "NUM_ENROLLED", "STATUS", "SECTION_CODE"]:
        return [False, "Unknown Subscription Type: " + subscription["type"]]

    if unsubscribe:
        # Check if user is subscribed
        if conn.sismember("subscriptions", json.dumps(subscription)):
            return [True, ""]
        
        return [False, f"No subscription found for {subscription_title(subscription)}"]
    else:
        response = requests.get(f"https://api.peterportal.org/rest/v0/schedule/soc?term={subscription['year']}{subscription['term']}&department={subscription['department'].replace('&', '%26').replace('/', '%2F')}&courseNumber={subscription['course_num']}")
        if response.status_code != 200:
            return [False, f"Could not find {subscription_title(subscription, omit_type=True)}"]
        
        if not response.json()["schools"]:
            return [False, f"Could not find {subscription_title(subscription, omit_type=True)}"]

        # Check if user is already subscribed
        if conn.sismember("subscriptions", json.dumps(subscription)):
            return [False, f"You are already subscribed to {subscription_title(subscription)}"]

        return [True, ""]

def subscription_title(sub, omit_type=False):
    type_text = f" with Subscription Type: {sub['type']}"
    return f'{sub["department"]} {sub["course_num"]} {sub["term"]} {sub["year"]}{type_text if not omit_type else ""}'

if __name__ == "__main__":
    print("Running subscription_request_manager.py")
    conn = redis.Redis(host="localhost", port=6379, db=0)
    while True:
        while sub_req := conn.lpop("subscription requests"):
            sub_req = json.loads(sub_req)
            subscription = sub_req["subscription"]

            valid_sub = valid_subscription(sub_req["unsubscribe"], subscription)
            if valid_sub[0]:
                # Subscription is valid. Send subscription to subscriptions database
                if sub_req["unsubscribe"]:
                    # Unsubscribe from course
                    conn.srem("subscriptions", json.dumps(subscription))
                    conn.rpush("notifications", json.dumps({"destination": sub_req["destination"], "text": f"{subscription['author']}, you have unsubscribed from {subscription_title(subscription)}"}))
                else:
                    # Subscribe to course
                    conn.sadd("subscriptions", json.dumps(subscription))
                    conn.rpush("notifications", json.dumps({"destination": sub_req["destination"], "text": f"{subscription['author']}, you have subscribed to {subscription_title(subscription)}"}))
            else:
                # Subscriptions is not valid. Send notification to notifications database
                notification = {"destination": sub_req["destination"], "text": f"{subscription['author']}, your request failed. Reason: {valid_sub[1]}"}
                conn.rpush("notifications", json.dumps(notification))