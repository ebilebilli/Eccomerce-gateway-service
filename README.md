# Ecommerce Gateway Service

Bu proje, ecommerce mikroservisleri için API Gateway servisidir. FastAPI kullanılarak geliştirilmiştir ve shop service ile shopping cart service'leri arasında proxy görevi görür.

## Proje Yapısı

```
eccomerce-gateway-service/
├── gateway/
│   ├── main.py              # FastAPI uygulaması
│   ├── schemas.py           # Pydantic modelleri
│   ├── services/
│   │   ├── shop_service.py      # Shop servisi proxy
│   │   └── shop_cart_service.py # Shopping cart servisi proxy
│   └── utils/
│       └── forward.py       # HTTP istekleri yönlendirme
├── Dockerfile
├── docker-compose.yml
├── docker-compose.dev.yml
├── docker-compose.prod.yml
├── requirements.txt
└── .env
```

## Özellikler

- **API Gateway**: Shop ve shopping cart servisleri için merkezi giriş noktası
- **Proxy Pattern**: HTTP isteklerini backend servislere yönlendirme
- **FastAPI**: Modern, hızlı web framework
- **Docker Support**: Containerization desteği
- **Health Checks**: Servis sağlık kontrolü
- **Environment Configuration**: Ortam değişkenleri ile konfigürasyon

## API Endpoints

### Shop Service Endpoints
- `GET /shops/` - Mağaza listesi
- `GET /shops/{shop_slug}/` - Mağaza detayı
- `POST /shops/create/` - Yeni mağaza oluşturma
- `PATCH/DELETE /shops/{shop_slug}/management/` - Mağaza yönetimi
- `GET /shops/{shop_slug}/comments/` - Mağaza yorumları
- `POST /shops/{shop_slug}/comment/create/` - Yorum oluşturma
- `GET /shops/{shop_slug}/branches/` - Mağaza şubeleri
- `GET /shops/{shop_slug}/social-media/` - Sosyal medya hesapları
- `GET /shops/{shop_slug}/media/` - Mağaza medya dosyaları

### Shopping Cart Service Endpoints
- `POST /shopcart/` - Sepet oluşturma
- `GET /shopcart/mycart` - Kullanıcı sepeti
- `GET /shopcart/{cart_id}` - Belirli sepet
- `POST /shopcart/items` - Sepete ürün ekleme
- `PUT /shopcart/items/update/{item_id}` - Sepet öğesi güncelleme
- `DELETE /shopcart/items/delete/{item_id}` - Sepet öğesi silme

## Docker ile Çalıştırma

### Development Ortamı
```bash
# Development ortamında çalıştırma
docker-compose -f docker-compose.dev.yml up --build

# Arka planda çalıştırma
docker-compose -f docker-compose.dev.yml up -d --build
```

### Production Ortamı
```bash
# Production ortamında çalıştırma
docker-compose -f docker-compose.prod.yml up --build

# Arka planda çalıştırma
docker-compose -f docker-compose.prod.yml up -d --build
```

### Temel Docker Compose
```bash
# Temel konfigürasyon ile çalıştırma
docker-compose up --build
```

## Servis Portları

- **Gateway Service**: `http://localhost:8000`
- **Shop Service**: `http://localhost:8001`
- **Shopping Cart Service**: `http://localhost:8002`
- **API Documentation**: `http://localhost:8000/docs`

## Environment Variables

`.env` dosyasında aşağıdaki değişkenleri ayarlayın:

```env
# Servis URL'leri
SHOP_SERVICE=http://shop-service:8000
SHOPCART_SERVICE=http://shopcart-service:8000

# Gateway konfigürasyonu
GATEWAY_HOST=0.0.0.0
GATEWAY_PORT=8000

# Veritabanı (opsiyonel)
# DATABASE_URL=postgresql://user:password@postgres:5432/ecommerce
# REDIS_URL=redis://redis:6379
```

## Geliştirme

### Lokal Geliştirme
```bash
# Virtual environment oluşturma
python -m venv gatewayvenv

# Virtual environment aktifleştirme
# Windows:
gatewayvenv\Scripts\activate
# Linux/Mac:
source gatewayvenv/bin/activate

# Bağımlılıkları yükleme
pip install -r requirements.txt

# Uygulamayı çalıştırma
uvicorn gateway.main:app --reload
```

### Yeni Servis Ekleme
1. `gateway/services/` klasörüne yeni servis dosyası ekleyin
2. `gateway/main.py` dosyasında router'ı dahil edin
3. `.env` dosyasında servis URL'ini tanımlayın
4. Docker Compose dosyalarını güncelleyin

## Monitoring ve Health Checks

Gateway servisi otomatik health check'ler içerir:
- Her 30 saniyede bir kontrol
- 10 saniye timeout
- 3 retry denemesi
- 40 saniye başlangıç süresi

Health check endpoint: `http://localhost:8000/docs`

## Troubleshooting

### Servis Bağlantı Sorunları
1. Environment variables'ları kontrol edin
2. Servis URL'lerinin doğru olduğundan emin olun
3. Docker network'ünün çalıştığını kontrol edin

### Port Çakışmaları
Eğer portlar kullanımda ise, `docker-compose.yml` dosyasında port numaralarını değiştirin.

### Log Kontrolü
```bash
# Container loglarını görüntüleme
docker-compose logs gateway

# Belirli servisin loglarını takip etme
docker-compose logs -f gateway
```

## Notlar

- Bu proje placeholder servislerle gelir (nginx)
- Gerçek shop ve cart servislerinizi bu placeholder'ların yerine koyun
- Production ortamında güvenlik ayarlarını gözden geçirin
- Database ve Redis servisleri opsiyoneldir, ihtiyacınıza göre aktifleştirin