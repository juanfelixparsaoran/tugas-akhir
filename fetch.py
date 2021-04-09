

import requests
import json

url_data_nasional = "https://pemilu2019.kpu.go.id/static/json/hr/ppwp.json"
url_id_nasional = "https://pemilu2019.kpu.go.id/static/json/wilayah/0.json"

fetch_data_nasional = requests.get(url_data_nasional)
data_nasional = json.loads(fetch_data_nasional.content)

fetch_id_nasional = requests.get(url_id_nasional)
id_nasional = json.loads(fetch_id_nasional.content)

# with open('data_nasional.json', 'w') as f:
#     json.dump(data_nasional, f)
# with open('id_nasional.json', 'w') as f:
#     json.dump(id_nasional, f)

form_d_sum = {}
id_found_kel = []


for id in id_nasional:
    if id == "42385":
        print(id)
        form_d_sum[id] = {}
        url_data_provinsi = "https://pemilu2019.kpu.go.id/static/json/hr/ppwp/"+ id +".json"
        fetch_data_provinsi = requests.get(url_data_provinsi)
        data_provinsi = json.loads(fetch_data_provinsi.content)
        # with open("provinsi/"+id + '.json', 'w') as f:
        #     json.dump(data_provinsi, f)
        if data_provinsi['table'] is not None:
            url_id_provinsi = "https://pemilu2019.kpu.go.id/static/json/wilayah/"+id+".json"
            fetch_id_provinsi = requests.get(url_id_provinsi)
            id_provinsi_dict = json.loads(fetch_id_provinsi.content)


            for id_kot in id_provinsi_dict:
                form_d_sum[id][id_kot] = {}
                url_data_kota = "https://pemilu2019.kpu.go.id/static/json/hr/ppwp/"+ id +"/"+id_kot+".json"
                fetch_data_kota = requests.get(url_data_kota)
                data_kota = json.loads(fetch_data_kota.content)
                # with open("kota/"+id_kot + '.json', 'w') as f:
                #     json.dump(data_kota, f)
                if data_kota['table'] is not None:
                    url_id_kota = "https://pemilu2019.kpu.go.id/static/json/wilayah/"+id+"/"+id_kot+".json"
                    fetch_id_kota = requests.get(url_id_kota)
                    id_kot_dict = json.loads(fetch_id_kota.content)


                    for id_kec in id_kot_dict:
                        form_d_sum[id][id_kot][id_kec] = {}
                        url_data_kec = "https://pemilu2019.kpu.go.id/static/json/hr/ppwp/"+ id +"/"+id_kot+"/"+id_kec+".json"
                        fetch_data_kec = requests.get(url_data_kec)
                        data_kec = json.loads(fetch_data_kec.content)
                        # with open("kecamatan/"+id_kec + '.json', 'w') as f:
                        #     json.dump(data_kec, f)'

                        if data_kec['table'] is not None:
                        
                            url_id_kec = "https://pemilu2019.kpu.go.id/static/json/wilayah/"+id+"/"+id_kot+"/"+id_kec+".json"
                            fetch_id_kec = requests.get(url_id_kec)
                            id_kec_dict = json.loads(fetch_id_kec.content)


                            for id_kel in id_kec_dict:
                                form_d_sum[id][id_kot][id_kec][id_kel] = {}
                                url_data_kel = "https://pemilu2019.kpu.go.id/static/json/hr/ppwp/"+ id +"/"+id_kot+"/"+id_kec + "/" + id_kel + ".json"
                                fetch_data_kel = requests.get(url_data_kel)
                                data_kel = json.loads(fetch_data_kel.content)
                                
                                # with open("kelurahan/"+id_kel + '.json', 'w') as f:
                                #     json.dump(data_kel, f)
                                
                                # url_id_kel = "https://pemilu2019.kpu.go.id/static/json/wilayah/"+id+"/"+id_kot+"/"+id_kec+"/"+id_kel+".json"
                                # fetch_id_kel = requests.get(url_id_kel)
                                # id_kel_dict = json.loads(fetch_id_kel.content)

                                temp = 0
                                temp2 = 0
                                if data_kel['table'] is not None:
                                    for data_paslon in data_kel['table']:
                                        
                                        temp = temp + data_kel['table'][data_paslon]['21']
                                        temp2 = temp2 + data_kel['table'][data_paslon]['22']

                                    form_d_sum[id][id_kot][id_kec][id_kel]['paslon1'] = temp
                                    form_d_sum[id][id_kot][id_kec][id_kel]['paslon2'] = temp2

                                # print("Membandingkan "+id+"/"+id_kot+"/"+id_kec+"/"+id_kel)
                                if data_kec['table'][id_kel]['21'] != temp:
                                    path = id+"/"+id_kot+"/"+id_kec+"/"+id_kel
                                    print("found in id_kel = "+id_kel)
                                    if path not in id_found_kel:
                                        id_found_kel.append(path)
                                
                                if data_kec['table'][id_kel]['22'] != temp2:
                                    print("found in id_kel = "+id_kel)
                                    path = id+"/"+id_kot+"/"+id_kec+"/"+id_kel
                                    if path not in id_found_kel:
                                        id_found_kel.append(path)

                            temp = 0
                            temp2 = 0
                            for data_paslon in data_kec['table']:
                                
                                temp = temp + data_kec['table'][data_paslon]['21']
                                temp2 = temp2 + data_kec['table'][data_paslon]['22']

                            form_d_sum[id][id_kot][id_kec]['paslon1'] = temp
                            form_d_sum[id][id_kot][id_kec]['paslon2'] = temp2
                            # print("Membandingkan "+id+"/"+id_kot+"/"+id_kec)
                            if data_kota['table'][id_kec]['21'] != temp:
                                print("found in id_kec = "+id_kec)
                                path = id+"/"+id_kot+"/"+id_kec
                                if path not in id_found_kel:
                                    id_found_kel.append(path)
                            
                            if data_kota['table'][id_kec]['22'] != temp2:
                                print("found in id_kec = "+id_kec)
                                path = id+"/"+id_kot+"/"+id_kec
                                if path not in id_found_kel:
                                    id_found_kel.append(path)
                        
                    temp = 0
                    temp2 = 0
                    for data_paslon in data_kota['table']:
                        
                        temp = temp + data_kota['table'][data_paslon]['21']
                        temp2 = temp2 + data_kota['table'][data_paslon]['22']

                    form_d_sum[id][id_kot]['paslon1'] = temp
                    form_d_sum[id][id_kot]['paslon2'] = temp2
                    # print("Membandingkan "+id+"/"+id_kot)
                    if data_provinsi['table'][id_kot]['21'] != temp:
                        print("found in id_kot = "+id_kot)
                        path = id+"/"+id_kot
                        if path not in id_found_kel:
                            id_found_kel.append(path)
                    
                    if data_provinsi['table'][id_kot]['22'] != temp2:
                        print("found in id_kot = "+id_kot)
                        path = id+"/"+id_kot
                        if path not in id_found_kel:
                            id_found_kel.append(path)
            temp = 0
            temp2 = 0
            for data_paslon in data_provinsi['table']:
                
                temp = temp + data_provinsi['table'][data_paslon]['21']
                temp2 = temp2 + data_provinsi['table'][data_paslon]['22']

            form_d_sum[id]['paslon1'] = temp
            form_d_sum[id]['paslon2'] = temp2
            # print("Membandingkan "+id)
            if data_nasional['table'][id]['21'] != temp:
                print("found in id = "+id)
                path = id
                if path not in id_found_kel:
                    id_found_kel.append(path)
            
            if data_nasional['table'][id]['22'] != temp2:
                print("found in id = "+id)
                path = id
                if path not in id_found_kel:
                    id_found_kel.append(path)
        with open(id+".txt", "w") as txt_file:
            for line in id_found_kel:
                txt_file.write(line+ "\n") # works with any number of elements in a line