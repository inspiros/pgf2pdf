import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sn

plt.rcParams.update({
    "font.family": "serif",  # use serif/main font for text elements
    "text.usetex": True,     # use inline math for ticks
    "pgf.rcfonts": False,    # don't setup fonts from rc parameters
})

cm = [
    [13, 1, 1, 0, 2],
    [3, 9, 6, 0, 1],
    [0, 0, 16, 2, 0],
    [0, 0, 0, 13, 0],
    [0, 0, 0, 0, 15],
]

fig, ax = plt.subplots(1, 1, figsize=(5, 4))

df_cm = pd.DataFrame(cm)
sn.heatmap(df_cm, annot=True, annot_kws={'size': 16}, ax=ax)

plt.show()
fig.savefig('example_fig.pgf')
