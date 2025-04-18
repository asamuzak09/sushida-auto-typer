# 寿司打自動タイピングツール - OCR処理モジュール

import pytesseract
import re
from config import DEBUG

def extract_text(image):
    """画像からテキストを抽出"""
    # Tesseract OCRのカスタム設定
    # --psm 6: 単一の均一なテキストブロックとして扱う
    # --oem 1: LSTMエンジンのみを使用
    # 文字の制限を緩和し、大文字小文字両方を許可
    custom_config = r'--psm 6 --oem 1'
    
    # Tesseract OCRを使用してテキスト抽出
    # 英語のみを認識するようにlanguageパラメータを設定
    text = pytesseract.image_to_string(image, lang='eng', config=custom_config)
    
    # 改行や空白を削除
    text = text.strip()
    
    if DEBUG:
        print(f"OCR抽出テキスト: {text}")
    
    return text

def clean_text(text):
    """抽出したテキストの後処理"""
    # 複数行のテキストを処理する場合、小文字アルファベットの数が最も多い行を選択
    lines = text.split('\n')
    
    # 空でない行のみをフィルタリング
    non_empty_lines = [line.strip() for line in lines if line.strip()]
    
    if not non_empty_lines:
        if DEBUG:
            print("テキストが検出されませんでした")
        return ""
    
    # 各行の小文字アルファベットの数をカウント
    line_scores = []
    for line in non_empty_lines:
        # 小文字アルファベットの数をカウント
        alpha_count = sum(1 for c in line if c.islower() and c.isalpha())
        line_scores.append((line, alpha_count))
        
        if DEBUG:
            print(f"行: '{line}' - 小文字アルファベット数: {alpha_count}")
    
    # 小文字アルファベットの数が最も多い行を選択
    best_line, best_score = max(line_scores, key=lambda x: x[1])
    
    if DEBUG:
        print(f"最も小文字アルファベットが多い行: '{best_line}' (スコア: {best_score})")
    
    # 選択した行から小文字アルファベットとハイフンとクエスチョンマークと感嘆符以外の文字を削除
    cleaned_text = re.sub(r'[^a-z\-\?\!]', '', best_line)
    
    if DEBUG:
        print(f"クリーニング後のテキスト: {cleaned_text}")
    
    return cleaned_text

def verify_text(text):
    """テキストの検証（オプション機能）
    
    OCRの誤認識を検出するための追加チェック
    例: 特定の文字の置換や、辞書との照合など
    """
    # 一般的な誤認識パターンの修正
    corrections = {
        '1': 'l',  # 数字の1とアルファベットのlの混同
        '0': 'o',  # 数字の0とアルファベットのoの混同
        '5': 's',  # 数字の5とアルファベットのsの混同
    }
    
    verified_text = text
    for wrong, correct in corrections.items():
        verified_text = verified_text.replace(wrong, correct)
    
    if DEBUG and verified_text != text:
        print(f"検証後のテキスト: {verified_text}")
    
    return verified_text