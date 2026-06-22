import requests
import json
from datetime import datetime, timedelta

def fetch_taiwan_lottery_10_periods():
    print("🚀 [AI 分析站後端] 開始抓取台彩官方最新數據...")
    
    url = "https://api.taiwanlottery.com.tw/TLCAPIWeB/Lottery/BingoBingoResult"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return False
            
        res_json = response.json()
        content = res_json.get("content", [])
        
        if not content:
            return False
            
        latest_data = []
        
        # 嚴格只抓最新的 10 期歷史紀錄
        for item in content[:10]:
            period_num = str(item.get("period"))
            nums = sorted([int(n) for n in item.get("drawNo", []) if str(n).isdigit()])
            super_num = int(item.get("superNo", 0)) if str(item.get("superNo")).isdigit() else (nums[0] if nums else 1)
            
            if len(nums) == 20:
                latest_data.append({
                    "period": period_num,
                    "numbers": nums,
                    "super_num": super_num
                })
                
        if not latest_data:
            return False

        latest_data.sort(key=lambda x: int(x["period"]), reverse=True)

        # --- AI 智慧統計預測：精選 10 顆號碼（含超級獎號） ---
        all_numbers = []
        for period in latest_data:
            all_numbers.extend(period["numbers"])
            
        num_counts = {i: all_numbers.count(i) for i in range(1, 81)}
        sorted_by_hot = sorted(num_counts, key=num_counts.get, reverse=True)
        
        # 挑選前 9 個熱門號碼
        ai_recommended_nums = sorted([
            sorted_by_hot[0], sorted_by_hot[1], sorted_by_hot[2],
            sorted_by_hot[3], sorted_by_hot[4], sorted_by_hot[5],
            sorted_by_hot[6], sorted_by_hot[7], sorted_by_hot[8]
        ])
        # 第一熱門的號碼直接當作超級獎號（第10顆球）
        ai_recommended_super = sorted_by_hot[0]
        
        next_period_num = str(int(latest_data[0]["period"]) + 1)
        
        tw_now = datetime.utcnow() + timedelta(hours=8)
        current_time_str = tw_now.strftime("%Y-%m-%d %H:%M:%S")
        
        output_data = {
            "last_updated": current_time_str,
            "latest_data": latest_data, # 這裡剛好就是 10 期
            "prediction": {
                "next_period": next_period_num,
                "recommended_numbers": ai_recommended_nums,
                "recommended_super_number": ai_recommended_super
            }
        }
        
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
            
        print(f"✅ 成功！已鎖定近 10 期數據與 10 顆預測球。")
        return True

    except Exception as e:
        print(f"❌ 錯誤: {str(e)}")
        return False

if __name__ == "__main__":
    fetch_taiwan_lottery_10_periods()
