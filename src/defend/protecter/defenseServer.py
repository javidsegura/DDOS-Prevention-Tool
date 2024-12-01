from flask import Flask, request
import subprocess
import os
import time
import threading
import signal
from analyzeTraffic import DefendStrategy
import json

app = Flask(__name__)


@app.route('/trigger-defense', methods=['POST'])
def trigger_defense() -> dict:
    print("Triggering defense")
    data = request.get_json()
    wait_time = data.get('wait_time', 7)    # Default to 7 if not provided
    tresholdAttacker = data.get('tresholdAttacker', 0.2)
    print(f"Wait time: {wait_time}")
    def host_function():
        print("Starting to sniff the network...")
        # Start packet sniffer as a subprocess
        process = subprocess.Popen(['./packetSniffer/bin/packet_sniffer'])
        
        # Wait for 7 seconds
        time.sleep(wait_time)
        
        # Terminate the process
        process.terminate()
        process.wait()  # Wait for the process to actually terminate

        print("Analyzing the traffikkk")

        # Start analyzing the traffic
        defense = DefendStrategy()
        under_attack, ip, history, ip_counts = defense.analyze_traffic(tresholdAttacker=tresholdAttacker)

        result = {
              "under_attack": under_attack,
              "ip": ip,
              "history": history.to_dict(),
              "ip_counts": ip_counts
        }       

        print(f"Result: {result}")
        return json.dumps(result)
    return host_function()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12345)