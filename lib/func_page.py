import streamlit as st
import pandas as pd 
from lib.func_data import import_data, sec_to_time, avg_perc

def set_singola():
    st.session_state.page = "singola"

def set_home():
    st.session_state.page = "home"

def set_aggregato():
    st.session_state.page = "aggregato"

def home():
    data, df_results = import_data()

    # Inizializzo session state
    list_season = list(set(list(data.season.values)))
    list_season.reverse()
    if 'scelta_season' not in st.session_state:
        st.session_state['scelta_season'] = list_season[0]
    list_team = list(set(list(data.loc[data.season == st.session_state.scelta_season].my_team.values)))
    if 'scelta_team' not in st.session_state:
        st.session_state['scelta_team'] = list_team[0]

    data = data.loc[ (data.my_team == st.session_state.scelta_team) & (data.season == st.session_state.scelta_season ) ]

    col1, col2, _ = st.columns(3)
    st.session_state.scelta_season = col1.radio("Stagione:", list_season, horizontal=True)

    st.session_state.scelta_team = col2.radio("Squadra BK Chiavenna:", list_team, horizontal=True)

    data = data.loc[ (data.my_team == st.session_state.scelta_team) & (data.season == st.session_state.scelta_season ) ]

    col11, col12 = st.columns(2)
    col12.markdown("### Visualizza:")
    col12.button("👀 Statistiche partite 👀", on_click=set_singola)
    col12.button("👀 Statistiche aggregate 👀", on_click=set_aggregato)


    res_vis = df_results.loc[(df_results.Season == st.session_state.scelta_season) & (df_results.my_team == st.session_state.scelta_team)][["Squadra", "Data", "Luogo","Chiav", "Avversari", "W/L"]].reset_index(drop=True)
    col11.markdown("### Risultati:")
    col11.write(res_vis)




def singola():
    data, df_results = import_data()

    # Inizializzo session state
    list_season = list(set(list(data.season.values)))
    if 'scelta_season' not in st.session_state:
        st.session_state['scelta_season'] = list_season[0]
    list_team = list(set(list(data.loc[data.season == st.session_state.scelta_season].my_team.values)))
    if 'scelta_team' not in st.session_state:
        st.session_state['scelta_team'] = list_team[0]

    data = data.loc[ (data.my_team == st.session_state.scelta_team) & (data.season == st.session_state.scelta_season ) ]

    col01, col02, col03 = st.columns([0.1, 0.8, 0.1])
    col01.button("🔙 Home", on_click=set_home)
    col02.write(f"### Squadra selezionata: :orange[{st.session_state.scelta_team} - {st.session_state.scelta_season}] ")
    col03.button("👀 Statistiche aggregate 👀", on_click=set_aggregato)

    col11, col12 = st.columns(2)

    list_other = list(set(list(data.loc[(data.my_team == st.session_state.scelta_team) & (data.season == st.session_state.scelta_season)].other_team.values)))
    scelta_other = col11.radio("Nemico:", list_other, horizontal=True)

    list_date = list(set(list(data.loc[(data.my_team == st.session_state.scelta_team) & (data.season == st.session_state.scelta_season) & \
                                    (data.other_team == scelta_other)].date.values)))
    scelta_date = col11.radio("Data:", list_date, horizontal=True)

    data_single = data.loc[(data.other_team == scelta_other) & (data.date == scelta_date)]

    data_single = data_single.drop(columns=["season","my_team", "other_team", "date", "PFD", "sec", "min_", "sec_"])
    data_single["TS%"] = (data_single.PTS / (2*(data_single.FGA + 0.44*data_single.FTA)))*100
    data_single_players = data_single.loc[data_single.Giocatore != "Totale"]
    data_single_team = data_single.loc[data_single.Giocatore == "Totale"].reset_index(drop=True).drop(columns=['Nr','MIN'])

    res_vis = df_results.loc[(df_results.Season == st.session_state.scelta_season) & (df_results.my_team == st.session_state.scelta_team) & (df_results.Squadra == scelta_other) &\
            (df_results.Data == scelta_date) ][["Data","Luogo","Chiav", "Avversari", "W/L"]].reset_index(drop=True)
    col12.markdown("### Risultato:")
    col12.write(res_vis)

    st.markdown("### Statistiche giocatori:")
    st.write(data_single_players)
    st.markdown("### Statistiche squadra:")
    st.write(data_single_team)


def aggregato():
    data, _ = import_data()

    # Inizializzo session state
    list_season = list(set(list(data.season.values)))
    if 'scelta_season' not in st.session_state:
        st.session_state['scelta_season'] = list_season[0]
    list_team = list(set(list(data.loc[data.season == st.session_state.scelta_season].my_team.values)))
    if 'scelta_team' not in st.session_state:
        st.session_state['scelta_team'] = list_team[0]

    data = data.loc[ (data.my_team == st.session_state.scelta_team) & (data.season == st.session_state.scelta_season ) ]

    mrg_1 = data.loc[data.season == st.session_state.scelta_season].drop(columns=["Nr"]).groupby(["Giocatore"]).mean().reset_index().round(1)
    mrg_2 = data.loc[data.season == st.session_state.scelta_season].drop(columns=["Nr"]).groupby(["Giocatore"]).agg( {"MIN":"count"} ).reset_index().rename(columns={"MIN":"Nr_partite"})

    data_mean = mrg_1.merge(mrg_2, on=["Giocatore"])
    data_mean["MIN"] = data_mean.sec.apply(lambda x: sec_to_time(x) )

    data_mean['FG%'] = data_mean.apply(lambda row: avg_perc(row['FGM'], row['FGA']), axis=1)
    data_mean['3P%'] = data_mean.apply(lambda row: avg_perc(row['3PM'], row['3PA']), axis=1)
    data_mean['2P%'] = data_mean.apply(lambda row: avg_perc(row['2PM'], row['2PA']), axis=1)
    data_mean['FT%'] = data_mean.apply(lambda row: avg_perc(row['FTM'], row['FTA']), axis=1)
    chart_data = data_mean[[ 'Giocatore', 'sec', 'EFF' ]]
    chart_data['MIN'] = chart_data.sec // 60
    chart_data = chart_data.drop(columns=["sec"])

    data_mean = data_mean[['Giocatore', 'Nr_partite', 'MIN', 'PTS', 'FGM', 'FGA', 'FG%', '3PM', '3PA', '3P%', '2PM', '2PA',
        '2P%', 'FTM', 'FTA', 'FT%', 'OREB', 'DREB', 'REB', 'AST', 'TOV', 'STL', 'BLK', 'SR', 'PF', 'PIR', 'EFF' ]]
    data_mean["TS%"] = (data_mean.PTS / (2*(data_mean.FGA + 0.44*data_mean.FTA)))*100


    data_mean_players = data_mean.loc[data_mean.Giocatore != "Totale"]
    data_mean_team = data_mean.loc[data_mean.Giocatore == "Totale"].reset_index(drop=True).drop(columns=['MIN'])


    col01, col02, col03 = st.columns([0.1, 0.8, 0.1])
    col01.button("🔙 Home", on_click=set_home)
    col02.write(f"### Squadra selezionata: :orange[{st.session_state.scelta_team} - {st.session_state.scelta_season}] ")
    col03.button("👀 Statistiche partite 👀", on_click=set_singola)
    st.markdown("### Statistiche giocatori:")
    st.write(data_mean_players)
    st.markdown("### Statistiche squadra:")
    st.write(data_mean_team)
    list_player = list(set(list(data.loc[(data.my_team == st.session_state.scelta_team) & (data.season == st.session_state.scelta_season)].Giocatore.values)))
    list_player.insert(0, list_player.pop(list_player.index("Totale")))
    st.markdown("### Storico per voce statistica:")
    scelta_player = st.radio("Giocatore:", list_player, horizontal=True)
    list_feat = ['PTS', 'MIN', 'EFF', 'OREB', 'DREB', 'REB', 'AST', 'TOV', 'STL', 'BLK', 'SR', 'PF',
                    'PIR', 'FGM', 'FGA',  '3PM', '3PA', '2PM', '2PA','FTM', 'FTA' ] # 'FG%','3P%', '2P%', , 'FT%'
    scelta_feat = st.radio("Voci statistiche:", list_feat, horizontal=True)
    st.markdown(f"Storico per {scelta_feat} - {scelta_player}:")
    data_plot = data.loc[(data.season == st.session_state.scelta_season) & (data.my_team == st.session_state.scelta_team) &  (data.Giocatore == scelta_player)]
    data_plot.date = pd.to_datetime(data_plot.date, format='%d-%m-%Y')
    data_plot = data_plot.sort_values(by=["date"])
    if scelta_player != "Totale":
        data_plot['MIN'] = data_plot['MIN'].str.slice(0, 2).astype(int)
    st.line_chart(data_plot, x="date", y=scelta_feat)