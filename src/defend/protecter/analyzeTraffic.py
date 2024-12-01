import pandas as pd 
import streamlit as st
import subprocess

HOST_IP = str(subprocess.check_output(['ipconfig', 'getifaddr', 'en0']).decode('utf-8').strip()) # Gets local IP addrs

class DefendStrategy:
      def __init__(self):
            self.path = "data/trafficResults.csv"

      def analyze_traffic(self, tresholdAttacker:float=0.2) -> tuple[bool, str, pd.DataFrame, pd.Series]:
            """ Returns [under attack, ip address attacker, dataframe of all traffic, ip counts] """

            df = pd.read_csv(self.path)
            df_original = df  # Store original dataframe
            total_traffic = len(df_original)  # Get total traffic count
            
            # Clean dataset. Only keep non-local traffic and traffic sent to local ip address
            df = df[df["dest_ip"] == HOST_IP]
            
            # Get ip address that has sent the most
            ip_counts = df["src_ip"].value_counts()
            
            # Filter out HOST_IP first
            filtered_counts = ip_counts[ip_counts.index != HOST_IP]

            # Filter out ips that dont have the XX.XXX.XX from the localhost ip address
            localPrefix = HOST_IP.split('.')[0] + '.' + HOST_IP.split('.')[1] + '.' + HOST_IP.split('.')[2]
            print(f"Local prefix: {localPrefix}")
            filtered_counts = filtered_counts[filtered_counts.index.str.startswith(localPrefix)]

            if filtered_counts.empty:
                  return False, None, df, ip_counts
            
            # Calculate percentages based on total traffic (including local)
            percentages = filtered_counts / total_traffic
            
            # Create restructured ip_counts dictionary
            ip_counts_dict = {
                  ip: [count, float(percentages[ip])] 
                  for ip, count in filtered_counts.items()
            }
            
            # Most frequent ip address (that is not own)
            most_frequent_ip = filtered_counts.index[0]
            percentageAttacker = percentages[most_frequent_ip] * 100
            
            print("IP counts: ", filtered_counts)
            print("Most frequent ip: ", most_frequent_ip)
            print("Ratio: ", percentageAttacker)
            print(f"Treshold attacker: {tresholdAttacker}, percentage: {percentageAttacker}")
            
            # If most_frequent_ip has sent disproportionate amount of traffic, then we are under attack
            if percentageAttacker > tresholdAttacker:
                  return True, most_frequent_ip, df, ip_counts_dict
            else:
                  return False, None, df, ip_counts_dict
