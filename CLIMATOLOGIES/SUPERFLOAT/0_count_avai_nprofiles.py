import argparse

def argument():
    parser = argparse.ArgumentParser(description = '''
    counts the available BGC-Argo float profiles per basin and plots their monthly distribution.
    ''', formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument(   '--outdir','-o',
                                type = str,
                                required = True,
                                help = 'input dir validation tmp')


    parser.add_argument(   '--variable', '-v',
                                type = str,
                                default = None,
                                required = True,
                                help = '''model variable''')
    return parser.parse_args()


args = argument()

from bitsea.commons.utils import addsep
import numpy as np
import pandas as pd
from bitsea.commons import timerequestors
from bitsea.instruments import superfloat
from bitsea.instruments import superfloat as bio_float
from bitsea.instruments.var_conversions import FLOATVARS
from bitsea.basins import V2 as OGS
from bitsea.basins.basin import ComposedBasin
import sys
import os

OUTDIR      = addsep(args.outdir)
varmod      = args.variable
output_file =  'profili_per_mese_per_bacino.csv'


# INIT
MONTHS = np.arange(1,13)
if OGS.atl in OGS.Pred.basin_list:
  OGS.Pred.basin_list.remove(OGS.atl) # tolgo Atlantic buffer
else: pass

SUBS    = OGS.Pred.basin_list[:]
print()
print('_________________start__________________')


if not os.path.exists(output_file):
    sub_names = [sub.name for sub in SUBS]
    df = pd.DataFrame(index=range(12), columns=sub_names)

    for nMonth in MONTHS[:]:
        print ('_____________ '+ str(nMonth) + ' ____________')
        SUB_COUNT = 0
        for ISUB in SUBS:
            print('_____________ '+ str(ISUB)  +' _____________')
            TI = timerequestors.Clim_month(nMonth)
            #TI = timerequestors.TimeInterval(starttime='20120101', endtime='20240101', dateformat='%Y%m%d')
            Profilelist = superfloat.FloatSelector(FLOATVARS[varmod], TI, ISUB)
            df.at[nMonth-1, ISUB.name] = len(Profilelist)

    df.to_csv(output_file)
else:
    df=pd.read_csv(output_file,index_col=0)
    print('')
    print(f" file already created: {output_file}")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.colors as mcolors
import matplotlib.cm as cm

df_plot = df.fillna(0).astype(int)
df_T = df_plot.T # to plot menths in x ax
month_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

monthly_colors = [
    '#a6cee3', '#1f78b4', '#08519c',     # Winter (shades of blue)
    '#a1d99b', '#41ab5d', '#006d2c',     # Spring (shades of green penna)
    '#fecc5c', '#fd8d3c', '#e31a1c',     # Summer (shades of orange)
    '#dadaeb', '#9e9ac8', '#6a51a3'      # Autumn (shades of purple)
]
#    '#fbb4b9', '#f768a1', '#c51b8a',     # Spring (shades of pink)

# Plot
fig, ax = plt.subplots(figsize=(14, 8))
bottom = np.zeros(len(df_T))

for i, month in enumerate(df_T.columns):
    ax.bar(df_T.index, df_T[month], bottom=bottom, label=month_labels[i], color=monthly_colors[i], alpha=0.5)
    bottom += df_T[month]

ax.set_ylabel('Number of profiles')
ax.set_title('Monthly distribution of profiles per basin (2012-2024-01-01)')
ax.set_xticks(np.arange(len(df_T.index)))
ax.set_xticklabels(df_T.index, rotation=45)

# Legenda mesi (orizzontale)
ax.legend(title='Months', bbox_to_anchor=(0.5, -0.15), loc='upper center', ncol=6)

totals = df_T.sum(axis=1)
for i, total in enumerate(totals):
    ax.text(i, total + 5, str(int(total)), ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.tight_layout()
#plt.show()
plt.savefig('stacked_barplot_N_float_profili.png', dpi=300)

