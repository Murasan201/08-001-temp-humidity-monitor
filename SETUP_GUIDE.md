# セットアップガイド

このガイドでは、温湿度モニタリングアプリを動作させるための環境構築手順を説明します。
初心者が1から構築できるよう、すべての手順を詳細に記載しています。

## 動作環境

- Raspberry Pi 5
- Raspberry Pi OS Bookworm以降
- Python 3.9以上
- DHT11温湿度センサー

## ハードウェア接続

### DHT11センサーの配線

| DHT11ピン | Raspberry Pi       | 説明                |
|-----------|--------------------|---------------------|
| VCC (+)   | 3.3V (Pin 1)       | 電源（3.3V）        |
| DATA      | GPIO4 (Pin 7)      | データ通信          |
| GND (-)   | GND (Pin 6)        | グランド            |

**注意**: 一部のDHT11モジュールにはプルアップ抵抗が内蔵されていない場合があります。その場合は、DATAピンとVCCの間に4.7kΩの抵抗を接続してください。

## ソフトウェアセットアップ

### 1. システムの更新

最初にシステムを最新の状態に更新します。

```bash
sudo apt update && sudo apt upgrade -y
```

### 2. 必要なシステムパッケージのインストール

以下のパッケージをインストールします。

```bash
sudo apt install -y python3-pip python3-venv libgpiod3 swig liblgpio-dev
```

**パッケージの説明**:
- `python3-pip`: Pythonパッケージマネージャー
- `python3-venv`: Python仮想環境を作成するためのツール
- `libgpiod3`: GPIO制御用ライブラリ（Bookwormではlibgpiod2ではなくlibgpiod3を使用）
- `swig`: lgpioのビルドに必要なコード生成ツール
- `liblgpio-dev`: lgpioのビルドに必要な開発ライブラリ

### 3. Python仮想環境の作成

Raspberry Pi OS Bookworm以降では、システム全体へのPythonパッケージのインストールが制限されています。
そのため、仮想環境（venv）を使用します。

```bash
# プロジェクトディレクトリに移動
cd /home/pi/work/project/08-001-temp-humidity-monitor

# 仮想環境を作成
python3 -m venv venv
```

### 4. 仮想環境を有効化

仮想環境を有効化します。**スクリプトを実行する前は必ずこのコマンドを実行してください。**

```bash
source venv/bin/activate
```

プロンプトの先頭に `(venv)` が表示されれば、仮想環境が有効化されています。

### 5. Pythonライブラリのインストール

仮想環境を有効化した状態で、以下のコマンドを実行します。

```bash
pip install adafruit-blinka adafruit-circuitpython-dht lgpio
```

**インストールされるパッケージ**:
- `adafruit-blinka`: Raspberry Pi上でCircuitPythonライブラリを使用するための互換レイヤー（`board`モジュールを提供）
- `adafruit-circuitpython-dht`: DHT11/DHT22センサー用ライブラリ（名前に「CircuitPython」とありますが、通常のPythonで使用可能）
- `lgpio`: Raspberry Pi 5のGPIO制御ライブラリ

または、requirements.txtを使用してインストールすることもできます：

```bash
pip install -r requirements.txt
```

### 6. GPIOの権限設定（必要に応じて）

GPIO操作に権限エラーが発生する場合は、ユーザーをgpioグループに追加します。

```bash
sudo usermod -aG gpio $USER
```

設定を反映するために、一度ログアウトして再ログインしてください。

## 動作確認

### 仮想環境を有効化

```bash
cd /home/pi/work/project/08-001-temp-humidity-monitor
source venv/bin/activate
```

### 基本スクリプトの実行

```bash
python3 dht11_basic.py
```

正常に動作すると、2秒間隔で温度と湿度が表示されます。

```
==================================================
DHT11 温湿度モニター（基本版）
==================================================
GPIOピン: GPIO4
測定間隔: 2.0秒
--------------------------------------------------
測定を開始します。Ctrl+Cで終了できます。
--------------------------------------------------
温度: 22.6°C (72.7°F)  湿度: 76.0%
温度: 22.6°C (72.7°F)  湿度: 76.0%
```

`Ctrl+C`で終了できます。

## トラブルシューティング

### ModuleNotFoundError: No module named 'board'

仮想環境が有効化されていないか、ライブラリがインストールされていません。

```bash
# 仮想環境を有効化
source venv/bin/activate

# ライブラリをインストール
pip install adafruit-blinka adafruit-circuitpython-dht lgpio
```

### ModuleNotFoundError: No module named 'lgpio'

lgpioがインストールされていません。以下を実行してください。

```bash
# 必要なシステムパッケージをインストール
sudo apt install -y swig liblgpio-dev

# lgpioをインストール
source venv/bin/activate
pip install lgpio
```

### 読み取りエラー: Checksum did not validate

これはDHT11センサーの仕様上、時々発生する正常なエラーです。次の読み取りで自動的にリトライされます。
頻発する場合は以下を確認してください：

1. **配線を確認**: VCC、DATA、GNDが正しく接続されているか
2. **プルアップ抵抗**: 4.7kΩのプルアップ抵抗が必要な場合がある
3. **配線の長さ**: 長い配線は避ける（30cm以内推奨）

### 読み取りエラー: DHT sensor not found

DHT11センサーが検出されません。以下を確認してください：

1. **配線を確認**: VCC、DATA、GNDが正しく接続されているか
2. **GPIO4に接続**: DATAピンがGPIO4（Pin 7）に接続されているか
3. **電源を確認**: VCCが3.3Vに接続されているか
4. **センサーの向き**: DHT11センサーの向きが正しいか

### PermissionError: /dev/gpiomem または /dev/gpiochip*

GPIOへのアクセス権限がありません。以下を実行してください。

```bash
sudo usermod -aG gpio $USER
# その後、再ログイン
```

### externally-managed-environment エラー

Raspberry Pi OS Bookworm以降で発生します。仮想環境を使用してください。

```bash
python3 -m venv venv
source venv/bin/activate
pip install <パッケージ名>
```

## インストール済みパッケージの確認

仮想環境を有効化した状態で、以下のコマンドを実行します。

```bash
pip list | grep -i adafruit
```

正常にインストールされていれば、以下のようなパッケージが表示されます：

```
Adafruit-Blinka                  8.x.x
adafruit-circuitpython-dht       4.x.x
Adafruit-PlatformDetect          3.x.x
...
```

## 仮想環境の終了

作業が終わったら、仮想環境を終了できます。

```bash
deactivate
```

---

## クイックセットアップ（コピー＆ペースト用）

以下のコマンドを順番に実行すると、環境構築が完了します。

```bash
# 1. システムパッケージのインストール
sudo apt update
sudo apt install -y python3-pip python3-venv libgpiod3 swig liblgpio-dev

# 2. プロジェクトディレクトリに移動
cd /home/pi/work/project/08-001-temp-humidity-monitor

# 3. 仮想環境の作成と有効化
python3 -m venv venv
source venv/bin/activate

# 4. Pythonライブラリのインストール
pip install adafruit-blinka adafruit-circuitpython-dht lgpio

# 5. 動作確認
python3 dht11_basic.py
```

---

## 依存関係まとめ

### システムパッケージ（apt）

| パッケージ名     | 説明                                      |
|------------------|-------------------------------------------|
| python3-pip      | Pythonパッケージマネージャー              |
| python3-venv     | Python仮想環境ツール                      |
| libgpiod3        | GPIO制御用ライブラリ                      |
| swig             | lgpioビルド用コード生成ツール             |
| liblgpio-dev     | lgpioビルド用開発ライブラリ               |

### Pythonパッケージ（pip）

| パッケージ名                   | 説明                                           |
|-------------------------------|------------------------------------------------|
| adafruit-blinka               | CircuitPython互換レイヤー（通常のPythonで使用可能） |
| adafruit-circuitpython-dht    | DHT11/DHT22センサーライブラリ                  |
| lgpio                         | Raspberry Pi 5 GPIO制御                        |

---

最終更新: 2025-12-23
