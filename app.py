from flask import Flask, request, jsonify, render_template, url_for
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # frontend'ten gelen isteklere izin verir

# ✅ NASA API sınıfı (senin kodun aynen korundu)
class NasaOSDRSearch:
    BASE_URL = "https://osdr.nasa.gov/osdr/data"
    
    def __init__(self):
        self.session = requests.Session()
    
    def search_studies(self, keyword, page=0, size=25, data_source="cgene"):
        search_url = f"{self.BASE_URL}/search"
        params = {
            'term': keyword,
            'from': page,
            'size': size,
            'type': data_source
        }
        try:
            response = self.session.get(search_url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Arama sırasında hata oluştu: {e}")
            return {"error": str(e)}
    
    def get_study_files(self, study_ids, page=0, size=25, all_files=False):
        files_url = f"{self.BASE_URL}/osd/files/{study_ids}/"
        params = {
            'page': page,
            'size': size,
            'all_files': str(all_files).lower()
        }
        try:
            response = self.session.get(files_url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Dosya bilgilerini alırken hata oluştu: {e}")
            return {"error": str(e)}
    
    def get_study_metadata(self, study_id):
        meta_url = f"{self.BASE_URL}/osd/meta/{study_id}"
        try:
            response = self.session.get(meta_url, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Metadata alınırken hata oluştu: {e}")
            return {"error": str(e)}

# NASA arama nesnesi oluştur
nasa_searcher = NasaOSDRSearch()

# ✅ 1️⃣ index.html'i render_template ile döndür (düzeltilen kısım)
@app.route('/')
def home():
    return render_template('index.html')

# ✅ 2️⃣ /api/search endpoint'i (frontend buradan veri çeker)
@app.route('/api/search', methods=['GET'])
def search_plants():
    keyword = request.args.get('keyword', '')
    if not keyword:
        return jsonify({"error": "Lütfen bir arama kelimesi girin"}), 400
    
    results = nasa_searcher.search_studies(keyword, size=10)
    if 'error' in results:
        return jsonify({"error": results['error']}), 500
    
    formatted_results = {
        "total_hits": results.get('hits', 0),
        "studies": []
    }
    
    for item in results.get('results', []):
        study = {
            "title": item.get('Study Title', 'Bilinmiyor'),
            "description": item.get('Study Description', 'Açıklama yok'),
            "organism": item.get('organism', 'Belirtilmemiş'),
            "accession": item.get('Accession', ''),
            "study_id": item.get('Accession', '').replace('OSD-', '')
        }
        formatted_results["studies"].append(study)
    
    return jsonify(formatted_results)

@app.route('/api/files/<study_id>', methods=['GET'])
def get_files(study_id):
    file_data = nasa_searcher.get_study_files(study_id)
    if 'error' in file_data:
        return jsonify({"error": file_data['error']}), 500
    return jsonify(file_data)

@app.route('/api/metadata/<study_id>', methods=['GET'])
def get_metadata(study_id):
    metadata = nasa_searcher.get_study_metadata(study_id)
    if 'error' in metadata:
        return jsonify({"error": metadata['error']}), 500
    return jsonify(metadata)

if __name__ == '__main__':
    print("🚀 gPlant Flask API başlatılıyor...")
    print("🔗 http://localhost:5000 adresinden erişebilirsin.")
    app.run(debug=True, port=5000)
