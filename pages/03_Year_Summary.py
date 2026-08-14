import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Year Summary", page_icon="📈", layout="wide")
st.title("📈 NFL Season Summary")

st.write("Season‑to‑date ATS performance based on all available weekly results.")

# -----------------------------------------
# Load all available weekly results
# -----------------------------------------
all_weeks = []

for wk in range(1, 19):
    path = f"Week{wk}_Results.csv"
    if os.path.exists(path):
        try:
            df = pd.read_csv(path)
            df["week"] = wk
            all_weeks.append(df)
        except:
            pass

# If no results exist yet
if len(all_weeks) == 0:
    st.info("No season results available yet. Summary will appear once Week 1 results are posted.")
    st.stop()

# Combine all weeks
season_df = pd.concat(all_weeks, ignore_index=True)

# -----------------------------------------
# Compute ATS metrics
# -----------------------------------------
if "actual_margin" not in season_df.columns:
    season_df["actual_margin"] = season_df["TeamScore"] - season_df["OppScore"]

if "cover_flag" not in season_df.columns:
    season_df["cover_flag"] = (season_df["actual_margin"] > season_df["spread_value"]).astype(int)

season_df["ATS_Result"] = season_df["cover_flag"].map({1: "Win", 0: "Loss"})

# -----------------------------------------
# Compute teaser results
# -----------------------------------------

def teaser_outcome(row):
    flag = str(row.get("teaser_flag", "")).strip()
    margin = row["actual_margin"]

    if flag == "":
        return ""

    spread = row["spread_value"]

    if flag == "6pt Teaser":
        teaser_spread = spread + 6 if spread > 0 else spread - 6
    elif flag == "10pt Teaser":
        teaser_spread = spread + 10 if spread > 0 else spread - 10
    else:
        return ""

    return "Win" if margin > teaser_spread else "Loss"

season_df["Teaser_Result"] = season_df.apply(teaser_outcome, axis=1)

total_games = len(season_df)
total_wins = season_df["cover_flag"].sum()
total_losses = total_games - total_wins
win_pct = round(total_wins / total_games * 100, 2)

# -----------------------------------------
# Display summary metrics
# -----------------------------------------
st.subheader("Season ATS Summary")

st.metric("Total Games", total_games)
st.metric("ATS Wins", total_wins)
st.metric("ATS Losses", total_losses)
st.metric("Win Percentage", f"{win_pct}%")

# -----------------------------------------
# Teaser Summary
# -----------------------------------------
st.subheader("Season Teaser Summary")

teaser_games = season_df[season_df["teaser_flag"] != ""]
teaser_wins = (teaser_games["Teaser_Result"] == "Win").sum()
teaser_losses = (teaser_games["Teaser_Result"] == "Loss").sum()

if len(teaser_games) > 0:
    teaser_win_pct = round(teaser_wins / len(teaser_games) * 100, 2)
else:
    teaser_win_pct = 0

st.metric("Teaser Plays", len(teaser_games))
st.metric("Teaser Wins", teaser_wins)
st.metric("Teaser Losses", teaser_losses)
st.metric("Teaser Win %", f"{teaser_win_pct}%")


# -----------------------------------------
# Team‑level ATS record (optional but useful)
# -----------------------------------------
st.subheader("Team‑Level ATS Performance")

team_summary = (
    season_df.groupby("Team")["cover_flag"]
    .agg(["count", "sum"])
    .rename(columns={"count": "Games", "sum": "ATS Wins"})
)

team_summary["ATS Losses"] = team_summary["Games"] - team_summary["ATS Wins"]
team_summary["Win %"] = (team_summary["ATS Wins"] / team_summary["Games"] * 100).round(2)

st.dataframe(team_summary, use_container_width=True)

st.subheader("Team‑Level Teaser Performance")

team_teaser = (
    season_df[season_df["teaser_flag"] != ""]
    .groupby("Team")["Teaser_Result"]
    .agg(["count", lambda x: (x == "Win").sum()])
)

team_teaser.columns = ["Teaser Plays", "Teaser Wins"]
team_teaser["Teaser Losses"] = team_teaser["Teaser Plays"] - team_teaser["Teaser Wins"]
team_teaser["Win %"] = (team_teaser["Teaser Wins"] / team_teaser["Teaser Plays"] * 100).round(2)

st.dataframe(team_teaser, use_container_width=True)

# -----------------------------------------
# Week‑by‑week breakdown
# -----------------------------------------
st.subheader("Week‑by‑Week ATS Results")

week_summary = (
    season_df.groupby("week")["cover_flag"]
    .agg(["count", "sum"])
    .rename(columns={"count": "Games", "sum": "ATS Wins"})
)

week_summary["ATS Losses"] = week_summary["Games"] - week_summary["ATS Wins"]
week_summary["Win %"] = (week_summary["ATS Wins"] / week_summary["Games"] * 100).round(2)

st.dataframe(week_summary, use_container_width=True)

# -----------------------------------------
# Download Year Summary (auto-sized Excel)
# -----------------------------------------
from excel_utils import autosize_excel

export_df = season_df.copy()
buffer = autosize_excel(export_df)

st.download_button(
    label="Download Full Season Summary",
    data=buffer,
    file_name="Season_Summary.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

team_buffer = autosize_excel(team_summary)

st.download_button(
    label="Download Team-Level ATS Summary",
    data=team_buffer,
    file_name="Team_ATS_Summary.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

week_buffer = autosize_excel(week_summary)

st.download_button(
    label="Download Week-by-Week ATS Summary",
    data=week_buffer,
    file_name="Week_ATS_Summary.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
