#!/usr/bin/env python3
"""
温湿度モニタリングアプリ
"""

import time
import board
import adafruit_dht

# DHT11センサーを初期化（GPIO4ピンを使用）
dht = adafruit_dht.DHT11(board.D4)

print("DHT11 温湿度モニター")
print("Ctrl+Cで終了")
print("-" * 30)

try:
    while True:
        try:
            # 温度と湿度を取得
            temperature = dht.temperature
            humidity = dht.humidity
            print(f"温度: {temperature}°C  湿度: {humidity}%")
        except RuntimeError as e:
            # センサー読み取りエラー時は次回再試行
            print(f"読み取りエラー: {e}")

        # 2秒待機（DHT11の最小読み取り間隔は1秒）
        time.sleep(2)

except KeyboardInterrupt:
    print("\n終了します")

finally:
    # センサーのリソースを解放
    dht.exit()
