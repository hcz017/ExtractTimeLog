import re


def test_extract_number(line_text, word):
    offset = 0
    match_step = re.search(word, line_text)
    if match_step:
        # in case step key contains number, like "step 4 do blender", need to add the offset of number "4"
        number_in_step_key = re.search(r'\d+', word)
        if number_in_step_key:
            offset = number_in_step_key.end()
        # match_step.start(0) => key world start position
        numbers = re.findall(r'\d+\.?\d*', line_text[match_step.start(0) + offset:])
        single_time = eval(numbers[0])
        print('number', single_time)
        return single_time


if __name__ == '__main__':
    print("I'm code_test.py")
    line = '02-01 10:03:39.355  8578  8578 D MainActivity: step  run time (200 ms).\n'
    step_key = 'step  run time'
    number = test_extract_number(line, step_key)
    assert number == 200

    step_key = 'step  run time.*'
    line = r'06-05 15:15:36.807 22932 22932 D MainActivity: step  run time: 2.6695076627745946s'
    number = test_extract_number(line, step_key)
    assert number == 2.6695076627745946

    step_key = 'step 2 run time.*'
    line = r'06-05 15:15:36.807 22932 22932 D MainActivity: step 2 run time: 2.6695076627745946s'
    number = test_extract_number(line, step_key)
    assert number == 2.6695076627745946
