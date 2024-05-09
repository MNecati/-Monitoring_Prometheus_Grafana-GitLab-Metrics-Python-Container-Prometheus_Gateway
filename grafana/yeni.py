import requests
import schedule
import time
from datetime import datetime, timedelta

# GitLab API'lerinin URL'leri
users_api_url = 'http://192.168.2.108:8929/api/v4/users'
projects_api_url = 'http://192.168.2.108:8929/api/v4/projects'

# GitLab API'lerine istek yapmak için kullanılacak token
gitlab_token = 'glpat-vDyvd94KWdxDPC993ePU'

# GitLab API'lerine istek yaparken kullanılacak header
headers = {'Private-Token': gitlab_token}

def get_gitlab_data(api_url):
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # HTTP hatalarını kontrol et
        return response.json()
    except requests.exceptions.RequestException as e:
        print("Request Error:", e)
        return None

def run_metrics():
    print(f"Starting task at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    users_data = get_gitlab_data(users_api_url)
    projects_data = get_gitlab_data(projects_api_url)

    if users_data and projects_data:
        # Prometheus için metrikler oluştur
        metrics = []
        metrics.append(f'gitlab_user_count {len(users_data)}\n')
        metrics.append(f'gitlab_project_count {len(projects_data)}\n')

        # Kullanıcı isimleri için metrikler
        for user in users_data:
            metrics.append(f'user_exists{{username="{user["username"]}"}} 1\n')

        # Proje isimleri için metrikler
        for project in projects_data:
            metrics.append(f'project_exists{{project_name="{project["name"]}"}} 1\n')

        # Metrikleri ekrana yazdır
        for metric in metrics:
            print(metric)

        # Pushgateway'in URL'si
        pushgateway_url = 'http://192.168.2.108:9091/metrics/job/gitlab_metrics'

        # Pushgateway'e metrikleri gönder (HTTP POST isteği kullanarak)
        try:
            response = requests.post(pushgateway_url, data=''.join(metrics), headers={"Content-Type": "text/plain"})
            response.raise_for_status()  # HTTP hatalarını kontrol et
            print("Metrikler başarıyla Pushgateway'e gönderildi.")
        except requests.exceptions.RequestException as e:
            print(f"Request Error: {e}")
    else:
        print("Hata! Kullanıcı veya proje verileri alınamadı.")

    next_run = datetime.now() + timedelta(minutes=10)
    print(f"Next run will be at {next_run.strftime('%Y-%m-%d %H:%M:%S')}")

# Her 10 dakikada bir görevi zamanlayıcıya ekle
schedule.every(10).minutes.do(run_metrics)

# İlk çalışmayı başlat
run_metrics()

# Sonsuz döngü içinde zamanlayıcıyı çalıştır
while True:
    schedule.run_pending()
    time.sleep(60)  # Her dakika kontrol et
