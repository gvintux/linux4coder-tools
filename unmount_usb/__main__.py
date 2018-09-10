#!/usr/bin/env python3
import subprocess as sp
import sys
import os

LS_CMD = ['ls', '-1']
PUMOUNT_CMD = ['pumount']
os.chdir('/media')


def get_devices_list():
    global LS_CMD
    with sp.Popen(LS_CMD, universal_newlines=True, stdout=sp.PIPE) as p:
        out, err = p.communicate()
    if p.returncode != 0:
        print(err, file=sys.stderr)
        sys.exit(1)
    return list(filter(lambda x: 'sd' in x, out.split()))


mounted_devices = get_devices_list()
if len(mounted_devices) == 0:
    print('Вы не примонтировали ни одного USB носителя', file=sys.stderr)
    print('Воспользуйтесь утилитой mount_usb', file=sys.stderr)
    sys.exit(1)
print('Ваши примонтированные разделы:')
for p in mounted_devices:
    print('* ' + p, sep=' ', end=None)
unmount_candidates = input('Перечислите список разделов которые вы желаете отмонтировать\n').split()
unmount_candidates_count = len(unmount_candidates)
unmount_candidates = list(filter(lambda mc: mc in mounted_devices, unmount_candidates))
if unmount_candidates_count != len(unmount_candidates):
    print('Некорректно заданные разделы будут пропущены', file=sys.stderr)
for c in unmount_candidates:
    with sp.Popen(PUMOUNT_CMD + ['/dev/' + c], universal_newlines=True, stdout=sp.PIPE, stderr=sp.PIPE) as p:
        out, err = p.communicate()
    if p.returncode == 0:
        print(c + ' успешно отмонтирован')
    else:
        print(err, file=sys.stderr)
print('Теперь вы можете отключить отмонтированные устройства')
