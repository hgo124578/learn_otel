import os
import signal

os.kill(27292, signal.SIGTERM)

print(f"send os kill")
