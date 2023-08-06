import glob
import os
from pathlib import Path
from re import Pattern
from typing import List, Set, Union

def find(directory, excludes = []):
    file_list=[]
    for root, directories, files in os.walk(directory):
        directories[:] = [d for d in directories if d not in ['thumbs']]
        for filename in files:
            filepath = os.path.join(root, filename)
            file_list.append(filepath)
    return file_list


def out_needs_rewrite_file(infile:Path, outfile:Path):
    return (not outfile.exists()) or (infile.stat().st_mtime > outfile.stat().st_mtime)

def out_needs_rewrite(src:str, out:str, out_in_src=False):
    if out_in_src:
        srcs = find(src,[out,])
    else:
        srcs = find(src)    
    dsts = find(out)

    src_m_time = max(map(os.path.getmtime,srcs))
    dst_m_time = max(map(os.path.getmtime,dsts))
    return src_m_time > dst_m_time


# def dir_mod_time(path: str, exclude:List[Pattern]=[]):
#     all_files = glob.glob(f"{path}/**",recursive=True) 
#     def excluded(path):
#         for ban in exclude:
#             if ban.match(path):
#                 return True
#         return False
#     files = map(excluded,all_files)
#     latest_file = max(files, key=os.path.getctime)
#     latest_file_time = os.path.getmtime(latest_file)

#     return latest_file_time




if __name__ == "__main__":
    print(out_needs_rewrite("razaltlib","dist",True))
    