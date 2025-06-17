import streamlit as st
import io
import zipfile
from PIL import Image
import numpy as np

st.set_page_config(
    page_title="הסרת רקע מתמונות",
    page_icon="🖼️",
    layout="wide"
)

# ייבוא rembg עם טיפול בשגיאות
try:
    from rembg import remove
    REMBG_AVAILABLE = True
except ImportError as e:
    st.error(f"שגיאה בייבוא rembg: {e}")
    REMBG_AVAILABLE = False

def remove_background(image):
    """
    מסיר רקע מתמונה ומחזיר את האלפה צ'אנל חתוך לגבולות האובייקט
    """
    try:
        # המרת התמונה לבייטים
        if isinstance(image, Image.Image):
            img_bytes = io.BytesIO()
            image.save(img_bytes, format='PNG')
            img_bytes = img_bytes.getvalue()
        else:
            img_bytes = image.read()
        
        # הסרת רקע
        result = remove(img_bytes)
        
        # טיפול בסוג התוצאה שחוזרת מ-remove
        if isinstance(result, bytes):
            result_image = Image.open(io.BytesIO(result))
        elif isinstance(result, Image.Image):
            result_image = result
        else:
            st.error("סוג תוצאה לא נתמך מ־rembg")
            return None
        
        # וידוא שיש אלפה צ'אנל
        if result_image.mode != 'RGBA':
            result_image = result_image.convert('RGBA')
        
        # חיתוך התמונה לגבולות האובייקט (הסרת שוליים)
        cropped_image = crop_to_object(result_image)
        
        return cropped_image
    
    except Exception as e:
        st.error(f"שגיאה בעיבוד התמונה: {str(e)}")
        return None

def crop_to_object(image):
    """
    חותך את התמונה לגבולות האובייקט - מסיר שוליים ריקים
    """
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    
    # קבלת ערכי האלפה צ'אנל
    alpha = image.split()[-1]
    
    # מציאת הגבולות הלא-שקופים
    bbox = alpha.getbbox()
    
    if bbox is None:
        # אם אין תוכן, החזר תמונה ריקה קטנה
        return Image.new('RGBA', (1, 1), (0, 0, 0, 0))
    
    # חיתוך התמונה לגבולות האובייקט
    cropped = image.crop(bbox)
    
    return cropped

def create_download_link(image, filename):
    """
    יוצר קישור להורדה של התמונה
    """
    img_bytes = io.BytesIO()
    image.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return img_bytes.getvalue()

def create_zip_file(images_data):
    """
    יוצר קובץ ZIP עם כל התמונות המעובדות
    """
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for i, (image, original_name) in enumerate(images_data):
            img_bytes = io.BytesIO()
            image.save(img_bytes, format='PNG')
            
            # שם קובץ חדש
            name_without_ext = original_name.rsplit('.', 1)[0] if '.' in original_name else original_name
            new_filename = f"{name_without_ext}_no_bg.png"
            
            zip_file.writestr(new_filename, img_bytes.getvalue())
    
    zip_buffer.seek(0)
    return zip_buffer.getvalue()

def main():
    st.title("🖼️ אפליקציה להסרת רקע מתמונות")
    st.markdown("העלה תמונה או מספר תמונות והסר את הרקע בקלות!")
    
    # בדיקה אם rembg זמין
    if not REMBG_AVAILABLE:
        st.error("⚠️ הספרייה rembg לא מותקנת כראוי. אנא התקן אותה עם: pip install rembg onnxruntime")
        st.stop()
    
    # העלאת קבצים
    uploaded_files = st.file_uploader(
        "בחר תמונות להעלאה",
        type=['png', 'jpg', 'jpeg'],
        accept_multiple_files=True,
        help="ניתן להעלות מספר תמונות בו-זמנית"
    )
    
    if uploaded_files:
        st.success(f"הועלו {len(uploaded_files)} תמונות")
        
        # כפתור לעיבוד
        if st.button("הסר רקע מכל התמונות", type="primary"):
            
            # בר התקדמות
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            processed_images = []
            
            for i, uploaded_file in enumerate(uploaded_files):
                status_text.text(f"מעבד תמונה {i+1} מתוך {len(uploaded_files)}: {uploaded_file.name}")
                
                # טעינת התמונה המקורית
                original_image = Image.open(uploaded_file)
                
                # הסרת רקע
                processed_image = remove_background(original_image)
                
                if processed_image:
                    processed_images.append((processed_image, uploaded_file.name))
                
                # עדכון בר התקדמות
                progress_bar.progress((i + 1) / len(uploaded_files))
            
            status_text.text("העיבוד הושלם!")
            
            if processed_images:
                st.success(f"עובדו בהצלחה {len(processed_images)} תמונות")
                
                # הצגת התוצאות
                st.subheader("תוצאות:")
                
                # יצירת עמודות להצגה
                cols = st.columns(min(3, len(processed_images)))
                
                for i, (processed_image, original_name) in enumerate(processed_images):
                    with cols[i % 3]:
                        st.image(processed_image, caption=f"ללא רקע: {original_name}", use_column_width=True)
                        
                        # כפתור הורדה בודדת
                        img_data = create_download_link(processed_image, original_name)
                        name_without_ext = original_name.rsplit('.', 1)[0] if '.' in original_name else original_name
                        st.download_button(
                            label=f"הורד {name_without_ext}",
                            data=img_data,
                            file_name=f"{name_without_ext}_no_bg.png",
                            mime="image/png"
                        )
                
                # הורדת כל הקבצים כ-ZIP
                if len(processed_images) > 1:
                    st.subheader("הורדה כללית:")
                    zip_data = create_zip_file(processed_images)
                    st.download_button(
                        label="הורד את כל התמונות כקובץ ZIP",
                        data=zip_data,
                        file_name="images_no_background.zip",
                        mime="application/zip"
                    )

    # הוראות שימוש
    with st.expander("הוראות שימוש"):
        st.markdown("""
        ### איך להשתמש:
        1. **העלה תמונות**: לחץ על "Browse files" והעלה תמונה אחת או יותר
        2. **עבד**: לחץ על "הסר רקע מכל התמונות"
        3. **הורד**: הורד תמונות בודדות או את כולן כקובץ ZIP
        
        ### פורמטים נתמכים:
        - PNG
        - JPG/JPEG
        
        ### טיפים:
        - התמונות יישמרו בפורמט PNG עם שקיפות
        - האפליקציה מותאמת במיוחד לבקבוקי יין על רקע לבן
        - ניתן להעלות מספר תמונות בו-זמנית לעיבוד אצווה
        """)

if __name__ == "__main__":
    main()