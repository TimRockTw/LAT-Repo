
import pandas as pd
import plotly.express as px

# 從 CSV 檔案中讀取數據
df = pd.read_csv('data.csv')

# 新增一個名為'year'的Series物件，其中包含年份數據
year_data = pd.Series(['104', '105', '106', '107', '108', '109', '110'], name='year') 

print(df)

# 將年份數據和原始DataFrame物件合併為一個新的DataFrame物件
df_new = pd.concat([year_data, df], axis=1)

print(df_new)

# 使用 Plotly 產生視覺化圖表
fig =  px.scatter_matrix(df_new, dimensions=["高級中等學校原住民一年級學生數", "高級中等學校原住民二年級學生數", "高級中等學校原住民三年級學生數", "高級中等學校原住民四年級學生數", "高級中等學校原住民延修生學生數","高級中等學校上學年度原住民畢業生人數"], color="year")
# 顯示圖表
fig.show()