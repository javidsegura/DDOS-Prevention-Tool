import pandas as pd 
import streamlit as st
import subprocess

HOST_IP = str(subprocess.check_output(['ipconfig', 'getifaddr', 'en0']).decode('utf-8').strip()) # Gets local IP addrs

class DefendStrategy:
      def __init__(self):
            self.path = "data/trafficResults.csv"

      def analyze_traffic(self) -> tuple[bool, str, pd.DataFrame, pd.Series]:
            """ Returns [under attack, ip address attacker, dataframe of all traffic, ip counts] """

            df = pd.read_csv(self.path)

            # Clean dataset. Only keep non-local traffic and traffic sent to local ip address
            df = df[df["dest_ip"] == HOST_IP]

            # Get ip address that has sent the msot
            ip_counts = df["src_ip"].value_counts()
            
            # Add new col percentage of traffic for each ip address
            ip_counts["percentage"] = ip_counts / len(df)

            # Most frequent ip address (that is not own)
            most_frequent_ip = ip_counts[ip_counts.index != HOST_IP].idxmax()

            print("IP counts: ", ip_counts)
            print("Most frequent ip: ", most_frequent_ip)
            print("Ratio: ", ip_counts[most_frequent_ip] / len(df))

            # If most_frequent_ip has sent disproportionate amount of traffic, then we are under attack
            if ip_counts["percentage"][most_frequent_ip] > 0.2:
                  return True, most_frequent_ip, df, ip_counts
            else:
                  return False, None, df, ip_counts
