#!/bin/bash
pkill -f "python3 main.py"
pkill -f "python main.py"
pkill -f "InstaManager"
echo "アプリケーションを強制終了しました。もう一度起動してください。"
exit 0
