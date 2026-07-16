import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="応力緩和処理サイト",
    layout="wide"
        )

st.title('ここでできること')
st.markdown("---")

st.header("「応力緩和測定」の結果処理")
st.subheader('１．測定結果の読み込み')
st.subheader('２．適正範囲の選択')
st.subheader('３．応力緩和グラフの表示')
st.subheader('４．ReSpectを用いたデータ処理')
st.markdown("---")

st.header("具体的な処理プロセス")
st.subheader('左のメニューバーから順次処理を選択')
st.subheader('メニューバーの内容説明は以下のタグで見てください')

tab1, tab2,tab3, tab4, tab5 = st.tabs(['Data_Upload', 'Select_Columns', 'Modify_Data', 'Plot_Data', 'Run ReSpect'])
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
    st.write('・「データ処理」のボタンをクリック')
    st.write('・「処理中」の表示を経て、「緩和関数」を「連続」と「離散」で求めた結果が表示されます')
    st.write('・同時に、上記の推定値による応力緩和グラフを測定値と合わせて表示されます')
    st.write('・処理済のデータのCSVファイルとグラフの画像データがZIPファイルとしてダウンロードできます')

st.markdown("---")