from pyzabbix import ZabbixAPI
import xlrd
import time

wb = xlrd.open_workbook(r'C:\Users\vlpro\Documents\branches_ip.xlsx')
sheet1 = wb.sheet_by_index(0)
col_location = sheet1.col_values(0)
col_ip01 = sheet1.col_values(1)
col_ip02 = sheet1.col_values(2)


def pop_type(arr):
    arr.pop(0)
    arr_total = []
    for i in arr:
        arr_total.append(i)
    return arr_total


col_location = pop_type(col_location)
col_ip01 = pop_type(col_ip01)
col_ip02 = pop_type(col_ip02)

z = ZabbixAPI(url="http://10.164.45.242/zabbix", user="", password="")

hosts = z.host.get(groupids='97', sortfield='hostid')
host_total = {}
host_count = []
for i in hosts:
    host_count.append(i['hostid'])
    host_total.update({i['hostid']: i['host']})

sort = list(range(int(host_count[0]), int(host_count[-1]) + 1))
hostif = z.hostinterface.get(hostids=sort)

if_total = []
for i in hostif:
    if_total.append([i['interfaceid'], i['hostid'], i['ip']])

if_update = []
for i in range(len(if_total)):
    if_update.append(if_total[i] + [host_total.get(if_total[i][1])])
for i in if_update:
    print(i)

new = zip(col_location, col_ip01)
new = dict(new)
new2 = zip(col_location, col_ip02)
new2 = dict(new2)

total_interface_table = []
for i in range(len(if_update)):
    total_interface_table.append(if_update[i] + [new.get(if_update[i][3])])

for i in total_interface_table:
    print(i)

















