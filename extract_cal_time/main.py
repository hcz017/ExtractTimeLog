# -*- coding: utf-8 -*-
import excel_help
import extract_key_word
import config_help as cfg_help
import utils
import sys
import os

CONFIG_FILE = 'config_ex.ini'
TIME_LOG_FILE = 'extract_time.log'
FILTERED_TIME_LOG = 'filtered_time_log.log'

# /////// start /////

# get config from xml
extract_cfg = cfg_help.get_configuration(CONFIG_FILE)
# override config with input params
argv = sys.argv[1:]
if len(argv) != 0:
    extract_cfg = cfg_help.override_configuration(argv)

# generate out file name for excel
if len(extract_cfg.out_file_name) > 0:
    out_excel_file = extract_cfg.out_file_name + '.xlsx'
else:
    out_excel_file = utils.gen_out_file_path(extract_cfg.src_log_file_name)

# flag for whether to ignore in complete log group
filter_incomplete_log_group = extract_cfg.filter_incomplete_log_group

extract_key_word.process_ori_log_file(extract_cfg.src_log_file_name, extract_cfg, TIME_LOG_FILE,
                                      filter_incomplete_log_group, FILTERED_TIME_LOG)

if filter_incomplete_log_group:
    excel_help.export2excel_and_draw_line_chart(FILTERED_TIME_LOG, out_excel_file, extract_cfg.e_step_list)
else:
    excel_help.export2excel_and_draw_line_chart(TIME_LOG_FILE, out_excel_file, extract_cfg.e_step_list)
