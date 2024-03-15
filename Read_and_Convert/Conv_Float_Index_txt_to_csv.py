import pandas as pd
import numpy as np

class Float_index_management():
    """ Class define the name and fileds of the input file wich is the catalogue file with main info """

    def __init__(self, FILENAME='Float_Index.txt'):
        self.namefile = FILENAME
        self.columns = ['WMO','Lat','Lon','Date', 'DOXY','NITRATE','CHLA',  'PRES','PSAL','TEMP','PH_IN_SITU_TOTAL', 'BBP700','BBP532', 'DOWNWELLING_PAR', 'CDOM','DOWN_IRRADIANCE380' ,'DOWN_IRRADIANCE412','DOWN_IRRADIANCE490' ]

    def Convert(string):
        """ useful to fill columns and convert file.txt in csv"""
        li = list(string.split(" "))
        return li

    def read_txt(self, namefile, columns, OUTDIR):
        """  read files.txt and convert it in file.csv """ 
        df = pd.read_csv(OUTDIR + namefile)
        df.columns= ['WMO','Lat','Lon','Date','VARS']
        df_to_fill = pd.DataFrame(index=df.index, columns = self.columns)
        for ROW in range(0,len(df)):
            tmp = df.iloc[ROW,:]
            df_to_fill.iloc[ROW,0:4] = tmp[0:4]
            VARLIST= Float_index_management.Convert(tmp.VARS)
            VARLIST.remove("")
            for VARS in VARLIST:
                df_to_fill.iloc[ROW][VARS]=1

        df_to_fill.dropna(axis=1, how='all', inplace=True)
        df_to_fill.columns
        return df_to_fill


#sys.path.append("/g100/home/userexternal/camadio0/CA_functions/")
#import funzioni_CA

import pandas as pd
import numpy as np
import sys
from Float_Index_to_functions import Float_index_management
OUTDIR='/g100_scratch/userexternal/camadio0/SUPERFLOAT_2017_2019_V9C_SMOOTH_CALIBR/'
ff = Float_index_management()
ff.read_txt(ff.namefile,ff.columns, OUTDIR )
new_df  = ff.read_txt(ff.namefile,ff.columns, OUTDIR )
"""
