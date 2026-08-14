import streamlit as st
import pandas as pd
import os

BASE = "C:/DraftKings/NFL/"

st.set_page_config(page_title="Model Accuracy", page_icon="🎯", layout="wide")
st.title("🎯 Model Accuracy Dashboard")

st.write("Evaluate how well the model performed ATS and on teaser plays.")

# -----------------------------------------
# Load all available weekly picks + results
# -----------------------------------------
all_weeks = []

for wk in range(1, 19):
    picks_path = f"{BASE}Week{wk}_Picks.xlsx"
    results_path = f"{BASE}Week{wk}_Results.csv"

    if os.path.exists(picks_path) and os.path.exists(results_path):
        try:
            picks = pd.read_excel(picks_path)
            results = pd.read_csv(results_path)

            picks["week"] = wk
            results["week"] = wk

            # Merge picks + results
            df = picks.merge(
                results,
                on=["Team", "Opp"],
                how="inner"
            )

            all_weeks.append(df)
        except:
            pass

# If no merged weeks exist yet
if len(all_weeks) == 0:
    st.info("No model accuracy data available yet. Accuracy will appear once Week 1 results are posted.")
    st.stop()

# Combine all weeks
season_df = pd.concat(all_weeks, ignore_index=True)

# -----------------------------------------
# Compute actual margin + ATS result
# -----------------------------------------
season_df["actual_margin"] = season_df["TeamScore"] - season_df["OppScore"]
season_df["ATS_Win"] = (season_df["actual_margin"] > season_df["spread_value"]).astype(int)

# -----------------------------------------
# Compute model ATS accuracy
# -----------------------------------------
def model_ats_win(row):
    pick = row["recommended_pick"]
    team = row["Team"]
    opp = row["Opp"]
    margin = row["actual_margin"]
    spread = row["spread_value"]

    # Determine which side the model picked
    pick_team = pick.startswith(team)

    # Spread of the picked side
    pick_spread = spread if pick_team else -spread

    # Model ATS win?
    return 1 if margin > pick_spread else 0

season_df["Model_ATS_Win"] = season_df.apply(model_ats_win, axis=1)

# -----------------------------------------
# Compute teaser accuracy
# -----------------------------------------
def teaser_outcome(row):
    flag = str(row.get("teaser_flag", "")).strip()
    margin = row["actual_margin"]
    spread = row["spread_value"]

    if flag == "":
        return ""

    if flag == "6pt Teaser":
        teaser_spread = spread + 6 if spread > 0 else spread - 6
    elif flag == "10pt Teaser":
        teaser_spread = spread + 10 if spread > 0 else spread - 10
    else:
        return ""

    return "Win" if margin > teaser_spread else "Loss"

season_df["Teaser_Result"] = season_df.apply(teaser_outcome, axis=1)

# -----------------------------------------
# Season Accuracy Summary
# -----------------------------------------
st.subheader("Season Accuracy Summary")

total_games = len(season_df)
model_ats_wins = season_df["Model_ATS_Win"].sum()
model_ats_losses = total_games - model_ats_wins
model_ats_pct = round(model_ats_wins / total_games * 100, 2)

st.metric("Model ATS Games", total_games)
st.metric("Model ATS Wins", model_ats_wins)
st.metric("Model ATS Losses", model_ats_losses)
st.metric("Model ATS Win %", f"{model_ats_pct}%")

# -----------------------------------------
# Teaser Accuracy Summary
# -----------------------------------------
st.subheader("Season Teaser Accuracy")

teaser_df = season_df[season_df["teaser_flag"] != ""]
teaser_games = len(teaser_df)
teaser_wins = (teaser_df["Teaser_Result"] == "Win").sum()
teaser_losses = teaser_games - teaser_wins
teaser_pct = round(teaser_wins / teaser_games * 100, 2) if teaser_games > 0 else 0

st.metric("Teaser Plays", teaser_games)
st.metric("Teaser Wins", teaser_wins)
st.metric("Teaser Losses", teaser_losses)
st.metric("Teaser Win %", f"{teaser_pct}%")

# -----------------------------------------
# Week-by-Week Accuracy
# -----------------------------------------
st.subheader("Week-by-Week Model Accuracy")

week_summary = (
    season_df.groupby("week")["Model_ATS_Win"]
    .agg(["count", "sum"])
    .rename(columns={"count": "Games", "sum": "ATS Wins"})
)

week_summary["ATS Losses"] = week_summary["Games"] - week_summary["ATS Wins"]
week_summary["Win %"] = (week_summary["ATS Wins"] / week_summary["Games"] * 100).round(2)

st.dataframe(week_summary, use_container_width=True)

# -----------------------------------------
# Team-Level Accuracy
# -----------------------------------------
st.subheader("Team-Level Model Accuracy")

team_summary = (
    season_df.groupby("Team")["Model_ATS_Win"]
    .agg(["count", "sum"])
    .rename(columns={"count": "Games", "sum": "ATS Wins"})
)

team_summary["ATS Losses"] = team_summary["Games"] - team_summary["ATS Wins"]
team_summary["Win %"] = (team_summary["ATS Wins"] / team_summary["Games"] * 100).round(2)

st.dataframe(team_summary, use_container_width=True)

# -----------------------------------------
# Download Model Accuracy (auto-sized Excel)
# -----------------------------------------
from excel_utils import autosize_excel

# Full season model accuracy export
export_df = season_df.copy()
buffer = autosize_excel(export_df)

st.download_button(
    label="Download Full Model Accuracy",
    data=buffer,
    file_name="Model_Accuracy_Full.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# Week-by-week accuracy export
week_buffer = autosize_excel(week_summary)

st.download_button(
    label="Download Week-by-Week Accuracy",
    data=week_buffer,
    file_name="Model_Accuracy_Week_By_Week.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# Team-level accuracy export
team_buffer = autosize_excel(team_summary)

st.download_button(
    label="Download Team-Level Accuracy",
    data=team_buffer,
    file_name="Model_Accuracy_Team_Level.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

