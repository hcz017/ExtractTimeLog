import xlsxwriter
import re
import numpy as np


def export2excel_and_draw_line_chart(src_data, out_excel_file, cols_names):
    # cols_names : step list
    time_log_file = None
    matched_row_num = 0
    # 0. create workbook and sheet
    workbook = xlsxwriter.Workbook(out_excel_file)
    sheet = workbook.add_worksheet("performance")
    calc_results_str = ['avg', 'max', 'min', 'gap']
    sn_col_idx = 2
    # 1. write time data
    for step_idx in range(0, len(cols_names)):
        # 1.1 write step name
        sheet.write(0, sn_col_idx + step_idx + 1, cols_names[step_idx])
        matched_row_num = 0
        try:
            time_log_file = open(src_data)
        except IOError:
            print("!!!target file not found!!!")
            exit()
        time_list = []
        # 1.2 write time data
        for line in time_log_file:
            match_step = re.search(cols_names[step_idx], line)
            offset = 0
            if match_step:
                matched_row_num += 1
                # write serial number
                row_idx = len(calc_results_str) + 1 + matched_row_num
                sheet.write(row_idx, sn_col_idx, matched_row_num)
                # in case step key contains number, like "step 4 do blender", need to add the offset of number "4"
                number_in_step_key = re.search(r'\d+', cols_names[step_idx])
                if number_in_step_key:
                    offset = number_in_step_key.end()
                # match_step.start(0) => key world start position
                numbers = re.findall(r'\d+\.?\d*', line[match_step.start(0) + offset:])
                single_time = eval(numbers[0])
                # write single time data
                sheet.write(row_idx, sn_col_idx + step_idx + 1, float(single_time))
                time_list.append(single_time)
        if len(time_list) == 0:
            continue
        # 1.2 write calc result
        # avg
        row_idx = 1
        col_idx = sn_col_idx + step_idx + 1
        sheet.write(row_idx, sn_col_idx, calc_results_str[0])
        sheet.write(row_idx, col_idx, np.mean(time_list))
        # max
        row_idx += 1
        sheet.write(row_idx, sn_col_idx, calc_results_str[1])
        sheet.write(row_idx, col_idx, np.max(time_list))
        # min
        row_idx += 1
        sheet.write(row_idx, sn_col_idx, calc_results_str[2])
        sheet.write(row_idx, col_idx, np.min(time_list))
        # gap
        row_idx += 1
        sheet.write(row_idx, sn_col_idx, calc_results_str[3])
        sheet.write(row_idx, col_idx, np.max(time_list) - np.min(time_list))
        time_log_file.close()
    # 2. draw line chart
    chart = workbook.add_chart({'type': 'line'})
    color = ['black', 'blue', 'brown', 'cyan', 'gray', 'magenta', 'navy', 'orange', 'pink', 'purple', 'red', 'silver',
             'white', 'yellow']
    for step_idx in range(0, len(cols_names)):
        # Or using a list of values instead of category/value formulas:
        #     [sheetname, first_row, first_col, last_row, last_col]
        chart.add_series({
            'name': ['performance', 0, sn_col_idx + step_idx + 1],
            'categories': ['performance', len(calc_results_str) + 2, sn_col_idx,
                           len(calc_results_str) + 1 + matched_row_num, sn_col_idx],
            'values': ['performance', len(calc_results_str) + 2, sn_col_idx + step_idx + 1,
                       len(calc_results_str) + 1 + matched_row_num, sn_col_idx + step_idx + 1],
            'line': {'color': color[step_idx % len(color)]},
        })
        chart.set_size({'x_scale': 2, 'y_scale': 2})
    sheet.insert_chart('I2', chart, {'x_offset': 50, 'y_offset': 50})

    print("exported result to: ", out_excel_file)

    workbook.close()


if __name__ == '__main__':
    print("I'm excel_help.py")
