import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import io
import zipfile
from datetime import datetime
###
def main():
	st.set_page_config(
		page_title="応力緩和処理サイト",
		layout="wide"
			)
	st.title('データ選択')

	if 'cut_df' not in st.session_state:
		st.write('データはまだ選択されていません')
	else:
		st.write('現時点でのデータ形式は以下です')
		st.dataframe(st.session_state.cut_df)

		make_graph(st.session_state.cut_df)
	
	if st.button("これで良ければクリック"):
		st.success('このページは終了')

	return

# グラフ生成関数
def create_plot(cond):
	fig, ax = plt.subplots()
	#
	ax.plot(cond['x'], cond['y'])
	ax.set_title(cond['title'])
	ax.set_xlabel(cond['x_label'])
	ax.set_ylabel(cond['y_label'])
	ax.set_xscale(cond['x_scale'])
	ax.set_yscale(cond['y_scale'])
	#
	fig.tight_layout()
	return fig

# ZIP作成関数
def create_zip(figs):
	# CSV出力
	csv_buffer = io.StringIO()
	st.session_state.cut_df.to_csv(csv_buffer, index=False)
	csv_buffer.seek(0)
	#
	zip_buffer = io.BytesIO()
	with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
		for i, fig in enumerate(figs, start=1):
			img_buffer = io.BytesIO()
			fig.savefig(img_buffer, format="png")
			img_buffer.seek(0)
			zip_file.writestr(f"graph_{i}.png", img_buffer.read())
		zip_file.writestr("table.csv", csv_buffer.getvalue())
	zip_buffer.seek(0)
	return zip_buffer

def make_graph(df):
	cond_1 = {
		"title": "G(t)",
		"x": df['Mod. Time'][1:].to_numpy(),
		"y": df['G(t)'][1:].to_numpy(),
		"x_label": "Time",
		"y_label": "G(t)",
		"x_scale": "log",
		"y_scale": "log"
	}
	cond_2 = {
		"title": "Norm. G(t)",
		"x": df['Mod. Time'][1:].to_numpy(),
		"y": df['Norm. G(t)'][1:].to_numpy(),
		"x_label": "Time",
		"y_label": "Norm. G(t)",
		"x_scale": "log",
		"y_scale": "log"
	}
	# グラフ作成
	figs = [
		create_plot(cond_1),
		create_plot(cond_2)
	]

	# 表示
	col1, col2 = st.columns(2)
	for i, fig in enumerate(figs):
		with [col1, col2][i]:
			st.pyplot(fig)
	#
	zip_data = create_zip(figs)

	# ダウンロードボタン
	st.download_button(
		label="📦 ZIPで一括ダウンロード",
		data=zip_data,
		file_name=f"graphs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
		mime="application/zip"
	)
	return

###
if __name__ == "__main__":
	main()