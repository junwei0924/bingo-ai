import requests
import json
from datetime import datetime

def fetch_bingo():
    # 這是最關鍵的 Header，偽裝成來自 Chrome 的正常瀏覽請求
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://www.taiwanlottery.com.tw/",
        "Origin": "https://www.taiwanlottery.com.tw",
        "Connection": "keep-alive"
    }
    
    url = "https://api.taiwanlottery.com.tw/TLCAPIWeB/Lottery/BingoBingoResult"
    
    try:
        # 使用 Session 來保持連線狀態，有時這能騙過防火牆
        session = requests.Session()
        response = session.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            # 確保資料存在
            if "content" in data:
                # 這裡抓取你需要的近 20 期數據
                results = data["content"][:20]
                
                # 存檔
                with open("data.json", "w", encoding="utf-8") as f:
                    json.dump(results, f, ensure_ascii=False, indent=2)
                print("✅ 資料抓取成功並寫入 data.json")
            else:
                print("❌ 抓到了但格式不對，台彩可能更改了 API 格式")
        else:
            print(f"❌ 錯誤碼: {response.status_code}，請檢查是否被 IP 封鎖")
            
    except Exception as e:
        print(f"❌ 爬蟲執行失敗: {e}")

if __name__ == "__main__":
    fetch_bingo()
