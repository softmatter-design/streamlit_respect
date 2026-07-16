import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pyrespect_time import ReSpect, ReSpectConfig
import io
import zipfile
from datetime import datetime
###
def main():
	st.set_page_config(
		page_title="シンプルアプリ",
		layout="wide"
			)
	st.title('ReSpectでデータ処理')
	#
	if 'cut_df' not in st.session_state:
		st.write('データはまだ選択されていません')
	else:
		st.success('有効なデータフレームが作成されています')
		if st.button('データ処理しますか？'):
			st.success('処理中です')
			run_respect(st.session_state.cut_df)
	return

def run_respect(df):
	time = df['Mod. Time'][0:].to_numpy()
	gt = df['G(t)'][0:].to_numpy()

	# Default settings — fit from a data file
	solver = ReSpect()
	solver.fit(time, gt)  # "Gt.dat" file contains data

	# Access results
	df_gt=pd.DataFrame(np.stack([solver.t,solver.Gt,solver.continuous.G_fit,solver.discrete.G_fit],1))
	df_gt.columns=['Time', 'G(t)', 'Continuous G_fit', 'Discrete G_fit']
	#
	df_cont=pd.DataFrame(np.stack([solver.continuous.s, solver.continuous.H], 1))
	df_cont.columns=['Continuous.s', 'Continuous.H']
	df_disc=pd.DataFrame(np.stack([solver.discrete.tau, solver.discrete.g], 1))
	df_disc.columns=['Discrete.tau', 'Discrete.g'] 
	#
	files = [[df_cont, df_disc], [df_gt]]
	title = ['緩和関数の連続と離散での推定値', '推定値と実測の応力緩和関数との比較']
	#
	cond_1 = {
		"title": r'$g, h(\tau)$',
		"data": [
					[solver.continuous.s,
					np.exp(solver.continuous.H),
					'CRS',
					'none',
					'-'
					],
					[
						solver.discrete.tau,
						solver.discrete.g,
						'DRS',
						's',
						'-'
					]
		],
		"x_label": r'$\tau$',
		"y_label": r'$g, h(\tau)$',
	}
	cond_2 = {
		"title": "G(t)",
		"data": [
					[solver.t,
					solver.Gt,
					'Data',
					'x',
					''
					],
					[
						solver.t,
						solver.continuous.G_fit,
						'continuous fit',
						'none',
						'-'
					],
					[
						solver.t,
						solver.discrete.G_fit,
						'discrete fit',
						'none',
						'--'
					]
		],
		"x_label": r'$t$',
		"y_label": r'$G(t)$',
	}
	# グラフ作成
	figs = [
		plot_base(cond_1),
		plot_base(cond_2)
		# plot_base_2(t, Gt, cont_fit, disc_fit)
	]
	# 表示
	show_columns(files, figs, title)
	#
	zip_data=create_zip(figs, files)
	# ダウンロードボタン
	st.download_button(
		label="📦 ZIPで一括ダウンロード",
		data=zip_data,
		file_name=f"graphs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
		mime="application/zip"
	)

	return

def plot_base(cond):
	# ---- discrete modes overlaid on continuous spectrum ----
	fig, ax = plt.subplots()
	ax.set_title(cond['title'])
	for data in cond['data']:
		ax.loglog(data[0], data[1], label=data[2], marker=data[3], linestyle=data[4])
	ax.set_xlabel(cond['x_label'])
	ax.set_ylabel(cond['y_label'])
	ax.legend()
	fig.tight_layout()
	return fig

def show_columns(files, figs, title):
	for i, fig in enumerate(figs):
		st.write(title[i])
		col1, col2=st.columns(2)
		with col1:
			for file in files[i]:
				st.dataframe(file)
		with col2:
			st.pyplot(fig)
	return

# ZIP作成関数
def create_zip(figs, files):
	zip_buffer = io.BytesIO()
	with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
		# fig 出力
		for i, fig in enumerate(figs):
			img_buffer = io.BytesIO()
			fig.savefig(img_buffer, format="png")
			img_buffer.seek(0)
			zip_file.writestr(f"graph_{i}.png", img_buffer.read())
			# CSV出力
			for j, file in enumerate(files[i]):
				csv_buffer = io.StringIO()
				file.to_csv(csv_buffer, index=False)
				csv_buffer.seek(0)
				zip_file.writestr(f"table_{i}_{j}.csv", csv_buffer.getvalue())
	zip_buffer.seek(0)
	return zip_buffer

###
if __name__ == "__main__":
	main()