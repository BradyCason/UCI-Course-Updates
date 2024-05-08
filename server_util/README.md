Redis: Remote Dictionary Service

Note for admin:
How to Start Server:
cd C:\Users\brady\OneDrive\Documents
redis-server.exe redis.windows.conf

How to Stop Server:
Ctrl + c


Server databases:
"subscription requests": {"unsubscribe": True, "subscription":{"department": department, "course_num": course_num, "term": term, "year":year, "author": str(ctx.author)}}

"notifications": 
{"destination": "user" or "general", "text": "string"}

"subscriptions":
{"type": "all", "author": "bradycason", "department": "COMPSCI", "course_num": "161", "term": "Fall", "year": "2024"}

"watched courses":
{"course": "COMPSCI 161 Fall 2024", "sections": []}