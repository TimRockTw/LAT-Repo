import pandas as pd

df_110 = pd.read_csv('110.csv')
df_109 = pd.read_csv('109.csv')
df_108 = pd.read_csv('108.csv')
df_107 = pd.read_csv('107.csv')
df_106 = pd.read_csv('106.csv')
df_105 = pd.read_csv('105.csv')
df_104 = pd.read_csv('104.csv')

df_110

new_df_110 = df_110.drop(["學校代碼","學校名稱"], axis=1)
new_df_109 = df_109.drop(["學校代碼","學校名稱"], axis=1)
new_df_108 = df_108.drop(["學校代碼","學校名稱"], axis=1)
new_df_107 = df_107.drop(["學校代碼","學校名稱"], axis=1)
new_df_106 = df_106.drop(["學校代碼","學校名稱"], axis=1)
new_df_105 = df_105.drop(["學校代碼","學校名稱"], axis=1)
new_df_104 = df_104.drop(["學校代碼","學校名稱"], axis=1)

df_110