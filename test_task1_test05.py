import os
import time
import task1_test05

dir_struct = {
    'root':{
        'dir1': {
            'dir11':{
                'file111.txt':'file', 
                'file112.txt':'file'
                },
            'file11.txt':'file', 
            'file12.txt':'file'
        },
        'file1.txt': 'file', 
        'file2.txt': 'file',
        'dir2': {
            'file21.txt':'file', 
            'file22.txt':'file'
            }, 
    }
} 


def create_file_struct(dict_in, parent = '', delayed_filename = 'file2.txt', time_diff = 120):
    for key in dict_in:
        if isinstance(dict_in[key], dict):
            dir_path = parent.replace("]", "/").replace("[", "") + key
            #print(dir_path)
            if not os.path.isdir(dir_path):
                os.mkdir(dir_path)
            create_file_struct(dict_in[key], parent + '[{}]'.format(key)) 
        else:
            filepath = os.path.join(parent.replace("]", "/").replace("[", ""), key)
            #print(filepath)
            if  not os.path.isfile(filepath):
                if key == delayed_filename:
                    time.sleep(time_diff)
            os.mknod(filepath)

def test_deleting_old_file():
    create_file_struct(dir_struct)
    task1_test05.deleting_old_file(list(dir_struct)[0], 100, 800, 900)    
    file_num = sum(len(files) for _, _, files in os.walk(list(dir_struct)[0]))
    assert file_num == 3

