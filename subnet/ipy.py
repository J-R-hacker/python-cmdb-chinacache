#!/usr/bin/env python
#-*-   encoding: utf-8 -*-
#this class change ip to network id etc.
#点分十进制变为二进制返回的是str
def ip_bin(decimal):
    binary = ''
    for d in decimal.split('.'):
        b = bin(int(d))[2:]
        if len(b) != 8:
            for i in range (0,8-len(b)):
                b = '0' + b
        binary += b
    return binary
#二进制变为点分十进制返回str
def ip_int(binary):
    decimal = []
    for i in range (0,32,8):
        b = binary[i:i+8]
        decimal.append(str(int(b,2)))
    return '.'.join(decimal)
#根据二进制给出子网掩码长度返回str
def mask_len(binary):
    s = 0
    for i in binary:
        if i == '1':s += 1
    return str(s)
#给出需要的主机数得到对应的子网掩码返回str
def get_mask(hosts):
    binary = ['1' for i in range (0,32)]
    for i in range (1,32):
        if (2**i - 2) < hosts:
            binary[32-i] = '0'
        else:break
    binary[32-i] = '0'
    return ''.join(binary)
#计算出下一个子网的子网号
def next_id(ip, mask):
    lenth = int(mask_len(mask))
    b = bin(int(ip[:lenth], 2) + 1)[2:] + ip[lenth:]
    if len(b) != 32:
        for i in range (0,32 - len(b)):
            b = '0' + b
    id = ip_int(b)
    return id
'''
ip = '10.0.2.0'
hosts = 300
mask = get_mask(hosts)
print ip + "/" + mask_len(mask)
ip = ip_bin(ip)
id = next_id(ip, mask)
print id
'''