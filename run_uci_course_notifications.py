import threading
import subprocess
import time

def run_script(script_name):
    subprocess.run(["python", script_name])

def run_redis_server():
    redis_server_executable = r"C:\Users\brady\OneDrive\Documents\redis-server.exe"
    redis_conf_file = r"C:\Users\brady\OneDrive\Documents\redis.windows.conf"
    
    try:
        # Run Redis server
        subprocess.run([redis_server_executable, redis_conf_file], cwd=r"C:\Users\brady\OneDrive\Documents", check=True)
    except subprocess.CalledProcessError as e:
        print("Error running Redis server:", e)

if __name__ == "__main__":
    redis_server_thread = threading.Thread(target=run_redis_server)
    redis_server_thread.start()

    # Give some time for Redis server to start
    time.sleep(2)

    # Run scripts
    discord_bot_thread = threading.Thread(target=run_script, args=("./discord_bot/bot_initializer.py",))
    subscription_request_manager_thread = threading.Thread(target=run_script, args=("./subscription_request_manager/subscription_request_manager.py",))
    course_watcher_thread = threading.Thread(target=run_script, args=("./course_watcher/course_watcher.py",))

    discord_bot_thread.start()
    subscription_request_manager_thread.start()
    course_watcher_thread.start()

    # Wait for all threads to complete
    redis_server_thread.join()
    discord_bot_thread.join()
    subscription_request_manager_thread.join()
    course_watcher_thread.join()