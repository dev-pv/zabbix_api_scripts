from pyzabbix import ZabbixAPI
import xlrd
import time

wb = xlrd.open_workbook(r'C:\Users\vlpro\Documents\branches_ip_host_create.xlsx')
sheet1 = wb.sheet_by_index(0)
col_location = sheet1.col_values(0)
col_ip01 = sheet1.col_values(1)
col_ip02 = sheet1.col_values(2)

z = ZabbixAPI(url = "http://10.164.45.242/zabbix", user = "", password = "")

hosts = z.host.get(groupids='97')


def pop_type (arr):
    arr.pop(0)
    arr_total = []
    for i in arr:
        arr_total.append(i)
    return arr_total

col_location = pop_type(col_location)
col_ip01 = pop_type(col_ip01)
col_ip02 = pop_type(col_ip02)

total_hosts = []
for i in hosts:
    total_hosts.append(i['host'])

for i in col_location:
    if i not in total_hosts:
        print(i)

time.sleep(10)
for i in col_location:
    if i not in total_hosts:
        index_num = col_location.index(i)
        ip01_num = col_ip01[index_num]
        ip02_num = col_ip02[index_num]
        if ip02_num == '':
            z.host.create({
                "host": i,
                "interfaces": [
                    {
                        "type": 1,
                        "main": 1,
                        "useip": 1,
                        "ip": ip01_num,
                        "dns": "",
                        "port": "10050"
                    }],
                "groups": [
                    {
                        "groupid": "97"
                    }],
            })
        else:
            z.host.create({
                "host": i,
                "interfaces": [
                    {
                        "type": 1,
                        "main": 1,
                        "useip": 1,
                        "ip": ip01_num,
                        "dns": "",
                        "port": "10050"
                    },
                    {
                        "type": 1,
                        "main": 0,
                        "useip": 1,
                        "ip": ip02_num,
                        "dns": "",
                        "port": "10050"
                    }],
                "groups": [
                    {
                        "groupid": "97"
                    }],
            })
