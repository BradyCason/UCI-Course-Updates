# server_util
Tools for debugging and interacting with server. This script is not run in the main application. It is just for debugging purposes.

# Form of data in redis server database
- "subscription requests": `{"unsubscribe": bool, "subscription":{"department": str, "course_num": str, "term": str, "year":str, "author": str}}`
- "notifications": `{"destination": "user" or "general", "text": str}`
- "subscriptions": `{"type": str, "author": str, "department": str, "course_num": str, "term": str, "year": str}`
- "watched courses": `{"course": "COMPSCI 161 Fall 2024", "sections": []}`