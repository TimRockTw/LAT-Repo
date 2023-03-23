import pandas as pd

df_110 = pd.read_csv('110.csv')
df_109 = pd.read_csv('109.csv')
df_108 = pd.read_csv('108.csv')
df_107 = pd.read_csv('107.csv')
df_106 = pd.read_csv('106.csv')
df_105 = pd.read_csv('105.csv')
df_104 = pd.read_csv('104.csv')

list_df=[df_110,df_109,df_108,df_107,df_106,df_105,df_104,0]

for i in range(len(list_df)-1):
    list_df[i]=list_df[i].drop(["學校代碼","學校名稱"], axis=1)
    list_df[i]['year']=110-i

list_all=pd.concat([list_df[0],list_df[1],list_df[2],list_df[3],list_df[4],list_df[5],list_df[6]],axis=0)
res=list_all.groupby('year').sum()
res
res.to_csv('data.csv', index=False)