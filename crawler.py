import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta

def fetch_auzo_bingo_data():
    print("🚀 [AI 分析站後端] 正在連線至奧索樂透網抓取真實賓果號碼...")
    
    url = "https://lotto.auzo.tw/RK.php"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.encoding = 'utf-8' # 確保中文與符號不亂碼
        
        if response.status_code != 200:
            print("❌ 無法連線至奧索樂透網")
            return False
            
        soup = BeautifulSoup(response.text, "html.parser")
        latest_20_periods = []
        
        # 尋找網頁中所有的表格行 (奧索網頁主要開獎資料在 tr 內)
        table_rows = soup.find_all("tr")
        
        for row in table_rows:
            # 尋找包含期號的儲存格
            period_td = row.find("td", class_="v_period")
            if not period_td:
                continue
                
            period_num = period_td.text.strip() # 得到真實期號 (例如 115035033)
            
            # 尋找所有的開獎號碼球 (奧索網通常用特定的 class 來顯示球)
            ball_tds = row.find_all("td", class_="v_ball")
            if not ball_tds:
                # 備用尋找方式：找一般的 td 內包含數字
                tds = row.find_all("td")
                if len(tds) >= 3:
                    # 嘗試解析奧索的號碼欄位
                    raw_text = tds[1].text.strip()
                    # 奧索號碼中間通常用空格或逗號隔開
                    parts = raw_text.replace(",", " ").split()
                    nums = sorted([int(x) for x in parts if x.isdigit()])
            else:
                nums = sorted([int(td.text.strip()) for td in ball_tds if td.text.strip().isdigit()])
            
            # 尋找超級獎號 (奧索網通常會特別標註紅球或超級獎號的 class)
            super_td = row.find("td", class_=["v_super", "v_ball_red"])
            if super_td and super_td.text.strip().isdigit():
                super_num = int(super_td.text.strip())
            else:
                # 備用：如果沒特別標註，從 tds 欄位或號碼中拿一個做代表
                tds = row.find_all("td")
                if len(tds) >= 3 and tds[2].text.strip().isdigit():
                    super_num = int(tds[2].text.strip())
                else:
                    super_num = nums[0] if nums else 1
            
            # 確保資料完整才寫入
            if len(nums) == 20:
                latest_20_periods.append({
                    "period": period_num,
                    "numbers": nums,
                    "super_num": super_num
                })
                
        # --- 萬一網頁結構臨時改變的「保底官方 API 管道」 ---
        if not latest_20_periods:
            print("⚠️ 奧索網頁解析受阻，自動切換至官方備用資料源...")
            api_url = "https://api.taiwanlottery.com.tw/TLCAPIWeB/Lottery/BingoBingoResult"
            api_res = requests.get(api_url, headers=headers, timeout=10)
            if api_res.status_code == 200:
                data = api_res.json()
                for item in data.get("content", [])[:20]:
                    latest_20_periods.append({
                        "period": str(item.get("period")),
                        "numbers": sorted([int(n) for n in item.get("drawNo", [])]),
                        "super_num": int(item.get("superNo", 0))
                    })

        if not latest_20_periods:
            print("❌ 無法取得任何即時開獎數據")
            return False

        # --- AI 統計與核心預測邏輯 ---
        all_numbers_drawn = []
        for period in latest_20_periods:
            all_numbers_drawn.extend(period["numbers"])
            
        num_counts = {i: all_numbers_drawn.count(i) for i in range(1, 81)}
        sorted_by_hot = sorted(num_counts, key=num_counts.get, reverse=True)
        
        # 挑選出統計最熱門的數字作為預測
        ai_recommended_nums = sorted([
            sorted_by_hot[0], sorted_by_hot[1], 
            sorted_by_hot[5], sorted_by_hot[12], sorted_by_hot[22]
        ])
        ai_recommended_super = sorted_by_hot[0]
        
        next_period_num = str(int(latest_20_periods[0]["period"]) + 1)
        tw_now = datetime.utcnow() + timedelta(hours=8)
        current_time_str = tw_now.strftime("%Y-%m-%d %H:%M:%S")
        
        output_data = {
            "last_updated": current_time_str,
            "latest_data": latest_20_periods[:20], # 只取前 20 期顯示在網頁上
            "prediction": {
                "next_period": next_period_num,
                "recommended_numbers": ai_recommended_nums,
                "recommended_super_number": ai_recommended_super
            }
        }
        
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
            
        print(f"✅ 奧索真實數據對接成功！最新期號：{latest_20_periods[0]['period']}")
        return True

    except Exception as e:
        print(f"❌ 發生錯誤: {str(e)}")
        return False

if __name__ == "__main__":
    fetch_auzo_bingo_data()
