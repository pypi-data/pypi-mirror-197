import glob
import os
from pathlib import Path
from typing import Union

def file_is_newer(infile:Path, outfile:Path):
    return (not outfile.exists()) or (infile.stat().st_mtime > outfile.stat().st_mtime)

def dir_is_newer(indir:Path,outdir:Path):
    return (not indir.exists()) or (get_dir_latest_content_modification_time(indir)>get_dir_latest_content_modification_time(outdir))

def get_dir_latest_content_modification_time(path: str):
    list_of_files = glob.glob(f"{path}/**",recursive=True) # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    latest_file_time = os.path.getmtime(latest_file)
    # for file in list_of_files:
    #     # path:Path = Path(file)
    #     print(file, os.path.getmtime(file))
    # print("--------",latest_file,latest_file_time)
    return latest_file_time




if __name__ == "__main__":
    print(dir_is_newer(Path("./razaltlib"),Path("./dist")))
    