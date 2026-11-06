"""Compile the canonical Overleaf source and replace the website's CV PDF."""
from pathlib import Path
import argparse
import os
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'cv/latex'
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output', type=Path, default=ROOT/'assets/Kleanthis-Avramidis-CV.pdf')
parser.add_argument('--engine', help='Path or command name for latexmk, pdflatex or tectonic.')
parser.add_argument('--source-dir', type=Path, default=SOURCE,
                    help='Project directory; defaults to the bundled editable CV.')
parser.add_argument('--main-file', default='main.tex', help='Project-relative main TeX file.')
args = parser.parse_args()
source = args.source_dir.resolve()
main = (source / args.main_file).resolve()
if not main.is_relative_to(source) or not main.is_file() or main.suffix != '.tex':
    raise SystemExit('Main file must be an existing .tex file inside the source directory.')
main_argument = str(main.relative_to(source))
requested = args.engine or os.environ.get('CV_TEX_ENGINE')
engine = shutil.which(requested) if requested else next((p for name in ('latexmk', 'pdflatex', 'tectonic') if (p := shutil.which(name))), None)
if engine is None:
    raise SystemExit('Install a TeX distribution or Tectonic, use --engine /path/to/compiler, or compile cv/latex/main.tex in Overleaf. The website uses its prebuilt PDF without a compiler.')
name = Path(engine).name.lower()
with tempfile.TemporaryDirectory(prefix='kleanthis-cv-') as folder:
    driver = None
    output_stem = main.stem
    if 'tectonic' in name:
        command = [engine, '--keep-logs', '--outdir', folder, main_argument]
        # XeTeX cannot address curly apostrophes directly in legacy T1 fonts.
        # Expand the character through LaTeX, without changing the source project.
        source_text = main.read_text()
        if 'fontenc' in source_text and '’' in source_text and 'fontspec' not in source_text:
            driver = '\\catcode"2019=13\n\\def’{\\textquoteright{}}\n\\input{\\detokenize{'+main_argument+'}}\n'
            command[-1] = '-'
            output_stem = 'texput'
        passes = 1
    elif 'latexmk' in name:
        command = [engine, '-pdf', '-interaction=nonstopmode', '-halt-on-error', '-outdir='+folder, main_argument]
        passes = 1
    elif 'pdflatex' in name:
        command = [engine, '-interaction=nonstopmode', '-halt-on-error', '-file-line-error', '-output-directory='+folder, main_argument]
        passes = 2
    else:
        raise SystemExit('Supported engines: latexmk, pdflatex and tectonic.')
    for _ in range(passes):
        # Authentication is only needed for fetching, never for TeX execution.
        environment = os.environ.copy()
        environment.pop('OVERLEAF_GIT_TOKEN', None)
        subprocess.run(command, cwd=source, env=environment, check=True,
                       input=driver, text=True)
    for log in Path(folder).glob('*.log'):
        if 'Missing character:' in log.read_text(errors='replace'):
            raise SystemExit('The compiler reported missing characters; existing website CV was preserved.')
    pdf = Path(folder)/(output_stem+'.pdf')
    if not pdf.is_file() or not pdf.read_bytes().startswith(b'%PDF-'):
        raise SystemExit('Compilation did not produce a PDF; existing website CV was preserved.')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(pdf, args.output)
print(args.output.resolve())
