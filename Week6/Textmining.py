import openai
import pandas as pd
with open('01.txt', 'r', encoding='utf-8') as fh:
    tmp = fh.read()
    itemlist = tmp.split(',')
with open('02.txt', 'r', encoding='utf-8') as fh:
    tmp = fh.read()
    itemlist2 = tmp.split(',')
with open('03.txt', 'r', encoding='utf-8') as fh:
    tmp = fh.read()
    itemlist3 = tmp.split(',')
with open('04.txt', 'r', encoding='utf-8') as fh:
    tmp = fh.read()
    itemlist4 = tmp.split(',')
with open('05.txt', 'r', encoding='utf-8') as fh:
    tmp = fh.read()
    itemlist5 = tmp.split(',')
itemlist = str(itemlist)
itemlist2 = str(itemlist2)
itemlist3 = str(itemlist3)
itemlist4 = str(itemlist4)
itemlist5 = str(itemlist5)
keyfile = open("key.txt", "r")
key = keyfile.readline()
openai.api_key = key
data = [itemlist[0:3200], itemlist[3201:6400], 
        itemlist[6401:9600], itemlist[9601:12800], itemlist[12801:16000]]
data2 = [itemlist[0:3200], itemlist[3201:6400], 
        itemlist[6401:9600], itemlist[9601:12800], itemlist[12801:16000]]
data3 = [itemlist[0:3200], itemlist[3201:6400], 
        itemlist[6401:9600], itemlist[9601:12800], itemlist[12801:16000]]
data4 = [itemlist[0:3200], itemlist[3201:6400], 
        itemlist[6401:9600], itemlist[9601:12800], itemlist[12801:16000]]
data5 = [itemlist[0:3200], itemlist[3201:6400], 
        itemlist[6401:9600], itemlist[9601:12800], itemlist[12801:16000]]
def chatgptfn(sub_list):
    result = ''
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an assistant"},
            {"role": "user", "content": f"{sub_list} :give me a summary"}
        ]
    )
    for choice in response.choices:
        result += choice.message.content
    return result

for i in range(0,5):
    data[i] = chatgptfn(data[i])
for i in range(0,5):
    data2[i] = chatgptfn(data2[i])
for i in range(0,5):
    data3[i] = chatgptfn(data3[i])
for i in range(0,5):
    data4[i] = chatgptfn(data4[i])
for i in range(0,5):
    data5[i] = chatgptfn(data5[i])

all=''
for i in range(0,5):
    all=all+all[i]
all2=''
for i in range(0,5):
    all2=all2+all2[i]
all3=''
for i in range(0,5):
    all3=all3+all3[i]
all4=''
for i in range(0,5):
    all4=all4+all4[i]
all5=''
for i in range(0,5):
    all5=all5+all5[i]
all_plus=[all,all2,all3,all4,all5]
import gensim
from gensim import corpora
from pprint import pprint
# 創建詞袋
texts = [[word for word in document.lower().split()] for document in data]
dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]
# 訓練 LDA 模型
lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, 
                                            num_topics=3, random_state=100, update_every=1, 
                                            chunksize=100, passes=10, alpha='auto', per_word_topics=True)
# 輸出主題模型分析結果
import pyLDAvis.gensim
pyLDAvis.enable_notebook()
vis = pyLDAvis.gensim.prepare(lda_model, corpus, dictionary)
pyLDAvis.display(vis)