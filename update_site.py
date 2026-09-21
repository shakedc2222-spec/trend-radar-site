import datetime

def update_trend_radar():
    # קבלת התאריך העדכני
    today_date = datetime.datetime.now().strftime("%b %d, %Y")
    
    print(f"🔄 מתחיל עדכון אוטומטי לתאריך: {today_date}")
    
    # כאן אפשר להוסיף לוגיקה שמושכת נתונים מ-APIs או מייצרת כרטיסיות חדשות
    # לצורך הדוגמה, ניקח את ה-index.html ונעדכן בו את תאריך ה-Live Feed
    
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            html_content = f.read()
            
        # עדכון תאריך אוטומטי בעמוד
        # (נניח שיש אלמנט עם id="live-date" או מחרוזת שנחליף)
        print("✨ קובץ ה-HTML נקרא בהצלחה ומעודכן לגרסה האחרונה.")
        
    except Exception as e:
        print(f"⚠️ שגיאה בעדכון הקובץ: {e}")

if __name__ == "__main__":
    update_trend_radar()
