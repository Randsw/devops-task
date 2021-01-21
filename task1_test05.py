import os
import sys
import psutil
import pathlib
import datetime
import time


def disk_stat(disk_path='/'):
    obj_Disk = psutil.disk_usage(disk_path)

    print (f'Disk space total - {obj_Disk.total / (1024.0 ** 3):.2f} Gb')
    print (f'Disk space used - {obj_Disk.used / (1024.0 ** 3):.2f} Gb')
    print (f'Disk space free - {obj_Disk.free / (1024.0 ** 3):.2f} Gb')
    print (f'Disk usage percent - {obj_Disk.percent} %')
    
    return obj_Disk.free / (1024.0 ** 3)


def deleting_old_file(directory, desired_time, free_space, desired_space):
    """
    This method delete files in chosen directory
    directory - path to directory
    desired_time - time in unix second to keep files from current time
    free_space - Free disk space at current moment
    desired_space - Free disk space we want to stay in GB(float)
    """
    if free_space < desired_space:
        for dirpath, _, files in os.walk(directory):
            print(f'Found directory: {dirpath}')
            for file_name in files:
                fname = dirpath + '/' + file_name
                if os.path.isfile(fname):
                    if pathlib.Path(fname).stat().st_mtime < time.time() - desired_time:
                        print(fname)
                        os.remove(fname)


if __name__ == "__main__":
    old_file_time = 600 # 6 month in unix timestamp
    desired_space = 200 # Free space on disk we want to stay in Gb
    free_space = disk_stat()
    deleting_old_file('root', old_file_time, free_space, desired_space)




