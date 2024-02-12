#!/bin/bash

INDIR='/g100_scratch/userexternal/camadio0/PPCON/SUPERFLOAT_PPCon_202312/'
ln -s $INDIR ${INDIR}/SUPERFLOAT

export ONLINE_REPO='/g100_scratch/userexternal/camadio0/PPCON/SUPERFLOAT_PPCon_202312/'
export PYTHONPATH='/g100/home/userexternal/camadio0/bit.sea_py3/'

##    1. Check if chlorophyll-a profiles have negative concentrations.
# The program stops when the first negative value is found.
# (glob based not bit.sea)

#python 0_Check_negative_chla.py -i $INDIR -vv CHLA
#python 0_Check_negative_chla.py -i $INDIR -vv CHLA_PPCON


##    2. replacing negative values of chla
# glob based not bit.sea
#python 1_Correct_negative_chla.py -i $INDIR -vv CHLA # --> in this case we dedided to overwrite the input dataset 
#python 1_Correct_negative_chla.py -i $INDIR -vv CHLA_PPCON # --> in this case we dedided to overwrite the input dataset

## 3. run again the check of neg values
#python 0_Check_negative_chla.py -i $INDIR -vv CHLA
#python 0_Check_negative_chla.py -i $INDIR -vv CHLA_PPCON

# copiato un po da /g100/home/userexternal/camadio0/PSEUDORUN_SCRIPTS/SCRIPT_Float_Index
## 4. renaming varname from QC_NITRATE to NITRATE_QC

############## rename e.g. QC_VAR in VAR_QC #################################
#python 2_Check_on_qc_name.py  -i $INDIR -v CHLA
#python 2_Check_on_qc_name.py  -i $INDIR -v NITRATE
#python 2_Check_on_qc_name.py  -i $INDIR -v BBP700

#alternatively we can do same with nco
#for FILE_NC in $INDIR/*/*.nc; do
        #echo $FILE_NC  ;
        #ncrename -v QC_{VARNAME}, {VARNAME}_QC $FILE_NC
#done
############################# END  #############################################


# Update Float_index.txt
cp 1_dump_index.py $INDIR
python ${INDIR}/3_dump_index.py -i $INDIR -o ${INDIR}/Float_Index.txt -t superfloat

echo "Dataset modified"
echo "to analyse dataset go to ANALISI_DATASET directory"
exit 0

# Update Float_index.txt
#export     ONLINE_REPO=/g100_scratch/userexternal/camadio0/PPCON/PROVA/
#export      OPA_VENV_1=/g100_work/OGS21_PRACE_P/COPERNICUS/py_env_3.6.8/
#source $OPA_VENV_1/bin/activate
#python 1_dump_index.py -i $INDIR -o ${INDIR}/Float_Index.txt -t superfloat
