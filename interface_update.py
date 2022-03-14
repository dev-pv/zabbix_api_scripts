from pyzabbix import ZabbixAPI
import xlrd
import time

wb = xlrd.open_workbook(r'C:\Users\vlpro\Documents\zabbix_hosts.xlsx')

z = ZabbixAPI(url = "http://10.164.45.242/zabbix", user = "", password = "")
answer = z.do_request('apiinfo.version')

hosts = z.host.get(groupids='97', sortfield='hostid')
for i in hosts:
    print(i['hostid'], i['name'])

ids = list(range(12600, 12648))
hostif = z.hostinterface.get(hostids=ids, sortfield='interfaceid')
for i in hostif:
    print(i['interfaceid'], i['hostid'], i['ip'])


def pop_type (arr):
    arr.pop(0)
    arr_total = []
    for i in arr:
        i = int(i)
        i = str(i)
        arr_total.append(i)
    return arr_total

sheet1 = wb.sheet_by_index(0)
col_hostid = sheet1.col_values(0)
col_ifid = sheet1.col_values(1)

col_ip = sheet1.col_values(3)
col_ip.pop(0)

col_hostid = pop_type(col_hostid)
col_ifid = pop_type(col_ifid)
print(col_hostid)
print(col_ifid)
print(col_ip)

time.sleep(5)
for i,k,l in zip(col_hostid, col_ifid, col_ip):
    z.hostinterface.update({
        "hostid": i,
        "interfaceid": k,
        "ip": l
    })
