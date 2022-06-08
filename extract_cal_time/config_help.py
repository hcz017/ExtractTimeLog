import configparser
import getopt
import os
import sys


class Configuration:
    filter_incomplete_log_group = False
    exclude_first_snapshot = False
    out_file_name = ''
    pass


def load_configs(config_file):
    # print(" -------- load_configs --------")
    cf = configparser.ConfigParser()
    cf.read(config_file)

    # read by type
    Configuration.e_all_step = cf.get('e_steps', 'e_all_step')
    Configuration.e_step_list = cf.get('e_steps', 'e_step_list').split('\n')
    Configuration.src_log_file_name = cf.get('file', 'file_name')
    Configuration.exclude_first_snapshot = cf.getboolean('calc', 'exclude_first_snapshot')
    Configuration.filter_incomplete_log_group = cf.getboolean('etc', 'filter_incomplete_log_group')
    if len(Configuration.e_all_step) == 0:
        all_step = ""
        for i in range(0, len(Configuration.e_step_list)):
            all_step = all_step + Configuration.e_step_list[i]

            if i != len(Configuration.e_step_list) - 1:
                all_step = all_step + "|"
            Configuration.e_all_step = all_step

    # print('all step: ', Configuration.e_all_step, ' len ', len(Configuration.e_all_step))
    # print('e_step_list: ', Configuration.e_step_list, ' len ', len(Configuration.e_step_list))
    # print(" -------- load_configs --------\n")


def get_configuration(config_file=""):
    if not os.path.exists(config_file):
        print('config file not exist!!')
        return
    if len(config_file) != 0:
        load_configs(config_file)
    return Configuration


def override_configuration(argv):
    # print(" -------- override -------- ")
    try:
        opts, args = getopt.getopt(argv, "hi:E:o:", ["input=", "expression="])
        # print(opts, args)
    except getopt.GetoptError:
        print('test.py -i <input_file> -E <expression>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <input_file> -E <expression> -o <output(xlsx)>')
            sys.exit()
        elif opt in ("-i", "--input"):
            Configuration.src_log_file_name = arg
            # print("input file: ", Configuration.src_log_file_name)
        elif opt in ("-o", "--output"):
            Configuration.out_file_name = arg
        elif opt in ("-E", "--expression"):
            input_steps = arg
            # print("input_steps: ", input_steps)
            Configuration.e_all_step = input_steps
            Configuration.e_step_list = input_steps.split('|')

            # print("e_all_step ", Configuration.e_all_step)
            # print("e_step_list ", Configuration.e_step_list)
    # print(" -------- override --------\n ")

    return Configuration


if __name__ == '__main__':
    print("I'm config_help.py")
