import subprocess
import re

go_command = ['go', 'run', '.\\steamserverinfo.go', '103.152.197.191', '2303']
result = subprocess.run(go_command, capture_output=True, text=True)
output_lines = result.stdout.strip().split('\n')
server_info = {}
for line in output_lines:
    match = re.search(r'(\w+): (.+)', line)
    if match:
        key = match.group(1)
        value = match.group(2)
        server_info[key] = value

name = server_info.get("NAME", "")
players = server_info.get("PLAYERS", "")
max_players = server_info.get("MAXPLAYERS", "")
map = server_info.get("MAP","")
bots = server_info.get("BOTS","")
ping = server_info.get("PING", "")

print(f'Server:',name)
print(f'Online:',players, '/' ,max_players)
print(f'Ping:',ping)
print(f'map:',map)