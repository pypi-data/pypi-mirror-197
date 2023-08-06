import yake
import datasets
import pandas as pd
import os
from tqdm import tqdm
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-xl")
tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-xl", max_length=1024, truncation=True)



file_list = []

# root_dir = "/home/dingyx/project/SciAssist/data/"
# root_dir = "/home/dingyx/project/SciAssist/data/Task2/From-ScisummNet-2019/"

# for dirpath,dirnames,files in os.walk(root_dir):
#     file_list = dirnames
#     break

root_dir = "/home/dingyx/project/SciAssist/data/"
for dirpath,dirnames,files in os.walk(root_dir):
    file_l = files
    break
file_l.sort()
file_list=[]
for i in file_l:
    if i[-4:]==".txt":
        file_list.append(i)

def keyword_extraction(input_text):
    # with open(os.path.join(root_dir,input_text),"r") as f:
    # # with open(os.path.join(root_dir, input_text, "summary",input_text + ".scisummnet_human.txt"), "r") as f:
    #     input_text = f.readlines()
    #     input_text= " ".join(input_text)
    inputs = tokenizer("What entities does this scientific document talk about?" + input_text + "Entities: ", return_tensors="pt", max_length=1024, truncation=True)
    outputs = model.generate(**inputs)
    keywords_res = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    keywords_res = [ k.strip().split() for k in keywords_res ]
    keywords_res = [ " ".join(k) for k in keywords_res]
    keywords_res = list(set(keywords_res))
    keyword_str = ",".join(keywords_res)
    # print(keyword_str)
    return keyword_str


# In[197]:


# ### Different setting of keyword extraction

# In[841]:

raw_datasets = datasets.load_dataset(
    "allenai/mup",
    cache_dir="/home/dingyx/.cache/sciassist"
)

print("loading finished.")
file_list = raw_datasets["train"]
# file_list = raw_datasets["validation"].select(range(1000))

summ = file_list["summary"]
# scisumm = {"File": file_list}
# print(scisumm["File"])
scisumm = {"title": file_list["paper_name"], "summary":summ, "text":file_list["text"] }
scisumm = pd.DataFrame(scisumm)
tqdm.pandas(desc='progress bar')
scisumm['keyword']=scisumm["summary"].progress_apply(keyword_extraction,args=())
# scisumm['keyword']=scisumm["File"].progress_apply(keyword_extraction,args=())
scisumm.to_csv(os.path.join(root_dir,"train.csv"), index=True)