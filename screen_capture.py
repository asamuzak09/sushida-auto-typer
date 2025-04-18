# 寿司打自動タイピングツール - 画面キャプチャモジュール

import pyautogui
import cv2
import numpy as np
import time
import os
import json
import tkinter as tk
from config import TEXT_REGION, DEBUG

# OCR画像保存用ディレクトリ
OCR_IMAGES_DIR = 'ocr_images'

def ensure_dir_exists(directory):
    """ディレクトリが存在しない場合は作成する"""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"ディレクトリを作成しました: {directory}")

def capture_text_region():
    """テキスト表示領域のスクリーンショットを撮影して返す"""
    # OCR画像保存用ディレクトリを確保
    ensure_dir_exists(OCR_IMAGES_DIR)
    
    # 固定ファイル名
    capture_filename = os.path.join(OCR_IMAGES_DIR, 'debug_capture.png')
    
    try:
        # キャプチャ領域のみをスクリーンショット
        region = (
            TEXT_REGION['left'],
            TEXT_REGION['top'],
            TEXT_REGION['width'],
            TEXT_REGION['height']
        )
        
        # 直接領域を指定してスクリーンショット
        text_region = pyautogui.screenshot(region=region)
        
        # OpenCV形式に変換
        text_region_cv = cv2.cvtColor(np.array(text_region), cv2.COLOR_RGB2BGR)
        
        # 画像を保存（上書き）
        cv2.imwrite(capture_filename, text_region_cv)
    
    except Exception as e:
        print(f"[エラー] スクリーンショットの取得に失敗しました: {e}")
        # エラー時は黒い画像を返す
        text_region_cv = np.zeros((TEXT_REGION['height'], TEXT_REGION['width'], 3), dtype=np.uint8)
        
        # エラー情報を画像に書き込む
        cv2.putText(text_region_cv, f"Error: {str(e)}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    
    return text_region_cv

def show_capture_region():
    """テキスト領域を画像として保存する（ウィンドウは表示しない）"""
    # 画面全体のスクリーンショット
    screenshot = pyautogui.screenshot()
    screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    
    # テキスト領域を矩形で表示
    x1 = TEXT_REGION['left']
    y1 = TEXT_REGION['top']
    x2 = x1 + TEXT_REGION['width']
    y2 = y1 + TEXT_REGION['height']
    
    # 赤色の矩形を描画（太さ2ピクセル）
    cv2.rectangle(screenshot_cv, (x1, y1), (x2, y2), (0, 0, 255), 2)
    
    # 座標情報を表示
    info_text = f"X={x1}, Y={y1}, W={TEXT_REGION['width']}, H={TEXT_REGION['height']}"
    cv2.putText(screenshot_cv, info_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
    # 座標情報を表示
    print(f"\nキャプチャ領域: {info_text}")
    print("テキスト領域の設定を確認してください")
    
    return

def adjust_capture_region():
    """完全に透明なウィンドウを表示し、そのウィンドウの位置とサイズをリアルタイムでキャプチャ領域として使用する"""
    global TEXT_REGION
    
    # 現在の設定を取得
    left = TEXT_REGION['left']
    top = TEXT_REGION['top']
    width = TEXT_REGION['width']
    height = TEXT_REGION['height']
    
    print("\nキャプチャ領域の調整モードを開始します")
    print("透明なウィンドウをマウスで移動・サイズ変更してください")
    print("ウィンドウの位置とサイズは常にキャプチャ領域として使用されます")
    print("調整が完了したら、Enterキーを押してください")
    
    # tkinterウィンドウを作成
    root = tk.Tk()
    root.title("キャプチャ領域の調整")
    root.geometry(f"{width}x{height}+{left}+{top}")  # 初期位置とサイズを設定
    root.attributes('-topmost', True)  # 最前面に表示
    root.wm_attributes("-transparent", True)  # ウィンドウを透明に
    
    # 透明なフレームを作成
    frame = tk.Frame(root, width=width, height=height)
    frame.configure(bg="systemTransparent")  # macOSの透明背景
    frame.pack(fill=tk.BOTH, expand=True)
    
    # フレームとキャンバスを正しく設定
    frame.pack_propagate(False)  # フレームのサイズを固定
    
    # 枠線を作成（キャンバスを使用）
    canvas = tk.Canvas(frame, highlightthickness=0)
    canvas.configure(bg="systemTransparent")  # macOSの透明背景
    canvas.pack(fill=tk.BOTH, expand=True)
    
    # 矩形を描画（赤色、線の太さ2ピクセル）
    rectangle = canvas.create_rectangle(
        0, 0, width, height,
        outline='red', width=2
    )
    
    # 説明ラベルを追加（透明背景）
    label = tk.Label(
        frame,
        text="このウィンドウをマウスで移動・サイズ変更してください\nEnterキーを押すと確定します",
        fg='white',
        font=('Arial', 12)
    )
    label.configure(bg="systemTransparent")  # macOSの透明背景
    label.place(relx=0.5, rely=0.3, anchor='center')
    
    # 座標情報を表示するラベル（透明背景）
    info_label = tk.Label(
        frame,
        text=f"X={left}, Y={top}, 幅={width}, 高さ={height}",
        fg='white',
        font=('Arial', 12)
    )
    info_label.configure(bg="systemTransparent")  # macOSの透明背景
    info_label.place(relx=0.5, rely=0.7, anchor='center')
    
    # ウィンドウサイズ変更時のイベント処理
    def on_resize(event=None):
        # 現在のウィンドウサイズを取得
        current_width = root.winfo_width()
        current_height = root.winfo_height()
        
        # フレームのサイズを更新
        frame.config(width=current_width, height=current_height)
        
        # キャンバスのサイズを更新
        canvas.config(width=current_width, height=current_height)
        
        # 矩形のサイズを更新（ウィンドウ全体をカバー）
        canvas.coords(rectangle, 0, 0, current_width, current_height)
        
        # 座標情報を更新
        current_left = root.winfo_x()
        current_top = root.winfo_y()
        info_label.config(text=f"X={current_left}, Y={current_top}, 幅={current_width}, 高さ={current_height}")
    
    # 初期サイズで更新
    root.update_idletasks()
    on_resize()
    
    # ウィンドウサイズ変更イベントをバインド
    root.bind("<Configure>", on_resize)
    
    # 説明ラベルを追加（透明背景）
    label = tk.Label(
        frame,
        text="このウィンドウをマウスで移動・サイズ変更してください\nEnterキーを押すと確定します",
        fg='white',
        font=('Arial', 12)
    )
    label.configure(bg="systemTransparent")  # macOSの透明背景
    label.place(relx=0.5, rely=0.3, anchor='center')
    
    # 座標情報を表示するラベル（透明背景）
    info_label = tk.Label(
        frame,
        text=f"X={left}, Y={top}, 幅={width}, 高さ={height}",
        fg='white',
        font=('Arial', 12)
    )
    info_label.configure(bg="systemTransparent")  # macOSの透明背景
    info_label.place(relx=0.5, rely=0.7, anchor='center')
    
    # キーボードイベントを処理する関数
    def on_key_press(event):
        if event.keysym == 'Return':  # Enterキー
            # 現在のウィンドウの位置とサイズを取得
            current_left = root.winfo_x()
            current_top = root.winfo_y()
            current_width = root.winfo_width()
            current_height = root.winfo_height()
            
            # キャプチャ領域を更新
            TEXT_REGION['left'] = current_left
            TEXT_REGION['top'] = current_top
            TEXT_REGION['width'] = current_width
            TEXT_REGION['height'] = current_height
            
            # 設定を保存して終了
            save_config()
            print("Enterキーが押されました - 設定を保存しました")
            
            # ウィンドウを閉じる（プログラムは続行）
            root.destroy()
            root.update()
    
    # キーボードイベントをバインド
    root.bind('<KeyPress>', on_key_press)
    
    # ウィンドウが閉じられたときの処理
    def on_close():
        # 現在のウィンドウの位置とサイズを取得
        current_left = root.winfo_x()
        current_top = root.winfo_y()
        current_width = root.winfo_width()
        current_height = root.winfo_height()
        
        # キャプチャ領域を更新
        TEXT_REGION['left'] = current_left
        TEXT_REGION['top'] = current_top
        TEXT_REGION['width'] = current_width
        TEXT_REGION['height'] = current_height
        
        # 設定を保存して終了
        save_config()
        
        # ウィンドウを閉じる（プログラムは続行）
        root.destroy()
    
    # 閉じるボタンの処理をオーバーライド
    root.protocol("WM_DELETE_WINDOW", on_close)
    
    # イベントループを開始
    try:
        root.mainloop()
    except Exception as e:
        print(f"エラーが発生しました: {e}")
    
    # 最終的な設定を表示
    print(f"\n調整後のキャプチャ領域: X={TEXT_REGION['left']}, Y={TEXT_REGION['top']}, "
          f"幅={TEXT_REGION['width']}, 高さ={TEXT_REGION['height']}")
    
    return TEXT_REGION

def save_config():
    """設定をJSONファイルに保存する"""
    config_file = 'capture_config.json'
    with open(config_file, 'w') as f:
        json.dump(TEXT_REGION, f, indent=4)
    
    print(f"\n設定を保存しました: {config_file}")
    return

def load_config():
    """設定をJSONファイルから読み込む"""
    global TEXT_REGION
    
    config_file = 'capture_config.json'
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                loaded_config = json.load(f)
                
                # 必要なキーがすべて含まれているか確認
                required_keys = ['left', 'top', 'width', 'height']
                if all(key in loaded_config for key in required_keys):
                    TEXT_REGION = loaded_config
                    print(f"\n設定を読み込みました: {config_file}")
                    print(f"キャプチャ領域: X={TEXT_REGION['left']}, Y={TEXT_REGION['top']}, "
                          f"幅={TEXT_REGION['width']}, 高さ={TEXT_REGION['height']}")
                else:
                    print(f"\n設定ファイルの形式が正しくありません: {config_file}")
        except Exception as e:
            print(f"\n設定ファイルの読み込みに失敗しました: {e}")
    
    return TEXT_REGION

def preprocess_image(image):
    """OCR精度向上のための画像前処理"""
    # OCR画像保存用ディレクトリを確保
    ensure_dir_exists(OCR_IMAGES_DIR)
    
    # 固定ファイル名
    processed_filename = os.path.join(OCR_IMAGES_DIR, 'debug_processed.png')
    
    try:
        # グレースケール変換
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # 画像のサイズを3倍に拡大（OCRの精度向上のため）
        height, width = gray.shape
        enlarged = cv2.resize(gray, (width * 3, height * 3), interpolation=cv2.INTER_CUBIC)
        
        # ガウシアンブラーでノイズ軽減
        blurred = cv2.GaussianBlur(enlarged, (5, 5), 0)
        
        # 大津の二値化（グローバルな閾値を自動決定）
        _, binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # 膨張と収縮の組み合わせでテキストを強調
        kernel = np.ones((3, 3), np.uint8)
        dilated = cv2.dilate(binary, kernel, iterations=1)
        eroded = cv2.erode(dilated, kernel, iterations=1)
        
        # 処理後の画像を保存（上書き）
        cv2.imwrite(processed_filename, eroded)
        
        # 元の画像も保存（比較用）
        original_filename = os.path.join(OCR_IMAGES_DIR, 'debug_original.png')
        cv2.imwrite(original_filename, image)
        
        return eroded
        
    except Exception as e:
        print(f"[エラー] 画像の前処理に失敗しました: {e}")
        # エラー時は元の画像をそのまま返す
        cv2.imwrite(processed_filename, image)
        return image
