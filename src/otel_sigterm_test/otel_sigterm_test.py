import signal
import time
import os

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    ConsoleSpanExporter,
    SimpleSpanProcessor,
)

# OpenTelemetry 初期化
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)
span_processor = SimpleSpanProcessor(ConsoleSpanExporter())
trace.get_tracer_provider().add_span_processor(span_processor)


def handle_sigterm(signum, frame):
    print(f"\nReceived SIGTERM ({signum}). Shutting down tracer...")
    trace.get_tracer_provider().shutdown()
    print("Tracer shutdown complete. Exiting.")
    exit(0)


# SIGTERMを捕捉
signal.signal(signal.SIGTERM, handle_sigterm)

print(f"Running... PID = {os.getpid()}")

while True:
    with tracer.start_as_current_span("test-span"):
        print("Doing some traced work...")
        time.sleep(5)