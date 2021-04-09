import glob, os
import requests
import json
os.chdir("gap")

sum_global_gap = 0
da1_db1 = 0
daa1_da1 = 0
db1_dc1 = 0
dc1_dd1 = 0

sum_suara_gap1 = 0
sum_suara_gap2 = 0
gap_null = 0
max_gap1 = -1
max_gap2 = -1
absurd = []

for file in glob.glob("*.txt"):
    # if file == "6728.txt":
        # print(len(glob.glob("*.txt")))
        with open(file, 'r') as f:
            text = f.read()
            
            for path in text.split():
                
                sum_global_gap = sum_global_gap + 1
                if (path.count("/") == 0):
                    dc1_dd1 = dc1_dd1 + 1
                elif (path.count("/") == 1):
                    db1_dc1 = db1_dc1 + 1
                elif (path.count("/") == 2):
                    da1_db1 = da1_db1 + 1
                elif (path.count("/") == 3):
                    daa1_da1 = daa1_da1 + 1
                
                url_data_gap1 = "https://pemilu2019.kpu.go.id/static/json/hr/ppwp/"+ path+".json"
                fetch_data_gap1 = requests.get(url_data_gap1)
                data_gap1 = json.loads(fetch_data_gap1.content)

                path_split = path.rsplit("/",1)
                url_data_gap2 = "https://pemilu2019.kpu.go.id/static/json/hr/ppwp/"+ path_split[0]+".json"
                fetch_data_gap2 = requests.get(url_data_gap2)
                data_gap2 = json.loads(fetch_data_gap2.content)

                if data_gap1['chart'] != None:
                    temp = 0
                    temp2 = 0
                    for data_paslon in data_gap1['table']:
                            
                        temp = temp + data_gap1['table'][data_paslon]['21']
                        temp2 = temp2 + data_gap1['table'][data_paslon]['22']
                    
                    gap1 = abs(temp - data_gap2['table'][path_split[1]]['21'])
                    # if gap1 < 1000:
                    sum_suara_gap1 = sum_suara_gap1 + gap1
                    if gap1 > max_gap1:
                        max_gap1 = gap1
                        max_path1 = path
                # else:
                    # if path not in absurd:
                    #     absurd.append(path)

                    gap2 = abs(temp2 - data_gap2['table'][path_split[1]]['22'])
                    
                    # if gap2 < 1000:
                    sum_suara_gap2 = sum_suara_gap2 + gap2
                    if gap2 > max_gap2:
                        max_gap2 = gap2
                        max_path2 = path
                # else:
                    # if path not in absurd:
                    #     absurd.append(path)
                # else:
                #     sum_suara_gap1 = sum_suara_gap1 + data_gap2['table'][path_split[1]]['21']
                #     sum_suara_gap2 = sum_suara_gap2 + data_gap2['table'][path_split[1]]['22']
                else:
                    gap_null = gap_null+1

                print(path_split)
                # print(sum_suara_gap1)
                # print(sum_suara_gap2)
            

print("Total gap suara paslon 1 : "+str(sum_suara_gap1))
print("Total gap suara paslon 2 : "+str(sum_suara_gap2))
print("Total data wilayah yang null : "+str(gap_null))
print("Gap maksimal paslon 1: "+str(max_gap1))
print("Gap maksimal paslon 2: "+str(max_gap2))
print("Path wilayah gap maksimal paslon 1 :"+str(max_path1))
print("Path wilayah gap maksimal paslon 2 :"+str(max_path2))
# print(absurd)
            
# print(sum_global_gap)
# print(dc1_dd1)
# print(db1_dc1)
# print(da1_db1)
# print(daa1_da1)