import xlsxwriter
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

workbook = xlsxwriter.Workbook('Rekap Form D.xlsx')
worksheet_perbandingan = workbook.add_worksheet("Perbandingan")
worksheet_null = workbook.add_worksheet("Wilayah Null")
worksheet_nol = workbook.add_worksheet("Wilayah 0 Suara")

row_perbandingan = 0
col_perbandingan = 0

row_null = 0
col_null = 0

row_nol = 0
col_nol = 0

worksheet_perbandingan.write(row_perbandingan,col_perbandingan, "ID Wilayah")
worksheet_perbandingan.write(row_perbandingan,col_perbandingan + 1, "Kategori Wilayah")
worksheet_perbandingan.write(row_perbandingan,col_perbandingan + 2, "Suara Paslon 1 pada parent")
worksheet_perbandingan.write(row_perbandingan,col_perbandingan + 3, "Suara Paslon 2 pada parent")
worksheet_perbandingan.write(row_perbandingan,col_perbandingan + 4, "Suara Paslon 1")
worksheet_perbandingan.write(row_perbandingan,col_perbandingan + 5, "Suara Paslon 2")
worksheet_perbandingan.write(row_perbandingan,col_perbandingan + 6, "Gap Paslon 1")
worksheet_perbandingan.write(row_perbandingan,col_perbandingan + 7, "Gap Paslon 2")
worksheet_perbandingan.write(row_perbandingan,col_perbandingan + 8, "Path Parent")

worksheet_nol.write(row_nol, col_nol,"ID Wilayah")
worksheet_nol.write(row_nol, col_nol + 1,"Kategori Wilayah")
worksheet_nol.write(row_nol, col_nol + 2,"ID Child")
worksheet_nol.write(row_nol, col_nol + 3,"Path Parent")


worksheet_null.write(row_null,col_null, "ID Wilayah")
worksheet_null.write(row_null,col_null + 1, "Kategori Wilayah")   
worksheet_null.write(row_null,col_null + 2, "Path Parent")          

row_perbandingan = 1
row_nol = 1
row_null = 1

for file in glob.glob("*.txt"):
    # if file == "42385.txt":
        # print(len(glob.glob("*.txt")))
        with open(file, 'r') as f:
            text = f.read()
            
            for path in text.split():

                url_data_gap1 = "https://pemilu2019.kpu.go.id/static/json/hr/ppwp/"+ path+".json"
                fetch_data_gap1 = requests.get(url_data_gap1)
                data_gap1 = json.loads(fetch_data_gap1.content)

                path_split = path.rsplit("/",1)
                url_data_gap2 = "https://pemilu2019.kpu.go.id/static/json/hr/ppwp/"+ path_split[0]+".json"
                fetch_data_gap2 = requests.get(url_data_gap2)
                data_gap2 = json.loads(fetch_data_gap2.content)

                # assign kategori
                if (path.count("/") == 0):
                    kategori = "provinsi"
                elif (path.count("/") == 1):
                    kategori = "kabko"
                elif (path.count("/") == 2):
                    kategori = "kec"
                elif (path.count("/") == 3):
                    kategori = "kel"

                #perbandingan
                if data_gap1['chart'] != None:
                    temp = 0
                    temp2 = 0
                    for data_paslon in data_gap1['table']:
                            
                        temp = temp + data_gap1['table'][data_paslon]['21']
                        temp2 = temp2 + data_gap1['table'][data_paslon]['22']

                        if (data_gap1['table'][data_paslon]['21'] == 0):
                            worksheet_nol.write(row_nol, col_nol,path_split[1])
                            worksheet_nol.write(row_nol, col_nol + 1,kategori)
                            worksheet_nol.write(row_nol, col_nol + 2,data_paslon)
                            worksheet_nol.write(row_nol, col_nol + 3,path_split[0])

                            row_nol += 1
                    if (temp != 0 and data_gap2['table'][path_split[1]]['21'] !=0) or (temp2 !=0 and data_gap2['table'][path_split[1]]['22'] !=0):
                        worksheet_perbandingan.write(row_perbandingan,col_perbandingan, path_split[1])
                        worksheet_perbandingan.write(row_perbandingan,col_perbandingan + 1, kategori)
                        worksheet_perbandingan.write(row_perbandingan,col_perbandingan + 8, path_split[0])
                        if temp != 0 and data_gap2['table'][path_split[1]]['21'] !=0:
                            gap1 = data_gap2['table'][path_split[1]]['21'] - temp                            
            
                            worksheet_perbandingan.write(row_perbandingan,col_perbandingan + 2, data_gap2['table'][path_split[1]]['21'])
                            
                            worksheet_perbandingan.write(row_perbandingan,col_perbandingan + 4, temp)
                            
                            worksheet_perbandingan.write(row_perbandingan,col_perbandingan + 6, gap1)

                        if temp2 != 0 and data_gap2['table'][path_split[1]]['22'] !=0:
                            gap2 = data_gap2['table'][path_split[1]]['22'] - temp2

                            worksheet_perbandingan.write(row_perbandingan,col_perbandingan + 3, data_gap2['table'][path_split[1]]['22'])
                            worksheet_perbandingan.write(row_perbandingan,col_perbandingan + 5, temp2)
                            worksheet_perbandingan.write(row_perbandingan,col_perbandingan + 7, gap2)
                        row_perbandingan += 1
                else:

                    worksheet_null.write(row_null,col_null, path_split[1])
                    worksheet_null.write(row_null,col_null + 1, kategori)
                    worksheet_null.write(row_null,col_null + 2, path_split[0])    
                    row_null += 1

workbook.close()