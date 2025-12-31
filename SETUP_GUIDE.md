# セットアップガイド

温湿度モニタリングアプリの環境構築手順です。

## 動作環境

- Raspberry Pi 5
- Raspberry Pi OS Bookworm以降
- Python 3.9以上
- DHT11温湿度センサー

## ハードウェア接続

DHT11センサーをRaspberry Piに接続します。

| DHT11ピン | Raspberry Pi  | 説明       |
|-----------|---------------|------------|
| VCC (+)   | 3.3V (Pin 1)  | 電源       |
| DATA      | GPIO4 (Pin 7) | データ通信 |
| GND (-)   | GND (Pin 6)   | グランド   |

## ソフトウェアセットアップ

### 1. システムパッケージのインストール

```bash
sudo apt update
sudo apt install -y python3-pip python3-venv libgpiod3
```

### 2. 仮想環境の作成

Raspberry Pi OS Bookworm以降では仮想環境が必要です。

```bash
cd /home/pi/work/project/08-001-temp-humidity-monitor
python3 -m venv venv
```

### 3. 仮想環境の有効化

```bash
source venv/bin/activate
```

プロンプトに`(venv)`が表示されれば有効化されています。

### 4. Pythonライブラリのインストール

```bash
pip install adafruit-blinka adafruit-circuitpython-dht
```

## 動作確認

```bash
cd /home/pi/work/project/08-001-temp-humidity-monitor
source venv/bin/activate
python3 dht11_basic.py
```

正常に動作すると、2秒間隔で温度と湿度が表示されます。

```
DHT11 温湿度モニター
Ctrl+Cで終了
------------------------------
温度: 22°C  湿度: 65%
温度: 23°C  湿度: 64%
```

`Ctrl+C`で終了できます。

## トラブルシューティング

### ModuleNotFoundError: No module named 'board'

仮想環境が有効化されていません。

```bash
source venv/bin/activate
pip install adafruit-blinka adafruit-circuitpython-dht
```

### 読み取りエラー: DHT sensor not found

センサーが検出されません。配線を確認してください。

- VCCが3.3V (Pin 1)に接続されているか
- DATAがGPIO4 (Pin 7)に接続されているか
- GNDがGND (Pin 6)に接続されているか

### 読み取りエラー: Checksum did not validate

DHT11の仕様上、時々発生します。次の読み取りで自動リトライされます。

### PermissionError

GPIOへのアクセス権限がありません。

```bash
sudo usermod -aG gpio $USER
# 再ログインが必要
```

## クイックセットアップ

```bash
sudo apt update
sudo apt install -y python3-pip python3-venv libgpiod3
cd /home/pi/work/project/08-001-temp-humidity-monitor
python3 -m venv venv
source venv/bin/activate
pip install adafruit-blinka adafruit-circuitpython-dht
python3 dht11_basic.py
```
