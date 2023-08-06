from contextlib import suppress
import os
os.environ["ZFIT_DISABLE_TF_WARNINGS"] = "1"
from .plotting import *
import pkg_resources

from types import SimpleNamespace
arguments={}
arguments["verbose"]=False
arguments["estimate_pulls"]=True
arguments["bbox_inches"]='tight'
arguments["no_errors_on_zero_bins"]=False

DATA_PATH = pkg_resources.resource_filename('alexPlot', '')

def help():
    os.system(f'cat {DATA_PATH}/help.txt')
    print('\n')
    for key in list(arguments.keys()):
        # print(key, arguments[key])
        print('{:<40s}{:>16s}'.format(key, str(arguments[key])))
    print('\n')
    print('Example: alexPlot.options.estimate_pulls = False')
    print('\n\n')

def examples():
    os.system(f'cat {DATA_PATH}/example.txt')

    
options = SimpleNamespace(**arguments)
