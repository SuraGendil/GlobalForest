import sys
import os
import pandas as pd
from datetime import datetime

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

try:
    from app.db_connection import get_collection
except ImportError:
    print("Error: Tidak bisa import app.db_connection. Pastikan dijalankan dari root backend.")
    sys.exit(1)

def import_news_from_excel(file_path: str):
    """
    Membaca file Excel dan menyimpan data berita ke MongoDB collection 'news'.
    Diharapkan Excel memiliki kolom: Title, Summary, Date, Link
    """
    # Cek keberadaan file
    if not os.path.exists(file_path):
        alt_path = os.path.join(os.path.dirname(__file__), file_path)
        if os.path.exists(alt_path):
            file_path = alt_path
        else:
            print(f"File tidak ditemukan: {file_path}")
            return

    try:
        print(f"Membaca data dari: {file_path}...")
        # Membaca Excel menggunakan pandas
        df = pd.read_excel(file_path, engine='openpyxl')
        
        # Normalisasi header kolom (lowercase & strip whitespace) agar tidak case-sensitive
        df.columns = [str(col).lower().strip() for col in df.columns]
        
        # Validasi kolom minimal
        required_cols = ['title', 'summary', 'date', 'link']
        for col in required_cols:
            if col not in df.columns:
                print(f"Warning: Kolom '{col}' tidak ditemukan di Excel. Pastikan header sesuai.")
        
        news_list = []
        for _, row in df.iterrows():
            # Format Tanggal
            raw_date = row.get('date')
            date_display = ""
            
            if pd.isna(raw_date):
                date_display = datetime.now().strftime("%d %B %Y")
            elif isinstance(raw_date, datetime):
                # Format tanggal agar seragam (misal: 06 Januari 2026)
                # Kita gunakan format string agar langsung tampil rapi di Frontend Vue
                try:
                    months = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                    date_display = f"{raw_date.day} {months[raw_date.month - 1]} {raw_date.year}"
                except:
                    date_display = raw_date.strftime("%d %B %Y")
            else:
                date_display = str(raw_date)

            news_item = {
                "title": row.get('title', 'No Title'),
                "summary": row.get('summary', ''),
                "date": date_display,
                "link": row.get('link', '#'),
                "created_at": datetime.now()
            }
            news_list.append(news_item)
            
        if news_list:
            # Ambil koneksi database (menggunakan koneksi yang sudah ada di app)
            cases_collection = get_collection()
            db = cases_collection.database
            news_collection = db['news'] 
            
            result = news_collection.insert_many(news_list)
            print(f"Sukses! Berhasil mengimport {len(result.inserted_ids)} berita ke collection 'news'.")
        else:
            print("Tidak ada data yang dapat diimport.")

    except Exception as e:
        print(f"Terjadi kesalahan saat import: {e}")

if __name__ == "__main__":
    # Nama file default
    filename = "Newspaper.xlsx"
    
    # Bisa dijalankan dengan argumen: python import_news_excel.py NamaFile.xlsx
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        
    import_news_from_excel(filename)