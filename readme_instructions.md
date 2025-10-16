# 🖼️ אפליקציה להסרת רקע מתמונות

אפליקציה פשוטה להסרת רקע מתמונות באמצעות AI.

---

## 📋 דרישות מקדימות

- Python 3.9 או גרסה חדשה יותר
- חיבור לאינטרנט (להורדת המודל בהפעלה הראשונה)

---

## 🪟 הוראות להתקנה והפעלה - Windows

### שלב 1: פתח Command Prompt או PowerShell
לחץ `Win + R`, הקלד `cmd` ולחץ Enter

### שלב 2: נווט לתיקיית הפרויקט
```bash
cd path\to\your\project
```

### שלב 3: צור סביבה וירטואלית
```bash
python -m venv venv
```

### שלב 4: הפעל את הסביבה הוירטואלית
```bash
venv\Scripts\activate
```

### שלב 5: התקן את הספריות
```bash
pip install -r requirements.txt
```

### שלב 6: הרץ את האפליקציה
```bash
streamlit run app.py
```

### 🎉 זהו! הדפדפן יפתח אוטומטית

אם הדפדפן לא נפתח, גש ל: `http://localhost:8501`

---

## 🍎 הוראות להתקנה והפעלה - Mac/Linux

### שלב 1: פתח Terminal

### שלב 2: נווט לתיקיית הפרויקט
```bash
cd path/to/your/project
```

### שלב 3: צור סביבה וירטואלית
```bash
python3 -m venv venv
```

### שלב 4: הפעל את הסביבה הוירטואלית
```bash
source venv/bin/activate
```

### שלב 5: התקן את הספריות
```bash
pip install -r requirements.txt
```

### שלב 6 (Linux בלבד): התקן תלויות מערכת
```bash
sudo apt-get update && sudo apt-get install -y libgl1
```

### שלב 7: הרץ את האפליקציה
```bash
streamlit run app.py
```

### 🎉 זהו! הדפדפן יפתח אוטומטית

אם הדפדפן לא נפתח, גש ל: `http://localhost:8501`

---

## 🔄 הפעלה חוזרת (לאחר ההתקנה הראשונה)

### Windows:
```bash
cd path\to\your\project
venv\Scripts\activate
streamlit run app.py
```

### Mac/Linux:
```bash
cd path/to/your/project
source venv/bin/activate
streamlit run app.py
```

---

## 🛑 עצירת האפליקציה

לחץ `Ctrl + C` בטרמינל/Command Prompt

---

## ❓ פתרון בעיות

### "python לא מזוהה כפקודה" (Windows)
נסה להשתמש ב-`py` במקום `python`:
```bash
py -m venv venv
```

### שגיאה בהתקנת ספריות
ודא שיש לך גרסה עדכנית של pip:
```bash
python -m pip install --upgrade pip
```

### האפליקציה לא נפתחת
העתק את הכתובת מהטרמינל (בדרך כלל `http://localhost:8501`) והדבק בדפדפן

---

## 📝 שימוש באפליקציה

1. העלה תמונה או מספר תמונות (PNG, JPG, JPEG)
2. לחץ על "הסר רקע מכל התמונות"
3. הורד את התמונות בנפרד או כולן יחד כקובץ ZIP

---

## 📦 מה כלול?

- **app.py** - קוד האפליקציה הראשי
- **requirements.txt** - רשימת הספריות הנדרשות
- **packages.txt** - תלויות מערכת (לסטרימלית קלאוד)
- **runtime.txt** - גרסת Python מומלצת

---

## 🎯 תכונות

✅ הסרת רקע אוטומטית באמצעות AI  
✅ עיבוד אצווה (מספר תמונות בו-זמנית)  
✅ חיתוך אוטומטי לגבולות האובייקט  
✅ הורדת תמונות בודדות או כקובץ ZIP  
✅ ממשק בעברית וידידותי למשתמש  

---

**נוצר עם ❤️ באמצעות Streamlit ו-rembg**