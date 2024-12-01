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
    ban_duration = data.get('ban_duration', 60)
    print(f"Wait time: {wait_time}")
    print(f"Ban duration: {ban_duration}")
    
    def block_ip(ip, ban_duration=60):
        try:
            # Use /tmp directory for rules
            rules_dir = '/tmp/pf_rules'
            os.makedirs(rules_dir, exist_ok=True)
            
            # Create a temporary rule file for this IP
            rule_file = f'{rules_dir}/rule_{ip.replace(".", "_")}.conf'
            with open(rule_file, 'w') as f:
                f.write(f'block in from {ip} to any\n')
            
            # Add the rule
            subprocess.run(['/usr/bin/sudo', '/sbin/pfctl', '-f', rule_file], check=True)
            subprocess.run(['/usr/bin/sudo', '/sbin/pfctl', '-E'], check=True)
            print(f"Successfully blocked IP: {ip}")
            
            # Schedule unban
            def unban():
                time.sleep(ban_duration)
                try:
                    # Remove the rule file
                    os.remove(rule_file)
                    # Reload the default rules file
                    subprocess.run(['/usr/bin/sudo', '/sbin/pfctl', '-f', '/etc/pf.conf'], check=True)
                    print(f"Successfully unbanned IP: {ip}")
                    return True
                except Exception as e:
                    print(f"Failed to unban IP: {str(e)}")
                    return False

            # Start unban thread
            threading.Thread(target=unban, daemon=True).start()
        except Exception as e:
            print(f"Failed to block IP: {str(e)}")

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
        under_attack, ip, ip_counts = defense.analyze_traffic(tresholdAttacker=tresholdAttacker)

        banned = False
        if under_attack and ip:
            banned = block_ip(ip, ban_duration)

        result = {
              "under_attack": under_attack,
              "ip": ip,
              "ip_counts": ip_counts,
              "banned": banned
        }       

        print(f"Result: {result}")
        return json.dumps(result)
    return host_function()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12345)