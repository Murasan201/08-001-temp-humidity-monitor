#!/usr/bin/env python3
"""
DHT11温度・湿度測定プログラム（基本版）
DHT11センサーから温度と湿度を定期的に読み取り、コンソールに表示します。
"""

# 標準ライブラリ
import time

# サードパーティライブラリ
import board
import adafruit_dht

# 定数
GPIO_PIN = board.D4  # DHT11センサーが接続されているGPIOピン
MEASUREMENT_INTERVAL = 2.0  # 測定間隔（秒）


def setup_sensor():
    """
    DHT11センサーを初期化する

    Returns:
        adafruit_dht.DHT11: 初期化されたDHT11センサーオブジェクト
    """
    dht_device = adafruit_dht.DHT11(GPIO_PIN)
    print("DHT11センサーを初期化しました")
    return dht_device


def read_sensor_data(dht_device):
    """
    センサーから温度と湿度を読み取る

    Args:
        dht_device: DHT11センサーオブジェクト

    Returns:
        tuple: (温度(°C), 湿度(%)) または (None, None) エラー時
    """
    try:
        temperature_c = dht_device.temperature
        humidity = dht_device.humidity
        return temperature_c, humidity
    except RuntimeError as error:
        # センサーの読み取りエラーは比較的頻繁に発生します
        print(f"センサー読み取りエラー: {error.args[0]}")
        return None, None


def display_data(temperature_c, humidity):
    """
    測定データをコンソールに表示する

    Args:
        temperature_c (float): 温度（摂氏）
        humidity (float): 湿度（％）
    """
    if temperature_c is not None and humidity is not None:
        # 華氏に変換
        temperature_f = temperature_c * (9 / 5) + 32
        print(f"温度: {temperature_c:.1f}°C ({temperature_f:.1f}°F)  湿度: {humidity:.1f}%")


def cleanup_sensor(dht_device):
    """
    センサーのリソースを解放する

    Args:
        dht_device: DHT11センサーオブジェクト
    """
    dht_device.exit()
    print("センサーをクリーンアップしました")


def main():
    """
    メイン処理：センサーから定期的にデータを読み取り表示する
    """
    dht_device = setup_sensor()

    print("DHT11センサーから温度と湿度を測定します")
    print("Ctrl+Cで終了します")

    try:
        while True:
            # センサーデータを読み取り
            temperature_c, humidity = read_sensor_data(dht_device)

            # データを表示
            display_data(temperature_c, humidity)

            # DHT11は1秒に1回しか読み取れないため、2秒待機
            time.sleep(MEASUREMENT_INTERVAL)

    except KeyboardInterrupt:
        print("\n測定を終了します")
    finally:
        # 必ずセンサーをクリーンアップ
        cleanup_sensor(dht_device)


if __name__ == "__main__":
    main()
