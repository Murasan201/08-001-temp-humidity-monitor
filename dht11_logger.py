#!/usr/bin/env python3
"""
DHT11温度・湿度ログ記録プログラム
DHT11センサーから温度と湿度を定期的に読み取り、CSVファイルに記録します。
"""

# 標準ライブラリ
import time
import csv
import datetime

# サードパーティライブラリ
import board
import adafruit_dht

# 定数
GPIO_PIN = board.D4  # DHT11センサーが接続されているGPIOピン
MEASUREMENT_INTERVAL = 60.0  # 測定間隔（秒）


def setup_sensor():
    """
    DHT11センサーを初期化する

    Returns:
        adafruit_dht.DHT11: 初期化されたDHT11センサーオブジェクト
    """
    dht_device = adafruit_dht.DHT11(GPIO_PIN)
    print("DHT11センサーを初期化しました")
    return dht_device


def create_csv_file():
    """
    CSVファイルを作成し、ヘッダー行を書き込む

    Returns:
        str: 作成したCSVファイル名
    """
    csv_filename = f"temperature_humidity_{datetime.date.today()}.csv"

    with open(csv_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['日時', '温度(°C)', '湿度(%)'])

    print(f"CSVファイル '{csv_filename}' を作成しました")
    return csv_filename


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
        print(f"センサー読み取りエラー: {error.args[0]}")
        return None, None


def log_to_csv(csv_filename, timestamp, temperature_c, humidity):
    """
    測定データをCSVファイルに記録する

    Args:
        csv_filename (str): CSVファイル名
        timestamp (str): タイムスタンプ
        temperature_c (float): 温度（摂氏）
        humidity (float): 湿度（％）
    """
    with open(csv_filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([timestamp, temperature_c, humidity])


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
    メイン処理：センサーから定期的にデータを読み取りCSVに記録する
    """
    dht_device = setup_sensor()
    csv_filename = create_csv_file()

    print(f"環境データを{csv_filename}に記録します")
    print("Ctrl+Cで終了します")

    try:
        while True:
            # センサーデータを読み取り
            temperature_c, humidity = read_sensor_data(dht_device)

            if temperature_c is not None and humidity is not None:
                # 現在時刻を取得
                now = datetime.datetime.now()
                timestamp = now.strftime('%Y-%m-%d %H:%M:%S')

                # コンソールに表示
                print(f"{timestamp} - 温度: {temperature_c:.1f}°C  湿度: {humidity:.1f}%")

                # CSVファイルに記録
                log_to_csv(csv_filename, timestamp, temperature_c, humidity)

            # 60秒間隔で測定（ログ記録用）
            time.sleep(MEASUREMENT_INTERVAL)

    except KeyboardInterrupt:
        print("\n測定を終了します")
    finally:
        # 必ずセンサーをクリーンアップ
        cleanup_sensor(dht_device)
        print(f"データは{csv_filename}に保存されました")


if __name__ == "__main__":
    main()
