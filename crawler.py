import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta

def fetch_auzo_real_data():
    print("🚀 [AI 分析站後端] 開始用直攻法抓取奧索樂透網賓果數據...")
    
    url = "https://lotto.auzo.tw/RK.php"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        # 連線奧索
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        
        if response.status_code != 200:
            print("❌ 連線奧索失敗，狀態碼：", response.status_code)
            return False
            
        soup = BeautifulSoup(response.text, "html.parser")
        latest_20_periods = []
        
        # 尋找網頁中所有的表格列
        rows = soup.find_all("tr")
        
        for row in rows:
            tds = row.find_all("td")
            # 奧索的賓果表格通常每一列會有：期號、開獎號碼、超級獎號
            if len(tds) >= 3:
                period_text = tds[0].text.strip()
                
                # 檢查第一欄是不是純數字的期號（例如 115035033）
                if not period_text.isdigit() or len(period_text) < 7:
                    continue
                    
                # 解析開獎號碼 (第二欄，號碼之間通常有空格或逗號)
                nums_text = tds[1].text.strip()
                # 把號碼切開，轉成整數並排序
                raw_nums = nums_text.replace(",", " ").split()
                nums = sorted([int(x) for x in raw_nums if x.isdigit()])
                
                # 解析超級獎號 (第三欄)
                super_text = tds[2].text.strip()
                super_num = int(super_text) if super_text.isdigit() else (nums[0] if nums else 1)
                
                # 只要剛好是 20 個號碼，就是我們要的賓果資料！
                if len(nums) == 20:
                    latest_20_periods.append({
                        "period": period_text,
                        "numbers": nums,
                        "super_num": super_num
                    })

        if not latest_20_periods:
            print("❌ 奧索結構解析失敗，啟動緊急官方 API 保底方案...")
            # 保底方案：避免網頁掛掉時畫面全空
            api_url = "https://api.taiwanlottery.com.tw/TLCAPIWeB/Lottery/BingoBingoResult"
            api_res = requests.get(api_url, headers=headers, timeout=5)
            if api_res.status_code == 200:
                content = api_res.json().get("content", [])
                for item in content[:20]:
                    latest_20_periods.append({
                        "period": str(item.get("period")),
                        "numbers": sorted([int(n) for n in item.get("drawNo", [])]),
                        "super_num": int(item.get("superNo", 0))
                    })

        if not latest_20_periods:
            print("❌ 無法取得任何資料")
            return False

        # 按期號由大到小排序，確保最新的一期在最上面
        latest_20_periods.sort(key=lambda x: int(x["period"]), reverse=True)

        # --- AI 預測邏輯 ---
        all_numbers = []
        for period in latest_20_periods:
            all_numbers.extend(period["numbers"])
        num_counts = {i: all_numbers.count(i) for i in range(1, 81)}
        sorted_by_hot = sorted(num_counts, key=num_counts.get, reverse=True)
        
        ai_recommended_nums = sorted([
            sorted_by_hot[0], sorted_by_hot[1], 
            sorted_by_hot[5], sorted_by_hot[12], sorted_by_hot[22]
        ])
        ai_recommended_super = sorted_by_hot[0]
        
        # 下一期期號
        next_period_num = str(int(latest_20_periods[0]["period"]) + 1)
        
        # 台灣時間
        tw_now = datetime.utcnow() + timedelta(hours=8)
        current_time_str = tw_now.strftime("%Y-%m-%d %H:%M:%S")
        
        output_data = {
            "last_updated": current_time_str,
            "latest_data": latest_20_periods[:20],
            "prediction": {
                "next_period": next_period_num,
                "recommended_numbers": ai_recommended_nums,
                "recommended_super_number": ai_recommended_super
            }
        }
        
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
            
        print(f"✅ 奧索真實數據同步成功！最新即時期號：{latest_20_periods[0]['period']}")
        return True

    except Exception as e:
        print(f"❌ 發生錯誤: {str(e)}")
        return False

if __name__ == "__main__":
    fetch_auzo_real_data()
