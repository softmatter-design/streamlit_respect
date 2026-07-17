import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="応力緩和処理サイト",
    layout="wide"
        )

st.title('ここでできること')
st.markdown("---")

st.header('pyReSpect-timeによる応力緩和関数$G(t)$から応力緩和スペクトル（連続）への変換')
st.subheader('応力緩和関数$G(t)$から応力緩和スペクトル$\\mathcal{H}(s)$')
st.markdown('応力緩和関数$G(t)$は、以下のように連続的な応力緩和スペクトル$\\mathcal{H}(s)$の積分表現、あるいは、一般化マックスウェルモデルとして離散的な緩和時間$\\tau_i$を有する緩和強度$g_i$のサンメンションとして表される')
st.markdown(r"""
            $$
            \begin{align}
            G(t) &= G_0 + \int_{-\infty}^{\infty} \mathcal{H}(s) e^{-t/s} d \ln s \cdots \text{連続表現} \\
            G(t) &= G_0 + \sum_{i=1}^{N} g_i e^{-t/\tau_i} \cdots \text{離散表現}
            \end{align}
            $$
            """)

st.subheader('pyReSpect-timeとは')
st.markdown('pyReSpect-timeは、数値シミュレーションにより上記の関係の逆問題を解くことで連続的な応力緩和スペクトル$\\mathcal{H}(s)$を導出し、その結果から一般化マックスウェルモデルの離散的な緩和時間$\\tau_i$を有する緩和強度$g_i$の組を求めるpythonスクリプトである')
st.markdown('- 連続スペクトル$\\mathcal{H}(s)$は、「チホノフ正則化 (Tikhonov Regularization)」手法を用いたベイズ推定により求めている\n- 一般化マックスウェルモデルはAIC最小化により導出している')
st.markdown('[pyReSpect-timeのサイト](https://github.com/shane5ul/pyReSpect-time)')
st.subheader('参考文献')
st.markdown('> Shanbhag, S., "pyReSpect: A Computer Program to Extract Discrete and Continuous Spectra from Stress Relaxation Experiments", Macromolecular Theory and Simulations, 2019, 1900005.')
st.markdown('> Takeh, A. and Shanbhag, S., "A computer program to extract the continuous and discrete relaxation spectra from dynamic viscoelastic measurements", Applied Rheology, 2013, 23, 24628.')
st.markdown("---")

st.header("ここでの処理の流れ")
st.subheader('処理の流れを以下に示した')
st.markdown('1. 測定結果の読み込み\n1. 適正範囲の選択\n1. 応力緩和グラフの表示\n1. pyReSpectを用いたデータ処理')
st.markdown("---")

st.header("具体的な処理プロセス")
st.subheader('左のメニューバーから順次処理を選択')
st.write('メニューバーのそれぞれのページでの処理内容についての説明は以下のタグで見てください')

tab1, tab2,tab3, tab4, tab5 = st.tabs(['Data_Upload', 'Select_Columns', 'Modify_Data', 'Plot_Data', 'Run_pyReSpect'])
with tab1:
    st.subheader('このページでは、処理対象のデータをアップロードします')
    st.write('・必要に応じてオプションを選択')
    st.write('・手元のPCのファイルをアップロード')
    st.write('・内容に問題なければ「ボタンをクリック」')
with tab2:
    st.subheader('このページでは、「時間」と「緩和弾性率」のカラムを選択します')
    st.write('・前のページで読み込んだファイルの中身が表示されます')
    st.write('・自動選択がうまく行っていれば、やることはありません')
    st.write('・まず、「時間」に対応する列を選択します')
    st.write('・次に、「緩和弾性率」に対応する列を選択します')
    st.write('・内容に問題なければ「ボタンをクリック」')
    st.write('・何度でもやり直し可能です')
with tab3:
    st.subheader('このページでは、初期値となる行を選択します')
    st.write('・行数を直接入力することもできます')
    st.write('・右側の「ーボタン」と「＋ボタン」で一行ずつ変更もできます')
    st.write('・開始行を変更した結果は下にリアルタイムで表示されます')
    st.write('・内容に問題なければ「ボタンをクリック」')
with tab4:
    st.subheader('このページでは、ここまでの処理で出来上がった入力ファイルに基づく「応力緩和のグラフ」を表示します')
    st.write('・規格化したグラフも同時に作成されます')
    st.write('・処理済のデータのCSVファイルとグラフの画像データがZIPファイルとしてダウンロードできます')
    st.write('・内容に問題なければ「ボタンをクリック」')
with tab5:
    st.subheader('このページでは、ここまでの処理結果をReSpectに入力して、データ処理を行います')
    st.write('・必要に応じてオプションを選択')
    st.write('・「データ処理」のボタンをクリック')
    st.write('・「処理中」の表示を経て、「緩和関数」を「連続」と「離散」で求めた結果が表示されます')
    st.write('・同時に、上記の推定値による応力緩和グラフを測定値と合わせて表示されます')
    st.write('・処理済のデータのCSVファイルとグラフの画像データがZIPファイルとしてダウンロードできます')

st.markdown("---")