#!/usr/bin/env python3
"""
温湿度モニタリングアプリ

DHT11センサーから温度・湿度データを取得し、
コンソール表示、LCD1602ディスプレイ表示、CSVファイル出力を行います。

要件定義書: 08-001_温湿度モニタリングアプリ_要件定義書.md
"""

# 標準ライブラリ
import argparse
import csv
import time
import signal
import sys
from datetime import datetime
from typing import Optional, Tuple

# サードパーティライブラリ
try:
    import Adafruit_DHT
    from RPLCD.i2c import CharLCD
except ImportError as e:
    print(f"必要なライブラリがインストールされていません: {e}")
    print("対処方法: pip3 install -r requirements.txt を実行してください")
    sys.exit(1)


class TemperatureHumidityMonitor:
    """
    温湿度モニタリングクラス
    初心者向けに機能を整理し、簡潔な実装にしています
    """

    def __init__(self, gpio_pin: int = 18, interval: int = 10,
                 csv_file: Optional[str] = None,
                 lcd_address: int = 0x27, lcd_port: int = 1):
        """
        温湿度モニターの初期化

        Args:
            gpio_pin (int): DHT11センサーが接続されているGPIOピン番号（通常18）
            interval (int): データ取得間隔（秒、最小1秒）
            csv_file (str): CSVログファイル名（指定しない場合はログ出力なし）
            lcd_address (int): LCD1602のI2Cアドレス（通常0x27または0x3F）
            lcd_port (int): I2Cポート番号（Raspberry Pi 5では通常1）
        """
        self.gpio_pin = gpio_pin
        self.interval = interval
        self.csv_file = csv_file
        # DHT11センサー型を指定（DHT22の場合はAdafruit_DHT.DHT22に変更）
        self.sensor = Adafruit_DHT.DHT11
        self.running = True

        # RPLCDライブラリを使用してPCF8574搭載のI2C接続LCDを初期化
        # 前提リポジトリ（06-002-lcd1602-display）の実装方法に準拠
        # PCF8574はI2C拡張チップで、LCDとRaspberry Piの橋渡しをする
        try:
            self.lcd = CharLCD('PCF8574', lcd_address, port=lcd_port)
            self.lcd.clear()  # 画面をクリア
            self.lcd.write_string("温湿度モニタ")  # 起動メッセージ表示
            time.sleep(2)  # ユーザーが確認できるよう2秒待機
            print("LCD1602ディスプレイを初期化しました")
        except Exception as e:
            print(f"LCD初期化エラー: {e}")
            print("対処方法: I2C設定と配線を確認してください")
            print("ヒント: i2cdetect -y 1 でアドレスを確認")
            print("LCDなしで動作を継続します")
            self.lcd = None
        
        # CSVファイルヘッダー作成
        if self.csv_file:
            self._initialize_csv_file()
        
        # シグナルハンドラー設定（適切な終了処理）
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _initialize_csv_file(self) -> None:
        """
        CSVファイルの初期化（ヘッダー行の追加）

        CSVファイルを新規作成し、ヘッダー行（timestamp, temperature, humidity）を書き込む
        既存ファイルは上書きされるので注意
        """
        try:
            # CSVファイルを書き込みモードで開く（既存ファイルは上書き）
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                # ヘッダー行を書き込み（各列の意味を定義）
                writer.writerow(['timestamp', 'temperature', 'humidity'])
            print(f"CSVファイル '{self.csv_file}' を初期化しました")
        except Exception as e:
            print(f"CSVファイル初期化エラー: {e}")
            # エラー時はCSV出力を無効化
            self.csv_file = None
    
    def _signal_handler(self, signum, frame) -> None:
        """
        シグナルハンドラー（Ctrl+C や kill コマンドで適切に終了）

        Args:
            signum: 受信したシグナル番号
            frame: 現在のスタックフレーム（Pythonが自動的に渡す）
        """
        print("\n終了シグナルを受信しました。クリーンアップ中...")
        self.running = False  # メインループを停止
        if self.lcd:
            try:
                self.lcd.clear()
                self.lcd.write_string("終了しました")  # 終了メッセージ表示
                time.sleep(1)  # ユーザーが確認できるよう待機
                self.lcd.clear()  # 画面をクリアして終了
            except Exception as e:
                print(f"LCD終了処理エラー: {e}")
        sys.exit(0)  # プログラムを正常終了
    
    def read_sensor_data(self) -> Tuple[Optional[float], Optional[float]]:
        """
        DHT11センサーからデータを読み取り

        Returns:
            Tuple[temperature, humidity]: 温度（℃）と湿度（％）
            読み取り失敗時はNone値を返す
        """
        try:
            # DHT11センサーからデータ読み取り（3回リトライ）
            # read_retry関数はAdafruit_DHTライブラリの機能で自動的にリトライする
            for attempt in range(3):
                humidity, temperature = Adafruit_DHT.read_retry(
                    self.sensor, self.gpio_pin, retries=2, delay_seconds=0.5
                )

                # センサーから正常にデータが取得できたか確認
                if humidity is not None and temperature is not None:
                    # データ妥当性チェック（DHT11の仕様範囲内か確認）
                    # DHT11: 湿度0-100%, 温度0-50℃（余裕を持って-40-80℃で判定）
                    if 0 <= humidity <= 100 and -40 <= temperature <= 80:
                        # 小数点1桁に丸めて返す
                        return round(temperature, 1), round(humidity, 1)
                    else:
                        print(f"異常値検出: 温度={temperature}℃, 湿度={humidity}%")

                # リトライメッセージ表示（最終回は表示しない）
                if attempt < 2:
                    print(f"読み取り失敗、リトライ中... ({attempt + 1}/3)")
                    time.sleep(1)

            print("センサーデータの読み取りに失敗しました")
            print("対処方法: センサーの配線とGPIOピン番号を確認してください")
            return None, None

        except Exception as e:
            print(f"センサー読み取りエラー: {e}")
            print("対処方法: DHT11センサーが正しく接続されているか確認してください")
            return None, None
    
    def display_console(self, temperature: Optional[float], 
                       humidity: Optional[float], timestamp: str) -> None:
        """
        コンソールにデータ表示
        
        Args:
            temperature: 温度（℃）
            humidity: 湿度（％）
            timestamp: タイムスタンプ
        """
        if temperature is not None and humidity is not None:
            print(f"{timestamp} - 温度: {temperature}℃, 湿度: {humidity}%")
        else:
            print(f"{timestamp} - データ読み取り失敗")
    
    def display_lcd(self, temperature: Optional[float],
                   humidity: Optional[float]) -> None:
        """
        LCD1602ディスプレイにデータ表示（前提リポジトリの実装方法に準拠）

        Args:
            temperature (float): 温度（℃）
            humidity (float): 湿度（％）
        """
        # LCDが初期化されていない場合は何もしない
        if not self.lcd:
            return

        try:
            # 画面をクリアして新しいデータを表示
            self.lcd.clear()

            if temperature is not None and humidity is not None:
                # 1行目: 温度表示（LCD1602は16文字×2行）
                line1 = f"温度: {temperature}C"
                self.lcd.write_string(line1)

                # 2行目: 湿度表示（crlf()で改行）
                self.lcd.crlf()
                line2 = f"湿度: {humidity}%"
                self.lcd.write_string(line2)
            else:
                # エラー時の表示
                self.lcd.write_string("読み取りエラー")

        except Exception as e:
            print(f"LCD表示エラー: {e}")
    
    def log_to_csv(self, temperature: Optional[float],
                   humidity: Optional[float], timestamp: str) -> None:
        """
        CSVファイルにデータ出力（追記モード）

        Args:
            temperature (float): 温度（℃）
            humidity (float): 湿度（％）
            timestamp (str): タイムスタンプ（YYYY-MM-DD HH:MM:SS形式）
        """
        # CSVファイルが指定されていない場合は何もしない
        if not self.csv_file:
            return

        try:
            # CSVファイルを追記モードで開く（既存データは保持）
            with open(self.csv_file, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                # データ行を追記（タイムスタンプ, 温度, 湿度）
                writer.writerow([timestamp, temperature, humidity])
        except Exception as e:
            print(f"CSVファイル書き込みエラー: {e}")
    
    def run_monitoring(self) -> None:
        """
        メインの監視ループ：定期的にセンサーデータを取得・表示
        """
        print("温湿度モニタリングを開始します...")
        print(f"測定間隔: {self.interval}秒")
        print(f"GPIOピン: {self.gpio_pin}")
        if self.csv_file:
            print(f"CSVログ: {self.csv_file}")
        print("Ctrl+C で終了")
        print("-" * 50)

        try:
            while self.running:
                # 現在時刻取得（タイムスタンプ形式）
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # センサーデータ読み取り
                temperature, humidity = self.read_sensor_data()

                # コンソール表示
                self.display_console(temperature, humidity, timestamp)

                # LCD表示
                self.display_lcd(temperature, humidity)

                # CSVログ出力
                self.log_to_csv(temperature, humidity, timestamp)

                # 指定間隔で待機（次の測定まで）
                time.sleep(self.interval)

        except KeyboardInterrupt:
            # Ctrl+C が押された場合
            print("\nキーボード割り込みを受信しました")
        except Exception as e:
            print(f"予期しないエラー: {e}")
        finally:
            # 必ずリソースをクリーンアップ
            self._cleanup()
    
    def _cleanup(self) -> None:
        """
        リソースのクリーンアップ処理

        プログラム終了時に必ず実行される処理
        LCDディスプレイをクリアして、終了メッセージを表示
        """
        print("\nクリーンアップ中...")
        if self.lcd:
            try:
                self.lcd.clear()
                self.lcd.write_string("終了")  # 終了メッセージを表示
                time.sleep(1)  # ユーザーが確認できるよう待機
                self.lcd.clear()  # 画面をクリアして終了
            except Exception as e:
                print(f"LCD終了処理エラー: {e}")
        print("モニタリングを終了しました")


def main():
    """
    メイン関数：コマンドライン引数を処理して温湿度モニタリングを実行
    """
    # コマンドライン引数の設定
    parser = argparse.ArgumentParser(
        description="DHT11センサーを使用した温湿度モニタリングアプリ",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  python3 temp_humidity_monitor.py                    # 基本実行
  python3 temp_humidity_monitor.py --interval 30     # 30秒間隔で測定
  python3 temp_humidity_monitor.py --gpio 22         # GPIO22ピンを使用
  python3 temp_humidity_monitor.py --csv log.csv     # CSVファイルに記録
  python3 temp_humidity_monitor.py --lcd-addr 0x3f   # LCD I2Cアドレス指定
        """
    )

    # 引数の定義
    parser.add_argument(
        '--gpio', type=int, default=18,
        help='DHT11センサーのGPIOピン番号 (デフォルト: 18)'
    )
    parser.add_argument(
        '--interval', type=int, default=10,
        help='データ取得間隔（秒） (デフォルト: 10)'
    )
    parser.add_argument(
        '--csv', type=str, default=None,
        help='CSVログファイル名 (指定しない場合はログ出力なし)'
    )
    parser.add_argument(
        '--lcd-addr', type=lambda x: int(x, 0), default=0x27,
        help='LCD1602のI2Cアドレス (デフォルト: 0x27)'
    )
    parser.add_argument(
        '--lcd-port', type=int, default=1,
        help='I2Cポート番号 (デフォルト: 1)'
    )

    args = parser.parse_args()

    # 引数の妥当性検証
    if args.interval < 1:
        print("エラー: interval は1秒以上である必要があります")
        sys.exit(1)

    if not (1 <= args.gpio <= 40):
        print("エラー: GPIOピン番号は1-40の範囲である必要があります")
        sys.exit(1)

    try:
        # 温湿度モニターの初期化
        monitor = TemperatureHumidityMonitor(
            gpio_pin=args.gpio,
            interval=args.interval,
            csv_file=args.csv,
            lcd_address=args.lcd_addr,
            lcd_port=args.lcd_port
        )
        # モニタリング実行
        monitor.run_monitoring()

    except Exception as e:
        print(f"アプリケーションエラー: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()