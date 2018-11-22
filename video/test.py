import datetime

def get_start_time(file_name):
    time_str = file_name.split('_')[3]
    year = int(time_str[:4])
    month = int(time_str[4:6])
    day = int(time_str[6:8])
    hour = int(time_str[8:10])
    minute = int(time_str[10:12])
    second = int(time_str[12:14])

    res = datetime.datetime(year, month, day, hour, minute, second)
    return res

def solve():
    v = []
    v.append((1, 2))
    v.append((3, 4))
    return v

if __name__ == "__main__":
    a = 'Camera1_cam2_cam2_20181113114949_20181113115534_6528826'
    time_begin = get_start_time(a)
    name = 'Nam'
    frame_indice = 1400
    time_appear = time_begin + datetime.timedelta(0, frame_indice / 25)
    result = open('result.txt', 'a')
    result.write(name + '\t' + str(time_appear) + '\n')