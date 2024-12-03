import streamlit as st
import pandas as pd
import os
from utils.resourceController import startDefense
import subprocess

st.set_page_config(page_title="Network Protecter", layout="wide")

st.title("Network Protecter Settings")
on = st.toggle("Activate Defense")

memoryCol, attackerCol = st.columns(2)
with memoryCol:
      tresholdMemory = st.slider("Treshold Memory (%)", min_value=0.0, max_value=100.0, value=50.0, step=.01)
with attackerCol:
      tresholdAttacker = st.slider("Treshold Attacker (%)", min_value=0.0, max_value=100.0, value=50.0, step=.01)

waitCol, banCol = st.columns(2)
with waitCol:
      wait_time = st.slider("Time for traffic analysis (s)", min_value=0.0, max_value=30.0, value=8.0, step=0.1)
with banCol:
      ban_duration = st.slider("Ban duration (s)", min_value=0.0, max_value=3600.0, value=60.0, step=0.1)
st.divider()
if on:
      defense_data = startDefense(tresholdMemory=tresholdMemory, tresholdAttacker=tresholdAttacker, wait_time=wait_time, ban_duration=ban_duration)
      print(f"Defense: {defense_data}")
      ip_counts_dict = defense_data["ip_counts"]
      ip = defense_data["ip"]
      underAttack = defense_data["under_attack"]
      banned = defense_data["banned"]

      if underAttack:
            ip_counts_df = pd.DataFrame.from_dict(
                  ip_counts_dict, 
                  orient='index', 
                  columns=['Packets', 'Percentage of total taffic']
                  )
      else:
            ip_counts_df = pd.DataFrame.from_dict(
                  ip_counts_dict, 
                  orient='index', 
                  columns=['Packets']
                  )
      st.title("Network Analysis")
      st.subheader("Status")
      col1, col2, col3 = st.columns(3)
      with col1:
            st.markdown("**Under Attack**")
            st.markdown(":red[True]" if underAttack else ":green[False]")
      if underAttack:
            with col2:
                  st.markdown("**Attacker IP**")
                  st.write(f"IP: {ip}")
            with col3:
                  st.markdown("**Banned IP**")
                  st.write(f":red[False]" if banned else ":green[True]")

      st.divider()
      st.subheader("Traffic Record")

      st.markdown("**IP Counts**")
      st.dataframe(ip_counts_df)
