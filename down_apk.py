# -*- coding: UTF-8 -*-
import sys
import os
import re
import xlrd
import requests
import xlwt

def get_apk_list():
	data = xlrd.open_workbook('Third_apk.xlsx')
	sheet1 = data.sheet_by_index(0)
	apk_list = sheet1.col_values(0)

	return apk_list

def get_apk_search(apk_list):
	user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
	headers = {"User-Agent": user_agent}
	down_url_list = []
	for apk in apk_list:
		apk_search_html = requests.get('http://shouji.baidu.com/s?wd=%s' %apk,headers=headers).text
		a = re.search(r'data_url=".*?"',apk_search_html).group(0)
		down_url = re.search(r'"(.*?)"',a).group(1)
		down_url_list.append(down_url)

	return down_url_list

def get_the_web_version(apk_list):
	user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
	headers = {"User-Agent": user_agent}
	web_version = []
	for apk in apk_list:
		apk_search_html = requests.get('http://shouji.baidu.com/s?wd=%s' %apk,headers = headers).text
		a = re.search(r'data_versionname=".*?"',apk_search_html).group(0)
		b = re.search(r'"(.*?)"',a).group(1)
		web_version.append(b)

	return web_version

def download_apk(down_url_list,apk_list):
	for downapk,down in zip(down_url_list,apk_list):
		file_name = down.split('/')[-1]
		print (file_name)
		r = requests.get(downapk, stream=True)
		total_size = int(r.headers['Content-Length'])
		temp_size = 0


		# download started
		with open('./apk/%s.apk' %file_name, 'wb') as f:
			for chunk in r.iter_content(chunk_size=1024):
				if chunk:
					temp_size += len(chunk)
					f.write(chunk)
					f.flush()
					done = int(50 * temp_size / total_size)
					sys.stdout.write("\r[%s%s] %d%%" % ('█' * done, ' ' * (50 - done), 100 * temp_size / total_size))
					#sys.stdout.flush()

		print("  downloaded!\n")


	print("All apk downloaded!")

	return

def write_the_info(apk_list,web_version):
	f = xlwt.Workbook()
	sheet1 = f.add_sheet(u'sheet1',cell_overwrite_ok = True)
	for i in range(len(apk_list)):
		sheet1.write(i,0,apk_list[i])
	for i in range(len(web_version)):
		sheet1.write(i,1,web_version[i])

	f.save('check_info.xls')

if __name__ == "__main__":
	apk_list = get_apk_list()
	down_url_list = get_apk_search(apk_list)
	web_version = get_the_web_version(apk_list)
	download_apk(down_url_list,apk_list)
	write_the_info(apk_list,web_version)







