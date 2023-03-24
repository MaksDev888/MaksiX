# input STR
# U,D UP/DOWN
# DU

def find_down(str1):
    count = 0
    stop_count = -1
    str2 = str1

    while count != stop_count:
        neutral_line = 0
        if str2[count] == 'U':
            neutral_line += 1
        else:
            neutral_line -= 1

        if 'DU' in str2 and neutral_line <= 0 :
            count += 1
            stop_count += 1
            str2 = str2.replace('DU', '1',1)
        else:
            stop_count += 1
    return count

print(find_down('UUUDUDUDDD'))