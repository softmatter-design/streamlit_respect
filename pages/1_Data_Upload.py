import streamlit as st
import pandas as pd

###
### Main ###
def main():
	st.set_page_config(
		page_title="応力緩和処理サイト",
		layout="wide"
			)
	st.title('アップロードするファイルを選択')
	#
	if 'load_df' in st.session_state:
		st.write(f'Selected File = {st.session_state.filename}')
	#
	read_file()
	#
	if st.button("これで良ければクリック"):
		st.success('このページは終了')
	
	return

def read_file():
	# 初期値
	r_header = '読む'
	r_sep = 'タブ'
	r_encode = 'utf-8'
	#
	option = st.checkbox('オプションを設定しますか？')
	if option:
		r_header = st.radio('ヘッダー行は読みますか？', ['読む', '読まない'])
		r_sep = st.radio('セパレタを指定しますか？', ['スペース','カンマ', 'タブ'])
		r_encode = st.radio('エンコードを指定しますか？', ['utf-8','cp932', 'shift-jis'])
	#
	selected_file = st.file_uploader("データファイルをアップロードしてください", type=["txt", "dat", "csv", "xls", "xlsx"])
	#
	if selected_file is not None:
		st.session_state.filename = selected_file.name
		file_type = selected_file.name.split(".")[-1].lower()
		try:
			if file_type == "csv":
				if r_header == '読まない':
					load_df = pd.read_csv(selected_file, header=None, encoding=r_encode)
				else:
					load_df = pd.read_csv(selected_file, encoding=r_encode)
			elif file_type in ["dat", "txt"]:
				if r_sep == 'スペース':
					load_df = pd.read_table(selected_file, header=None, encoding=r_encode, dtype=float) 
				elif r_sep == 'カンマ':
					load_df = pd.read_table(selected_file, header=None, encoding=r_encode, sep=",")
				elif r_sep == 'タブ':
					load_df = pd.read_table(selected_file, header=None, encoding=r_encode, sep="\t")

			elif file_type in ["xlsx", "xls"]:
				if r_header == '読む':
					load_df = pd.read_excel(selected_file) 
				else:
					load_df = pd.read_excel(selected_file, header=None) 
			else:
				st.error("対応していないファイル形式です。")
				st.stop()
		except Exception as e:
			st.error(f"ファイルの読み込みに失敗しました: {e}")
			st.stop()
		#
		show_data(load_df)

		check_col(load_df)

	return

def show_data(load_df):
	if not load_df.empty:
		load_df = convert_to_number(load_df)
		#
		st.success("データプレビュー（数値データ以外を消去済み）")
		st.write(f'データ数: {len(load_df)}行')
		st.dataframe(load_df)
		st.session_state['load_df'] = load_df
	return

def convert_to_number(load_df):
	for col in load_df:
		# 文字列化
		series_str = load_df[col].astype(str)
		# 数字・小数点・マイナス以外を削除
		series_str = series_str.str.replace(r"[^0-9.-]", "", regex=True)
		# 空文字は NaN に
		series_str = series_str.replace("", None)
		# 数値変換（失敗時は NaN）
		load_df[col] = pd.to_numeric(series_str, errors="coerce")
	return load_df

def check_col(load_df):
	if ('時間' in load_df.columns.tolist()) and ('緩和弾性率' in load_df.columns.tolist()):
		sel_df = load_df[['時間', '緩和弾性率']]
		sel_df.columns = ['Time', 'G(t)']
		st.session_state['sel_df'] = sel_df
		return
	else:
		list_col=[]
		for i in range(len(load_df.columns)):
			list_col.append('col_'+str(i))
		load_df.columns = list_col		
		st.session_state['sel_df'] = pd.DataFrame()
	return

###
if __name__ == "__main__":
	main()