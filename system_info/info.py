import platform
import psutil
import socket
import requests
from cpuinfo import get_cpu_info


def get_os_info():
    """
    Get the name, version and architecture of the current operating system.

    Returns:
        tuple: A tuple containing the OS name, version and architecture.
    """
    # Get the name of the operating system
    os_name = platform.system()
    # Get the version of the operating system
    os_version = platform.release()
    # Get the architecture of the operating system
    os_arch = platform.machine()
    # Return a string containing the OS name, version and architecture
    return os_name, os_version, os_arch


def get_memory_info():
    """
    Get the total, free and used memory in GB

    Returns:
        tuple: A tuple containing the total, free and used memory in GB
    """
    # Get the total memory in bytes
    total_memory_bytes = psutil.virtual_memory().total
    # Convert the total memory from bytes to GB
    total_memory = total_memory_bytes / (1024.0 ** 3)
    # Get the free memory in bytes
    free_memory_bytes = psutil.virtual_memory().available
    # Convert the free memory from bytes to GB
    free_memory = free_memory_bytes / (1024.0 ** 3)
    # Calculate the used memory in bytes
    used_memory_bytes = total_memory_bytes - free_memory_bytes
    # Calculate the used memory in GB
    used_memory = used_memory_bytes / (1024.0 ** 3)
    # Return a tuple containing the total, free, and used memory in GB
    return total_memory, free_memory, used_memory


def get_cpu_information():
    """
    Get the name, number of cores and load of the CPU.

    Returns:
        tuple: A tuple containing the name, number of cores and load of the CPU.
    """
    # Get the name of the CPU
    cpu_name = get_cpu_info()['brand_raw']
    # Get the number of cores
    core_numbers = get_cpu_info()['count']
    # Get the load of the CPU over 1 second
    cpu_load = psutil.cpu_percent(interval=1)
    # Return a tuple containing the name, number of cores and load of the CPU
    return cpu_name, core_numbers, cpu_load


def get_hdd_information():
    """
    Get the total, free and used storage space of the root partition in GB

    Returns:
        tuple: A tuple containing the total, free and used storage space of
        the root partition in GB and the percentage of the used storage.
    """
    # Get the total storage space of the root partition in bytes
    root_partition_total_bytes = psutil.disk_usage('/').total
    # Convert the total storage space from bytes to GB
    hdd_total = root_partition_total_bytes / (1024.0 ** 3)

    # Get the free storage space of the root partition in bytes
    root_partition_free_bytes = psutil.disk_usage('/').free
    # Convert the free storage space from bytes to GB
    hdd_free = root_partition_free_bytes / (1024.0 ** 3)

    # Calculate the used storage space of the root partition in bytes
    root_partition_used_bytes = root_partition_total_bytes - root_partition_free_bytes
    # Calculate the used storage space of the root partition in GB
    hdd_used = root_partition_used_bytes / (1024.0 ** 3)

    # Get the percentage of the used storage space of the root partition
    hdd_percent = psutil.disk_usage('/').percent

    # Return a tuple containing the total, free and used storage space of
    # the root partition in GB and the percentage of the used storage
    return hdd_total, hdd_free, hdd_used, hdd_percent


def get_ip_information():
    """
    Get the internal and external IP addresses of the machine.

    Returns:
        tuple: A tuple containing the internal and external IP addresses.
    """
    # Get the internal IP address of the machine
    # This is the IP address that is used to communicate with other machines
    # on the same network
    ip_address = socket.gethostbyname(socket.gethostname())

    # Get the external IP address of the machine using an online service
    # This is the IP address that is visible to the outside world
    ip_address_external = requests.get('https://ifconfig.co/ip').text.strip()

    return ip_address, ip_address_external


# for key, value in get_cpu_info().items():
#         print("{0}: {1}".format(key, value))

if __name__ == "__main__":
    os_info = get_os_info()
    os_info_text = f"OS: {os_info[0]} {os_info[1]} ({os_info[2]})"

    memory_info = get_memory_info()
    memory_info_text = f"Memory: Total={memory_info[0]:.2f}GB, Free={memory_info[1]:.2f}GB, Used={memory_info[2]:.2f}GB"

    cpu_info = get_cpu_information()
    cpu_info_text = f"CPU: {cpu_info[0]}, Cores={cpu_info[1]}, Load={cpu_info[2]}%"

    hdd_info = get_hdd_information()
    hdd_info_text = f"HDD: Total={hdd_info[0]:.2f}GB, Free={hdd_info[1]:.2f}GB, Used={hdd_info[2]:.2f}GB, Used%={hdd_info[3]}%"

    ip_info = get_ip_information()
    ip_info_text = f"IP: {ip_info[0]}, {ip_info[1]}"

    system_info = (os_info_text + "\n" + memory_info_text + "\n" + cpu_info_text + "\n" +
                   hdd_info_text + "\n" + ip_info_text)

    print(system_info)
