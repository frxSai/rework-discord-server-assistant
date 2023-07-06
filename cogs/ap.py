import subprocess
import re

# Define the Go command
go_command = ['go', 'run', '.\\steamserverinfo.go', '103.152.197.191', '2303']

# Run the Go command and capture the output
result = subprocess.run(go_command, capture_output=True, text=True)

# Parse the captured output
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
ping = server_info.get("PING", "")

# Combine the extracted fields into a single string
server_info_string = "Server Name: {}, Number of Players: {}, Maximum Players: {}, Ping: {}".format(
    server_info.get("NAME", ""),
    server_info.get("PLAYERS", ""),
    server_info.get("MAXPLAYERS", ""),
    server_info.get("PING", "")
)

# Print the server information
print(server_info_string)
