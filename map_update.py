from pyzabbix import ZabbixAPI
import xlrd
import itertools
import time

wb = xlrd.open_workbook(r'C:\Users\vlpro\Documents\zabbix_hosts.xlsx')

z = ZabbixAPI(url = "http://10.164.45.242/zabbix", user = "", password = "")

#Получаем список хостов и создаем лист с общим количеством хостов вида [[id], [hostname]], а также создаем словарь с аналогичными данными только в варианте ключ:значение
#(словарь в данном скрипте не используем)
hosts = z.host.get(groupids='97', sortfield='hostid')
host_count = []
host_total = {}
for i in hosts:
    host_count = host_count + [[i['hostid']] + [i['host']]]
    host_total.update({i['hostid']: i['host']})

#Создаем списки с данными по координатами и шагу для размещения в соответствии с ними элементы на карте zabbix, создаем так что бы по горизонтале X вмещалось 18 элементов,
#ну и столько же по вертикале Y, тоже 18 что бы в будущем цикле было по 18 итераций
coordinates_x = list(range(20, 1820, 100))
coordinates_y = list(range(20, 2520, 140))

#Создаем функцию list_split, которая на вход будет получать лист arr и делить этот лист слайсом на списки-отрезки по n элементов
#(в соответствии с координатами выше нам нужны списки по 18 элементов)
#Используется yeild и создается генератор, который при функции next(arr) будет вызывать функцию list_split и отдавать по n элементов до тех пор пока элементы в списке arr не закончатся
def list_split(arr, n):
    for i in range(0, len(arr), n):
        yield arr[i:i + n]

#Сначала нам надо понять какое количество списков с n элементами мы получили из списка arr в предыдущей функции, поэтому просто прогоняем функцию list_arr и возвращаем
#значение P количества списков по n элементов что бы правильно настроить цикл в следующем шаге.
arr = list_split(host_count, 18)
p = 0
for i, k in enumerate(arr):
    p = i
p = p + 1

#Теперь уже вызываем функцию что бы извлечь из нее непосредственно данные из списка host_count, разделенные на списки по 18 элементов
arr_2 = list_split(host_count, 18)

#Теперь мы имеем в строгом соответсвии по 18 элементов в списках координат X и Y, а также генератор, который настроен что бы отдавать нам по 18
#элементов из списка host_count. Теперь настраиваем цикл, который будет вызываться P раз и внутренний цикл, который будет создавать лист a,
#с данными о координатах X, Y, именем хоста из host_count и номером id хоста. Здесь используется вариат с вызовом функции а не просто цикла, хотя
#необходимости в этом в данном случае нет.
a = []
def xy_attach(x_range, y_range):
    for i in range(p):
        y = y_range[i]
        y_range_new = [y] * len(y_range)
        for i, x, y, l in zip(itertools.count(start=0, step=1), x_range, y_range_new, next(arr_2)):
            a.append({'sysmapid': '7',
                       'elementtype': '0',
                       'iconid_off': '192',
                       'iconid_on': '193',
                       'label': l[1],
                       'label_location': '-1',
                       'x': x,
                       'y': y,
                       'elements': [{'hostid': l[0]}],
                       'urls': [],
                       'permission': 2})

v = xy_attach(coordinates_x, coordinates_y)

#теперь просто запускаем функцию api map.update, которая будет аплейтить пустую карту с ID 7 в zabbix для хостов из списка host_count и в соответствии с координатами X и Y
time.sleep(10)
z.map.update({'sysmapid': '7', 'selements': a})

#С этой функции мы можем получить список созданных карт и их ID, для обновления map.update.
#maps = z.map.get(selectSelements='extend', sysmapids='7')
