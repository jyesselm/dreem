            
# USER EDIT PARAMETERS HERE
####################################################################

PATH_TO_DATA = 'test/resources/'
FILES_PER_SAMPLE = ['r1.fastq','r2.fastq','ref.fasta','library.csv']
SAMPLES = ['case_1','case_2']
args = {
    '--overwrite':True,
    '--RNAstructure_path':'/Users/ymdt/src/RNAstructure/exe',
    '--sample_info':PATH_TO_DATA+'samples.csv',
    '--temperature':False,
    '--add_any_info':False,
    '--bootstrap':True
}
VERBOSE = True
####################################################################


## SANITY CHECKS
####################################################################

import pandas as pd
import os

# check that every file is there
for s in SAMPLES:
    for f in FILES_PER_SAMPLE:
        assert os.path.exists(PATH_TO_DATA+s+'/'+f), f"{PATH_TO_DATA}{s}/{f} doesn't exist"
assert os.path.exists(PATH_TO_DATA+'samples.csv'), f"{PATH_TO_DATA}samples.csv doesn't exist"

# check the sanity of samples.csv
df_samples = pd.read_csv('test/resources/samples.csv')
assert len(df_samples['sample']) == len(df_samples['sample'].unique()), "Every line isn't unique in samples.csv"

# check that every sample as a corresponding line of samples.csv
for s in SAMPLES:
    assert s in list(df_samples['sample']), f"{s} doesn't have a corresponding line in samples.csv"


## RUN 
####################################################################

from dreem import util

## TO REMOVE
print(util.run_command('pip3 install .')[0])


for s in SAMPLES:
    cmd = 'dreem'
    for fast_arg, fast_file in zip(['-fq1','-fq2','-fa','--library_info'],FILES_PER_SAMPLE):
        cmd += ' '+fast_arg+' '+PATH_TO_DATA+f"{s}/"+fast_file
    for key, val in args.items():
        if (not (type(val) == bool)) or val:
            cmd += ' '+ key + ' '+ (val if type(val) != bool else '')
    cmd += ' --sample '+s
    if VERBOSE: print(cmd)
    print(util.run_command(cmd)[0]) if VERBOSE else util.run_command(cmd)

## TO REMOVE
print(util.run_command('/Library/Frameworks/Python.framework/Versions/3.10/bin/python3.10 /Users/ymdt/src/dreem/my_test_zone.py')[0])
