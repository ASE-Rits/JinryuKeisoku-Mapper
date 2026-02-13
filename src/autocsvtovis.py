import sys
import pandas as pd
import numpy as np
import datashader as ds
import datashader.transfer_functions as tf

# メイン処理
def main():
#     引数のチェック
#    if len(sys.argv) < 2:
#        print("使用方法: python script.py 処理するCSVファイル名")
#    #    sys.exit(1)
    
    input_file = "/rplidar/JM/dev/sample.csv"
    output_file = input_file.replace(".csv", "_with_coordinates.csv")
    output_image = input_file.replace(".csv", "_datashader_plot.png")
    
    # CSVファイルを読み込む
    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"エラー: ファイル {input_file} が見つかりません。")
        sys.exit(1)
    
    # ThetaとDistanceを数値型に変換（エラーが発生した場合はNaNに置き換え）
    df['Theta'] = pd.to_numeric(df['Theta'], errors='coerce')
    df['Distance'] = pd.to_numeric(df['Distance'], errors='coerce')

    # NaNがある場合の処理（エラーのある行を削除）
    df = df.dropna(subset=['Theta', 'Distance'])

    # ThetaとDistanceからx, y座標を計算 (Thetaは度からラジアンに変換)
    df['x'] = df['Distance'] * np.cos(np.radians(df['Theta']))
    df['y'] = df['Distance'] * np.sin(np.radians(df['Theta']))

    # 新しいCSVファイルに保存
    df.to_csv(output_file, index=False)
    print(f"座標を追加したCSVファイルを {output_file} に保存しました！")

    # Datashaderで描画
    canvas = ds.Canvas(plot_width=800, plot_height=600)
    agg = canvas.points(df, 'x', 'y')
    img = tf.shade(agg, cmap=["lightblue", "darkblue"])

    # Datashader画像を保存
    img.to_pil().save(output_image)
    print(f"Datashaderによる高速プロットを {output_image} に保存しました。")

# エントリーポイント
if __name__ == "__main__":
    main()