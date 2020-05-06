import configparser
import re
import numpy as np
from matplotlib import pyplot as plt


def load_configs():
    global E_ALL_STEP, E_STEP_LIST
    global file_name, exclude_first_snapshot, addend_list
    cf = configparser.ConfigParser()
    cf.read("config_ex.ini")

    # read by type
    E_ALL_STEP = cf.get("e_steps", "e_all_step")
    E_STEP_LIST = cf.get("e_steps", "e_step_list").split("\n")
    file_name = cf.get("file", "file_name")
    exclude_first_snapshot = cf.getboolean("calc", "exclude_first_snapshot")
    addend_list = cf.get("sum", "e_addend_list").split("\n")


def generate_wa_time_split_log():
    global file_object, wa_time_file, wa_time_spilt_file
    try:
        # encoding maybe wrong
        file_object = open(file_name, encoding='iso-8859-1')
        wa_time_file = open('extract_time.log', 'w')
        wa_time_spilt_file = open('extract_split_time.log', 'w')
    except IOError:
        print("!!!target file not found!!!")
        exit()

    global group_count
    # print("generate_wa_time_split_log")
    group_count = 0
    line_num = 0
    for line in file_object:
        line_num += 1
        g = re.search(E_ALL_STEP, line)
        if g:
            if re.findall(E_STEP_LIST[0], g.group()):
                group_count += 1
            wa_time_file.writelines(line)  # not necessary
            wa_time_spilt_file.writelines(g.group() + '\n')
    file_object.close()
    wa_time_file.close()
    wa_time_spilt_file.close()


def get_step_time(step_name, time_log_object):
    # print("get_step_time:", step_name)
    match_count = 0
    line_num = 0
    time_list = []
    for line in time_log_object:
        line_num += 1
        match_step = re.search(step_name, line)
        if match_step:
            match_count += 1
            times = re.findall(r"\d+\.\d*", line)
            for time_s in times:
                # print(match_count, '\t', time_s)
                # print("time list:", time_list)
                # use eval() to get ride of '
                time_list.append(eval(time_s))
    return time_list


def calc_step_avg_time():
    global all_time_table
    global max_time_val
    max_time_val = 0
    all_time_table = []
    total_time = 0
    for step in E_STEP_LIST:
        time_log = open("extract_split_time.log")
        step_time_list = get_step_time(step, time_log)
        all_time_table.append(step_time_list)
        if len(step_time_list) == 0:
            print("no step: ", step, "please check!")
            exit()
        else:
            max_time_val = max(max(step_time_list), max_time_val)
        time_log.close()
        # print("all_time_table", all_time_table)
        # print("step:", step, '\ntimelist:', step_time_list, "len:", len(step_time_list))

        if exclude_first_snapshot:
            print("step:", step, "avg: ", (sum(step_time_list) - step_time_list[0]) / (len(step_time_list) - 1))
        else:
            print("step:", step, "avg: ", np.mean(step_time_list))
        if step in addend_list:
            if exclude_first_snapshot:
                total_time += (sum(step_time_list) - step_time_list[0]) / (len(step_time_list) - 1)
            else:
                total_time += np.mean(step_time_list)
    print("e_addend_list sum time: ", total_time)


def draw_line_chart(all_time):
    x = np.arange(1, len(all_time[0]) + 1, 1)
    step_name_index = 0
    for step_time_list in all_time:
        # print("x:", len(x), " len step_time_list: ", len(step_time_list))
        plt.plot(x, step_time_list, label=E_STEP_LIST[step_name_index])
        step_name_index += 1

    plt.xlabel("times")
    plt.ylabel("time/s")
    plt.yticks(np.linspace(0, int(max_time_val + 1), int(max_time_val + 1) * 2 + 1))
    plt.xticks([x for x in range(len(all_time[0]) + 1) if x % 2 == 0])
    plt.grid(color='#95a5a6', linestyle='--', linewidth=1, axis='y', alpha=0.4)
    plt.title("steps run time")
    plt.legend()
    plt.show()


load_configs()

generate_wa_time_split_log()

calc_step_avg_time()

print("group_count", group_count)

draw_line_chart(all_time_table)
