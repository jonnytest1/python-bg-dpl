import re

data='--publish "0.0.0.0:15748:4747/tcp" \\   --publish "0.0.0.0:15748:4747/tcp" \\'

repl=re.sub(r'--publish "0.0.0.0:([0-9]*):([0-9]*)/t',r'+-publish "0.0.0.0:20000-30000:\g<2>/t',data)

print(repl)
