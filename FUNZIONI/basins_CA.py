import pandas as pd
import numpy as np
import basins.OGS as OGS
import basins.V2 as basV2
from basins.region import Region, Rectangle

class Basins_med_analysis():
    #from commons_ import cross_Med_basins
    """ it allow to investigate 2nd level of metadata (e.g. if a podition is in the West-east or name of subbasin)"""
    def __init__(self, FILENAME='Float_Index.txt'):
        self.name = 'BGC_float'
    def which_Med_basins(self, RECTANGLE):
        """ from a rectangle in bit.sea it return the name
            of subbasin.  ex cross_Med_basins in home"""
        if RECTANGLE.cross(basV2.eas3):
           LIST_REGION=['lev1','lev2','lev3','lev4','aeg']
           if RECTANGLE.cross(basV2.lev1):
              return(basV2.lev1.name, basV2.lev1.borders, )
           elif RECTANGLE.cross(basV2.lev2):
              return(basV2.lev2.name, basV2.lev2.borders)
           elif RECTANGLE.cross(basV2.lev3):
              return(basV2.lev3.name, basV2.lev3.borders)
           elif RECTANGLE.cross(basV2.lev4):
              return(basV2.lev4.name, basV2.lev4.borders)
           elif RECTANGLE.cross(basV2.aeg):
              return(basV2.aeg.name, basV2.aeg.borders)
        elif  RECTANGLE.cross(basV2.wes3):
            LIST_REGION=['alb','nwm','tyr1','tyr2','swm1','swm2']
            if RECTANGLE.cross(basV2.alb):
               return(basV2.alb.name, basV2.alb.borders)
            elif RECTANGLE.cross(basV2.nwm):
               return(basV2.nwm.name, basV2.nwm.borders)
            elif RECTANGLE.cross(basV2.tyr1):
               return(basV2.tyr1.name, basV2.tyr1.borders)
            elif RECTANGLE.cross(basV2.tyr2):
               return(basV2.tyr2.name, basV2.tyr2.borders)
            elif RECTANGLE.cross(basV2.swm1):
               return(basV2.swm1.name, basV2.swm1.borders)
            elif RECTANGLE.cross(basV2.swm2):
               return(basV2.swm2.name, basV2.swm2.borders)
        elif RECTANGLE.cross(basV2.mid3):
            LIST_REGION=['adr1','adr2','ion1','ion2','ion3']
            if RECTANGLE.cross(basV2.adr1):
               return(basV2.adr1.name, basV2.adr1.borders)
            elif RECTANGLE.cross(basV2.adr2):
               return(basV2.adr2.name, basV2.adr2.borders)
            elif RECTANGLE.cross(basV2.ion1):
               return(basV2.ion1.name, basV2.ion1.borders)
            elif RECTANGLE.cross(basV2.ion2):
               return(basV2.ion2.name, basV2.ion2.borders)
            elif RECTANGLE.cross(basV2.ion3):
               return(basV2.ion3.name, basV2.ion3.borders)
        
    def col_to_basin(df,lon_col_name='lon', lat_col_name='lat'):
        df['Basin'] = np.nan
        for III in range(0,len(df)):
           tmp_lat = df.iloc[III,:][lat_col_name]
           tmp_lon = df.iloc[III,:][lon_col_name]
           ARGO       = Rectangle(np.float(tmp_lon ) , np.float( tmp_lon) , np.float(tmp_lat) , np.float(tmp_lat))
           NAME_BASIN , BORDER_BASIN = cross_Med_basins(ARGO)
           df['Basin'].iloc[III] = NAME_BASIN
        return (df)
 
    def West_or_East(namebasin):
        """ dipende da funzione sopra which_Med_basins """
        if namebasin in ['adr1','adr2','ion2','ion3', 'lev1','lev2','lev3','lev4','aeg']:
           VAR = 'East'
        else:
           VAR = 'West'
        return (VAR)

    def Is_in_Med(lat, lon):
      LN_MIN=-6
      LT_MIN=36
      LN_MAX=30
      LT_MAX=46
      return LT_MIN < lat < LT_MAX and LN_MIN < lon < LN_MAX
    
