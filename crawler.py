import requests
import json
from datetime import datetime, timedelta

def fetch_taiwan_lottery_10_nums():
    print("🚀 [AI 分析站後端] 正在直攻台彩官方 API 並計算 10 組核心號碼...")
    
    url = "https://api.taiwanlottery.com.tw/TLCAPIWeB/Lottery/BingoBingoResult"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"❌ 台彩伺服器回應狀態碼：{response.status_code}")
            return False
            
        res_json = response.json()
        content = res_json.get("content", [])
        
        if not content:
            print("❌ 官方資料庫目前未回傳內容")
            return False
            
        latest_20_periods = []
        
        for item in content[:20]:
            period_num = str(item.get("period"))
            nums = sorted([int(n) for n in item.get("drawNo", []) if str(n).isdigit()])
            super_num = int(item.get("superNo", 0)) if str(item.get("superNo")).isdigit() else (nums[0] if nums else 1)
            
            if len(nums) == 20:
                latest_20_periods.append({
                    "period": period_num,
                    "numbers": nums,
                    "super_num": super_num
                })
                
        if not latest_20_periods:
            return False

        latest_20_periods.sort(key=lambda x: int(x["period"]), reverse=True)

        # --- AI 大數據熱門統計預測 (擴充至 10 個號碼) ---
        all_numbers = []
        for period in latest_20_periods:
            all_numbers.extend(period["numbers"])
            
        num_counts = {i: all_numbers.count(i) for i in range(1, 81)}
        sorted_by_hot = sorted(num_counts, key=num_counts.get, reverse=True)
        
        # 挑選出統計中前 9 個最熱門的數字
        ai_recommended_nums = sorted([
            sorted_by_hot[0], sorted_by_hot[1], sorted_by_hot[2],
            sorted_by_hot[3], sorted_by_hot[4], sorted_by_hot[5],
            sorted_by_hot[8], sorted_by_hot[12], sorted_by_hot[18]
        ])
        # 熱門第一名作為超級獎號
        ai_recommended_super = sorted_by_hot[0]
        
        next_period_num = str(int(latest_20_periods[0]["period"]) + 1)
        
        tw_now = datetime.utcnow() + timedelta(hours=8)
        current_time_str = tw_now.strftime("%Y-%m-%d %H:%M:%S")
        
        output_data = {
            "last_updated": current_time_str,
            "latest_data": latest_20_periods,
            "prediction": {
                "next_period": next_period_num,
                "recommended_numbers": ai_recommended_nums, # 這裡包含 9 個號碼
                "recommended_super_number": ai_recommended_super # 加上這 1 個，總共 10 個號碼
            }
        }
        
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
            
        print(f"✅ 成功同步！最新期號：{latest_20_periods[0]['period']}，已生成 10 個預測號碼。")
        return True

    except Exception as e:
        print(f"❌ 發生錯誤: {str(e)}")
        return False

if __name__ == "__main__":
    fetch_taiwan_lottery_10_nums()
