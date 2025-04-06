# HeyRaina Trading Bot
Bot untuk kirim signal trading berdasarkan RSI dan Moving Average via Telegram.
Deploy ke Railway atau VPS.

## Setup
1. Buat `.env` file dari `.env.example`
2. Install package:
```
pip install -r requirements.txt
```
3. Jalankan
```
python main.py
```

## Deploy Railway
- Pastikan ada `Procfile`, `runtime.txt`, `requirements.txt`, dan `.env`