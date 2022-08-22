import os
from dreem import parameters, bit_vector, util
import pandas as pd
import numpy as np
from subprocess import PIPE, run
                
class RNAstructure(object): #TODO
    def __init__(self) -> None:
        pass  

    #ref = 'test/resources/case_1/test.fasta' 
    def run(self, mut_hist, roi=None, cmd='Fold'):
        p = parameters.get_parameters()

        # Extract name/sequence
        if roi == None:
            name, sequence = mut_hist.name, mut_hist.sequence
        else:
            assert (len(roi)==2) and (type(roi) in [tuple,list]), 'roi argument must be a 2-ints tuple or a 2-ints list'
            assert roi[0]<roi[1], 'ROI_start must be inferior to ROI_stop'
            name, sequence = mut_hist.name, mut_hist.sequence[roi[0]:roi[1]]

        # Make temp sub-folder to store files
        temp_folder = 'temp/'+ p.ins.sample 
        isExist = os.path.exists(temp_folder)
        if not isExist:
            os.makedirs(temp_folder)

        # push the ref into a temp file
        if roi == None:
            temp_prefix = temp_folder+'/'+name
        else:
            temp_prefix = temp_folder+'/'+name+'_ROI'

        temp_fasta = open(temp_prefix+'.fasta', 'w')
        temp_fasta.write('>'+name+'\n'+sequence)
        temp_fasta.close()

        output = {'name':name}

        if cmd == 'Fold':
            # Compute the mutation rate vector
            def generate_normalized_mut_rate(mh, MAX_MUT=0.04):
                mut_rate = np.array([min(base, MAX_MUT) for base in mh.mut_bases[1:]/mh.info_bases[1:]])        
                pd.DataFrame((mut_rate-min(mut_rate))/(max(mut_rate)-min(mut_rate)),index=list(range(1,1+len(mh.info_bases[1:]))))\
                            .to_csv(temp_prefix+'_DMS_signal.txt', header=False)
            generate_normalized_mut_rate(mut_hist)

            # Define files
            CT_FILES = [f"{temp_prefix}.ct", f"{temp_prefix}_DMS.ct"]
            DOT_FILES = [f"{temp_prefix}_dot.txt", f"{temp_prefix}_dot_DMS.txt"]

            # use RNAstructure to predict the structure 
            args = p.ins.RNAstructure_args + (f" --temperature {mut_hist.temperature}" if p.ins.temperature else '')
            temp_ct = open(temp_prefix+'.ct', 'w')
            temp_ct.close()

            for dms, ct_file in zip(['', f" -dms {temp_prefix}_DMS_signal.txt"],CT_FILES):
                util.run_command(f"{p.ins.RNAstructure_path}Fold {temp_prefix}.fasta {ct_file} "+args+dms)
                assert os.path.getsize(ct_file) != 0, f"{ct_file} is empty, check that RNAstructure works"

            # cast the temp file into a dot_bracket structure and extract the attributes
            def extract_deltaG_struct(ct_file, dot_file):
                util.run_command(f"ct2dot {ct_file} 1 {dot_file}")
                temp_dot = open(dot_file, 'r')
                first_line = temp_dot.readline().split()
                # If only dots in the structure, no deltaG 
                if len(first_line) == 4:
                    _, _, deltaG, name = first_line
                    deltaG = float(deltaG)
                if len(first_line) == 1:
                    deltaG, name = 'void', first_line[0][1:]

                sequence = temp_dot.readline()[:-1] #  Remove the \n
                structure = temp_dot.readline()[:-1] # Remove the \n
                return deltaG, sequence, structure

            suffixes = ['','_DMS']
            if roi != None:
                suffixes = ['_ROI'+s for s in suffixes]
            for ct_file, dot_file, suffix in zip(CT_FILES, DOT_FILES, suffixes):
                output['deltaG_min'+suffix], output['sequence'+suffix], output['structure'+suffix] = extract_deltaG_struct(ct_file, dot_file)

        if cmd == 'EnsembleEnergy':           
            cmd = f"{p.ins.RNAstructure_path}EnsembleEnergy {temp_prefix}.fasta --DNA --sequence" +(f" --temperature {mut_hist.temperature}" if p.ins.temperature else '')
            split_output = util.run_command(cmd)[0].split(' ')
            output['deltaG_ens'+ ('_ROI' if roi != None else '')] = float(split_output[split_output.index(f"{temp_prefix}.fasta:")+1])

        if cmd == 'partition':
            print('\n \n \n PARTITION \n')
            cmd = f"{p.ins.RNAstructure_path}partition {temp_prefix}.fasta {temp_prefix}.pfs --DNA" +(f" --temperature {mut_hist.temperature}" if p.ins.temperature else '')
            split_output = util.run_command(cmd)[0].split(' ')
        return output
