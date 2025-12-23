#!/usr/bin/env python3
"""
DHT11温度・湿度測定プログラム（基本版）
DHT11センサーから温度と湿度を定期的に読み取り、コンソールに表示します。
要件定義書: 08-001_温湿度モニタリングアプリ_要件定義書.md
"""

# 標準ライブラリ
import sys
import time

# サードパーティライブラリ
# adafruit_dhtはDHT11/DHT22センサーを制御するためのライブラリです
# 名前に「CircuitPython」とありますが、Raspberry Pi上の通常のPythonで使えます
# インストール: pip install adafruit-circuitpython-dht adafruit-blinka lgpio
import board
import adafruit_dht

# =============================================================================
# 定数定義
# =============================================================================
# DHT11センサーが接続されているGPIOピン
# boardモジュールでは「D4」のようにピン番号を指定します
# GPIO4ピン（物理ピン7番）を使用
GPIO_PIN = board.D4

# 測定間隔（秒）
# DHT11は最小でも1秒間隔が必要なため、2秒に設定
MEASUREMENT_INTERVAL = 2.0


def setup_sensor():
    """
    DHT11センサーを初期化する

    Returns:
        adafruit_dht.DHT11: 初期化されたDHT11センサーオブジェクト
    """
    # DHT11センサーオブジェクトを作成
    # DHT22を使用する場合は adafruit_dht.DHT22(GPIO_PIN) に変更
    dht_device = adafruit_dht.DHT11(GPIO_PIN)
    return dht_device


def read_sensor_data(dht_device):
    """
    DHT11センサーから温度と湿度を読み取る

    DHT11センサーは通信が不安定なことがあり、読み取りに失敗することがあります。
    失敗した場合はNoneを返し、次の読み取りで再試行します。

    Args:
        dht_device: DHT11センサーオブジェクト

    Returns:
        tuple: (温度(°C), 湿度(%)) または (None, None) エラー時
    """
    try:
        # センサーから温度と湿度を取得
        # temperatureは摂氏、humidityはパーセント
        temperature = dht_device.temperature
        humidity = dht_device.humidity
        return temperature, humidity
    except RuntimeError as error:
        # センサーの読み取りエラーは比較的頻繁に発生します
        # エラーメッセージを表示して、次の読み取りで再試行
        print(f"読み取りエラー: {error.args[0]}")
        return None, None


def display_data(temperature, humidity):
    """
    測定データをコンソールに表示する

    Args:
        temperature (float): 温度（摂氏）
        humidity (float): 湿度（％）
    """
    if temperature is not None and humidity is not None:
        # 華氏に変換（アメリカなどで使用される温度単位）
        # 変換式: °F = °C × 9/5 + 32
        temperature_f = temperature * (9 / 5) + 32
        print(f"温度: {temperature:.1f}°C ({temperature_f:.1f}°F)  湿度: {humidity:.1f}%")


def cleanup_sensor(dht_device):
    """
    センサーのリソースを解放する

    プログラム終了時に必ず呼び出してリソースを解放します。

    Args:
        dht_device: DHT11センサーオブジェクト
    """
    dht_device.exit()
    print("センサーをクリーンアップしました。")


def main():
    """
    メイン処理：センサーから定期的にデータを読み取り表示する

    Ctrl+Cで終了できます。
    """
    print("=" * 50)
    print("DHT11 温湿度モニター（基本版）")
    print("=" * 50)
    print(f"GPIOピン: GPIO4")
    print(f"測定間隔: {MEASUREMENT_INTERVAL}秒")
    print("-" * 50)
    print("測定を開始します。Ctrl+Cで終了できます。")
    print("-" * 50)

    # センサーを初期化
    dht_device = setup_sensor()

    try:
        while True:
            # センサーデータを読み取り
            temperature, humidity = read_sensor_data(dht_device)

            # データを表示
            display_data(temperature, humidity)

            # 次の測定まで待機
            # DHT11は1秒に1回しか読み取れないため、余裕を持って2秒待機
            time.sleep(MEASUREMENT_INTERVAL)

    except KeyboardInterrupt:
        # Ctrl+Cが押された場合の処理
        print("\n")
        print("-" * 50)
        print("測定を終了します。")
        print("-" * 50)

    finally:
        # 必ずセンサーをクリーンアップ
        cleanup_sensor(dht_device)
        sys.exit(0)


if __name__ == "__main__":
    main()
