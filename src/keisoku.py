import subprocess
import time
import signal
import os


csv_process = None  # グローバル変数として定義


def signal_handler(sig, frame):
    print('\nプロセスが中断されました。')
    print('残存するプロセスを確認中...')
    # csv_processが存在する場合、すべて終了するまで待機
    if csv_process is not None:
        for proc in csv_process:
            proc.terminate()
        for proc in csv_process:
            proc.wait()
    print('すべてのプロセスが終了しました。プログラムを終了します。')
    exit(0)



def main():
    # 終了シグナルのハンドラを設定
    signal.signal(signal.SIGINT, signal_handler)

    # 設定ファイルを読み込み
    config = {}
    with open('keisoku.conf', 'r') as conf_file:
        for line in conf_file:
            if '=' in line:
                key, value = line.strip().split('=', 1)
                config[key.strip()] = value.strip().strip('"')


    timeout = int(config.get('max_measurement_time', 100000))  # Set your timeout in seconds
    ultra_simple_path = os.path.join(config.get('ultra_simple_dir', '/rplidar/sdk/output/Linux/Release'), 'ultra_simple')
    output_dir = config.get('output_dir', '/rplidar/output')
    raw_logs_dir = os.path.join(output_dir, 'raw_logs')
    csv_dir = os.path.join(output_dir, 'csv')
    interval = int(config.get('interval', 60))  # Measurement interval in seconds
    start_time = time.time()
    global csv_process
    csv_process = []

    # 出力ディレクトリの作成
    os.makedirs(raw_logs_dir, exist_ok=True)
    os.makedirs(csv_dir, exist_ok=True)

    # 計測ループ
    while True:
        if time.time() - start_time > timeout:
            print('計測時間の上限に達しました。計測を終了します。')
            break

        log_name = f'{int(time.time())}.log'
        log_path = os.path.join(
            raw_logs_dir,
            log_name
            )
        
        with open(log_path, 'w') as log_file:
            # ultra_simpleのコマンド
            keisoku_process = subprocess.Popen([ultra_simple_path, '--channel', '--serial', '/dev/ttyUSB0', '256000'], stdout=log_file)
            try:
                keisoku_process.wait(timeout=float(interval))
            except subprocess.TimeoutExpired:
                keisoku_process.kill()
                keisoku_process.wait()
        
        # CSV変換プロセス
        csv_process.append(subprocess.Popen(['python3', 'makecsv.py', log_path, os.path.join(
            csv_dir, f'{log_name}.csv')]))
        # 終了したプロセスを削除
        csv_process = [proc for proc in csv_process if proc.poll() is None]


if __name__ == "__main__":
    main()