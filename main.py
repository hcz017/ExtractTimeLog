# -*- coding: utf-8 -*-
from excel_help import export2excel_and_draw_line_chart
from extract_key_word import process_ori_log_file, get_step_list, get_src_file_name

CONFIG_FILE = 'config/config_ex.ini'
TIME_LOG_FILE = 'out/extract_time.log'
FILTERED_TIME_LOG = 'out/filtered_time_log.log'
# EXPORTED_EXCEL_FILE = 'out/calc_result.xlsx'
EXPORTED_EXCEL_FILE = None

# /////// start /////
filter_incomplete_log_group = True
process_ori_log_file(CONFIG_FILE, TIME_LOG_FILE, filter_incomplete_log_group, FILTERED_TIME_LOG)

if EXPORTED_EXCEL_FILE is None:
    out_excel_file = 'out/' + get_src_file_name().split('/')[-1].split('.')[-2] + '.xlsx'
else:
    out_excel_file = EXPORTED_EXCEL_FILE

if filter_incomplete_log_group:
    export2excel_and_draw_line_chart(FILTERED_TIME_LOG, out_excel_file, get_step_list())
else:
    export2excel_and_draw_line_chart(TIME_LOG_FILE, out_excel_file, get_step_list())
