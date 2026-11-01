#!/usr/bin/env python3
"""Make the L08 'expected' and 'recorded' files (no Docker needed):

  python3 -I assets/terminal/expected_outputs.py <L08_llm_finetuning.ipynb> videos/ac215-l08-llm-finetuning

Writes
  assets/source/colab/cell-NN.py|.md   every non-empty cell of the course Colab "Tutorial - Finetuning with QLoRA",
                                       source unchanged; NN = the cell's 0-based index in the .ipynb (digest.md's
                                       "nb cell N"). One change: cell-00.redacted.md (the title cell) has the
                                       instructor's full name replaced by the chip text <instructor>.
  assets/terminal/expected/colab-cNN-<what>.txt   "recorded": the notebook's stored outputs (an A100 run)
  assets/terminal/expected/readme-<what>.txt      "expected": outputs and texts the README documents
The first line of every expected/ file says exactly where it comes from. Names are masked in expected/ files (the
series rule for L08): the instructor's name (full or first) -> <instructor>, the uploader's Hugging Face account
-> <hf-user>. ANSI colour codes are removed; progress bars keep their final state.
"""
import html
import json
import os
import re
import sys

NB_URL = 'https://colab.research.google.com/drive/1oX3ADMHphW2v7mwV7zkEWD5oYewJZEAC'
REPO = 'dlops-io/llm-finetuning @ 44ef6f0 (main)'
INSTR = '‹instructor›'      # the grey chip text the scenes show
HFUSER = '‹hf-user›'
ANSI = re.compile(r'\x1b\[[0-9;?]*[A-Za-z]')

nb_path, video = sys.argv[1], sys.argv[2]
nb = json.load(open(nb_path))
cells = nb['cells']
src_dir = os.path.join(video, 'assets', 'source', 'colab')
exp_dir = os.path.join(video, 'assets', 'terminal', 'expected')
os.makedirs(src_dir, exist_ok=True)
os.makedirs(exp_dir, exist_ok=True)


# the uploader's Hugging Face account, as nb cell 88's stored output prints it
HF_NAMES = set()
for c in cells:
    for o in c.get('outputs', []):
        m = re.search(r'Detected Hugging Face username: (\S+)', ''.join(o.get('text', '')))
        if m:
            HF_NAMES.add(m.group(1))


def mask(text):
    text = re.sub(r'Pavlos\s+P[a-z]+', INSTR, text)   # first name + surname
    text = text.replace('Pavlos', INSTR)
    for name in HF_NAMES:
        text = re.sub(r'\b%s\b' % re.escape(name), HFUSER, text)
    return text


# ---- source/colab: every non-empty cell, unchanged (cell 0 redacted) ----
for i, c in enumerate(cells):
    s = ''.join(c['source'])
    if not s.strip():
        continue
    ext = '.py' if c['cell_type'] == 'code' else '.md'
    if i == 0:
        s2 = re.sub(r'Pavlos\s+P[a-z]+', INSTR, s)
        assert s2 != s
        open(os.path.join(src_dir, 'cell-00.redacted' + ext), 'w').write(s2)
        continue
    open(os.path.join(src_dir, 'cell-%02d%s' % (i, ext)), 'w').write(s)


# ---- recorded: stored outputs ----
def progress_final(t):
    """carriage-return overwrites: keep what the terminal finally shows on each line"""
    out = []
    for ln in t.split('\n'):
        if '\r' in ln:
            parts = [p for p in ln.split('\r') if p.strip()]
            ln = parts[-1] if parts else ''
        out.append(ln.rstrip())
    return '\n'.join(out)


def html_text(h):
    h = re.sub(r'<progress[^>]*></progress>', '', h)
    h = re.sub(r'</t[dh]>\s*<t[dh][^>]*>', '\t', h)
    h = re.sub(r'<br\s*/?>|</tr>|</div>|</p>', '\n', h)
    h = re.sub(r'<[^>]+>', '', h)
    h = html.unescape(h)
    return '\n'.join(ln.strip() for ln in h.split('\n') if ln.strip())


def outputs_text(i):
    parts = []
    for o in cells[i].get('outputs', []):
        if o['output_type'] == 'stream':
            parts.append(''.join(o['text']))
        elif o['output_type'] in ('execute_result', 'display_data'):
            d = o.get('data', {})
            if 'text/html' in d and 'IPython.core.display.HTML' in ''.join(d.get('text/plain', '')):
                parts.append(html_text(''.join(d['text/html'])) + '\n')
            elif 'application/vnd.jupyter.widget-view+json' in d:
                # a progress widget: Colab shows the finished bar; only its start state is stored
                parts.append('[progress widget] ' + ''.join(d.get('text/plain', '')).strip() + '\n')
            elif 'image/png' in d:
                parts.append('[image: ' + ''.join(d.get('text/plain', '')).strip() + ']\n')
            else:
                parts.append(''.join(d.get('text/plain', '')) + '\n')
        elif o['output_type'] == 'error':
            parts.append('\n'.join(o.get('traceback', [])) + '\n')
    t = ANSI.sub('', ''.join(parts))
    return mask(progress_final(t)).rstrip() + '\n'


RECORDED = {
    8: 'install', 10: 'hf-token', 12: 'versions', 14: 'drive-mount', 16: 'hf-download',
    21: 'opt-350m-4bit-model', 25: 'tokenize', 27: 'opt-generate', 31: 'gpu-bf16-check', 36: 'load-qwen-4bit',
    38: 'num-params', 42: 'qwen-config', 45: 'baseline-generate', 48: 'trainable-before', 51: 'gdown-dataset',
    53: 'sample-1000', 55: 'extract-qa', 59: 'chat-template-map', 61: 'train-test-split', 63: 'one-example',
    64: 'token-histogram', 72: 'sfttrainer-trainable', 75: 'train', 77: 'tensorboard', 80: 'eval-loss-perplexity',
    82: 'base-vs-finetuned', 84: 'save-adapters', 86: 'merge-and-save', 88: 'push-to-hub',
}
for i, what in RECORDED.items():
    c = cells[i]
    head = ('# recorded: Colab "Tutorial - Finetuning with QLoRA" (%s), nb cell %d (execution count %s): the '
            'notebook\'s stored output from the authors\' run on an A100 (metadata.colab.gpuType); not run here. '
            'Names masked (%s, %s).\n') % (NB_URL, i, c.get('execution_count'), INSTR, HFUSER)
    open(os.path.join(exp_dir, 'colab-c%02d-%s.txt' % (i, what)), 'w').write(
        head + '$ ' + mask(''.join(c['source'])).replace('\n', '\n  ') + '\n' + outputs_text(i))


# ---- expected: what the README documents ----
readme = open(os.path.join(video, 'assets', 'source', 'README.md')).read().split('\n')


def readme_block(name, a, b, what):
    head = ('# expected: README.md:%d-%d of %s: %s. Documented by the tutorial, not produced here. '
            'Names masked (%s).\n') % (a, b, REPO, what, INSTR)
    open(os.path.join(exp_dir, 'readme-%s.txt' % name), 'w').write(head + mask('\n'.join(readme[a - 1:b])) + '\n')


readme_block('system-prompt-excerpt', 114, 135, 'the README\'s excerpt of the --generate system prompt (older than '
             'dataset-creator/cli.py:83-101, see digest E4)')
readme_block('input-prompt', 143, 145, 'the --generate input prompt (word for word dataset-creator/cli.py:169)')
readme_block('generate-sample-qa', 163, 175, 'sample results of `python cli.py --generate` ("Here are some sample '
             'results from when you run the --generate option")')
readme_block('prepare-gemini-format', 191, 212, 'the Gemini fine-tuning data format that --prepare writes (one '
             'line per example in train.jsonl/test.jsonl, pretty-printed here)')
readme_block('cost-table', 267, 278, 'Cost of Fine-tuning (Gemini 1.5 Flash pricing, 3 epochs; the code now tunes '
             'gemini-3.1-flash-lite for 1 epoch, see digest E6)')
readme_block('chat-example', 288, 301, 'what `python cli.py --chat` does, and its example (older query "How is '
             'cheese made?"; the code asks "How is cheese made in Greece? Answer pavlos style?", '
             'gemini-finetuner/cli.py:109)')
print('wrote', len(RECORDED), 'recorded and 6 README files')
