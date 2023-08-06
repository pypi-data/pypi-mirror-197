from subprocess import check_output, Popen, PIPE
import sys

def execute(cmd, shell=False):
    if sys.version_info.major == 3:
        output = check_output(cmd, encoding='UTF-8', shell=shell)
    else:
        output = check_output(cmd, shell=shell)
    return output.rstrip()

def execute_live(cmd):
    process = Popen(cmd, stdout=PIPE)
    for line in iter(process.stdout.readline, b''):
        print(line.decode('utf-8'), end='')
    process.stdout.close()
    process.wait()

def filter_none(list_to_filter):
    return [x for x in list_to_filter if x is not None]
