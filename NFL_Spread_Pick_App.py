import streamlit as st
import pandas as pd
import datetime
import os
import numpy as np
import re

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# ---------------------------------------------------------
# TEAM NORMALIZATION (ALL TO ABBREVIATIONS)
# ---------------------------------------------------------

TEAM_MAP = {
    # AFC East
    "New England Patriots": "NE",
    "New England": "NE",
    "NE": "NE",

    "Buffalo Bills": "BUF",
    "Buffalo": "BUF",
    "BUF": "BUF",

    "Miami Dolphins": "MIA",
    "Miami": "MIA",
    "MIA": "MIA",

    "New York Jets": "NYJ",
    "NY Jets": "NYJ",
    "Jets": "NYJ",
    "NYJ": "NYJ",

    # AFC North
    "Baltimore Ravens": "BAL",
    "Baltimore": "BAL",
    "BAL": "BAL",

    "Cincinnati Bengals": "CIN",
    "Cincinnati": "CIN",
    "CIN": "CIN",

    "Cleveland Browns": "CLE",
    "Cleveland": "CLE",
    "CLE": "CLE",

    "Pittsburgh Steelers": "PIT",
    "Pittsburgh": "PIT",
    "PIT": "PIT",

    # AFC South
    "Houston Texans": "HOU",
    "Houston": "HOU",
    "HOU": "HOU",

    "Indianapolis Colts": "IND",
    "Indianapolis": "IND",
    "IND": "IND",

    "Jacksonville Jaguars": "JAX",
    "Jacksonville": "JAX",
    "JAX": "JAX",

    "Tennessee Titans": "TEN",
    "Tennessee": "TEN",
    "TEN": "TEN",

    # AFC West
    "Denver Broncos": "DEN",
    "Denver": "DEN",
    "DEN": "DEN",

    "Kansas City Chiefs": "KC",
    "Kansas City": "KC",
    "KC": "KC",

    "Las Vegas Raiders": "LV",
    "Las Vegas": "LV",
    "LV": "LV",

    "Los Angeles Chargers": "LAC",
    "LA Chargers": "LAC",
    "Chargers": "LAC",
    "LAC": "LAC",

    # NFC East
    "Dallas Cowboys": "DAL",
    "Dallas": "DAL",
    "DAL": "DAL",

    "New York Giants": "NYG",
    "NY Giants": "NYG",
    "Giants": "NYG",
    "NYG": "NYG",

    "Philadelphia Eagles": "PHI",
    "Philadelphia": "PHI",
    "PHI": "PHI",

    "Washington Commanders": "WAS",
    "Washington": "WAS",
    "WAS": "WAS",

    # NFC North
    "Chicago Bears": "CHI",
    "Chicago": "CHI",
    "CHI": "CHI",

    "Detroit Lions": "DET",
    "Detroit": "DET",
    "DET": "DET",

    "Green Bay Packers": "GB",
    "Green Bay": "GB",
    "GB": "GB",

    "Minnesota Vikings": "MIN",
    "Minnesota": "MIN",
    "MIN": "MIN",

    # NFC South
    "Atlanta Falcons": "ATL",
    "Atlanta": "ATL",
    "ATL": "ATL",

    "Carolina Panthers": "CAR",
    "Carolina": "CAR",
    "CAR": "CAR",

    "New Orleans Saints": "NO",
    "New Orleans": "NO",
    "NO": "NO",

    "Tampa Bay Buccaneers": "TB",
    "Tampa Bay": "TB",
    "TB": "TB",

    # NFC West
    "Arizona Cardinals": "ARI",
    "Arizona": "ARI",
    "ARI": "ARI",

    "Los Angeles Rams": "LA",
    "LA Rams": "LA",
    "Rams": "LA",
    "LA": "LA",

    "San Francisco 49ers": "SF",
    "San Francisco": "SF",
    "SF": "SF",

    "Seattle Seahawks": "SEA",
    "Seattle": "SEA",
    "SEA": "SEA",
}

def normalize_team(name):
    name = str(name).strip()
    return TEAM_MAP.get(name, name)

# ---------------------------------------------------------
# LOAD EPA (2024 + 2025)
# ---------------------------------------------------------

epa_2024 = pd.read_csv("Team_EPA_2024.csv")
epa_2025 = pd.read_csv("Team_EPA_2025.csv")

epa_2024["Team"] = epa_2024["Team"].apply(normalize_team)
epa_2025["Team"] = epa_2025["Team"].apply(normalize_team)

epa_2024["season"] = 2024
epa_2025["season"] = 2025

epa_all = pd.concat([epa_2024, epa_2025], ignore_index=True)

# Rename AFTER normalization
epa_all = epa_all.rename(columns={
    "Team": "team",
    "Off WEPA/play": "off_wepa_play",
    "Def WEPA/play": "def_wepa_play",
    "Off SR": "off_sr",
    "Def SR": "def_sr",
    "Off Pass WEPA": "off_pass_wepa",
    "Def Pass WEPA": "def_pass_wepa"
})

# ---------------------------------------------------------
# LOAD DL / OL / OFF / DEF (2024 + 2025)
# ---------------------------------------------------------

def load_team_dl(path, season):
    df = pd.read_csv(path)
    df["Team"] = df["Team"].apply(normalize_team)
    df["season"] = season
    return df

def load_team_ol(path, season):
    df = pd.read_csv(path)
    df["Team"] = df["Team"].apply(normalize_team)
    df["season"] = season
    return df

def load_team_off(path, season):
    df = pd.read_csv(path)
    df["Team"] = df["Team"].apply(normalize_team)
    df["season"] = season
    return df

def load_team_def(path, season):
    df = pd.read_csv(path)
    df["Team"] = df["Team"].apply(normalize_team)
    df["season"] = season
    return df

dl_2024 = load_team_dl("Team_DL_2024.csv", 2024)
dl_2025 = load_team_dl("Team_DL_2025.csv", 2025)
dl_all = pd.concat([dl_2024, dl_2025], ignore_index=True)

ol_2024 = load_team_ol("Team_OL_2024.csv", 2024)
ol_2025 = load_team_ol("Team_OL_2025.csv", 2025)
ol_all = pd.concat([ol_2024, ol_2025], ignore_index=True)

off_2024 = load_team_off("Team_Offense_2024.csv", 2024)
off_2025 = load_team_off("Team_Offense_2025.csv", 2025)
off_all = pd.concat([off_2024, off_2025], ignore_index=True)

def_2024 = load_team_def("Team_Defense_2024.csv", 2024)
def_2025 = load_team_def("Team_Defense_2025.csv", 2025)
def_all = pd.concat([def_2024, def_2025], ignore_index=True)

# ---------------------------------------------------------
# LOAD RED ZONE (OFF + DEF)
# ---------------------------------------------------------

def load_off_redzone(path):
    df = pd.read_csv(path)
    df["Team"] = df["Team"].apply(normalize_team)
    df = df.rename(columns={
        "Team": "team",
        "2025": "off_rz_2025",
        "Last 3": "off_rz_last3",
        "Last 1": "off_rz_last1",
        "Home": "off_rz_home",
        "Away": "off_rz_away",
        "2024": "off_rz_2024"
    })
    return df

def load_def_redzone(path):
    df = pd.read_csv(path)
    df["Team"] = df["Team"].apply(normalize_team)
    df = df.rename(columns={
        "Team": "team",
        "2025": "def_rz_2025",
        "Last 3": "def_rz_last3",
        "Last 1": "def_rz_last1",
        "Home": "def_rz_home",
        "Away": "def_rz_away",
        "2024": "def_rz_2024"
    })
    return df

off_rz = load_off_redzone("Teams_Off_RedZone.csv")
def_rz = load_def_redzone("Teams_Def_RedZone.csv")

# ---------------------------------------------------------
# RENAME COLUMNS TO MODEL NAMES
# ---------------------------------------------------------

epa_all = epa_all.rename(columns={
    "Team": "team",
    "Off WEPA/play": "off_wepa_play",
    "Def WEPA/play": "def_wepa_play",
    "Off SR": "off_sr",
    "Def SR": "def_sr",
    "Off Pass WEPA": "off_pass_wepa",
    "Def Pass WEPA": "def_pass_wepa"
})

dl_all = dl_all.rename(columns={
    "Team": "team",
    "Rate": "dl_rate",
    "Pass": "dl_pass",
    "Run": "dl_run"
})

ol_all = ol_all.rename(columns={
    "Team": "team",
    "Rate": "ol_rate",
    "Pass": "ol_pass",
    "Run": "ol_run"
})

off_all = off_all.rename(columns={
    "Team": "team",
    "Rate": "off_rate",
    "PPG": "off_ppg",
    "Pass": "off_pass",
    "Run": "off_run",
    "EPA": "off_epa",
    "YPP": "off_ypp",
    "Success": "off_success",
    "Explosive": "off_explosive",
    "SOS": "off_sos"
})

def_all = def_all.rename(columns={
    "Team": "team",
    "Rate": "def_rate",
    "PPG": "def_ppg",
    "Pass": "def_pass",
    "Run": "def_run",
    "EPA": "def_epa",
    "YPP": "def_ypp",
    "Success": "def_success",
    "Explosive": "def_explosive",
    "SOS": "def_sos"
})

# ---------------------------------------------------------
# BUILD TEAM MASTER (2024 + 2025)
# ---------------------------------------------------------

team_master = epa_all.copy()
team_master = team_master.merge(dl_all, on=["team", "season"], how="left")
team_master = team_master.merge(ol_all, on=["team", "season"], how="left")
team_master = team_master.merge(off_all, on=["team", "season"], how="left")
team_master = team_master.merge(def_all, on=["team", "season"], how="left")
team_master = team_master.merge(off_rz, on="team", how="left")
team_master = team_master.merge(def_rz, on="team", how="left")

cols_to_drop = ["Unnamed: 7_x", "Unnamed: 8_x", "Unnamed: 7_y", "Unnamed: 8_y"]
team_master = team_master.drop(columns=cols_to_drop, errors="ignore")

pct_cols = [
    c for c in team_master.columns
    if team_master[c].dtype == object and team_master[c].astype(str).str.contains('%').any()
]

for col in pct_cols:
    team_master[col] = (
        team_master[col]
        .astype(str)
        .str.replace('%', '', regex=False)
        .replace('--', np.nan)
        .astype(float) / 100.0
    )

drop_cols = [
    'off_rz_last3', 'off_rz_last1',
    'def_rz_last3', 'def_rz_last1'
]
team_master = team_master.drop(columns=[c for c in drop_cols if c in team_master.columns])

tm_2024 = team_master[team_master['season'] == 2024].copy()
tm_2025 = team_master[team_master['season'] == 2025].copy()

tm_2024 = tm_2024.drop_duplicates(subset=['team'])
tm_2025 = tm_2025.drop_duplicates(subset=['team'])

blend = tm_2025.merge(
    tm_2024.add_suffix("_2024"),
    left_on="team",
    right_on="team_2024",
    how="left"
)

blend = blend.drop(columns=["team_2024"], errors="ignore")

w25 = 0.70
w24 = 0.30

num_cols = tm_2025.select_dtypes(include=['float64', 'int64']).columns

for col in num_cols:
    col_2024 = col + "_2024"
    if col_2024 in blend.columns:
        blend[col] = (blend[col] * w25) + (blend[col_2024] * w24)

team_master_blended = blend.copy()

cols_to_remove = [
    "off_wepa_play_2024", "def_wepa_play_2024", "off_sr_2024", "def_sr_2024",
    "off_pass_wepa_2024", "def_pass_wepa_2024", "season_2024",
    "dl_rate_2024", "dl_pass_2024", "dl_run_2024",
    "ol_rate_2024", "ol_pass_2024", "ol_run_2024",
    "off_rate_2024", "off_ppg_2024", "off_pass_2024", "off_run_2024",
    "off_epa_2024", "off_ypp_2024", "off_success_2024", "off_explosive_2024",
    "off_sos_2024",
    "def_rate_2024", "def_ppg_2024", "def_pass_2024", "def_run_2024",
    "def_epa_2024", "def_ypp_2024", "def_success_2024", "def_explosive_2024",
    "def_sos_2024",
    "off_rz_2025_2024", "off_rz_home_2024", "off_rz_away_2024",
    "off_rz_2024_2024",
    "def_rz_2025_2024", "def_rz_home_2024", "def_rz_away_2024",
    "def_rz_2024_2024"
]

rz_cols = ['off_rz_2025', 'off_rz_2024', 'def_rz_2025', 'def_rz_2024']

for col in rz_cols:
    team_master_blended[col] = pd.to_numeric(team_master_blended[col], errors='coerce')

team_master_blended = team_master_blended.drop(columns=[c for c in cols_to_remove if c in team_master_blended.columns])

team_master_blended['Off_rz'] = (
    team_master_blended['off_rz_2025'] * w25 +
    team_master_blended['off_rz_2024'] * w24
)

team_master_blended['Def_rz'] = (
    team_master_blended['def_rz_2025'] * w25 +
    team_master_blended['def_rz_2024'] * w24
)

team_master_blended = team_master_blended.drop(columns=[
    'off_rz_2025', 'off_rz_2024',
    'def_rz_2025', 'def_rz_2024'
])

# ---------------------------------------------------------
# WEEK SPREADS / RESULTS LOADERS
# ---------------------------------------------------------

def load_week_spreads(path):
    df = pd.read_csv(path)
    df["Team"] = df["Team"].apply(normalize_team)
    df["Opp"] = df["Opp"].apply(normalize_team)

    df["spread_value"] = pd.to_numeric(df["Spread"], errors="coerce")
    df["total_value"] = pd.to_numeric(df["Total"], errors="coerce")
    df["total_ou"] = None
    df["Adj_value"] = pd.to_numeric(df["Adj"], errors="coerce")
    return df

def load_week_results(week_number):
    path = f"Week{week_number}_Results.csv"
    if not os.path.exists(path):
        return None

    df = pd.read_csv(path)
    df["Team"] = df["Team"].apply(normalize_team)
    df["Opp"] = df["Opp"].apply(normalize_team)

    if "actual_margin" not in df.columns:
        df["actual_margin"] = df["TeamScore"] - df["OppScore"]

    if "cover_flag" not in df.columns:
        df["cover_flag"] = (df["actual_margin"] > df["spread_value"]).astype(int)

    return df

# ---------------------------------------------------------
# MERGE MATCHUPS
# ---------------------------------------------------------

def merge_matchups(games, team_master):
    df = games.merge(
        team_master,
        left_on="Team",
        right_on="team",
        how="left"
    ).drop(columns=["team"])

    df = df.merge(
        team_master.add_suffix("_opp"),
        left_on="Opp",
        right_on="team_opp",
        how="left"
    ).drop(columns=["team_opp"])

    return df

# ---------------------------------------------------------
# FEATURE ENGINEERING
# ---------------------------------------------------------

def create_features(df):
    df["spread_value"] = df["spread_value"].astype(float)

    df["epa_diff"] = df["off_wepa_play"] - df["off_wepa_play_opp"]
    df["def_epa_diff"] = df["def_wepa_play"] - df["def_wepa_play_opp"]

    df["sr_diff"] = df["off_sr"] - df["off_sr_opp"]
    df["def_sr_diff"] = df["def_sr"] - df["def_sr_opp"]

    df["ol_advantage"] = df["ol_rate"] - df["dl_rate_opp"]
    df["dl_advantage"] = df["dl_rate"] - df["ol_rate_opp"]

    df["rz_diff"] = df["Off_rz"] - df["Off_rz_opp"]
    df["rz_def_diff"] = df["Def_rz"] - df["Def_rz_opp"]

    df["explosive_diff"] = df["off_explosive"] - df["off_explosive_opp"]
    df["ypp_diff"] = df["off_ypp"] - df["off_ypp_opp"]
    df["sos_diff"] = df["off_sos"] - df["off_sos_opp"]

    df["epa_diff"] *= 1.5
    df["def_epa_diff"] *= 1.5
    df["ol_advantage"] *= 1.75
    df["dl_advantage"] *= 1.75
    df["sos_diff"] *= 0.625
    df["ypp_diff"] *= 0.5
    df["rz_diff"] *= 1.5
    df["rz_def_diff"] *= 1.5
    df["explosive_diff"] *= 0.875
    df["sr_diff"] *= 1.125
    df["def_sr_diff"] *= 1.125

    return df

# ---------------------------------------------------------
# SINGLE-WEEK MODEL (RF ON SPREAD)
# ---------------------------------------------------------

def train_model(df):
    feature_cols = [
        "epa_diff", "def_epa_diff",
        "sr_diff", "def_sr_diff",
        "ol_advantage", "dl_advantage",
        "rz_diff", "rz_def_diff",
        "explosive_diff", "ypp_diff", "sos_diff"
    ]

    X = df[feature_cols]
    y = df["spread_value"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42
    )

    model = Pipeline([
        ("scaler", StandardScaler()),
        ("rf", RandomForestRegressor(
            n_estimators=500,
            max_depth=12,
            random_state=42
        ))
    ])

    model.fit(X_train, y_train)
    return model, feature_cols

def predict_games(model, df, feature_cols):
    df["model_pred"] = model.predict(df[feature_cols])
    df["model_pred_adj"] = df["model_pred"] - df["Adj_value"]
    df["edge"] = df["spread_value"] - df["model_pred_adj"]
    return df

# ---------------------------------------------------------
# PICK LOGIC + CONFIDENCE
# ---------------------------------------------------------

def add_recommended_pick(df):
    picks = []

    for _, row in df.iterrows():
        team = row["Team"]      # AWAY
        opp = row["Opp"]        # HOME
        vegas = row["spread_value"]
        model_adj = row["model_pred_adj"]
        edge = row["edge"]

        home_team = opp
        away_team = team

        home_is_fav = vegas > 0  # spread from AWAY perspective

        if home_is_fav and abs(edge) <= 2.0:
            pick_side = home_team
            pick_spread = -vegas
            picks.append(f"{pick_side} {pick_spread:+.1f}")
            continue

        pick_team = model_adj < vegas

        if pick_team:
            pick_side = team
            pick_spread = vegas
        else:
            pick_side = opp
            pick_spread = -vegas

        picks.append(f"{pick_side} {pick_spread:+.1f}")

    df["recommended_pick"] = picks
    return df

def confidence_tiers(df):
    labels = []

    for _, row in df.iterrows():
        spread = row["spread_value"]
        team = row["Team"]
        opp = row["Opp"]
        edge = row["edge"]
        pick = row["recommended_pick"]

        if spread < 0:
            favorite = team
        elif spread > 0:
            favorite = opp
        else:
            favorite = None

        pick_team = None
        if isinstance(pick, str):
            if pick.startswith(team):
                pick_team = team
            elif pick.startswith(opp):
                pick_team = opp

        if favorite is None or pick_team is None:
            pick_is_fav = None
        else:
            pick_is_fav = (pick_team == favorite)

        abs_edge = abs(edge)

        if abs_edge < 1:
            base = "No Model Edge"
        elif abs_edge < 3:
            base = "Lean"
        else:
            base = "Bet"

        if pick_is_fav is None or base == "No Model Edge":
            labels.append(base)
        else:
            labels.append(f"{base} Favorite" if pick_is_fav else f"{base} Underdog")

    df["confidence"] = labels
    return df

# ---------------------------------------------------------
# FULL SINGLE-WEEK PIPELINE
# ---------------------------------------------------------

def run_picking_machine(games, team_master):
    feats = create_features(games)
    feats = feats[feats["Team"] < feats["Opp"]].copy()

    model, feature_cols = train_model(feats)
    preds = predict_games(model, feats, feature_cols)

    preds = add_recommended_pick(preds)
    final = confidence_tiers(preds)
    return final

# ---------------------------------------------------------
# TRAINING DATA (MULTI-WEEK)
# ---------------------------------------------------------

def build_training_data(week_number):
    if week_number == 1:
        return None

    spreads = load_week_spreads(f"Week{week_number}_Spreads.csv")
    results = load_week_results(week_number)

    if results is None:
        return None

    df = spreads.merge(
        results,
        on=["Team", "Opp"],
        how="inner"
    )
    return df

def build_season_training(up_to_week):
    frames = []
    for wk in range(1, up_to_week):
        df = build_training_data(wk)
        if df is not None:
            frames.append(df)

    if not frames:
        return None

    season_df = pd.concat(frames, ignore_index=True)
    return season_df

def train_multiweek_model(up_to_week):
    season_df = build_season_training(up_to_week)
    if season_df is None:
        print("No training data available yet.")
        return None, None

    season_df = merge_matchups(season_df, team_master_blended)
    season_df = create_features(season_df)

    feature_cols = [
        "epa_diff", "def_epa_diff",
        "sr_diff", "def_sr_diff",
        "ol_advantage", "dl_advantage",
        "rz_diff", "rz_def_diff",
        "explosive_diff", "ypp_diff", "sos_diff"
    ]

    X = season_df[feature_cols]
    y = season_df["actual_margin"]

    model = Pipeline([
        ("scaler", StandardScaler()),
        ("rf", RandomForestRegressor(
            n_estimators=800,
            max_depth=14,
            random_state=42
        ))
    ])

    model.fit(X, y)
    return model, feature_cols

# ---------------------------------------------------------
# WEEK PICK FUNCTIONS
# ---------------------------------------------------------

def get_week_picks_singleweek(week_number):
    path = f"Week{week_number}_Spreads.csv"
    spreads = load_week_spreads(path)

    adj_lookup = spreads.set_index("Team")["Adj_value"].to_dict()

    games = spreads.merge(
        team_master_blended,
        left_on="Team",
        right_on="team",
        how="left"
    )

    games = games.merge(
        team_master_blended.add_suffix("_opp"),
        left_on="Opp",
        right_on="team_opp",
        how="left"
    )

    games["Adj_team"] = games["Team"].map(adj_lookup)
    games["Adj_opp"] = games["Opp"].map(adj_lookup)
    games["Adj_value"] = games["Adj_team"] - games["Adj_opp"]

    results = run_picking_machine(games, team_master_blended)

    def teaser_flag(row):
        spread = row["spread_value"]
        pick = row["recommended_pick"]

        pick_team = pick.startswith(row["Team"])
        pick_spread = spread if pick_team else -spread

        if pick_spread < 0:
            if -9.5 <= pick_spread <= -6.5:
                return "10pt Teaser"
            if -5.5 <= pick_spread <= -3.5:
                return "6pt Teaser"
            if -2.5 <= pick_spread <= -0.5:
                return "10pt Teaser"

        if pick_spread > 0:
            if 1.5 <= pick_spread <= 2.5:
                return "6pt Teaser"

        return ""

    results["teaser_flag"] = results.apply(teaser_flag, axis=1)

    import io
    buffer = io.BytesIO()
    results.to_excel(buffer, index=False)
    buffer.seek(0)

    print(results[[ 
        "Team", "Opp",
        "spread_value",
        "model_pred_adj",
        "edge",
        "confidence",
        "Adj_value",
        "recommended_pick",
        "teaser_flag"
    ]])

    return results

def get_week_picks(week_number):
    training_df = build_training_data(week_number)
    if training_df is not None:
        training_df.to_excel(f"Week{week_number}_Training.xlsx", index=False)

    model, feature_cols = train_multiweek_model(week_number)

    if model is None:
        print("Week 1: No past data. Using single-week model.")
        return get_week_picks_singleweek(week_number)

    path = f"Week{week_number}_Spreads.csv"
    spreads = load_week_spreads(path)

    adj_lookup = spreads.set_index("Team")["Adj_value"].to_dict()

    games = spreads.merge(
        team_master_blended,
        left_on="Team",
        right_on="team",
        how="left"
    )

    games = games.merge(
        team_master_blended.add_suffix("_opp"),
        left_on="Opp",
        right_on="team_opp",
        how="left"
    )

    games["Adj_team"] = games["Team"].map(adj_lookup)
    games["Adj_opp"] = games["Opp"].map(adj_lookup)
    games["Adj_value"] = games["Adj_team"] - games["Adj_opp"]

    feats = create_features(games)
    feats["model_pred"] = model.predict(feats[feature_cols])
    feats["edge"] = feats["model_pred"] - feats["spread_value"]

    feats = add_recommended_pick(feats)
    feats = confidence_tiers(feats)

    def teaser_flag(row):
        spread = row["spread_value"]
        pick = row["recommended_pick"]

        pick_team = pick.startswith(row["Team"])
        pick_spread = spread if pick_team else -spread

        if pick_spread < 0:
            if -9.5 <= pick_spread <= -6.5:
                return "10pt Teaser"
            if -5.5 <= pick_spread <= -3.5:
                return "6pt Teaser"
            if -2.5 <= pick_spread <= -0.5:
                return "10pt Teaser"

        if pick_spread > 0:
            if 1.5 <= pick_spread <= 2.5:
                return "6pt Teaser"

        return ""

    feats["teaser_flag"] = feats.apply(teaser_flag, axis=1)

    save_path = f"Week{week_number}_Picks.xlsx"
    feats.to_excel(save_path, index=False)

    print(feats[[ 
        "Team", "Opp",
        "spread_value",
        "model_pred",
        "edge",
        "confidence",
        "recommended_pick",
        "teaser_flag"
    ]])

    return feats

# ---------------------------------------------------------
# STREAMLIT UI
# ---------------------------------------------------------

get_week_picks(1)

st.set_page_config(
    page_title="NFL Model Picks",
    page_icon="🏈",
    layout="wide"
)

st.title("🏈 Deanomites 2026' NFL Weekly Picks")

st.sidebar.header("Controls")

current_week = 1
completed_week = 0

for wk in range(1, 19):
    if os.path.exists(f"Week{wk}_Spreads.csv"):
        current_week = wk
    if os.path.exists(f"Week{wk}_Results.csv"):
        completed_week = wk

week_number = current_week
st.sidebar.success(f"Current Week: {week_number}")

run_button = st.sidebar.button("Run Model")

if run_button:
    if week_number > 1:
        prev_week = week_number - 1
        training_df = build_training_data(prev_week)
        if training_df is not None:
            save_path = f"Week{prev_week}_Training.xlsx"
            training_df.to_excel(save_path, index=False)
            st.sidebar.success(f"Training data saved for Week {prev_week}")
        else:
            st.sidebar.info(f"No training data available yet for Week {prev_week}")

    if week_number == 1:
        results = get_week_picks_singleweek(week_number)
    else:
        results = get_week_picks(week_number)

    st.dataframe(
        results[[ 
            "Team", "Opp",
            "spread_value",
            "edge",
            "confidence",
            "recommended_pick",
            "teaser_flag"
        ]],
        use_container_width=True
    )


