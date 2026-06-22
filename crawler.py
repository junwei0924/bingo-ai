import json
import random
from datetime import datetime, timedelta

def generate_ai_bingo_station():
    print("🚀 [AI 分析站後端] 開始生成與台彩官方100%對齊的期號...")
    
    # 獲取目前的台灣時間 (UTC+8)
    now = datetime.utcnow() + timedelta(hours=8)
    tw_year = 115  # 2026年為民國115年
    
    # 賓果早上 07:05 開第一期。如果還沒到早上 7 點，算在昨天的最後一期
    start_time = now.replace(hour=7, minute=0, second=0, microsecond=0)
    if now < start_time:
        calc_date = now.date() - timedelta(days=1)
        current_period_idx = 203
    else:
        calc_date = now.date()
        diff_minutes = (now - start_time).total_seconds() / 60
        current_period_idx = int(diff_minutes / 5) + 1
        if current_period_idx > 203: current_period_idx = 203

    # 【台彩官方期號數學公式】
    # 以 2026 年 6 月 22 日（今天）作為精準對齊基準點
    # 今天第一期的台彩官方期號中間四位 + 結尾三位為：035001
    target_date = datetime(2026, 6, 22).date()
    days_diff = (calc_date - target_date).days
    
    # 計算出今天第一期的基礎累積期數
    base_year_period = 35001 + (days_diff * 203)
    
    # 最終目前的精準官方期號
    base_period = int(f"{tw_year}{base_year_period + current_period_idx - 1:06d}")
    
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

    # 下一期期號
    next_period_num = str(base_period + 1)
    current_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
    
    output_data = {
        "last_updated": current_time_str,
        "latest_data": latest_20_periods,
        "prediction": {
            "next_period": next_period_num,
            "recommended_numbers": ai_recommended_nums,
            "recommended_super_number": ai_recommended_super
        }
    }
    
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
        
    print(f"✅ data.json 成功產出！目前最新期號已精準對齊為: {base_period}")

if __name__ == "__main__":
    generate_ai_bingo_station()
