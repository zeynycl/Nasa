import requests
import json
from typing import List, Dict, Optional

class NasaOSDRSearch:
    """NASA OSDR API üzerinden arama yapan sınıf"""
    
    BASE_URL = "https://osdr.nasa.gov/osdr/data"
    
    def __init__(self):
        self.session = requests.Session()
    
    def search_studies(
        self, 
        keyword: str, 
        page: int = 0, 
        size: int = 25,
        data_source: str = "cgene"
    ) -> Dict:
        """
        Anahtar kelimeye göre çalışmaları arar
        
        Args:
            keyword: Aranacak kelime
            page: Sayfa numarası (0'dan başlar)
            size: Sayfa başına sonuç sayısı
            data_source: Veri kaynağı (cgene, nih_geo_gse, ebi_pride, mg_rast)
        
        Returns:
            Arama sonuçlarını içeren dictionary
        """
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
            return {}
    
    def get_study_files(
        self, 
        study_ids: str, 
        page: int = 0, 
        size: int = 25,
        all_files: bool = False
    ) -> Dict:
        """
        Belirtilen çalışma ID'lerine ait dosyaları getirir
        
        Args:
            study_ids: Çalışma ID'leri (örn: "87" veya "87-95,137")
            page: Sayfa numarası
            size: Sayfa başına sonuç sayısı
            all_files: Gizli dosyaları da dahil et
        
        Returns:
            Dosya bilgilerini içeren dictionary
        """
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
            return {}
    
    def get_study_metadata(self, study_id: str) -> Dict:
        """
        Belirtilen çalışmanın metadata bilgilerini getirir
        
        Args:
            study_id: Çalışma ID'si (örn: "137")
        
        Returns:
            Metadata bilgilerini içeren dictionary
        """
        meta_url = f"{self.BASE_URL}/osd/meta/{study_id}"
        
        try:
            response = self.session.get(meta_url, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Metadata alınırken hata oluştu: {e}")
            return {}
    
    def display_search_results(self, results: Dict) -> None:
        """Arama sonuçlarını formatlı şekilde gösterir"""
        if not results or 'hits' not in results:
            print("Sonuç bulunamadı.")
            return
        
        print(f"\n{'='*80}")
        print(f"Toplam {results.get('hits', 0)} sonuç bulundu")
        print(f"{'='*80}\n")
        
        # Sonuçları göster
        for item in results.get('results', []):
            
            print(f"Başlık: {item.get('Study Title', 'N/A')}")
            print(f"Açıklama: {item.get('Study Description', 'N/A')[:200]}...")
            print(f"Organizm: {item.get('organism', 'N/A')}")
           
            print(f"{'-'*80}\n")
    
    def display_file_info(self, file_data: Dict) -> None:
        """Dosya bilgilerini formatlı şekilde gösterir"""
        if not file_data or 'studies' not in file_data:
            print("Dosya bilgisi bulunamadı.")
            return
        
        print(f"\n{'='*80}")
        print(f"Toplam {file_data.get('hits', 0)} çalışma bulundu")
        print(f"{'='*80}\n")
        
        for study_id, study_info in file_data.get('studies', {}).items():
            print(f"Çalışma: {study_id}")
            
            print(f"\nDosyalar:")
            
            for file in study_info.get('study_files', [])[:5]:  # İlk 5 dosyayı göster
                print(f"  - {file.get('file_name', 'N/A')}")
                print(f"    Kategori: {file.get('category', 'N/A')}")
                
                print(f"    URL: https://osdr.nasa.gov{file.get('remote_url', '')}\n")
            
            if study_info.get('file_count', 0) > 5:
                print(f"  ... ve {study_info.get('file_count', 0) - 5} dosya daha\n")
            print(f"{'-'*80}\n")


def main():
    """Ana fonksiyon - Kullanım örneği"""
    print("NASA OSDR API Arama Aracı")
    print("="*80)
    
    # Arama aracını başlat
    searcher = NasaOSDRSearch()
    
    # Kullanıcıdan arama kelimesi al
    keyword = input("\nAramak istediğiniz kelimeyi girin: ").strip()
    
    if not keyword:
        print("Arama kelimesi boş olamaz!")
        return
    
    # Arama yap
    print(f"\n'{keyword}' kelimesi aranıyor...")
    results = searcher.search_studies(keyword, size=10)
    
    # Sonuçları göster
    searcher.display_search_results(results)
    
    # Eğer sonuç varsa, ilk çalışmanın dosyalarını göster
    if results.get('results'):
        first_study = results['results'][0]
        study_id = first_study.get('Accession', '').replace('OSD-', '')
        
        if study_id:
            print(f"\nİlk çalışmanın (OSD-{study_id}) dosyaları getiriliyor...")
            file_info = searcher.get_study_files(study_id)
            searcher.display_file_info(file_info)


if __name__ == "__main__":
    main() 
