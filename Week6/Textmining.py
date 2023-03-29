import openai
import pandas as pd
with open('01.txt', 'r') as fh:
    tmp = fh.read()
    itemlist = tmp.split(',')
itemlist = str(itemlist)
keyfile = open("key.txt", "r")
key = keyfile.readline()
openai.api_key = key
data = [itemlist[0:3200], itemlist[3201:6400], 
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
print(data[0])
import gensim
from gensim import corpora
from pprint import pprint
# 創建詞袋
data_all=[data[0],data[1],data[2],data[3],data[4]]
data_all_0=" ".join(data_all)
print(data_all_0)
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