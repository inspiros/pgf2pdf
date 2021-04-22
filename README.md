# PGF to PDF converter

## Why?
- No more blurry images.
- Native text typeset.
- Beautiful plots (*depends*).

## How?
### 1. Plot with `matplotlib` and save as `.pgf` format

Python's `matplotlib` provides ease integration with LaTeX. Try this simple python file `example_fig.py` that saves the
figure in `.pgf` format for importing in LaTeX.

```python
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sn

# Optional
plt.rcParams.update({
    "font.family": "serif",  # use serif/main font for text elements
    "text.usetex": True,  # use inline math for ticks
    "pgf.rcfonts": False,  # don't setup fonts from rc parameters
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
```

In addition, you can configure `pgf`'s preamble to define any macros that you have implemented in your LaTeX document
and that you wish to use in your plots.

```python
plt.rcParams.update({
    "font.family": "serif",  # use serif/main font for text elements
    "text.usetex": True,  # use inline math for ticks
    "pgf.rcfonts": False,  # don't setup fonts from rc parameters
    "pgf.preamble": "\n".join([
        r"\usepackage{url}",  # load additional packages
        r"\usepackage{unicode-math}",  # unicode math setup
        r"\setmainfont{DejaVu Serif}",  # serif font via preamble
    ])
})
```

Ref: https://matplotlib.org/stable/gallery/userdemo/pgf_preamble_sgskip.html

### 2. Load `.pgf` file in LaTeX

#### 2.1. Directly import `.pgf` files

The generated `.pgf` file consists of `pgfplots`'s code, which will direct LaTeX what to render. Try to compile the
following `.tex` file (`example.tex`):

```latex
\documentclass{report}
\usepackage{pgf}

\begin{document}
    This is a minimal working example.

    \begin{figure}[htbp]
        \centering
        \resizebox{.8\linewidth}{!}{\input{example.pgf}}
        \caption{Plot imported from \emph{matplotlib}.}
    \end{figure}
\end{document}
```

#### 2.2. Compile `.pgf` to `.pdf` first before loading in LaTeX

The method in 2. works like a charm, but not until you get main_memory overflow because of sheer number of
visualizations combined with figure's complexity. Hours of searching how to increase main_memory or enable
externalization gives you brain trauma.

This simple script `pgf2pdf.py` converts them to minimal `.pdf` files first, so that you can import later without extra
compilation.

##### 2.2.1. Requirements

*(to be decided)*

- python3
- pdflatex
- latexmk

On Windows, I recommend installing latest version of [TeXLive](https://www.tug.org/texlive/).

##### 2.2.2. Usage

*(to be decided)*

For now, run help first:

```terminal
python pgf2pdf.py --help
```

Without any configuration, try this simple usecase. This command will convert `example_fig.pgf` to `example_fig.pdf`:

```terminal
python pgf2pdf.py example_fig.pgf
```

##### 2.2.3.

Simply import it as an image.

```latex
\begin{figure}[htbp]
    \includegraphics{example_fig.pdf}
\end{figure}
```

## Note

![Picasso](https://www.biography.com/.image/ar_1:1%2Cc_fill%2Ccs_srgb%2Cg_face%2Cq_auto:good%2Cw_300/MTY2NTIzNTAyNjgwMDg5ODQy/pablo-picasso-at-his-home-in-cannes-circa-1960-photo-by-popperfoto_getty-images.jpg)  
*Don't fail me!*
