# NOTE
1. Attacker (Alex)
2. Defender (Javid)
3. Monitor (Diego)

# PROCEDURE
0. Go to src/defend/docker and build image 
1. Run the container script in src/defend/docker/scripts/weakApp.bash
2. Open the defender server running the script in other/scripts/defenseServer.bash
3. From the container start the webapp



# Network Protection System
A real-time network traffic monitoring and DDoS protection system built with Python, Streamlit, and Docker.


## Features
The system provides real-time monitoring of:
- Container memory usage
- Network traffic patterns
- Potential attacker IPs
- Traffic distribution statistics

## Set-up
1. Clone the repository
```
git clone https://github.com/javidsegura/Network-Protection-Tool.git
```
2. Run make to compile source code
```
clear make
make
```
3. Install dependencies with pip
```
pip install -r requirements.txt
```
4. Build the docker image
```
bash src/defend/docker/createDockerImage.bash
```
5. Start defense server
```
bash other/scripts/defenseServer.bash
```
6. Start webapp from container
```
bash src/defend/docker/startWebApp.bash
```
7. Initialize the attack
```
bash other/scripts/attack.bash
```



# OTHER 
- Show banned rules
```
sudo pfctl -sr
```
- Show banned IPs
```
sudo pfctl -t blockedips -T show
```