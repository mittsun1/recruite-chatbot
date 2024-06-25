import os
import gspread
import pandas as pd

gc = gspread.service_account(filename='chatbot-427023-df55912e42b8.json')
sh = gc.open("sample_sheet_2")

worksheet01 = sh.worksheet('employmentAgency')
worksheet02 = sh.worksheet('progressionOfRecruit')

list_of_agent = worksheet01.get_all_values()
list_of_recruit = worksheet02.get_all_values()

df = pd.DataFrame(list_of_recruit)
df = df[[0]]
print(df)