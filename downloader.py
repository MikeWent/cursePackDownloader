from multiprocessing.pool import Pool
from urllib.parse import unquote
import os,shutil,json,requests

mod_count=0


def download(url):
	response=requests.get(url.replace("\n",""),allow_redirects=True)
	new_url=response.url
	filename=unquote(new_url.split("/")[-1])
	full_file_path=modpack_path+"/minecraft/mods"+"/"+filename
	with open(full_file_path,"wb") as save_file:
		save_file.write(response.content)
		print(filename+" downloaded")
	#work fine
		
#Reading unpacked modpack folder path
is_path_correct=False
while is_path_correct!=True:
	print("Enter full path of \nMinecraft modpack folder: ")
	modpack_path=str(input())
	if os.path.exists(modpack_path)==True:
		is_path_correct=True
	else:
		print("Incorrect path\n")
		
#Creating dirs if not exists
if not os.path.exists(modpack_path+"/minecraft"):
	os.makedirs(modpack_path+"/minecraft")		
	
#Moving overrides
folders=os.listdir(modpack_path+"/overrides")
for folder in folders:
	shutil.move(modpack_path+"/overrides"+"/"+folder,modpack_path+"/minecraft")

#Reading manifest.json
manifest_path=modpack_path+"/manifest.json"
with open(manifest_path,"r") as json_file:
	manifest=json.load(json_file)
	
#Creating urlcache file for worker-processses
with open(modpack_path+"/urlcache","w") as urlcache:
	for dependency in manifest["files"]:
		url=(("http://minecraft.curseforge.com/projects/%s/files/%s/download" % (dependency["projectID"],dependency["fileID"])))
		urlcache.write(url+"\n")
		mod_count+=1

#Downloading mods
with open(modpack_path+"/urlcache","r") as urllist:
		urllist_iter=urllist.readlines()
		with Pool(processes=4) as pool:
			pool.map(download,urllist_iter)	
			
print("\n\nDone.")
