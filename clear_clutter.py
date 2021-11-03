import os

""" clear up the older data files
"""

clear_ext = ['csv','jpg','json']

data_path = 'data/'

file_list = os.listdir(data_path)

# delete all files with the extension in clear_ext
for file in file_list:
    os.remove(data_path + file) if file.split('.')[-1] in clear_ext else None