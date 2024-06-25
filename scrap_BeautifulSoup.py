import re
from requests_html import HTMLSession
from bs4 import BeautifulSoup

session = HTMLSession()

def string_modification(string):
    # print(string,'\n') # data mentah
    words = ['<script>',')</script>','self.__next_f.push(','https']
    for word in words:
        string=string.replace(word,'')

    # mencari data inflasi tahun 2024 di bulan januari dan februari
    numeric = re.findall(r'[0-9.]{1,11}+', string)
    key_index = [num for num in range(len(numeric)) if len(numeric[num]) == 11 or len(numeric[num]) == 10]
    number_of_inflation = [numeric[i+1] for i in key_index] 

    Januari = []
    Februari = []
    for num_inf in range(len(number_of_inflation)):
        if (num_inf % 2 == 0):
            Januari.append(number_of_inflation[num_inf])
        else:
            Februari.append(number_of_inflation[num_inf])

    # mencari nama provinsi
    alfa = re.findall(r'[A-Z]+', string) # hanya alfabet
    # print(alfa)                    
    # melakukan konversi dari sebuah array ke format provinsi sesuai dengan ketentuan
    index_ = [i for i in range(len(alfa)) if len(alfa[i]) > 3]
    # print(index_)
    province_name = alfa[min(index_):max(index_)+1] # daftar provinsi
    index_of_prov = [i for i in range (len(province_name)) if province_name[i] == 'PROV'] # index provinsi
    index_of_name = [i for i in range (len(province_name)) if province_name[i] != 'PROV']

    # print(province_name,index_of_prov,index_of_name)
    list_of_province = []
    pointer = 1
    for i in index_of_prov:
        if i == 0:
            list_of_province.append(province_name[:2])
        elif i > 0 :
            if pointer < len(index_of_prov):
                list_of_province.append(province_name[i:index_of_prov[pointer]])
            elif pointer == len(index_of_prov):
                pointer = index_of_name[len(index_of_name)-1]
                list_of_province.append(province_name[i:pointer])
        pointer = pointer + 1
    list_of_province.append(province_name[len(province_name)-1])
    # # menggabungkan list provinsi
    province=[]   # hasil nama provinsi
    for row in range(len(list_of_province)):
        var = ''
        if type(list_of_province[row]) is list:
            for column in range(len(list_of_province[row])):
                if column == 0:
                    var = var+list_of_province[row][column]
                else:
                    var = var +' '+list_of_province[row][column]
            province.append(var)
        else:
            province.append(list_of_province[row])
    # # #show value
    for col1,col2,col3 in zip(province,Januari,Februari):
        print(col1,"    ",col2,"    ",col3)
def doscrap(url):

    page = session.get(url)
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')
        content = soup.find_all("script") 
        # print(content)
        to_string = str(content[-2])
        # print(to_string)
        string_modification(to_string)

    else:
        print(f'Failed to retrieve the webpage. Status code: {page.status_code}')

if __name__ == "__main__":
    bps_url = "https://www.bps.go.id/id/statistics-table/2/MjI2MyMy/inflasi-tahunan--y-on-y--38-provinsi--2022-100-.html" # data bps
    url = "https://www.marinetraffic.com/en/data/?asset_type=vessels&columns=flag%2Cshipname%2Cphoto%2Crecognized_next_port%2Creported_eta%2Creported_destination%2Ccurrent_port%2Cimo%2Cship_type%2Cshow_on_live_map%2Ctime_of_latest_position%2Clat_of_latest_position%2Clon_of_latest_position%2Cnotes"  # data marine traffic
    # url_gallery_photos = "https://www.marinetraffic.com/en/photos?order=date_uploaded"
    doscrap(bps_url)
