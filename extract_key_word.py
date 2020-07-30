import configparser
import re
import numpy as np
from matplotlib import pyplot as plt

global E_ALL_STEP, E_STEP_LIST, SRC_LOG_FILE_NAME, exclude_first_snapshot, addend_list, all_time_table, max_time_val


def load_configs(config_file):
    global E_ALL_STEP, E_STEP_LIST
    global SRC_LOG_FILE_NAME, exclude_first_snapshot, addend_list
    cf = configparser.ConfigParser()
    cf.read(config_file)

    # read by type
    E_ALL_STEP = cf.get('e_steps', 'e_all_step')
    E_STEP_LIST = cf.get('e_steps', 'e_step_list').split('\n')
    SRC_LOG_FILE_NAME = cf.get('file', 'file_name')
    exclude_first_snapshot = cf.getboolean('calc', 'exclude_first_snapshot')
    addend_list = cf.get('sum', 'e_addend_list').split('\n')


def extract_time_log_to_file(result_file):
    src_file = None
    time_log_file = None
    try:
        # encoding maybe wrong
        src_file = open(SRC_LOG_FILE_NAME, encoding='iso-8859-1')
        time_log_file = open(result_file, 'w')
        # time_spilt_file = open('extract_split_time.log', 'w')  # not necessary
    except IOError:
        print('!!!target file not found!!!', SRC_LOG_FILE_NAME)
        exit()

    # print('generate_wa_time_split_log')
    for line in src_file:
        g = re.search(E_ALL_STEP, line)
        if g:
            time_log_file.writelines(line)
            # time_spilt_file.writelines(g.group() + '\n')  # not necessary
    src_file.close()
    time_log_file.close()
    # time_spilt_file.close()


def get_step_time(step_name, time_log_object):
    # print('get_step_time:', step_name)
    time_list = []
    for line in time_log_object:
        match_step = re.search(step_name, line)
        if match_step:
            numbers = re.findall(r'\d+\.\d*', line)
            single_time = eval(numbers[len(numbers) - 1])
            time_list.append(single_time)
    return time_list


def calc_step_avg_time(time_log_file):
    global all_time_table, max_time_val
    max_time_val = 0
    all_time_table = []
    total_time = 0
    for step in E_STEP_LIST:
        time_log = open(time_log_file)
        step_time_list = get_step_time(step, time_log)
        if len(step_time_list) == 0:
            print('no step: ', step, 'please check!')
            continue
        else:
            all_time_table.append(step_time_list)
            max_time_val = max(max(step_time_list), max_time_val)
        time_log.close()
        # print('all_time_table', all_time_table)
        # print('step:', step, '\t time list:', step_time_list, 'len:', len(step_time_list))

        if exclude_first_snapshot:
            print('[step:', step, '][times:', len(step_time_list) - 1, ']\t[avg:',
                  (sum(step_time_list) - step_time_list[0]) / (len(step_time_list) - 1), ']')
        else:
            print('[step:', step, '][times:', len(step_time_list), ']\t[avg:', np.mean(step_time_list), ']')
        if step in addend_list:
            if exclude_first_snapshot:
                total_time += (sum(step_time_list) - step_time_list[0]) / (len(step_time_list) - 1)
            else:
                total_time += np.mean(step_time_list)
    print('e_addend_list sum time: ', total_time)


def draw_line_chart(all_time):
    x = np.arange(1, len(all_time[0]) + 1, 1)
    step_name_index = 0
    for step_time_list in all_time:
        # print('x:', len(x), ' len step_time_list: ', len(step_time_list))
        plt.plot(x, step_time_list, label=E_STEP_LIST[step_name_index])
        step_name_index += 1

    plt.xlabel('times')
    plt.ylabel('time/ms')
    plt.yticks(np.linspace(0, int(max_time_val + 1), int(max_time_val * 2) + 1))
    plt.xticks([x for x in range(len(all_time[0]) + 1) if x % 2 == 0])
    plt.grid(color='#95a5a6', linestyle='--', linewidth=1, axis='y', alpha=0.4)
    plt.title('steps run time')
    plt.legend()
    plt.show()


def filter_time_log(time_log_file, out_file):
    step_list = E_STEP_LIST
    time_log = open(time_log_file)
    out_log = open(out_file, 'w')
    time_log_list = time_log.readlines()

    for line_idx in range(0, len(time_log_list)):
        if re.search(step_list[0], time_log_list[line_idx]):
            match_cnt = 0
            for i in range(1, len(step_list)):
                if re.search(step_list[i], time_log_list[line_idx + i]):
                    match_cnt += 1
            if len(step_list) - 1 == match_cnt:
                for j in range(line_idx, line_idx + len(step_list)):
                    out_log.writelines(time_log_list[j])
    time_log.close()
    out_log.close()


def process_ori_log_file(config, out_time_log_file, need_filter_log, filtered_time_log):
    load_configs(config)
    extract_time_log_to_file(out_time_log_file)
    if need_filter_log:
        filter_time_log(out_time_log_file, filtered_time_log)
        calc_step_avg_time(filtered_time_log)
        # draw_line_chart(all_time_table)
    calc_step_avg_time(out_time_log_file)


def get_step_list():
    return E_STEP_LIST


def get_src_file_name():
    return SRC_LOG_FILE_NAME
