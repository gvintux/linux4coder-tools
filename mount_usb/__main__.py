#!/usr/bin/env python3
import subprocess as sp
import sys
import os
import time
import string

LS_CMD = ['ls', '-1']
PMOUNT_CMD = ['pmount']
USB_DETECTION_DELAY = 3
os.chdir('/dev')


def get_devices_list():
    global LS_CMD
    with sp.Popen(LS_CMD, universal_newlines=True, stdout=sp.PIPE) as p:
        out, err = p.communicate()
    if p.returncode != 0:
        print(err, file=sys.stderr)
        sys.exit(1)
    return list(filter(lambda x: 'sd' in x, out.split()))


def delay(secs: int):
    for i in range(1, secs + 1):
        print('.', end='', flush=True)
        time.sleep(1)
    print()


dev_list_before = get_devices_list()
input("Подключите ваш USB носитель и нажмите <Enter>")
delay(USB_DETECTION_DELAY)
dev_list_after = get_devices_list()
connected_devices = []
for dev in dev_list_after:
    if dev not in dev_list_before:
        connected_devices.append(dev)
if len(connected_devices) == 0:
    print('Вы не подключили ни одного USB носителя', file=sys.stderr)
    print('Проверьте работоспособность носителя или увеличьте задержку USB_DETECTION_DELAY', file=sys.stderr)
    sys.exit(1)
connected_disks = []
connected_partitions = []
for dev in connected_devices:
    last_char = dev[-1:]
    if last_char in string.digits and dev not in connected_partitions:
        connected_partitions.append(dev)
    if last_char not in string.digits and dev not in connected_disks:
        connected_disks.append(dev)
disk_table = {}
for d in connected_disks:
    disk_table[d] = []
for d in connected_disks:
    for p in connected_partitions:
        if d in p and p not in disk_table[d]:
            disk_table[d].append(p)
for disk in disk_table.keys():
    disk_table[disk].sort()
print('Подключённые вами диски и их разделы:')
for disk, partitions in disk_table.items():
    print('* ' + disk)
    for p in partitions:
        print('  |')
        print('  |--' + p)
mount_candidates = input('Перечислите список разделов которые вы желаете примонтировать\n').split()
mount_candidates_count = len(mount_candidates)
mount_candidates = list(filter(lambda mc: mc in connected_devices, mount_candidates))
mount_candidates_filtered_count = len(mount_candidates)

if mount_candidates_count != mount_candidates_filtered_count:
    print('Некорректно заданные разделы будут пропущены', file=sys.stderr)
if mount_candidates_filtered_count == 0:
    sys.exit(0)
for c in mount_candidates:
    with sp.Popen(PMOUNT_CMD + ['/dev/' + c], universal_newlines=True, stdout=sp.PIPE, stderr=sp.PIPE) as p:
        out, err = p.communicate()
    if p.returncode == 0:
        print(c + ' успешно примонтирован в /media')
    else:
        print(err, file=sys.stderr)
print('Перед отключением накопителей отмонтируйте их с помощью unmount_usb')
