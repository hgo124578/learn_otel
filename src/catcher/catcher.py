import os
import signal
import time
import sys


def handle_sigterm(signum, frame):
    print(f"Received signal {signum} (SIGTERM)", flush=True)
    sys.exit(0)


signal.signal(signal.SIGTERM, handle_sigterm)

print("Running... PID:", os.getpid(), flush=True)
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Received KeyboardInterrupt (Ctrl+C)", flush=True)
    