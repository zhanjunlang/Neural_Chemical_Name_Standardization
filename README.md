# Neural_Chemical_Name_Standardization
Repository for paper "Chemical Names Standardization using Neural Sequence to Sequence Model"

## Requirements
A BPE tokenizer from https://github.com/rsennrich/subword-nmt<br>
OpenNMT-py http://opennmt.net/OpenNMT-py/index.html<br>
Python version: 2.7.12 <br>
torch.\__version__ = 1.0.0 <br>
torchtext.\__version__ = 0.4.0 <br>
onmt.\__version__ = 0.7.0 <br>

## How to run
Firstly, you need to put the non-systematic names into a text file, one name per line.<br><br>
Next, you need to do the BPE tokenization for the non-systematic names:<br>
<br>
`subword-nmt apply-bpe -c bpe5000 <your_name_files> output.txt`<br><br>
Finally, put the `output.txt` into the OpenNMT data folder. Run the seq2seq model and the output will be in `pred.txt`.<br><br>
`CUDA_VISIBLE_DEVICES=0 python translate.py -model chemModel_step_100000.pt -src data/output.txt -output pred.txt -replace_unk -verbose`
