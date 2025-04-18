# 寿司打自動タイピングツール - キーボード入力モジュール

import pyautogui
from config import DEBUG

def type_text(text):
    """テキストを自動入力"""
    if not text:
        if DEBUG:
            print("入力するテキストがありません")
        return False
    
    if DEBUG:
        print(f"入力: {text}")
    
    # テキスト全体を一度に入力
    pyautogui.write(text)
    
    return True