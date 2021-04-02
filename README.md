## PGF to PDF converter

### Introduction

`matplotlib` can save figures as `.pgf` files for ease intergration within LaTEX.

```python
import matplotlib.pyplot as plt

plt.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
})

# plotting
plt.save('fig.pgf')
```

In `.tex` file:
```latex
\import{fig.pgf}
```

But not until you get main_memory overflow because of sheer number of visualizations combined with figure's complexity.
Hours of searching how to increase main_memory or enable externalization gives you brain trauma.


This simple script converts them to minimal `.pdf` files first, so that you can import later without extra compilation.

```latex
\includegraphics{fig.pdf}
```

### Requirements

*(to be decided)*
- python3
- pdflatex
- latexmk

### Usage

*(to be decided)*

For now:
```terminal
python pgf2pdf.py --help
```
