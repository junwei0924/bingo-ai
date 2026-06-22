import json
import random
from datetime import datetime, timedelta

def generate_ai_bingo_station():
    print("🚀 [AI 分析站後端] 開始生成數據...")
    
    # 自動推算期號
    now = datetime.now()
    tw_year = now.year - 1911
    date_str = now.strftime("%m%d")
    
    start_time = now.replace(hour=7, minute=0, second=0, microsecond=0)
    if now < start_time:
        now = now - timedelta(days=1)
        tw_year = now.year - 1911
        date_str = now.strftime("%m%d")
        current_period_idx = 203
    else:
        diff_minutes = (now - start_time).total_seconds() / 60
        current_period_idx = int(diff_minutes / 5) + 1
        if current_period_idx > 203: current_period_idx = 203

    base_period = int(f"{tw_year}{date_str}{current_period_idx:03d}")
    
    # 仿真生成近 20 期數據
    latest_20_periods = []
    random.seed(base_period) 
    
    for i in range(20):
        period_num = str(base_period - i)
        nums = sorted(random.sample(range(1, 81), 20))
        super_num = random.choice(nums)
        
        latest_20_periods.append({
            "period": period_num,
            "numbers": nums,
            "super_num": super_num
        })
        
    # AI 統計預測邏輯
    all_numbers_drawn = []
    for period in latest_20_periods:
        all_numbers_drawn.extend(period["numbers"])
        
    num_counts = {i: all_numbers_drawn.count(i) for i in range(1, 81)}
    sorted_by_hot = sorted(num_counts, key=num_counts.get, reverse=True)
    
    ai_recommended_nums = sorted([
        sorted_by_hot[0], sorted_by_hot[1], 
        sorted_by_hot[25], sorted_by_hot[40], sorted_by_hot[-1]
    ])
    ai_recommended_super = sorted_by_hot[0]

    # 打包成標準 JSON 格式
    next_period_num = str(base_period + 1)
    current_time_str = (datetime.utcnow() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
    
    output_data = {
        "last_updated": current_time_str,
        "latest_data": latest_20_periods,
        "prediction": {
            "next_period": next_period_num,
            "recommended_numbers": ai_recommended_nums,
            "recommended_super_number": ai_recommended_super
        }
    }
    
    # 【核心修正】強制寫入目前目錄下的 data.json
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
        
    print("✅ data.json 成功產出！")

if __name__ == "__main__":
    generate_ai_bingo_station()
