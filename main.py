# 寿司打自動タイピングツール - メインモジュール

import time
import cv2
import sys
import os
from screen_capture import (
    capture_text_region, preprocess_image,
    show_capture_region, adjust_capture_region, load_config
)
from ocr_handler import extract_text, clean_text, verify_text
from keyboard_input import type_text
from config import DEBUG, TEXT_REGION, OCR_INTERVAL

def main():
    """メイン実行関数"""
    # グローバル変数の宣言（使用前に行う必要がある）
    global TEXT_REGION
    
    print("="*50)
    print("寿司打自動タイピングツールを開始します")
    print("="*50)
    
    # 設定ファイルの読み込み
    if os.path.exists('capture_config.json'):
        load_config()
    
    # 初期設定
    print("\n[設定情報]")
    print(f"テキスト領域: X={TEXT_REGION['left']}, Y={TEXT_REGION['top']}, "
          f"幅={TEXT_REGION['width']}, 高さ={TEXT_REGION['height']}")
    print(f"デバッグモード: {'有効' if DEBUG else '無効'}")
    
    # キャプチャ領域を表示して調整
    print("\nキャプチャ領域を表示します")
    show_capture_region()
    
    print("\nキャプチャ領域を調整します")
    print("透明なウィンドウをマウスで移動・サイズ変更してください")
    print("調整が完了したら、Enterキーを押してください")
    adjust_capture_region()
    
    print("\nゲーム画面を表示し、タイピング画面になったら準備完了です。")
    input("準備ができたらEnterキーを押してください...")
    
    print("\n自動タイピングを開始します！ゲーム画面にフォーカスしてください")
    time.sleep(1)  # ゲーム画面に切り替える時間
    
    # メインループの変数初期化
    last_text = ""
    consecutive_failures = 0
    max_failures = 5  # 連続失敗の最大回数
    total_words = 0
    
    try:
        print("\n実行中... (Ctrl+Cで停止)")
        
        # メインループ
        while consecutive_failures < max_failures:
            # テキスト領域のキャプチャ
            text_region = capture_text_region()
            
            # 画像の前処理
            processed_image = preprocess_image(text_region)
            
            # テキスト抽出
            text = extract_text(processed_image)
            cleaned_text = clean_text(text)
            
            # テキスト検証（オプション）
            verified_text = verify_text(cleaned_text)
            
            # テキストが存在する場合は入力（前回と同じでも入力する）
            if verified_text:
                # 前回と同じテキストの場合はデバッグ出力
                if verified_text == last_text and DEBUG:
                    print(f"前回と同じテキスト: {verified_text}")
                
                # 常に高速タイピングを使用
                success = type_text(verified_text)
                
                if success:
                    last_text = verified_text
                    consecutive_failures = 0
                    total_words += 1
                else:
                    consecutive_failures += 1
            else:
                # テキストが検出されない場合
                if DEBUG:
                    print("テキストが検出されませんでした")
                
                consecutive_failures += 1
            
            # OCRの間隔を空ける
            time.sleep(OCR_INTERVAL)
        
        print(f"\n連続で{max_failures}回テキスト検出に失敗したため、自動タイピングを停止します。")
    
    except KeyboardInterrupt:
        print("\n自動タイピングを停止しました")
    
    except Exception as e:
        print(f"\nエラーが発生しました: {e}")
    
    finally:
        print(f"\n合計{total_words}個の単語を入力しました")
        print("プログラムを終了します")

if __name__ == "__main__":
    main()