import argparse
import json
import os
import shutil
from multiprocessing.pool import Pool
from urllib.parse import unquote_plus
from urllib.request import urlopen

mods_count=int()

# getting args
parser=argparse.ArgumentParser()
parser.add_argument("-f", "--file", default="Nothing", help="Path to modpack folder\nwith (maybe..) overrides and manifest.json")
parser.add_argument("-p", "--process_count", type=int, default=5, help="Count of workers (processes) for multiprocessing downloading")
args=parser.parse_args()

if not os.path.exists(args.file):
	print("Wrong path")
	exit(1)

modpack_path = args.file

# parsing manifest.json	
manifest_path = modpack_path+"/manifest.json"
if not os.path.exists(manifest_path):
	print("Modpack folder doesn't contain manifest.json file")
	exit(1)

with open(manifest_path, "r") as manifest_obj:
	manifest = json.load(manifest_obj)

# creating temporary variable for urls
url_tmp = []
for dependency in manifest["files"]:
	mods_count += 1
	url_tmp += ["http://minecraft.curseforge.com/projects/{}/files/{}/download".format(dependency["projectID"], dependency["fileID"])]

# move overrides if exists 
if not os.path.exists(modpack_path+"/minecraft"):
	os.makedirs(modpack_path+"/minecraft")

if os.path.exists(modpack_path+"/overrides"):
	files=os.listdir(modpack_path+"/overrides")
	for f in files:
		shutil.move(modpack_path+"/overrides/"+f, modpack_path+"/minecraft")	

def download(url):
	response=urlopen(url)
	filename=unquote_plus(response.geturl()).split("/")[-1]
	with open(modpack_path+"/minecraft/mods/"+filename, "wb") as out_file:
		shutil.copyfileobj(response, out_file)
	print(filename)

with Pool(processes=args.process_count) as pool:
	pool.map(download, url_tmp)

print("\nDone")
