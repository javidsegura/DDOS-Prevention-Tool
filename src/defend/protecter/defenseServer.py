from flask import Flask
import subprocess
import os
import time
import threading
import signal
from analyzeTraffic import DefendStrategy


app = Flask(__name__)


@app.route('/trigger-defense', methods=['POST'])
def trigger_defense() -> dict:
    def host_function():
        # Start packet sniffer as a subprocess
        process = subprocess.Popen(['./packetSniffer/bin/packet_sniffer'])
        
        # Wait for 7 seconds
        time.sleep(7)
        
        # Terminate the process
        process.terminate()
        process.wait()  # Wait for the process to actually terminate

        print("Analyzing the traffic")

        # Start analyzing the traffic
        defense = DefendStrategy()
        under_attack, ip, history, ip_counts = defense.analyze_traffic()

        result = {
              "under_attack": under_attack,
              "ip": ip,
              "history": history.to_dict(),
              "ip_counts": ip_counts.to_dict()
        }
        
        return result
    return host_function()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12345)