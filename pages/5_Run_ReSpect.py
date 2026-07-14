import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pyrespect_time import ReSpect, ReSpectConfig
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
		st.write('対象データは以下です')
		st.dataframe(st.session_state.cut_df)
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
	st.dataframe(df_gt)
	#
	df_cont=pd.DataFrame(np.stack([solver.continuous.s, solver.continuous.H], 1))
	df_cont.columns=['Continuous.s', 'Continuous.H']
	df_disc=pd.DataFrame(np.stack([solver.discrete.tau, solver.discrete.g], 1))
	df_disc.columns=['Discrete.tau', 'Discrete.g']     # discrete mode weights
	
	#
	cont_time=solver.continuous.s
	cont_H=np.exp(solver.continuous.H)
	disc_tau=solver.discrete.tau
	disc_g=solver.discrete.g
	#
	t=solver.t
	Gt=solver.Gt
	cont_fit=solver.continuous.G_fit
	disc_fit=solver.discrete.G_fit
	#
	col1, col2=st.columns(2)
	with col1:
		st.dataframe(df_gt)
	with col2:
		st.pyplot(plot_base_2(t, Gt, cont_fit, disc_fit))

	# グラフ作成
	figs = [
		plot_base_1(cont_time,cont_H,disc_tau,disc_g),
		plot_base_2(t, Gt, cont_fit, disc_fit)
	]
	# 表示
	col1, col2 = st.columns(2)
	for i, fig in enumerate(figs):
		with [col1, col2][i]:
			st.pyplot(fig)
	return

def plot_base_1(cont_time,cont_H,disc_tau,disc_g):
	# ---- Left: discrete modes overlaid on continuous spectrum ----
	fig, ax = plt.subplots()
	ax.loglog(
		cont_time,cont_H,
		label='CRS',
	)
	ax.loglog(
		disc_tau,disc_g,
		'o-', label='DRS',
	)
	ax.set_xlabel(r'$\tau$')
	ax.set_ylabel(r'$g, h(\tau)$')
	ax.legend()
	fig.tight_layout()
	return fig

def plot_base_2(t, Gt, cont_fit, disc_fit):
	# ---- Right: G(t) data vs continuous and discrete fits ----
	fig, ax = plt.subplots()
	ax.loglog(t, Gt, 'x', label='data', c='gray')
	ax.loglog(t, cont_fit, label='continuous fit')
	ax.loglog(t, disc_fit, '--', label='discrete fit')
	ax.set_xlabel(r'$t$')
	ax.set_ylabel(r'$G(t)$')
	ax.legend()
	fig.tight_layout()
	return fig

###
if __name__ == "__main__":
	main()