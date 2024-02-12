#!/bin/bash

export ONLINE_REPO='/g100_scratch/userexternal/camadio0/PPCON/SUPERFLOAT_PPCon_202312/'
export PYTHONPATH='/g100/home/userexternal/camadio0/bit.sea_py3/'
INDIR='/g100_scratch/userexternal/camadio0/PPCON/SUPERFLOAT_PPCon_202312/'

##    1. Check if chlorophyll-a profiles have negative concentrations.
# The program stops when the first negative value is found.
# (glob based not bit.sea)

#python Check_negative_chla.py -i $INDIR -vv CHLA
python Check_negative_chla.py -i $INDIR -vv CHLA_PPCON


##    2. replacing negative values of chla
# glob based not bit.sea
#python Correct_negative_chla.py -i $INDIR -vv CHLA # --> in this case we dedided to overwrite the input dataset 
#python Correct_negative_chla.py -i $INDIR -vv CHLA_PPCON # --> in this case we dedided to overwrite the input dataset

## 3. run again the check of neg values
python Check_negative_chla.py -i $INDIR -vv CHLA
python Check_negative_chla.py -i $INDIR -vv CHLA_PPCON
exit 0

# copiato un po da /g100/home/userexternal/camadio0/PSEUDORUN_SCRIPTS/SCRIPT_Float_Index
## 4. renaming varname from QC_NITRATE to NITRATE_QC

VARNAME=CHLA
############## rename e.g. QC_NITRATE in NITRATE_QC #################################
python Controllo_QC_renamed.py -i $INDIR -v $VARNAME 
#for FILE_NC in $INDIR/*/*.nc; do
        #echo $FILE_NC  ;
        #ncrename -v QC_NITRATE,NITRATE_QC $FILE_NC
#done
############################# END  #############################################

exit 0

# Update Float_index.txt
export     ONLINE_REPO=/g100_scratch/userexternal/camadio0/PPCON/PROVA/
export      OPA_VENV_1=/g100_work/OGS21_PRACE_P/COPERNICUS/py_env_3.6.8/
source $OPA_VENV_1/bin/activate
python 1_dump_index.py -i $INDIR -o ${INDIR}/Float_Index.txt -t superfloat

#echo "Dataset modified"
#echo "to analyse dataset go to ANALISI_DATASET directory"


