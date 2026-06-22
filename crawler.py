import requests
import json
from datetime import datetime, timedelta

def fetch_pure_taiwan_lottery():
    print("🚀 [AI 分析站後端] 正在直攻台彩官方大數據資料庫...")
    
    # 台彩官方最核心、最即時的賓果賓果 API
    url = "https://api.taiwanlottery.com.tw/TLCAPIWeB/Lottery/BingoBingoResult"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            print(f"❌ 請求失敗，台彩伺服器狀態碼：{response.status_code}")
            return False
            
        res_json = response.json()
        content = res_json.get("content", [])
        
        if not content:
            print("❌ 官方資料庫目前未回傳任何開獎內容")
            return False
            
        latest_20_periods = []
        
        # 嚴格精準抓取台彩官方回傳的最新開獎數據
        for item in content[:20]:
            period_num = str(item.get("period")) # 這會直接拿到 115035041 這種格式
            
            # drawNo 是台彩官方的20個中獎號碼陣列
            nums = sorted([int(n) for n in item.get("drawNo", []) if str(n).isdigit()])
            
            # superNo 是官方超級獎號
            super_num = int(item.get("superNo", 0)) if str(item.get("superNo")).isdigit() else (nums[0] if nums else 1)
            
            if len(nums) == 20:
                latest_20_periods.append({
                    "period": period_num,
                    "numbers": nums,
                    "super_num": super_num
                })
                
        if not latest_20_periods:
            print("❌ 解析台彩官方陣列失敗")
            return False

        # 依照期號由大到小排序，確保最新的一期在最上面
        latest_20_periods.sort(key=lambda x: int(x["period"]), reverse=True)

        # --- AI 大數據熱門統計預測 ---
        all_numbers = []
        for period in latest_20_periods:
            all_numbers.extend(period["numbers"])
            
        num_counts = {i: all_numbers.count(i) for i in range(1, 81)}
        sorted_by_hot = sorted(num_counts, key=num_counts.get, reverse=True)
        
        # 依據台彩最新真實開獎，篩選最熱門與規律數字
        ai_recommended_nums = sorted([
            sorted_by_hot[0], sorted_by_hot[1], 
            sorted_by_hot[5], sorted_by_hot[12], sorted_by_hot[22]
        ])
        ai_recommended_super = sorted_by_hot[0]
        
        # 真正的下一期期號（當前最新期號 + 1）
        next_period_num = str(int(latest_20_periods[0]["period"]) + 1)
        
        # 強制轉為台灣時間（UTC+8）
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
        
        # 覆寫推回 data.json
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
            
        print(f"✅ 官方大數據對接成功！最新現場期號已同步為：{latest_20_periods[0]['period']}")
        return True

    except Exception as e:
        print(f"❌ 執行發生錯誤: {str(e)}")
        return False

if __name__ == "__main__":
    fetch_pure_taiwan_lottery()
