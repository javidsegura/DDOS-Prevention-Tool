import time
import psutil
import threading
import os
import requests

TRESHOLD = 0.75


def get_container_memory_usage():
    try:
        # Try cgroups v2 first
        if os.path.exists('/sys/fs/cgroup/memory.current'):
            with open('/sys/fs/cgroup/memory.current', 'r') as f:
                usage_bytes = int(f.read())
            with open('/sys/fs/cgroup/memory.max', 'r') as f:
                limit_bytes_str = f.read().strip()
                # Handle "max" value in cgroups v2
                limit_bytes = float('inf') if limit_bytes_str == "max" else int(limit_bytes_str)
        
        # Fall back to cgroups v1
        elif os.path.exists('/sys/fs/cgroup/memory/memory.usage_in_bytes'):
            with open('/sys/fs/cgroup/memory/memory.usage_in_bytes', 'r') as f:
                usage_bytes = int(f.read())
            with open('/sys/fs/cgroup/memory/memory.limit_in_bytes', 'r') as f:
                limit_bytes = int(f.read())
        
        else:
            process = psutil.Process(os.getpid())
            usage_bytes = process.memory_info().rss
            limit_bytes = psutil.virtual_memory().total
        
        # Convert to MB and calculate percentage
        usage_mb = usage_bytes / (1024 * 1024)
        limit_mb = limit_bytes / (1024 * 1024)
        percentage = (usage_bytes / limit_bytes) * 100 if limit_bytes != float('inf') else 0
        
        print(f"Memory Usage: {usage_mb:.2f}MB / {limit_mb:.2f}MB ({percentage:.1f}%)")
        return usage_mb, limit_mb, percentage
    except Exception as e:
        print(f"Error reading container memory: {e}")

def monitor_memory(tresholdMemory:float=TRESHOLD, 
                   tresholdAttacker:float=TRESHOLD,
                   wait_time:float=3,
                   ban_duration:float=60):
    while True:
        usage_mb, limit_mb, percentage = get_container_memory_usage()
        if percentage > tresholdMemory:
            print(f"\t\t!> Memory usage is greater than {tresholdMemory}%! Analyzing traffic")
            try:
                if limit_mb < 7000:
                    response = requests.post("http://host.docker.internal:12345/trigger-defense", 
                                         json={"wait_time": wait_time,
                                               "tresholdAttacker": tresholdAttacker,
                                               "ban_duration": ban_duration})
                else: # Working locally
                    response = requests.post("http://localhost:12345/trigger-defense", 
                                         json={"wait_time": wait_time,
                                               "tresholdAttacker": tresholdAttacker,
                                               "ban_duration": ban_duration})
                    
                defense_data = response.json()
                print(f"Defense response: {defense_data}")
                return defense_data
            except Exception as e:
                print(f"Error triggering defense: {e}")
                break
        time.sleep(wait_time)

def startDefense(tresholdMemory:float=TRESHOLD, tresholdAttacker:float=TRESHOLD, wait_time:float=3, ban_duration:float=60) -> dict:
    print(f"Starting defense with treshold {tresholdMemory} and wait time {wait_time}")
    global TRESHOLD
    TRESHOLD = tresholdMemory
    
    # Create an event to signal when monitor_memory returns
    event = threading.Event()
    defense_result = [None]  # Use a list to store the result
    
    def wrapped_monitor():
        defense_result[0] = monitor_memory(tresholdMemory=tresholdMemory, 
                                           tresholdAttacker=tresholdAttacker, 
                                           wait_time=wait_time,
                                           ban_duration=ban_duration)
        event.set()
    
    monitor_thread = threading.Thread(target=wrapped_monitor, daemon=True)
    monitor_thread.start()
    
    # Wait for the monitor thread to return data
    try:
        event.wait()
        return defense_result[0]
    except KeyboardInterrupt:
        print("\nStopping memory monitor...")
        return None



