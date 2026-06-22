import requests
import json
from datetime import datetime, timedelta

def fetch_fast_bingo_data():
    print("🚀 [AI 分析站後端] 正在連線至台彩官方高速 API 管道...")
    
    # 2026年最新台彩官方賓果賓果公開 API 網址
    url = "https://api.taiwanlottery.com.tw/TLCAPIWeB/Lottery/BingoBingoResult"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "Accept": "application/json"
    }
    
    try:
        # 設定超時時間為 5 秒，防止無限卡死
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code != 200:
            print("❌ 官方 API 連線失敗，狀態碼：", response.status_code)
            return False
            
        data = response.json()
        raw_content = data.get("content", [])
        
        if not raw_content:
            print("❌ 官方 API 未回傳任何開獎內容")
            return False
            
        latest_20_periods = []
        
        # 解析台彩官方回傳的最新 20 期真實開獎數據
        for item in raw_content[:20]:
            period_num = str(item.get("period"))
            
            # drawNo 是開獎號碼數組，將其轉換為整數並排序
            nums = sorted([int(n) for n in item.get("drawNo", []) if str(n).isdigit()])
            super_num = int(item.get("superNo", 0)) if str(item.get("superNo")).isdigit() else (nums[0] if nums else 1)
            
            if len(nums) == 20:
                latest_20_periods.append({
                    "period": period_num,
                    "numbers": nums,
                    "super_num": super_num
                })
                
        if not latest_20_periods:
            print("❌ 無法成功解析開獎數據")
            return False

        # --- AI 統計與核心預測邏輯 ---
        all_numbers_drawn = []
        for period in latest_20_periods:
            all_numbers_drawn.extend(period["numbers"])
            
        num_counts = {i: all_numbers_drawn.count(i) for i in range(1, 81)}
        sorted_by_hot = sorted(num_counts, key=num_counts.get, reverse=True)
        
        # 挑選出統計中最熱門的數字作為下期預測
        ai_recommended_nums = sorted([
            sorted_by_hot[0], sorted_by_hot[1], 
            sorted_by_hot[5], sorted_by_hot[12], sorted_by_hot[22]
        ])
        ai_recommended_super = sorted_by_hot[0]
        
        # 算出下一期期號
        next_period_num = str(int(latest_20_periods[0]["period"]) + 1)
        
        # 轉換為台灣時間 (UTC+8)
        tw_now = datetime.utcnow() + timedelta(hours=8)
        current_time_str = tw_now.strftime("%Y-%m-%d %H:%M:%S")
        
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
            
        print(f"✅ 官方真實數據同步成功！最新期號：{latest_20_periods[0]['period']}")
        return True

    except Exception as e:
        print(f"❌ 發生錯誤: {str(e)}")
        return False

if __name__ == "__main__":
    fetch_fast_bingo_data()
