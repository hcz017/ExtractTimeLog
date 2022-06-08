import xlsxwriter
import re
import numpy as np


def export2excel_and_draw_line_chart(src_data, out_excel_file, cols_names):
    time_log_file = None
    line_num = 0
    print("export result to: ", out_excel_file)
    workbook = xlsxwriter.Workbook(out_excel_file)
    sheet = workbook.add_worksheet("performance")
    chart = workbook.add_chart({'type': 'line'})
    color = ['black', 'blue', 'brown', 'cyan', 'gray', 'magenta', 'navy', 'orange', 'pink', 'purple', 'red', 'silver',
             'white', 'yellow']
    results = ['avg', 'max', 'min', 'gap']
    for i in range(0, len(cols_names)):
        sheet.write(0, i + 1, cols_names[i])
        line_num = 0
        try:
            time_log_file = open(src_data)
        except IOError:
            print("!!!target file not found!!!")
            exit()
        time_list = []
        for line in time_log_file:
            match_step = re.search(cols_names[i], line)
            if match_step:
                line_num += 1
                # add offset len(results) + 1
                sheet.write(line_num + len(results) + 1, 0, line_num)
                numbers = re.findall(r"\d+\.\d*", line)
                single_time = eval(numbers[len(numbers) - 1])
                time_list.append(single_time)
                sheet.write(line_num + len(results) + 1, i + 1, float(single_time))
        if (len(time_list) == 0):
            return
        # avg
        row_index = 1
        sheet.write(row_index, 0, results[0])
        sheet.write(row_index, i + 1, np.mean(time_list))
        # max
        row_index += 1
        sheet.write(row_index, 0, results[1])
        sheet.write(row_index, i + 1, np.max(time_list))
        # min
        row_index += 1
        sheet.write(row_index, 0, results[2])
        sheet.write(row_index, i + 1, np.min(time_list))
        # gap
        row_index += 1
        sheet.write(row_index, 0, results[3])
        sheet.write(row_index, i + 1, np.max(time_list) - np.min(time_list))

        time_log_file.close()
    for i in range(0, len(cols_names)):
        # Or using a list of values instead of category/value formulas:
        #     [sheetname, first_row, first_col, last_row, last_col]
        chart.add_series({
            'name':       ['performance', 0, i + 1],
            'categories': ['performance', len(results) + 2, 0, line_num + len(results) + 1, 0],
            'values':     ['performance', len(results) + 2, i + 1, line_num + len(results) + 1, i + 1],
            'line': {'color': color[i % len(color)]},
        })
        chart.set_size({'x_scale': 2, 'y_scale': 2})
    sheet.insert_chart('I2', chart, {'x_offset': 50, 'y_offset': 50})
    workbook.close()
