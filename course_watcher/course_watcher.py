# Watch for course changes for all subscriptions. Push notifications to redis
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

import time
import redis
import requests
import json

def get_dict_int(dict, field_name):
    ''' Returns the integer with key, field_name in dict '''
    data = dict[field_name]
    try:
        data = int(data)
        return data
    except:
        return 0

def check_for_changes(new_section, old_section, subscription):
    notifications = []

    # Get section data
    new_max_capacity = get_dict_int(new_section, "maxCapacity")
    new_num_enrolled = get_dict_int(new_section["numCurrentlyEnrolled"], "totalEnrolled")
    new_num_waitlist = get_dict_int(new_section, "numOnWaitlist")
    new_status = new_section['status']

    old_max_capacity = get_dict_int(old_section, "maxCapacity")
    old_num_enrolled = get_dict_int(old_section["numCurrentlyEnrolled"], "totalEnrolled")
    old_num_waitlist = get_dict_int(old_section, "numOnWaitlist")
    old_status = old_section['status']

    # Check if num seats is new
    if new_num_enrolled != old_num_enrolled and subscription["type"] in ["ALL", "NUM_ENROLLED"]:
        notifications.append({"destination": subscription["author"], "text": f"The Number of Seats in {course_title(subscription)} {section_title(new_section)} has changed from {old_num_enrolled}/{old_max_capacity} to {new_num_enrolled}/{new_max_capacity}"})
    
    # Check if num seats on waitlist changed
    if new_num_waitlist != old_num_waitlist and subscription["type"] in ["ALL", "NUM_ENROLLED"]:
        notifications.append({"destination": subscription["author"], "text": f"The Number of spots on the waitlist in {course_title(subscription)} {section_title(new_section)} has changed from {old_num_waitlist} to {new_num_waitlist}"})

    # Check if status changed (new spot opened up in section or waitlist)
    if new_status != old_status and subscription["type"] in ["ALL", "STATUS"]:
        notifications.append({"destination": subscription["author"], "text": f"The Status of {course_title(subscription)} {section_title(new_section)} has changed from {old_status} to {new_status}"})

    return notifications

def update_courses(conn):
    # Get all subscriptions and previous course data
    subscriptions = [json.loads(x) for x in conn.smembers("subscriptions")]
    old_courses_data = [json.loads(x) for x in conn.smembers("watched courses")]

    # Create list of all watched courses data
    new_courses_data = []
    for sub in subscriptions:
        course_data = requests.get(f'https://api.peterportal.org/rest/v0/schedule/soc?term={sub["year"]}{sub["term"]}&department={sub["department"].replace("&", "%26").replace("/", "%2F")}&courseNumber={sub["course_num"]}')
        response = course_data.json()
        sections = response["schools"][0]["departments"][0]["courses"][0]["sections"]

        new_courses_data.append({"course": course_title(sub), "sections": sections})

    # Check for differences in old database and new database
    notifications = []
    for sub in subscriptions:
        old_sections = None
        found_old = False
        for course in old_courses_data:
            if course.get("course") == course_title(sub):
                found_old = True
                old_sections = course["sections"]
        
        if found_old: # Ensure that the subscription is not new

            new_sections = None
            for course in new_courses_data:
                if course.get("course") == course_title(sub):
                    new_sections = course["sections"]

            for new_section in new_sections:
                found_old = False
                for old_section in old_sections:
                    if old_section["sectionCode"] == new_section["sectionCode"]:
                        found_old = True
                        notifications.extend(check_for_changes(new_section, old_section, sub))
                        break
                if not found_old:
                    # new section added
                    if (sub["type"] in ["ALL", "SECTION_ADDED"]):
                        notifications.append({"destination": sub["author"], "text": f"New section added for {course_title(sub)}: {section_title(new_section)}"})
            


    # Update the watched courses database
    if old_courses_data:
        for old_course in old_courses_data:
            conn.srem("watched courses", json.dumps(old_course))
    if new_courses_data:
        for new_course in new_courses_data:
            conn.sadd("watched courses", json.dumps(new_course))

    return notifications

def course_title(sub):
    return f'{sub["department"]} {sub["course_num"]} {sub["term"]} {sub["year"]}'

def section_title(section):
    return f'{section["sectionType"]} {section["sectionNum"]}, Code: {section["sectionCode"]}, Instructor{"s" if len(section["instructors"]) > 1 else ""}: {", ".join(section["instructors"])}'

if __name__ == "__main__":
    print("Running course_watcher.py")
    conn = redis.Redis(host="localhost", port=6379, db=0)

    while True:
        for notification in update_courses(conn):
            print(notification)
            conn.rpush("notifications", json.dumps(notification))
        time.sleep(300) # Update every 5 minutes