Paket ini dibuat untuk Railway dengan mode aman buat repo public:
session disimpan sebagai `TG_STRING_SESSION` di Railway Variables.

Isi folder:
- `listener.py` -> listener Telegram (Telethon)
- `export_string_session.py` -> ubah `session_test.session` jadi string session
- `requirements.txt` -> dependency Python
- `railway.json` -> start command otomatis untuk Railway
- `.env.example` -> contoh variabel environment

Langkah cepat deploy:
1. Dari mesin lokal, generate string session:
   - simpan `session_test.session` di folder ini
   - jalankan:
     - PowerShell: `$env:TG_API_ID="39135133"; $env:TG_API_HASH="isi_api_hash"; python export_string_session.py`
   - copy output string panjangnya
2. Buat project baru di Railway (Empty Project).
3. Deploy folder ini (via GitHub repo atau `railway up` dari folder ini).
4. Set Variables di Railway:
   - `TG_API_ID`
   - `TG_API_HASH`
   - `TG_STRING_SESSION` (hasil langkah 1)
5. Redeploy, lalu cek logs.

Catatan penting:
- Di Railway tidak ada browser desktop, jadi script akan log URL ke logs, bukan membuka Chrome.
- Kalau deploy via GitHub public, jangan commit file `.session`.
- `listener.py` tetap support file session kalau `TG_STRING_SESSION` tidak diisi.
