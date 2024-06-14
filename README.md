# URL Scanner

Bu basit Python betiği, verilen bir URL üzerinde güvenlik kontrolleri yaparak potansiyel güvenlik açıklarını tespit eder ve raporlar.

## Kurulum

### Linux ve PC Kullanıcıları için:

1. Bilgisayarınıza Python 3 kurulu olmalıdır. Eğer yoksa, Python'u [Python.org](https://www.python.org/downloads/) adresinden indirin ve kurun.

2. Bu GitHub deposunu bilgisayarınıza klonlayın. Bunun için bir terminal açın ve aşağıdaki komutu çalıştırın:

    ```bash
    git clone https://github.com/your_username/url-scanner.git
    ```

3. Terminali proje dizinine taşımak için aşağıdaki komutu kullanın:

    ```bash
    cd url-scanner
    ```

4. Gerekli Python paketlerini yükleyin:

    ```bash
    pip install -r requirements.txt
    ```

### Termux (Android) Kullanıcıları için:

1. Termux uygulamasını indirin ve kurun. Eğer henüz yüklemediyseniz, [Google Play Store](https://play.google.com/store/apps/details?id=com.termux) veya [F-Droid](https://f-droid.org/packages/com.termux/) üzerinden indirebilirsiniz.

2. Termux uygulamasını açın ve Python'u yüklemek için aşağıdaki komutu çalıştırın:

    ```bash
    pkg install python
    ```

3. Ardından, bu GitHub deposunu klonlayın:

    ```bash
    git clone https://github.com/your_username/url-scanner.git
    ```

4. Proje dizinine gidin:

    ```bash
    cd url-scanner
    ```

5. Gerekli Python paketlerini yükleyin:

    ```bash
    pip install -r requirements.txt
    ```

## Kullanım

1. Terminali açın ve proje dizinine gidin.

2. Python betiğini çalıştırın:

    ```bash
    python scanner.py
    ```

3. Açılan menüden "URL Tarayıcı" seçeneğini seçin.

4. Bir URL girin ve taramayı başlatın. 

5. Tarama sonuçlarını inceleyin.

## Komutlar

- Python betiğini çalıştırmak için:

    ```bash
    python scanner.py
    ```

- Gerekli Python paketlerini yüklemek için:

    ```bash
    pip install -r requirements.txt
    ```

## Kullanılan Modüller

- requests: HTTP istekleri yapmak için kullanılır.
- BeautifulSoup: HTML ve XML belgelerini ayrıştırmak için kullanılır.
- logging: Uygulama günlüklerini yönetmek için kullanılır.
- socket: Ağ ile iletişim kurmak için kullanılır.
- os: İşletim sistemi işlevlerine erişmek için kullanılır.
