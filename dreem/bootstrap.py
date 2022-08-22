
from attr import attrib
import scipy.stats
import numpy as np
import pandas as pd

class Bootstrap(object):
    def __init__(self) -> None:
        pass

    def boostrap_residue(self,df_col):
        # convert array to sequence
        data = np.array(df_col.dropna()).reshape(1,-1)

        #calculate 95% bootstrapped confidence interval for median
        bootstrap_ci = scipy.stats.bootstrap(data, np.std, confidence_level=0.95,
                                random_state=1, method='percentile')
        return bootstrap_ci

    def clean_df(self, df_raw):
        df = df_raw['Bit_vector'].str.split('', expand=True)
        df = df.drop(columns=[0,df.columns[-1]])
        
        def cast(c):
            # only keep 0s and 1s
            if c == '0': return 0
            if c == '1': return 1
            else: return np.nan
        for col in df.columns:
            df[col] = df[col].apply(lambda x: cast(x))

        return df

    def run(self, bitvector_path):
        df = self.clean_df(pd.read_csv(bitvector_path, sep='\t', header=2, usecols=['Bit_vector']))
        output = {'bootstrap_low':[0],'bootstrap_high':[0],'bootstrap_std':[0]}
        for col in df.columns:
            temp = self.boostrap_residue(df[col])
            output['bootstrap_low'].append(temp.confidence_interval.low)
            output['bootstrap_high'].append(temp.confidence_interval.high)
            output['bootstrap_std'].append(temp.standard_error)
        return output

if __name__ == '__main__':
    boot = Bootstrap()
    print(boot.run('output/case_1/BitVector_Files/mttr-6-alt-h3_bitvectors.txt'))
