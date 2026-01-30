from app.db_connection import get_collection
from typing import List, Dict

# Perbaikan: Ambil database dari collection default, lalu pilih collection 'news'
# Ini mencegah error jika get_collection() tidak menerima parameter
try:
    _default_col = get_collection()
    collection = _default_col.database['news']
except Exception:
    # Fallback jika struktur get_collection berbeda
    collection = get_collection("news")

def get_all_news() -> List[Dict]:
    # Mengambil berita terbaru, diurutkan berdasarkan created_at descending
    news_cursor = collection.find({}).sort("created_at", -1).limit(6)
    news_list = []
    for doc in news_cursor:
        doc['id'] = str(doc['_id'])
        del doc['_id']
        news_list.append(doc)
    return news_list