import streamlit as st
import pandas as pd
import os
from utils.resourceController import startDefense

st.set_page_config(page_title="Network Protecter", layout="wide")

st.title("Network Protecter Settings")
on = st.toggle("Activate Defense")

memoryCol, attackerCol = st.columns(2)
with memoryCol:
      tresholdMemory = st.slider("Treshold Memory (%)", min_value=0.0, max_value=100.0, value=50.0, step=.01)
with attackerCol:
      tresholdAttacker = st.slider("Treshold Attacker (%)", min_value=0.0, max_value=100.0, value=50.0, step=.01)
wait_time = st.slider("Time for traffic analysis (s)", min_value=0.0, max_value=30.0, value=15.0, step=0.1)
st.divider()
if on:
      defense_data = startDefense(tresholdMemory=tresholdMemory, tresholdAttacker=tresholdAttacker, wait_time=wait_time)
      print(f"Defense: {defense_data}")
      trafficRecord = defense_data["history"]
      ip_counts_dict = defense_data["ip_counts"]
      ip = defense_data["ip"]
      underAttack = defense_data["under_attack"]


      # if ip is not None:
      #       # Initialize subprocess to ban ip and capture the return code
      #       ban_success = os.system(f"bash utils/banIP.bash {ip}") == 0
      #       if ban_success:
      #             st.success(f"Successfully banned IP: {ip}")
      #       else:
      #             st.error(f"Failed to ban IP: {ip}")


      if trafficRecord is not None:
        trafficRecord = pd.DataFrame(trafficRecord)
        ip_counts_df = pd.DataFrame.from_dict(
                ip_counts_dict, 
                orient='index', 
                columns=['Packets', 'Percentage of total taffic']
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
                  st.write(f":red[False]")

      st.divider()
      st.subheader("Traffic Record")
      col4, col5 = st.columns(2)
      with col4:
            st.markdown("**Traffic Record**")
            st.dataframe(trafficRecord)
      with col5:
            st.markdown("**IP Counts**")
            st.dataframe(ip_counts_df)
