#!/bin/bash

# Copy dataset vXc into my scratch
# Input arguments to be inserted within the script
INDIR='/g100_scratch/userexternal/camadio0/PPCON/SUPERFLOAT_PPCon_202312/'
DATE_start='20190101'
DATE_end='20200101'
OUTDIR='/g100_scratch/userexternal/camadio0/PPCON/SUPERFLOAT_PPCon_202312_yr2019/'

export ONLINE_REPO=$INDIR
export PYTHONPATH='/g100/home/userexternal/camadio0/bit.sea_py3/'

#  make a copy of the dataset es V9C_GB into my scratch for the date range datastart to dataend
python 0_copy_subset_superfloat.py -i $INDIR -o $OUTDIR -s $DATE_start -e $DATE_end

# create float index
cp 1_dump_index.py $OUTDIR
python ${OUTDIR}/1_dump_index.py -i $OUTDIR -o ${OUTDIR}/Float_Index.txt -t superfloat

ln -s $OUTDIR ${OUTDIR}/SUPERFLOAT
export ONLINE_REPO=$OUTDIR
echo "exported dataset:"
echo $OUTDIR
python 2_Table_of_avail_floats.py -i $INDIR -o $OUTDIR -s $DATE_start -e $DATE_end

exit 0

# veccio scriot t cancel

# gurado quanti float ci sono per vars e creo una tabella 
# as in https://docs.google.com/presentation/d/1BAUIWEUpthU3b0uCtYCbQ3qSrr2ZHpPxVWET94d8cpY/edit#slide=id.gffe6e32a58_0_0
python 2_Table_of_avail_floats.py


# in 'SUPERFLOAT_CANYON' in scratch ci sono due dataset:
# 1. SUPERFLOAT_CANYON_20220721_SMOOTHED_bl
# 2. SUPERFLOAT_CANYON_20220721_SMOOTH_CALIBR
# I floats con var NITRATE E NITRATE_QC = -9999 vengono copiati nel dataset di output
# e.g. INPUTDIR  = BASEDIR + 'SUPERFLOAT_CANYON/SUPERFLOAT_CANYON_20220721_SMOOTHED_bl/'
#      OUTDIR    = BASEDIR + 'SUPERFLOAT_2017_2019_V9C/'

# e.g. INPUTDIR  = BASEDIR + 'SUPERFLOAT_CANYON/SUPERFLOAT_CANYON_20220721_SMOOTH_CALIBR/'
#      OUTDIR    = BASEDIR + 'SUPERFLOAT_2017_2019_V9C_QUALCOSA/' 

# prima faccio il check se sono vere le condizioni sopra
python 3_dump_pseudo_obs.py

# RICREO IL  float index
python 1_dump_index.py -i $OUTDIR -o ${OUTDIR}/Float_Index.txt -t superfloat

# vedo se ho fatto bene il copia incolla della pseudovar in var con qc -9999
python 4_check_pseudo_dump.py

export ONLINE_REPO='/g100_scratch/userexternal/camadio0/SUPERFLOAT_2017_2019_V9C/'
python 2_Table_of_avail_floats.py

# rinomino il Dataset di output
mv /g100_scratch/userexternal/camadio0/SUPERFLOAT_2017_2019_V9C/ /g100_scratch/userexternal/camadio0/SUPERFLOAT_2017_2019_V9C_SMOOTHED_bl/
