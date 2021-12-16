import os


# generate an out file name for excel
def gen_out_file_name(src_file_name):
    print(" -------- gen_out_file_name --------")
    src_file_name = os.path.basename(src_file_name)
    print(" base name ", os.path.basename(src_file_name))

    print(src_file_name.split('.'))
    post_fix_len = len(src_file_name.split('.')[-1])
    if post_fix_len == len(src_file_name):
        post_fix_len = -1

    out_file_name = src_file_name[0: len(src_file_name) - post_fix_len - 1] + ".xlsx"
    print("out_file_name", out_file_name)
    print(" -------- gen_out_file_name --------\n")

    return out_file_name
