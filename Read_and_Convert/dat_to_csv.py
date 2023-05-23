import numpy as np
import pandas as pd

INPUT='/g100_scratch/userexternal/camadio0/SYNTHETIC_2017_2018/wrkdir/MODEL/DA__FREQ_1/20181222.arg_mis.dat'
df = pd.read_csv(INPUT, header=1, sep='\t', index_col=0)
COL= ['Nr','VAR_type', 'lon', 'lat' , 'depth' ,'nr1','misfit', 'error', 'wmo']
df.index =np.arange(1,len(df)+1)
s = pd.Series(df.columns)
s.name= 0
s.index =df.columns
df = df.append(s)
df.columns  = COL
df.sort_index(inplace=True)
