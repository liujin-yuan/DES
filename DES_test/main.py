import re
import time

IP_table = [58, 50, 42, 34, 26, 18, 10, 2,
            60, 52, 44, 36, 28, 20, 12, 4,
            62, 54, 46, 38, 30, 22, 14, 6,
            64, 56, 48, 40, 32, 24, 16, 8,
            57, 49, 41, 33, 25, 17, 9, 1,
            59, 51, 43, 35, 27, 19, 11, 3,
            61, 53, 45, 37, 29, 21, 13, 5,
            63, 55, 47, 39, 31, 23, 15, 7]
IP_re_table = [40,8, 48, 16, 56, 24, 64, 32, 39,
             7, 47, 15, 55, 23, 63, 31, 38, 6,
             46, 14, 54, 22, 62, 30, 37,5, 45,
             13, 53, 21, 61, 29, 36, 4, 44, 12,
             52, 20, 60, 28, 35, 3, 43, 11, 51,
             19, 59, 27, 34, 2, 42, 10, 50, 18,
             58, 26, 33, 1, 41,9, 49, 17, 57, 25]
E  = [32, 1,  2,  3,  4,  5,  4,  5,
       6, 7,  8,  9,  8,  9, 10, 11,
      12,13, 12, 13, 14, 15, 16, 17,
      16,17, 18, 19, 20, 21, 20, 21,
      22, 23, 24, 25,24, 25, 26, 27,
      28, 29,28, 29, 30, 31, 32,  1]
P = [16,  7, 20, 21, 29, 12, 28, 17,
     1, 15, 23, 26,  5, 18, 31, 10,
     2,  8, 24, 14, 32, 27,  3,  9,
     19, 13, 30, 6, 22, 11,  4,  25]
S =  [
 [14, 4, 13,  1,  2, 15, 11,  8,  3, 10,  6, 12,  5,  9,  0,  7,
     0, 15,  7,  4, 14,  2, 13,  1, 10,  6, 12, 11,  9,  5,  3,  8,
     4,  1, 14,  8, 13,  6,  2, 11, 15, 12,  9,  7,  3, 10,  5,  0,
     15, 12,  8,  2,  4,  9,  1,  7,  5, 11,  3, 14, 10,  0,  6, 13 ],
[15,  1,  8, 14,  6, 11,  3,  4,  9,  7,  2, 13, 12,  0,  5, 10,
     3, 13,  4,  7, 15,  2,  8, 14, 12,  0,  1, 10,  6,  9, 11,  5,
     0, 14,  7, 11, 10,  4, 13,  1,  5,  8, 12,  6,  9,  3,  2, 15,
     13,  8, 10,  1,  3, 15,  4,  2, 11,  6,  7, 12,  0,  5, 14,  9],
[10,  0,  9, 14,  6,  3, 15,  5,  1, 13, 12,  7, 11,  4,  2,  8,
     13,  7,  0,  9,  3,  4,  6, 10,  2,  8,  5, 14, 12, 11, 15,  1,
     13,  6,  4,  9,  8, 15,  3,  0, 11,  1,  2, 12,  5, 10, 14,  7,
     1, 10, 13,  0,  6,  9,  8,  7,  4, 15, 14,  3, 11,  5,  2, 12 ],
[7, 13, 14,  3,  0,  6,  9, 10,  1,  2,  8,  5, 11,  12,  4, 15,
     13,  8, 11,  5,  6, 15,  0,  3,  4,  7,  2, 12,  1, 10, 14,9,
     10,  6,  9,  0, 12, 11,  7, 13, 15,  1,  3, 14,  5,  2,  8,  4,
     3, 15,  0,  6, 10,  1, 13,  8,  9,  4,  5, 11, 12,  7,  2, 14],
 [2, 12,  4,  1,  7, 10, 11,  6,  8,  5,  3, 15, 13,  0, 14,  9,
     14, 11,  2, 12,  4,  7, 13,  1,  5,  0, 15, 10,  3,  9,  8,  6,
     4,  2,  1, 11, 10, 13,  7,  8, 15,  9, 12,  5,  6,  3,  0, 14,
     11,  8, 12,  7,  1, 14,  2, 13,  6, 15,  0,  9, 10,  4,  5,  3],
[12,  1, 10, 15,  9,  2,  6,  8,  0, 13,  3,  4, 14,  7,  5, 11,
     10, 15,  4,  2,  7, 12,  9,  5,  6,  1, 13, 14,  0, 11,  3,  8,
     9, 14, 15,  5,  2,  8, 12,  3,  7,  0,  4, 10,  1, 13, 11,  6,
     4,  3,  2, 12,  9,  5, 15, 10, 11, 14,  1,  7,  6,  0,  8, 13],
[4, 11,  2, 14, 15,  0,  8, 13,  3, 12,  9,  7,  5, 10,  6,  1,
     13,  0, 11,  7,  4,  9,  1, 10, 14,  3,  5, 12,  2, 15,  8,  6,
     1,  4, 11, 13, 12,  3,  7, 14, 10, 15,  6,  8,  0,  5,  9,  2,
     6, 11, 13,  8,  1,  4, 10,  7,  9,  5,  0, 15, 14,  2,  3, 12],
[13,  2,  8,  4,  6, 15, 11,  1, 10,  9,  3, 14,  5,  0, 12,  7,
     1, 15, 13,  8, 10,  3,  7,  4, 12,  5,  6, 11,  0, 14,  9,  2,
     7, 11,  4,  1,  9, 12, 14,  2,  0,  6, 10, 13, 15,  3,  5,  8,
     2,  1, 14,  7,  4, 10,  8, 13, 15, 12,  9,  0,  3,  5,  6, 11],
]
#key
PC_1 = [57, 49, 41, 33, 25, 17,9,
       1, 58, 50, 42, 34, 26, 18,
      10,  2, 59, 51, 43, 35, 27,
      19, 11,  3, 60, 52, 44, 36,
      63, 55, 47, 39, 31, 23, 15,
       7, 62, 54, 46, 38, 30, 22,
      14,  6, 61, 53, 45, 37, 29,
      21, 13,  5, 28, 20, 12, 4]
PC_2 = [14, 17, 11, 24,  1,  5,  3, 28,
      15,  6, 21, 10, 23, 19, 12,  4,
      26,  8, 16,  7, 27, 20, 13,  2,
      41, 52, 31, 37, 47, 55, 30, 40,
      51, 45, 33, 48, 44, 49, 39, 56,
      34, 53, 46, 42, 50, 36, 29, 32]
#`秘钥左移的位数`
SHIFT = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]
def hex2bin(message):
    res=""
    for i in message:
        tmp=bin(int(i,16))[2:]
        for j in range(0,4-len(tmp)):
            tmp='0'+tmp
        res+=tmp
    return res
def bin2hex(bin_str):
    res = ""
    tmp = re.findall(r'.{4}', bin_str)
    for i in tmp:
        res += hex(int(i, 2))[2:]
    return res
#`IP盒处理`
def ip_change(bin_str):
    res = ""
    for i in IP_table:
        res += bin_str[i-1]
    return res
#`IP逆盒处理`
def ip_re_change(bin_str):
    res = ""
    for i in IP_re_table:
        res += bin_str[i-1]
    return res
#`E盒置换`
def e_str(bin_str):
    res = ""
    for i in E:
        res += bin_str[i-1]
    return res
#`字符串异或操作`
def str_xor(my_str1,my_str2):  #`str，key`
    res = ""
    for i in range(0,len(my_str1)):
        xor_res = int(my_str1[i],10)^int(my_str2[i],10)
        if xor_res == 1:
            res += '1'
        if xor_res == 0:
            res += '0'

    return res
#`循环左移操作`
def left_turn(my_str,num):
    left_res = my_str[num:len(my_str)]
    #left_res = my_str[0:num]+left_res
    left_res =  left_res+my_str[0:num]
    return left_res
#`秘钥的PC-1置换`
def change_key1(my_key):
    res = ""
    for i in PC_1:
        res += my_key[i-1]
    return res
#`秘钥的PC-2置换`
def change_key2(my_key):
    res  = ""
    for i in PC_2:
        res += my_key[i-1]
    return res
#`S盒`
def s_box(my_str):
    res = ""
    c = 0
    for i in range(0,len(my_str),6):
        now_str = my_str[i:i+6]
        row = int(now_str[0]+now_str[5],2)
        col = int(now_str[1:5],2)
        #row=0 #`删除e扩散`
        num = bin(S[c][row*16 + col])[2:]
        num=now_str[1:5] #`删除s`
        for gz in range(0,4-len(num)):
            num = '0'+ num
        res += num
        c  += 1
    return res
#`P盒置换`
def p_box(bin_str):
    res = ""
    for i in  P:
        res += bin_str[i-1]
    #res=bin_str #`删除p置换`
    return res

#` F函数的实现`
def fun_f(bin_str,key):
    first_output = e_str(bin_str)
    second_output = str_xor(first_output,key)
    third_output = s_box(second_output)
    last_output = p_box(third_output)
    #print(last_output)
    return last_output


def gen_key(key):
    key_list = []
    divide_output = change_key1(key)
    key_C0 = divide_output[0:28]
    key_D0 = divide_output[28:]
    for i in SHIFT:
        key_C0 = left_turn(key_C0,i)
        key_D0 = left_turn(key_D0,i)
        key_output = change_key2(key_C0 + key_D0)
        key_list.append(key_output)
    return key_list



def des_encrypt_one(bin_message,bin_key): #`64位二进制加密的测试`
    mes_ip_bin = ip_change(bin_message)
    key_lst = gen_key(bin_key)   #`生成子密钥`
    mes_left = mes_ip_bin[0:32]
    mes_right = mes_ip_bin[32:]
    for i in range(0,5):
        mes_tmp = mes_right
        f_result = fun_f(mes_tmp,key_lst[i])
        mes_right = str_xor(f_result,mes_left)
        mes_left = mes_tmp
    f_result = fun_f(mes_right,key_lst[5])
    mes_fin_left = str_xor(mes_left,f_result)
    mes_fin_right = mes_right
    fin_message = ip_re_change(mes_fin_left + mes_fin_right)
    return fin_message


#`简单判断以及处理信息分组`
def deal_mess(bin_mess):
    ans = len(bin_mess)
    if ans % 64 != 0:
        for i in range( 64 - (ans%64)):
            bin_mess += '0'
    return bin_mess


#`查看秘钥是否为64位`
def input_key_judge(bin_key):
    ans = len(bin_key)
    if len(bin_key) < 64:
        if ans % 64 != 0:
            for i in range(64 - (ans % 64)):
                bin_key += '0'
    return bin_key


def all_message_encrypt(message,key):
        bin_mess = deal_mess(hex2bin(message))
        res = ""
        bin_key = input_key_judge(hex2bin(key))
        tmp = re.findall(r'.{64}',bin_mess)
        for i in tmp:
            res += des_encrypt_one(i,bin_key)
        return res
def diff(a1,a2):
    fig=len(a1)
    res=0
    for i in range(fig):
        if(a1[i]!=a2[i]):
            res+=1
    return  res
if __name__ == '__main__':
        key = '0f1571c947d9e859'
        message = '02468aceeca86420'
        t1=time.time()
        s = all_message_encrypt(message, key)
        out_mess = bin2hex(s)
        print('加密过后的内容:',out_mess)
        print(s)
        print(time.time()-t1,'s')
        for i in range(8):
            print('从右数第',i+1,'位密钥改变')
            key_temp=list(hex2bin(key))
            key_temp[63-i]=str((int(key_temp[63-i])+1)%2)
            key_temp=''.join(key_temp)
            key_temp=bin2hex(key_temp)
            s = all_message_encrypt(message, key_temp)
            out_mess = bin2hex(s)
            print('加密过后的内容:',out_mess)
            print(s)
            print(diff('1110100010000111101100001100111101101110011000011000000001001100',hex2bin(out_mess)))
        for i in range(8):
            print('从右数第', i + 1, '位明文改变')
            message_temp = list(hex2bin(message))
            message_temp[63 - i] = str((int(message_temp[63 - i]) + 1) % 2)
            message_temp = ''.join(message_temp)
            message_temp = bin2hex(message_temp)
            s = all_message_encrypt(message_temp, key)
            out_mess = bin2hex(s)
            print('加密过后的内容:', out_mess)
            print(s)
            print(diff('1110100010000111101100001100111101101110011000011000000001001100', hex2bin(out_mess)))




