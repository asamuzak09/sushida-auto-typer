# 寿司打自動タイピングツール

[寿司打](https://sushida.net/play.html) で表示されるローマ字を自動的に認識し、入力するツールです。

## 機能

- 画面からローマ字テキストを自動認識（小文字アルファベットの数が最も多い行を選択）
- 認識したテキストを自動入力（テキスト全体を一度に入力）
- 特殊文字（ハイフン、クエスチョンマーク、感嘆符）にも対応
- テキスト領域の自動検出と調整
- デバッグモードによる動作確認

## 必要環境

- Python 3.8以上
- Tesseract OCR 5.0以上
- 必要なPythonパッケージ（requirements.txtに記載）

## インストール方法

1. このリポジトリをクローンまたはダウンロードします

```bash
git clone https://github.com/yourusername/sushida-auto-typer.git
cd sushida-auto-typer
```

2. 必要なPythonパッケージをインストールします

```bash
pip install -r requirements.txt
```

3. Tesseract OCRをインストールします

- Windows: [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)からインストーラをダウンロード
- macOS: `brew install tesseract`
- Linux: `sudo apt-get install tesseract-ocr`

## 使用方法

1. 寿司打のウェブサイト [https://sushida.net/play.html](https://sushida.net/play.html) を開きます
2. ゲームを開始し、タイピング画面が表示されるところまで手動で進めます
3. 以下のコマンドでツールを実行します

```bash
python main.py
```

4. 画面の指示に従って設定を行います
5. カウントダウン後、ゲーム画面にフォーカスすると自動タイピングが開始されます
6. 停止するには、ターミナルウィンドウに戻り、Ctrl+Cを押します

## 設定のカスタマイズ

`config.py`ファイルを編集することで、以下の設定をカスタマイズできます：

- テキスト領域の座標（画面によって調整が必要な場合があります）
- OCRの実行間隔（`OCR_INTERVAL`）- 小さくするほど高速だが負荷が増加
- デバッグモード（動作確認用の出力を表示）

## トラブルシューティング

### テキストが正しく認識されない場合

1. デバッグモードを有効にして、認識結果を確認します
2. `debug_capture.png`と`debug_processed.png`を確認し、テキスト領域が正しく切り出されているか確認します
3. テキスト領域の座標を調整します（`config.py`の`TEXT_REGION`）
4. 小文字アルファベットの数が最も多い行が選択されているか確認します

### 入力が正しく行われない場合

1. ゲーム画面が正しくフォーカスされているか確認します
2. OCRの実行間隔を調整します（`config.py`の`OCR_INTERVAL`）
3. キーボードレイアウトがゲームと一致しているか確認します
4. 前回と同じテキストでも再入力するようになっているため、入力が重複する場合があります

## 注意事項

- このツールは学習目的で作成されています
- 長時間の使用や公式大会での使用は避けてください
- 画面解像度やゲームの表示によっては、テキスト領域の座標調整が必要な場合があります

## ライセンス

MITライセンス
