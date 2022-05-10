import argparse
import pandas as pd
from datetime import datetime
from datetime import timedelta

# You should not modify this part.
def config():
    parser = argparse.ArgumentParser()
    parser.add_argument("--consumption", default="./sample_data/consumption.csv", help="input the consumption data path")
    parser.add_argument("--generation", default="./sample_data/generation.csv", help="input the generation data path")
    parser.add_argument("--bidresult", default="./sample_data/bidresult.csv", help="input the bids result path")
    parser.add_argument("--output", default="output.csv", help="output the bids path")

    return parser.parse_args()

def output(path, data):
    df = pd.DataFrame(data, columns=["time", "action", "target_price", "target_volume"])
    df.to_csv(path, index=False)
    return

# Maybe I can modify below~ :D 
def get_lasttime(time_str, date_format):
    '''取得最後的歷史時間
    rts: <class 'datetime.datetime'>'''
    last_time = datetime.strptime(time_str, date_format)
    return last_time



if __name__ == "__main__":
    args = config()

    # 取得耗電量歷史紀錄
    consumption_df = pd.read_csv(args.consumption) 

    # 取得最後時間 (耗電紀錄)
    date_format_str = '%Y-%m-%d %H:%M:%S'
    last_time = get_lasttime(time_str=consumption_df.iloc[-1].loc['time'], 
                             date_format=date_format_str)
    now_time = last_time + timedelta(hours=1)

    data = []
    for i in range(100):
        now_time = now_time + timedelta(minutes=10) #timedelta(hours=1)
        data.append([now_time.strftime(date_format_str), "sell", 0.01, 0.01]) # time, action, target_price, target_volume
    output(args.output, data)
