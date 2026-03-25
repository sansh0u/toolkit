import subprocess
import logging
config = [1]
cmd1 = [
    f"-in={config}"]
print(cmd1)
subprocess.run(cmd1, check=True)