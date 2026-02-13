import sys

# 入力ファイルと出力ファイルを指定
input_file = sys.argv[1]
output_file = sys.argv[2]

# 処理開始
with open(input_file, "r") as infile, open(output_file, "w") as outfile:
    # ヘッダーを挿入
    outfile.write("Theta,Distance\n")
    
    # ファイルを行ごとに処理
    for i, line in enumerate(infile):
        if i < 8:  # 先頭8行をスキップ
            continue
        line = line.replace(" ", "")  # すべての空白を削除
        if "theta:" in line and "Dist:" in line:  # 必要なデータが含まれる行のみ処理
            line = line.replace("theta:", "").replace("Dist:", ",")
            line = line.split("Q")[0]  # "Q"以降の文字を削除
            outfile.write(line + "\n")  # CSV形式で出力

print(f"処理が完了しました。出力ファイル: {output_file}")