from keybert import KeyBERT
from flair.embeddings import TransformerDocumentEmbeddings
import pandas as pd
import os

from tqdm import tqdm

file_list = []

root_dir = "/home/dingyx/project/SciAssist/data/Task2/From-ScisummNet-2019/"
for dirpath,dirnames,files in os.walk(root_dir):
    file_list = dirnames
    break


def keyword_extraction(input_text, kw_model, use_maxsum=True, use_mmr=False, ngram=3, topn=10, nr_cand=20, div=0.5):
    with open(os.path.join(root_dir, input_text, "summary",input_text + ".scisummnet_human.txt"), "r") as f:
        input_text = f.readlines()
        input_text= " ".join(input_text)
    if use_maxsum:
        keywords_res = kw_model.extract_keywords(input_text, keyphrase_ngram_range=(1, ngram), stop_words='english',
                                                 top_n=topn, use_maxsum=True, nr_candidates=nr_cand)
    elif use_mmr:
        keywords_res = kw_model.extract_keywords(input_text, keyphrase_ngram_range=(1, ngram), stop_words='english',
                                                 top_n=topn, use_mmr=True, diversity=div)
    keyword_str = "#".join([kw[0] for kw in keywords_res])
    return keyword_str


# In[197]:


# ### Different setting of keyword extraction

# In[841]:


# plm_name: roberta-base, allenai/scibert_scivocab_uncased, allenai/specter
plm_name = "allenai/scibert_scivocab_uncased"
plm = TransformerDocumentEmbeddings(plm_name)
kw_model = KeyBERT(model=plm)

use_maxsum = False
topn = 10
nr_cand = 20
use_mmr = True
ngram = 2
scisumm = {"File":file_list}
scisumm = pd.DataFrame(scisumm)
tqdm.pandas(desc='progress bar')
scisumm['Keyword']=scisumm["File"].progress_apply(keyword_extraction, args=(
                                kw_model, use_maxsum, use_mmr, ngram, topn, nr_cand))

scisumm.to_csv(os.path.join(root_dir,"scisumm_keywords10_mmr_bigram_target.csv"), index=False)