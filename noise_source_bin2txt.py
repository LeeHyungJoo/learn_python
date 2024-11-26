# -*- coding: utf-8 -*-

import binascii
import os

# {key : value} = {os_info : bin_file_os_prefix}
win32_os_dict = {
    "Windows7-32bit": "win7_32bit_",
    "Windows10-32bit": "win10_32bit_"
}

win64_os_dict = {
    "Windows7-64bit": "win7_64bit_",
    "Windows10-64bit": "win10_64bit_",
    "Windows11-64bit": "win11_64bit_",
}

linux_os_dict = {
    "Linux4.15.0": "linux_"
}

target_dict = {
    "Windows7-32bit" : "[x32] Win 7",
    "Windows10-32bit" : "[x32] Win10",
    "Windows7-64bit" : "[x64] Win 7",
    "Windows10-64bit": "[x64] Win10",
    "Windows11-64bit": "[x64] Win11",
}

# [NOTICE] noise_byte_size change between 32bit & 64bit. => Heap32, Module32, Process32
# [NOTICE] GetCursorPos is right, but bin data name of it is GetCursurPos.
# {key : [val1, val2]} = {noise_func : [bin_file_noise_name, noise_byte_size]}
win32_noise_func_dict = {
    "CoCreateGuid": ["CoCreateGuid", 16],
    "CryptGenRandom": ["CryptGenRandom", 131],
    "GetCursorPos": ["GetCursurPos", 8],
    "GetTickCount64": ["GetTickCount64", 8],
    "GlobalMemoryStatusEx": ["GlobalMemoryStatusEx", 64],
    "Heap32Next": ["Heap32Next", 36],
    "Module32Next": ["Module32Next", 1064],
    "NTQuerySystemInformation-Performance": ["NT_Performance", 312],
    "NTQuerySystemInformation-TimeOfDay": ["NT_TimeOfDay", 48],
    "Process32Next": ["Process32Next", 556],
    "QueryPerformanceCounter": ["QueryPerformanceCounter", 8],
    "Thread32Next": ["Thread32Next", 28]
}

win64_noise_func_dict = {
    "CoCreateGuid": ["CoCreateGuid", 16],
    "CryptGenRandom": ["CryptGenRandom", 131],
    "GetCursorPos": ["GetCursurPos", 8],
    "GetTickCount64": ["GetTickCount64", 8],
    "GlobalMemoryStatusEx": ["GlobalMemoryStatusEx", 64],
    "Heap32Next": ["Heap32Next", 56],
    "Module32Next": ["Module32Next", 1080],
    "NTQuerySystemInformation-Performance": ["NT_Performance", 312],
    "NTQuerySystemInformation-TimeOfDay": ["NT_TimeOfDay", 48],
    "Process32Next": ["Process32Next", 568],
    "QueryPerformanceCounter": ["QueryPerformanceCounter", 8],
    "Thread32Next": ["Thread32Next", 28]
}

linux_noise_func_dict = {
    "gettimeofday": ["gettimeofday", 16],
    "urandom": ["urandom", 244]
}


def bin_to_txt(dir_path, function_name, noise_byte_len, bin_name):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    noise_txt_data = ""
    sample_num_cnt = 0

    with open(bin_name, "rb") as f:
        while True:
            noise_bin_sample = f.read(noise_byte_len)
            if noise_bin_sample:
                noise_txt_data += "{}\n".format(binascii.b2a_hex(noise_bin_sample).decode('utf-8'))
                sample_num_cnt += 1
            else:
                break

    target_file_name = dir_path+"/"+function_name+".txt"
    print(">> {} collects {} samples".format(target_file_name, sample_num_cnt))
    with open(target_file_name, "wt") as f:
        f.write(noise_txt_data[:-1])


def bin_to_txt_windows():
    for win32_os in win32_os_dict:
        print(">> os : {}".format(win32_os))
        dir_path = "./{}".format(win32_os)
        for noise_function in win32_noise_func_dict:
            for idx in range(0,5):
                bin_name = "./{}/".format(target_dict[win32_os]) + win32_os_dict[win32_os] + win32_noise_func_dict[noise_function][0] + "_original[{}].bin".format(idx)
                noise_byte_len = win32_noise_func_dict[noise_function][1]
                bin_to_txt(dir_path, noise_function, noise_byte_len, bin_name)

    for win64_os in win64_os_dict:
        print(">> os : {}".format(win64_os))
        dir_path = "./{}".format(win64_os)
        for noise_function in win64_noise_func_dict:
            for idx in range(0, 5):
                bin_name = "./{}/".format(target_dict[win64_os]) + win64_os_dict[win64_os] + win64_noise_func_dict[noise_function][0] +  "_original[{}].bin".format(idx)
                noise_byte_len = win64_noise_func_dict[noise_function][1]
                bin_to_txt(dir_path, noise_function, noise_byte_len, bin_name)


def bin_to_txt_linux():
    for linux_os in linux_os_dict:
        print(">> os : {}".format(linux_os))
        dir_path = "./{}".format(linux_os)
        for noise_function in linux_noise_func_dict:
            for idx in range(0, 5):
                bin_name = linux_os_dict[linux_os] + linux_noise_func_dict[noise_function][0] +  "_original[" + idx + "].bin"
                noise_byte_len = linux_noise_func_dict[noise_function][1]
                bin_to_txt(dir_path, noise_function, noise_byte_len, bin_name)


def main():
    print("# --------- convert noise_source.bin -> noise_source.txt start --------- #")
    #print(">> OS information : 1.win7-32bit 2.win7-64bit, 3.win10-32bit, 4.win10-64bit")
    #print("                  : 5.win11-64bit, 6.linux  ")

    bin_to_txt_windows()
    #bin_to_txt_linux()


if __name__ == "__main__":
    main()


