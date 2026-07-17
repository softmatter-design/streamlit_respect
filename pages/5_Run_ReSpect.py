import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pyrespect_time import ReSpect, ReSpectConfig
import io
import zipfile
from datetime import datetime
import os
import tempfile
###
def main():
	st.set_page_config(
		page_title="応力緩和処理サイト",
		layout="wide"
			)
	st.title('ReSpectでデータ処理')
	#
	if 'cut_df' not in st.session_state:
		st.write('データはまだ選択されていません')
	else:
		st.success('有効なデータフレームが作成されています')
		make_config()
	return

def make_config():
	## Default Values ##
	# Continuous spectrum
	ns = 100
	plateau = False
	freq_end = "lenient"
	# Regularization
	lam_min = 1e-10
	lam_max = 1e3
	lam_C = None
	lam_density = 2
	SmFacLam = 0.0
    # Discrete spectrum
	max_num_modes = None
	delta_base_weight_dist = 0.2
	min_tau_spacing = 1.25
    # I/O
	resample = True
	n_resample = 100
	##################
	#
	level = st.radio("データ処理に関するオプションを設定しますか？", ("Default", "Simple", "Detailed"), horizontal=True)
	if level == 'Default':
		if st.button('オプションを設定しないでデータ処理するならクリック', key='respect'):
			config = ReSpectConfig(ns, plateau, freq_end, lam_min, lam_max, lam_C, lam_density, SmFacLam, max_num_modes, delta_base_weight_dist, min_tau_spacing, resample, n_resample)
			with st.spinner('処理中です。しばらくお待ちください…'):
				run_respect(st.session_state.cut_df, config)
	elif level == 'Simple':
		if st.checkbox('全体に関するオプションを設定しますか？', key='whole'):
			ns = st.number_input('入力したデータの間引き後のデータ数', min_value=100, max_value=1000, step=100)
			r_plateau = st.radio("ラバープラトーの有無？", ("No", "Yes"))
			if r_plateau == 'No':
				plateau = False
			else:
				plateau = True
		if st.checkbox('出力に関するオプションを設定しますか？', key='out'):
			out_res = st.radio("出力データの調整の有無？", ("Yes", "No"))
			if out_res == 'No':
				resample = False
			else:
				resample = True
				n_resample = st.number_input('データポイント数', min_value=100, max_value=1000, step=100)
		#
		if st.button('オプション入力を終了してデータ処理しますか？', key='Simple'):
			config = ReSpectConfig(ns, plateau, freq_end, lam_min, lam_max, lam_C, lam_density, SmFacLam, max_num_modes, delta_base_weight_dist, min_tau_spacing, resample, n_resample)
			with st.spinner('処理中です。しばらくお待ちください…'):
				run_respect(st.session_state.cut_df, config)
	else:
		# Continuous spectrum
		if st.checkbox('全体に関するオプションを設定しますか？', key='whole'):
			ns = st.number_input('入力したデータの間引き後のデータ数', min_value=100, max_value=1000, step=100)
			r_plateau = st.radio("ラバープラトーの有無？", ("No", "Yes"))
			if r_plateau == 'No':
				plateau = False
			else:
				plateau = True
			freq_end = st.radio("s軸の終端をどのように設定するのかを選択", ("lenient", "neutral", "strict"), horizontal=True)
		if st.checkbox('「正則化」に関するオプションを設定しますか？', key='cont'):
			sel_lam_min = st.radio(r"s軸の下限のデフォルト値は1e-10ですが、変更しますか？", ("No", "Yes"), horizontal=True)
			if sel_lam_min == 'Yes':
				lam_min = 10.**(st.slider('変更値', -11, -9, -10, 1, key='lam_min'))
			else:
				lam_min = 1e-10
			sel_lam_max = st.radio(r"s軸の上限のデフォルト値は1e3ですが、変更しますか？", ("No", "Yes"), horizontal=True)
			if sel_lam_max == 'Yes':
				lam_max = 10.**(st.slider('変更値', 2, 4, 3, 1, key='lam_max'))
			else:
				lam_max = 1e3
			sel_lam_C = st.radio("正則化パラメタ$\\lambda$のデフォルト値はNoneですが、変更しますか？", ("No", "Yes"), horizontal=True)
			if sel_lam_C == 'Yes':
				lam_C = st.slider('ベイズ最適化でのスムース性の調整', -1., 1., 0., .1, key='lam_C')
			else:
				lam_C = None
			sel_lam_density = st.radio("Lカーブ探索グリッド中の$\\lambda$の密度のデフォルト値は2ですが、変更しますか？", ("No", "Yes"), horizontal=True)
			if sel_lam_density == 'Yes':
				lam_density = st.slider('Lカーブ探索グリッド中の$\\lambda$の密度', 1, 3, 2, 1, key='lam_density')
			else:
				lam_density = 2
			sel_SmFacLam = st.radio("ベイズ最適化でのスムース性の調整のデフォルト値は0.0ですが、変更しますか？", ("No", "Yes"), horizontal=True)
			if sel_SmFacLam == 'Yes':
				SmFacLam = st.slider('ベイズ最適化でのスムース性の調整', -1.0, 1.0, 0.0, 0.1, key='smfaclam')
			else:
				SmFacLam = 0.0
		if st.checkbox('離散処理に関するオプションを設定しますか？', key='disc'):
			sel_max_num_modes = st.radio("一般化マックスウェルモデルのn数のデフォルト値はNoneで制限がありませんが、変更しますか？", ("No", "Yes"), horizontal=True)
			if sel_max_num_modes == 'Yes':
				max_num_modes = st.slider('一般化マックスウェルモデルのn数の調整', 1, 10, 5, 1, key='max_num_modes')
			else:
				max_num_modes = None
			sel_delta_base_weight_dist = st.radio("AIC探索の感度のデフォルト値は0.2ですが、変更しますか？", ("No", "Yes"), horizontal=True)
			if sel_delta_base_weight_dist == 'Yes':
				delta_base_weight_dist = st.slider('AIC探索感度の調整', 0.1, 1., 0.2, .1, key='delta_base_weight_dist')
			else:
				delta_base_weight_dist = 0.2
			sel_min_tau_spacing = st.radio("隣接する緩和時間分割に関するデフォルト値は1.25ですが、変更しますか？", ("No", "Yes"), horizontal=True)
			if sel_min_tau_spacing == 'Yes':
				min_tau_spacing = st.slider('緩和時間分割感度の調整', 1.1, 3., 1.5, .1, key='min_tau_spacing')
			else:
				min_tau_spacing = 1.25
		if st.checkbox('出力に関するオプションを設定しますか？', key='out'):
			out_res = st.radio("出力データの調整の有無？", ("Yes", "No"))
			if out_res == 'No':
				resample = False
			else:
				resample = True
				n_resample = st.number_input('データポイント数', min_value=100, max_value=1000, step=100)
		#
		if st.button('オプション入力を終了してデータ処理しますか？', key='Detailed'):
			config = ReSpectConfig(ns, plateau, freq_end, lam_min, lam_max, lam_C, lam_density, SmFacLam, max_num_modes, delta_base_weight_dist, min_tau_spacing, resample, n_resample)
			with st.spinner('処理中です。しばらくお待ちください…'):
				run_respect(st.session_state.cut_df, config)

	return

def run_respect(df, config):
	time = df['Mod. Time'][0:].to_numpy()
	gt = df['G(t)'][0:].to_numpy()

	# Default settings — fit from a data file
	solver = ReSpect(config)
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