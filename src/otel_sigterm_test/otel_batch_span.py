import os
import time
import signal
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

# トレースプロバイダーとエクスポーターの設定
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# ConsoleSpanExporter を設定
console_exporter = ConsoleSpanExporter()
span_processor = BatchSpanProcessor(console_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

pid = os.getpid()
print(f"このスクリプトの PID は {pid} です。")

# スパンを開始
span = tracer.start_span("sample_span")
print("Running... Press CTRL+C to exit or send SIGTERM")

# SIGTERM シグナルのハンドラー
def handle_sigterm(signal_number, frame):
    print("Received SIGTERM, ending span and flushing spans...")
    span.end()  # スパンを終了
    # success = span_processor.force_flush(timeout_millis=5000)  # 5秒間待機
    # if success:
    #     print("Spans successfully flushed.")
    # else:
    #     print("Timeout occurred while flushing spans.")
    trace.get_tracer_provider().shutdown()
    print("Flushed. Exiting...")
    exit(0)

# シグナルハンドラーを登録
signal.signal(signal.SIGTERM, handle_sigterm)

# メイン処理
try:
    time.sleep(60)  # 60秒間スリープして、手動でSIGTERMを送信
except KeyboardInterrupt:
    handle_sigterm(None, None)