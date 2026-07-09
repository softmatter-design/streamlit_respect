import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io
###
def main():
	st.set_page_config(
		page_title="シンプルアプリ",
		layout="wide"
			)
	st.title('データ選択')
	#
	if 'sel_df' not in st.session_state:
		st.write('データはまだ選択されていません')
	else:
		st.write('現時点でのデータ形式は以下です')
		st.dataframe(st.session_state.sel_df)
		cut_rows(st.session_state.sel_df)

	if st.button("これで良ければクリック"):
		st.success('このページは終了')

	return

def cut_rows(df):
	base = st.number_input('測定開始時間の行を入力してください', min_value=0, max_value=100, step=1)
	st.success(f'初期値は{base}行目')
	st.session_state['cut_df'] = show_mod_df(df, base)
	return

def show_mod_df(df, base):
	#
	cut_df = pd.DataFrame.empty
	#
	if base == 0:
		cut_df = df
		init_time = 0
		init_g = df.iloc[0,1]
	elif base > 2:
		init_time = df.iloc[base-1,0]
		init_g = df.iloc[base,1]
		cut_df = df.loc[base:]
	cut_df['Mod. Time']=cut_df['Time']-init_time
	cut_df['Norm. G(t)']=cut_df['G(t)']/init_g
	st.subheader(f"選択した列のデータを{base}行目から表示")
	st.dataframe(cut_df)  
	return cut_df

# def save_csv(df):
# 	csv_data=df.to_csv(index=False)
# 	st.download_button(
# 		label='Download CSV', data=csv_data, file_name='mod_data.csv', mime='text/csv'
# 	)
	
###
if __name__ == "__main__":
	main()