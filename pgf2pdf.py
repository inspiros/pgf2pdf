import argparse
import os
import tempfile

TEMPLATE = r"""
\documentclass[pgfplots]{standalone}

\usepackage{pgfplots}

\begin{document}
\input{FILENAME}
\end{document}
"""

TEX_BUILD_COMMAND = 'pdflatex -output-directory="{OUTPUT_DIR}" {TEXNAME}'
TEX_CLEAN_COMMAND = 'latexmk -c -output-directory="{OUTPUT_DIR}" {TEXNAME}'


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('--ext', nargs='*', default=['pgf'])
    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    input_files = []
    if os.path.isdir(args.input):
        for root, dirs, files in os.walk(args.input):
            for f in files:
                if os.path.splitext(f)[1][1:] in args.ext:
                    input_files.append(os.path.join(root, f))
    else:
        assert os.path.splitext(args.input)[1][1:] in args.ext, f"Input file not match the extension {args.ext}"
        input_files = [args.input]
    input_files = list(map(lambda _: _.replace(os.sep, '/'), input_files))

    # process
    for input_file in input_files:
        tex_file = os.path.join(tempfile.gettempdir(), os.path.basename(os.path.splitext(input_file)[0]) + '.tex')
        output_file_prefix = os.path.splitext(input_file)[0]
        try:
            tex = TEMPLATE.replace('FILENAME', input_file)
            with open(tex_file, 'w') as f:
                f.write(tex)
            os.system(TEX_BUILD_COMMAND.format(OUTPUT_DIR=os.path.dirname(output_file_prefix), TEXNAME=tex_file))
            os.system(TEX_CLEAN_COMMAND.format(OUTPUT_DIR=os.path.dirname(output_file_prefix), TEXNAME=tex_file))
            os.remove(tex_file)
        except Exception as e:
            os.remove(tex_file)
            raise e


if __name__ == '__main__':
    main()