#!/usr/bin/env python3
# OCRテストスクリプト

import cv2
import os
import sys
from screen_capture import preprocess_image
from ocr_handler import extract_text, clean_text, verify_text

def test_ocr(image_path):
    """指定された画像に対してOCRを実行し、結果を表示する"""
    print(f"=== OCRテスト: {image_path} ===")
    
    # 画像が存在するか確認
    if not os.path.exists(image_path):
        print(f"エラー: 画像ファイルが見つかりません: {image_path}")
        return
    
    try:
        # 画像を読み込む
        print("1. 画像を読み込み中...")
        image = cv2.imread(image_path)
        if image is None:
            print(f"エラー: 画像の読み込みに失敗しました: {image_path}")
            return
        
        print(f"   画像サイズ: {image.shape[1]}x{image.shape[0]}")
        
        # 画像の前処理
        print("2. 画像の前処理を実行中...")
        processed_image = preprocess_image(image)
        print(f"   前処理後の画像サイズ: {processed_image.shape[1]}x{processed_image.shape[0]}")
        
        # OCRでテキストを抽出
        print("3. OCRでテキストを抽出中...")
        text = extract_text(processed_image)
        print(f"   抽出されたテキスト: '{text}'")
        
        # テキストのクリーニング
        print("4. テキストのクリーニング中...")
        cleaned_text = clean_text(text)
        print(f"   クリーニング後のテキスト: '{cleaned_text}'")
        
        # テキストの検証
        print("5. テキストの検証中...")
        verified_text = verify_text(cleaned_text)
        print(f"   検証後のテキスト: '{verified_text}'")
        
        print("\n=== 最終結果 ===")
        print(f"元のテキスト: '{text}'")
        print(f"処理後のテキスト: '{verified_text}'")
        
        # 結果の評価
        if verified_text:
            print("\n✅ OCRは成功しました！")
        else:
            print("\n❌ OCRは失敗しました（テキストが抽出されませんでした）")
        
    except Exception as e:
        print(f"エラー: OCRテスト中に例外が発生しました: {e}")

if __name__ == "__main__":
    # コマンドライン引数から画像パスを取得するか、デフォルトパスを使用
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        image_path = "ocr_images/debug_capture.png"
    
    test_ocr(image_path)