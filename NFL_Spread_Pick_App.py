import streamlit as st
import pandas as pd
import datetime
import os

# -----------------------------
# Import your existing functions
# -----------------------------
import pandas as pd

# Load raw CSVs exactly as they are
epa_2024 = pd.read_csv("Team_EPA_2024.csv")
epa_2025 = pd.read_csv("Team_EPA_2025.csv")

# Add season column
epa_2024["season"] = 2024
epa_2025["season"] = 2025

# Combine into one dataframe
epa_all = pd.concat([epa_2024, epa_2025], ignore_index=True)

# Directory
BASE = "C:/DraftKings/NFL/"

# File paths
DL_2024_PATH = "Team_DL_2024.csv"
DL_2025_PATH = "Team_DL_2025.csv"

# Mapping full names → abbreviations
TEAM_MAP = {
    "New England Patriots": "NE",
    "Green Bay Packers": "GB",
    "Los Angeles Rams": "LA",
    "Buffalo Bills": "BUF",
    "San Francisco 49ers": "SF",
    "Seattle Seahawks": "SEA",
    "Dallas Cowboys": "DAL",
    "Detroit Lions": "DET",
    "Indianapolis Colts": "IND",
    "Jacksonville Jaguars": "JAX",
    "Philadelphia Eagles": "PHI",
    "Chicago Bears": "CHI",
    "Washington Commanders": "WAS",
    "Tampa Bay Buccaneers": "TB",
    "Denver Broncos": "DEN",
    "Atlanta Falcons": "ATL",
    "Baltimore Ravens": "BAL",
    "New York Giants": "NYG",
    "Houston Texans": "HOU",
    "Kansas City Chiefs": "KC",
    "Pittsburgh Steelers": "PIT",
    "Arizona Cardinals": "ARI",
    "Cincinnati Bengals": "CIN",
    "Carolina Panthers": "CAR",
    "Los Angeles Chargers": "LAC",
    "Miami Dolphins": "MIA",
    "New Orleans Saints": "NO",
    "Minnesota Vikings": "MIN",
    "Las Vegas Raiders": "LV",
    "Tennessee Titans": "TEN",
    "New York Jets": "NYJ",
    "Cleveland Browns": "CLE"
}

def normalize_team(name):
    name = str(name).strip()
    return TEAM_MAP.get(name, name)   # fallback: return raw name

def load_team_dl(path, season):
    df = pd.read_csv(path)

    # Normalize team names
    df["Team"] = df["Team"].apply(normalize_team)

    # Add season column
    df["season"] = season

    return df

# Load both seasons
dl_2024 = load_team_dl("Team_DL_2024.csv", 2024)
dl_2025 = load_team_dl("Team_DL_2025.csv", 2025)
dl_all = pd.concat([dl_2024, dl_2025], ignore_index=True)

# File paths
OL_2024_PATH = "Team_OL_2024.csv"
OL_2025_PATH = "Team_OL_2025.csv"

def normalize_team(name):
    name = str(name).strip()
    return TEAM_MAP.get(name, name)   # fallback: return raw name

def load_team_ol(path, season):
    df = pd.read_csv(path)

    # Normalize team names
    df["Team"] = df["Team"].apply(normalize_team)

    # Add season column
    df["season"] = season

    return df

# Load both seasons
ol_2024 = load_team_ol("Team_OL_2024.csv", 2024)
ol_2025 = load_team_ol("Team_OL_2025.csv", 2025)
ol_all = pd.concat([ol_2024, ol_2025], ignore_index=True)

# File paths
OFF_2024_PATH = "Team_Offense_2024.csv"
OFF_2025_PATH = "Team_Offense_2025.csv"

def normalize_team(name):
    name = str(name).strip()
    return TEAM_MAP.get(name, name)   # fallback: return raw name

def load_team_off(path, season):
    df = pd.read_csv(path)

    # Normalize team names
    df["Team"] = df["Team"].apply(normalize_team)

    # Add season column
    df["season"] = season

    return df

# Load both seasons
off_2024 = load_team_off("Team_Offense_2024.csv", 2024)
off_2025 = load_team_off("Team_Offense_2025.csv", 2025)
off_all = pd.concat([off_2024, off_2025], ignore_index=True)

# File paths
DEF_2024_PATH = "Team_Defense_2024.csv"
DEF_2025_PATH = "Team_Defense_2025.csv"

def normalize_team(name):
    name = str(name).strip()
    return TEAM_MAP.get(name, name)   # fallback: return raw name

def load_team_def(path, season):
    df = pd.read_csv(path)

    # Normalize team names
    df["Team"] = df["Team"].apply(normalize_team)

    # Add season column
    df["season"] = season

    return df

# Load both seasons
def_2024 = load_team_def("Team_Defense_2024.csv", 2024)
def_2025 = load_team_def("Team_Defense_2025.csv", 2025)
def_all = pd.concat([def_2024, def_2025], ignore_index=True)

import pandas as pd

BASE = "C:/DraftKings/NFL/"

# File paths
OFF_RZ_PATH = "Teams_Off_Redzone.csv"
DEF_RZ_PATH = "Teams_Def_Redzone.csv"

# Team name normalization map
TEAM_MAPPED = {
    "Philadelphia": "PHI",
    "Buffalo": "BUF",
    "Cincinnati": "CIN",
    "Washington": "WAS",
    "San Francisco": "SF",
    "Indianapolis": "IND",
    "LA Rams": "LA",
    "Detroit": "DET",
    "Jacksonville": "JAX",
    "Atlanta": "ATL",
    "Green Bay": "GB",
    "Kansas City": "KC",
    "Tennessee": "TEN",
    "Carolina": "CAR",
    "Chicago": "CHI",
    "Dallas": "DAL",
    "Minnesota": "MIN",
    "Pittsburgh": "PIT",
    "Miami": "MIA",
    "New England": "NE",
    "Denver": "DEN",
    "Seattle": "SEA",
    "Arizona": "ARI",
    "Tampa Bay": "TB",
    "Cleveland": "CLE",
    "Las Vegas": "LV",
    "NY Giants": "NYG",
    "Baltimore": "BAL",
    "Houston": "HOU",
    "LA Chargers": "LAC",
    "NY Jets": "NYJ",
    "New Orleans": "NO"
}


def normalize_team(name):
    return TEAM_MAPPED.get(str(name).strip(), name)

# --- Offensive Red Zone Loader ---
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

# --- Defensive Red Zone Loader ---
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

# Load both
off_rz = load_off_redzone("Teams_Off_Redzone.csv")
def_rz = load_def_redzone("Teams_Def_Redzone.csv")

# EPA
epa_all = epa_all.rename(columns={
    "Team": "team",
    "Off WEPA/play": "off_wepa_play",
    "Def WEPA/play": "def_wepa_play",
    "Off SR": "off_sr",
    "Def SR": "def_sr",
    "Off Pass WEPA": "off_pass_wepa",
    "Def Pass WEPA": "def_pass_wepa"
})

# DL
dl_all = dl_all.rename(columns={
    "Team": "team",
    "Rate": "dl_rate",
    "Pass": "dl_pass",
    "Run": "dl_run"
})

# OL
ol_all = ol_all.rename(columns={
    "Team": "team",
    "Rate": "ol_rate",
    "Pass": "ol_pass",
    "Run": "ol_run"
})

# Offense
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

# Defense
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

# Offensive Red Zone
off_rz = off_rz.rename(columns={
    "Team": "team",
    "2025": "off_rz_2025",
    "Last 3": "off_rz_last3",
    "Last 1": "off_rz_last1",
    "Home": "off_rz_home",
    "Away": "off_rz_away",
    "2024": "off_rz_2024"
})

# Defensive Red Zone
def_rz = def_rz.rename(columns={
    "Team": "team",
    "2025": "def_rz_2025",
    "Last 3": "def_rz_last3",
    "Last 1": "def_rz_last1",
    "Home": "def_rz_home",
    "Away": "def_rz_away",
    "2024": "def_rz_2024"
})

team_master = epa_all.copy()
team_master = team_master.merge(dl_all, on=["team", "season"], how="left")
team_master = team_master.merge(ol_all, on=["team", "season"], how="left")
team_master = team_master.merge(off_all, on=["team", "season"], how="left")
team_master = team_master.merge(def_all, on=["team", "season"], how="left")
team_master = team_master.merge(off_rz, on="team", how="left")
team_master = team_master.merge(def_rz, on="team", how="left")

# Save master table to Excel
cols_to_drop = ["Unnamed: 7_x", "Unnamed: 8_x", "Unnamed: 7_y", "Unnamed: 8_y"]
team_master = team_master.drop(columns=cols_to_drop, errors="ignore")

import numpy as np
# Identify percentage columns (object dtype + contains '%')
pct_cols = [
    c for c in team_master.columns
    if team_master[c].dtype == object and team_master[c].astype(str).str.contains('%').any()
]

# Convert percentage strings → numeric decimals
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

#team_master.to_excel("c:/DraftKings/NFL/team_master.xlsx", index=False)

# Split seasons
tm_2024 = team_master[team_master['season'] == 2024].copy()
tm_2025 = team_master[team_master['season'] == 2025].copy()

# Ensure no duplicates
tm_2024 = tm_2024.drop_duplicates(subset=['team'])
tm_2025 = tm_2025.drop_duplicates(subset=['team'])

# Merge 2024 + 2025 side-by-side
blend = tm_2025.merge(
    tm_2024.add_suffix("_2024"),
    left_on="team",
    right_on="team_2024",
    how="left"
)

# Drop duplicate team column
blend = blend.drop(columns=["team_2024"], errors="ignore")

# Weighting
w25 = 0.70
w24 = 0.30

# Identify numeric columns to blend
num_cols = tm_2025.select_dtypes(include=['float64', 'int64']).columns

for col in num_cols:
    col_2024 = col + "_2024"
    if col_2024 in blend.columns:
        blend[col] = (blend[col] * w25) + (blend[col_2024] * w24)

# Final blended master
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

team_master_blended = team_master_blended.drop(columns=[c for c in cols_to_remove if c in team_master_blended.columns])

# Blend offensive red zone
team_master_blended['Off_rz'] = (
    team_master_blended['off_rz_2025'] * w25 +
    team_master_blended['off_rz_2024'] * w24
)

# Blend defensive red zone
team_master_blended['Def_rz'] = (
    team_master_blended['def_rz_2025'] * w25 +
    team_master_blended['def_rz_2024'] * w24
)

# Drop the original season-specific red zone columns
team_master_blended = team_master_blended.drop(columns=[
    'off_rz_2025', 'off_rz_2024',
    'def_rz_2025', 'def_rz_2024'
])

#team_master_blended.to_excel("c:/DraftKings/NFL/team_master_blended.xlsx", index=False)

import re

BASE = "C:/DraftKings/NFL/"

def load_week_spreads(path):
    df = pd.read_csv(path)

    df["spread_value"] = pd.to_numeric(df["Spread"], errors="coerce")
    df["total_value"] = pd.to_numeric(df["Total"], errors="coerce")
    df["total_ou"] = None

    return df

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# ---------------------------------------------------------
# 1. MERGE WEEK 1 SPREADS WITH BLENDED TEAM MASTER
# ---------------------------------------------------------

def merge_matchups(games, team_master):
    # Merge team metrics
    df = games.merge(
        team_master,
        left_on="Team",
        right_on="team",
        how="left"
    ).drop(columns=["team"])

    # Merge opponent metrics
    df = df.merge(
        team_master.add_suffix("_opp"),
        left_on="Opp",
        right_on="team_opp",
        how="left"
    ).drop(columns=["team_opp"])

    return df


# ---------------------------------------------------------
# 2. FEATURE ENGINEERING
# ---------------------------------------------------------

def create_features(df):
    # Spread target (numeric)
    df["spread_value"] = df["spread_value"].astype(float)

    # EPA diffs
    df["epa_diff"] = df["off_epa"] - df["off_epa_opp"]
    df["def_epa_diff"] = df["def_epa"] - df["def_epa_opp"]

    # Success rate diffs
    df["sr_diff"] = df["off_sr"] - df["off_sr_opp"]
    df["def_sr_diff"] = df["def_sr"] - df["def_sr_opp"]

    # Trenches diffs
    df["ol_advantage"] = df["ol_rate"] - df["dl_rate_opp"]
    df["dl_advantage"] = df["dl_rate"] - df["ol_rate_opp"]

    # Red zone diffs
    df["rz_diff"] = df["Off_rz"] - df["Off_rz_opp"]
    df["rz_def_diff"] = df["Def_rz"] - df["Def_rz_opp"]

    # Explosive diffs
    df["explosive_diff"] = df["off_explosive"] - df["off_explosive_opp"]

    # YPP diffs
    df["ypp_diff"] = df["off_ypp"] - df["off_ypp_opp"]

    # SOS diffs
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
# 3. MODEL TRAINING PIPELINE
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


# ---------------------------------------------------------
# 4. WEEKLY PREDICTION ENGINE
# ---------------------------------------------------------

def predict_games(model, df, feature_cols):
    df["model_pred"] = model.predict(df[feature_cols])
    df["edge"] = df["model_pred"] - df["spread_value"]
    return df


# ---------------------------------------------------------
# 5. CONFIDENCE TIERS
# ---------------------------------------------------------

def confidence_tiers(df):
    labels = []

    for _, row in df.iterrows():
        edge = row["edge"]
        spread = row["spread_value"]
        team = row["Team"]
        opp = row["Opp"]

        # Who is the favorite?
        # If spread < 0, Team is favorite; if spread > 0, Opp is favorite
        if spread < 0:
            team_is_fav = True
        elif spread > 0:
            team_is_fav = False
        else:
            team_is_fav = None  # pick'em

        # Who did we pick? (recompute instead of parsing string)
        # Your pick logic: if model_pred < spread_value → pick Team, else Opp
        pick_team = row["model_pred"] < spread

        if pick_team:
            pick_is_fav = team_is_fav
        else:
            pick_is_fav = (not team_is_fav) if team_is_fav is not None else None

        # Edge magnitude → strength
        abs_edge = abs(edge)
        if abs_edge < 1:
            base = "No Play"
        elif abs_edge < 3:
            base = "Lean"
        else:
            base = "Bet"

        # If no favorite (true pick'em), just use base
        if pick_is_fav is None or base == "No Play":
            labels.append(base)
        else:
            if pick_is_fav:
                labels.append(f"{base} Favorite")
            else:
                labels.append(f"{base} Underdog")

    df["confidence"] = labels
    return df


# ---------------------------------------------------------
# 6. FULL PIPELINE FUNCTION
# ---------------------------------------------------------

#merged = merge_matchups(games, team_master) <---- removed
def run_picking_machine(games, team_master):
    feats = create_features(games)

    # Keep only one row per matchup (alphabetical fix)
    feats = feats[feats["Team"] < feats["Opp"]].copy()

    model, feature_cols = train_model(feats)
    preds = predict_games(model, feats, feature_cols)
    final = confidence_tiers(preds)
    final = add_recommended_pick(final)

    return final


def add_recommended_pick(df):
    picks = []

    for _, row in df.iterrows():
        team = row["Team"]
        opp = row["Opp"]
        vegas = row["spread_value"]
        model = row["model_pred"]

        # If model thinks TEAM should be stronger → pick TEAM
        if model < vegas:
            pick_side = team
            pick_spread = vegas
        else:
            pick_side = opp
            pick_spread = -vegas  # Opposite side of the spread

        picks.append(f"{pick_side} {pick_spread:+.1f}")

    df["recommended_pick"] = picks
    return df

def load_week_results(week_number):
    # Week 1 has no previous results
    if week_number == 1:
        return None

    path = f"C:/DraftKings/NFL/Week{week_number}_Results.csv"
    df = pd.read_csv(path)

    df["actual_margin"] = df["TeamScore"] - df["OppScore"]
    df["cover_flag"] = (df["actual_margin"] > df["spread_value"]).astype(int)

    return df

def build_training_data(week_number):
    # No training data exists before Week 1
    if week_number == 1:
        return None

    spreads = load_week_spreads(f"C:/DraftKings/NFL/Week{week_number}_Spreads.csv")
    results = load_week_results(week_number)

    # If results file missing, skip
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

    if len(frames) == 0:
        return None

    season_df = pd.concat(frames, ignore_index=True)
    return season_df

def train_multiweek_model(up_to_week):
    season_df = build_season_training(up_to_week)

    if season_df is None:
        print("No training data available yet.")
        return None, None

    # Build features
    season_df = merge_matchups(season_df, team_master_blended)
    season_df = create_features(season_df)

    feature_cols = [
        "epa_diff", "def_epa_diff",
        "sr_diff", "def_sr_diff",
        "ol_diff", "dl_diff",
        "rz_diff", "rz_def_diff",
        "explosive_diff", "ypp_diff", "sos_diff"
    ]

    X = season_df[feature_cols]
    y = season_df["actual_margin"]  # <-- REAL RESULTS

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

def get_week_picks_singleweek(week_number):
    path = f"C:/DraftKings/NFL/Week{week_number}_Spreads.csv"
    spreads = load_week_spreads(path)

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

    results = run_picking_machine(games, team_master_blended)
    
    results = confidence_tiers(results)
    results = add_recommended_pick(results)
     
    def teaser_flag(row):
        spread = row["spread_value"]
        pick = row["recommended_pick"]

        # Determine if pick is on Team or Opponent
        pick_team = pick.startswith(row["Team"])

        # Determine the spread of the side being picked
        pick_spread = spread if pick_team else -spread

        # --- FAVORITE RANGES ---
        if pick_spread < 0:
            # -9.5 to -6.5 → 10pt teaser (cross 0)
            if -9.5 <= pick_spread <= -6.5:
                return "10pt Teaser"

            # -5.5 to -3.5 → 6pt teaser (cross 0)
            if -5.5 <= pick_spread <= -3.5:
                return "6pt Teaser"

            # -2.5 to -0.5 → 10pt teaser (cross +7)
            if -2.5 <= pick_spread <= -0.5:
                return "10pt Teaser"

        # --- UNDERDOG RANGES ---
        if pick_spread > 0:
            # +1.5 to +2.5 → 6pt teaser (cross +7)
            if 1.5 <= pick_spread <= 2.5:
                return "6pt Teaser"

        return ""

    results["teaser_flag"] = results.apply(teaser_flag, axis=1)
    
    results.to_excel(f"C:/DraftKings/NFL/Week{week_number}_Picks.xlsx", index=False)

    print(results[[ 
        "Team", "Opp",
        "spread_value",
        "model_pred",
        "edge",
        "confidence",
        "recommended_pick",
        "teaser_flag"
    ]])

    return results


def get_week_picks(week_number):

    # Build training data only if week > 1
    training_df = build_training_data(week_number)
    if training_df is not None:
        training_df.to_excel(f"C:/DraftKings/NFL/Week{week_number}_Training.xlsx", index=False)

    # Train multi-week model using all past weeks
    model, feature_cols = train_multiweek_model(week_number)

    # If no model yet (week 1)
    if model is None:
        print("Week 1: No past data. Using single-week model.")
        # fallback to your original single-week model
        return get_week_picks_singleweek(week_number)

    # Load spreads
    path = f"C:/DraftKings/NFL/Week{week_number}_Spreads.csv"
    spreads = load_week_spreads(path)

    # Merge team + opponent metrics
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

    # Build features
    feats = create_features(games)

    # Predict actual margin
    feats["model_pred"] = model.predict(feats[feature_cols])

    # Convert actual margin prediction → spread edge
    feats["edge"] = feats["model_pred"] - feats["spread_value"]

    # Confidence tiers
    feats = confidence_tiers(feats)

    # Recommended pick
    feats = add_recommended_pick(feats)

    def teaser_flag(row):
        spread = row["spread_value"]
        pick = row["recommended_pick"]

        # Determine if pick is on Team or Opponent
        pick_team = pick.startswith(row["Team"])

        # Determine the spread of the side being picked
        pick_spread = spread if pick_team else -spread

        # --- FAVORITE RANGES ---
        if pick_spread < 0:
            # -9.5 to -6.5 → 10pt teaser (cross 0)
            if -9.5 <= pick_spread <= -6.5:
                return "10pt Teaser"

            # -5.5 to -3.5 → 6pt teaser (cross 0)
            if -5.5 <= pick_spread <= -3.5:
                return "6pt Teaser"

            # -2.5 to -0.5 → 10pt teaser (cross +7)
            if -2.5 <= pick_spread <= -0.5:
                return "10pt Teaser"

        # --- UNDERDOG RANGES ---
        if pick_spread > 0:
            # +1.5 to +2.5 → 6pt teaser (cross +7)
            if 1.5 <= pick_spread <= 2.5:
                return "6pt Teaser"

        return ""

    feats["teaser_flag"] = feats.apply(teaser_flag, axis=1)

    # Save weekly picks
    save_path = f"C:/DraftKings/NFL/Week{week_number}_Picks.xlsx"
    feats.to_excel(save_path, index=False)

    # Print clean pick sheet
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


# Bypass line below when running training below
get_week_picks(1)

# After games finish:
#Remove bypasses below when running picks and change week value
#training_week1 = build_training_data(1)
#training_week1.to_excel("C:/DraftKings/NFL/Week1_Training.xlsx", index=False)

# -----------------------------
# Streamlit Page Config
# -----------------------------
st.set_page_config(
    page_title="NFL Model Picks",
    page_icon="🏈",
    layout="wide"
)

st.title("🏈 Deanomites NFL Weekly Picks & Teaser Engine")

# -----------------------------
# Sidebar Controls
# -----------------------------
st.sidebar.header("Controls")

# -----------------------------------------
# Auto-detect latest completed week
# -----------------------------------------
latest_week = 1
for wk in range(1, 19):
    path = f"C:/DraftKings/NFL/Week{wk}_Results.csv"
    if os.path.exists(path):
        latest_week = wk

week_number = latest_week
st.sidebar.success(f"Current Week: {week_number}")


# Confidence filter
confidence_filter = st.sidebar.multiselect(
    "Filter by Confidence",
    ["Bet Favorite", "Bet Underdog", "Lean Favorite", "Lean Underdog", "No Play"],
    default=["Bet Favorite", "Bet Underdog", "Lean Favorite", "Lean Underdog", "No Play"]
)

# Teaser filter
teaser_only = st.sidebar.checkbox("Show Teaser Plays Only")

# Run button
run_button = st.sidebar.button("Run Model")

# -----------------------------
# Main App Logic
# -----------------------------
if run_button:

    # Run your model
    if week_number == 1:
        results = get_week_picks_singleweek(week_number)
    else:
        results = get_week_picks(week_number)

    # Apply confidence filter
    results = results[results["confidence"].isin(confidence_filter)]

    # Apply teaser filter
    if teaser_only:
        results = results[results["teaser_flag"] != ""]

    st.subheader(f"Selections for Week {week_number}")

    # Display table
    st.dataframe(
        results[[
            "Team", "Opp",
            "spread_value",
            "model_pred",
            "edge",
            "confidence",
            "recommended_pick",
            "teaser_flag"
        ]],
        use_container_width=True
    )

    from io import BytesIO

    # Trim to clean pick sheet columns
    export_df = results[[ 
        "Team", "Opp",
        "spread_value",
        "model_pred",
        "edge",
        "confidence",
        "recommended_pick",
        "teaser_flag"
    ]]

    # -----------------------------
    # Download Excel Button
    # -----------------------------
    from io import BytesIO
    from openpyxl import load_workbook

    buffer = BytesIO()

    # Write initial Excel file
    export_df.to_excel(buffer, index=False, engine="openpyxl")

    # Load workbook to adjust column widths
    buffer.seek(0)
    wb = load_workbook(buffer)
    ws = wb.active

    # Auto-size columns
    for col in ws.columns:
        max_length = 0
        col_letter = col[0].column_letter

        for cell in col:
            try:
                cell_length = len(str(cell.value))
                if cell_length > max_length:
                    max_length = cell_length
            except:
                pass

        ws.column_dimensions[col_letter].width = max_length + 2  # padding

    # Save adjusted workbook back into buffer
    from excel_utils import autosize_excel

    buffer = autosize_excel(export_df)

    # Streamlit download button
    st.download_button(
        label="Download Picks as Excel",
        data=buffer,
        file_name=f"Week{week_number}_Picks.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )



else:
    st.info("Apply filter if desired and click **Run Model** to generate picks.")
