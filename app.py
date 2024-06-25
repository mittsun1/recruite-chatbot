import streamlit as st
import os
from openai import OpenAI
import gspread
import pandas as pd

MODEL = os.environ.get("MODEL")


# Function to convert list of lists to CSV formatted text
def convert_to_csv(data):
    formatted_text = ""
    for row in data:
        formatted_text += ",".join(row) + "\n"
    return formatted_text

def generate_answer(user_question,prompt):
  response = client.chat.completions.create(
      model = MODEL,
      messages=[
          {"role":"system","content":prompt},
          {"role":"user","content":user_question},
          ],
      max_tokens=1000,
      temperature = 0.2,
      stop = None
  )
  return response.choices[0].message.content

gc = gspread.service_account(filename='chatbot-427023-df55912e42b8.json')
sh = gc.open("sample_sheet_2")

worksheet01 = sh.worksheet('employmentAgency')
worksheet02 = sh.worksheet('progressionOfRecruit')

list_of_agent = worksheet01.get_all_values()
list_of_recruit = worksheet02.get_all_values()

# Convert the recruitment data to CSV text
recruit_data = convert_to_csv(list_of_recruit)
agent_data = convert_to_csv(list_of_agent)

client = OpenAI(api_key = os.environ.get("OPENAI_API_KEY"))

#アプリケーション
st.title("25卒版_採用進捗チャットBot")
st.write("SFIDA Xの採用に関する進捗を確認できます")

df = pd.DataFrame(list_of_recruit)
st.dataframe(df[[0,1,3,5,6,7,8]], use_container_width=True)

user_question = st.text_area("ここに質問を投げかけてください")
if user_question:
   st.write(f"あなた：{user_question}")
   prompt = "あなたは弊社の採用アシスタントです。あなたの回答は以下の情報に準拠するものでなくてはならない。それ以外は答えないで。/n文章は人が見やすいように体裁を意識してほしい/n #拠点ごと・全国の採用進捗：全体的な採用の動向はこちらで把握して/n" + recruit_data + "#契約している人材紹介会社の進捗：現在契約状態の人材紹介についてはこちらで把握して/n" + agent_data
   st.write(generate_answer(user_question,prompt))
   st.write("追加の質問はできませんが、別の質問をすることができます！")