import argparse
import os
import tempfile

from collections.abc import Collection
from typing import List, Union, Optional

__all__ = ['pgf2pdf']

TEMPLATE = r"""
\documentclass[pgfplots]{standalone}

\usepackage{pgfplots}

\begin{document}
\input{FILENAME}
\end{document}
"""

TEX_BUILD_COMMAND = '{EXECUTABLE} -output-directory="{OUTPUT_DIR}" {TEXNAME}'
TEX_CLEAN_COMMAND = '{EXECUTABLE} -c -output-directory="{OUTPUT_DIR}" {TEXNAME}'


def _check_ext(input_file, exts):
    input_basename, input_ext = os.path.splitext(input_file)
    return input_ext in exts or input_ext[1:] in exts or len(exts) == 0 or exts is None


def pgf2pdf(input: str,
            output_dir: Optional[str] = None,
            engine: str = 'pdflatex',
            latexmk: Optional[str] = 'latexmk',
            exts: Union[str, List[str]] = ('pgf',),
            clean_exts: Union[str, List[str]] = ('aux', 'idx', 'ind',
                                                 'lof', 'lot', 'out',
                                                 'toc', 'acn', 'acr',
                                                 'alg', 'glg', 'glo',
                                                 'gls', 'ist', 'tex')
            ) -> None:
    """
    Convert PGF file to PDF.

    Args:
        input: Path to input file or directory (recursive).
        output_dir: Path to output directory. Defaults to be same directory as input.
        engine: Path to LaTeX engine executable, which is REQUIRED for building pdf file.
            Defaults to 'pdflatex'.
        latexmk: Path to LaTeXmk executable, which is optional. Defaults to 'latexmk'.
        exts: Input extension filters. Defaults to ['pgf'].
        clean_exts: Generated extensions to be cleaned. Defaults are ['aux', 'idx', 'ind', 'lof',
         'lot', 'out', 'toc', 'acn', 'acr', 'alg', 'glg', 'glo', 'gls', 'ist', 'tex'].
    """
    # sanity check
    if not os.path.exists(input):
        raise ValueError(f"Unable to locate find file or directory {input}.")
    input = os.path.abspath(input)
    if output_dir is not None:
        output_dir = output_dir
        if not os.path.isdir(output_dir):
            raise ValueError("output_dir must be path to a directory, not a file.")
    else:
        if os.path.isdir(input):
            output_dir = input
        else:
            output_dir = os.path.dirname(input)

    if exts is None:
        exts = []
    elif not isinstance(exts, Collection):
        exts = [exts]

    if clean_exts is None:
        clean_exts = []
    elif not isinstance(clean_exts, Collection):
        clean_exts = [clean_exts]

    # pre-process
    input_files = []
    if os.path.isdir(input):
        input_root = input
        for root, dirs, files in os.walk(input):
            for f in files:
                if _check_ext(f, exts):
                    input_files.append(os.path.join(root, f))
    else:
        if not _check_ext(input, exts):
            raise RuntimeError(f"Input file not match the extension {exts}.")
        input_root = os.path.dirname(input)
        input_files = [input]
    input_files = list(map(lambda _: _.replace(os.sep, '/'), input_files))

    # run
    for input_file in input_files:
        tex_file = os.path.join(tempfile.gettempdir(), os.path.basename(os.path.splitext(input_file)[0]) + '.tex')
        sub_output_dir = os.path.join(output_dir, os.path.dirname(input_file)[len(input_root):])
        tex_file = tex_file.replace(os.sep, '/')
        sub_output_dir = sub_output_dir.replace(os.sep, '/')
        os.makedirs(sub_output_dir, exist_ok=True)

        tex = TEMPLATE.replace('FILENAME', input_file)
        # build pdf
        try:
            with open(tex_file, 'w') as f:
                f.write(tex)
            os.system(TEX_BUILD_COMMAND.format(EXECUTABLE=engine,
                                               OUTPUT_DIR=sub_output_dir,
                                               TEXNAME=tex_file))
        except Exception as e:
            os.remove(tex_file)
            raise e

        # clean generated files
        try:
            os.system(TEX_CLEAN_COMMAND.format(EXECUTABLE=latexmk,
                                               OUTPUT_DIR=sub_output_dir,
                                               TEXNAME=tex_file))
            os.remove(tex_file)
        except Exception:
            generated_prefix = os.path.splitext(tex_file)[0]
            for clean_ext in clean_exts:
                if not clean_ext.startswith('.'):
                    clean_ext = '.' + clean_ext
                generated_file = generated_prefix + clean_ext
                if os.path.exists(generated_file):
                    os.remove(generated_file)


def parse_args():
    parser = argparse.ArgumentParser('PGF to PDF compiler')
    parser.add_argument('input',
                        help='Input file or directory')
    parser.add_argument('output_dir', nargs='?', default=None,
                        help='Output directory.')
    parser.add_argument('--engine', default='pdflatex',
                        help='Path to LaTeX engine executable.')
    parser.add_argument('--latexmk', default='latexmk',
                        help='Path to LaTeXmk executable.')
    parser.add_argument('--exts', nargs='*', default=['pgf'],
                        help='Input extension filters.')
    parser.add_argument('--clean_exts', nargs='*', default=['aux', 'idx', 'ind',
                                                            'lof', 'lot', 'out',
                                                            'toc', 'acn', 'acr',
                                                            'alg', 'glg', 'glo',
                                                            'gls', 'ist', 'tex'],
                        help='Generated extension filters to be cleaned.')
    args = parser.parse_args()
    return args


def main():
    """Console entry point.
    """
    args = parse_args()
    pgf2pdf(**vars(args))


if __name__ == '__main__':
    main()
