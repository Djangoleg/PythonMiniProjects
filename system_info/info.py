import platform
import psutil
from cpuinfo import get_cpu_info

# Get OS information
os_name = platform.system()
os_version = platform.release()
os_arch = platform.machine()

# Get memory information
mem_total = psutil.virtual_memory().total / (1024.0 ** 3)  # in GB
mem_free = psutil.virtual_memory().available / (1024.0 ** 3)  # in GB
mem_used = mem_total - mem_free

# Get CPU information
#cpu_name = platform.processor()
cpu_name = get_cpu_info()['brand_raw']
core_numbers = get_cpu_info()['count']
cpu_load = psutil.cpu_percent(interval=1)  # get CPU load over 1 second

# Get HDD information
hdd_total = psutil.disk_usage('/').total / (1024.0 ** 3)  # in GB
hdd_free = psutil.disk_usage('/').free / (1024.0 ** 3)  # in GB
hdd_used = hdd_total - hdd_free
hdd_percent = psutil.disk_usage('/').percent

# Print system information
print(f"OS: {os_name} {os_version} ({os_arch})")
print(f"Memory: Total={mem_total:.2f}GB, Free={mem_free:.2f}GB, Used={mem_used:.2f}GB")
print(f"CPU: {cpu_name}, Cores={core_numbers}, Load={cpu_load}%")
print(f"HDD: Total={hdd_total:.2f}GB, Free={hdd_free:.2f}GB, Used={hdd_used:.2f}GB, Used%={hdd_percent}%")

# for key, value in get_cpu_info().items():
#         print("{0}: {1}".format(key, value))
