# Sinf Sayti - Django Loyihasi

Bu loyiha sizning talablaringiz asosida yaratilgan "Sinf Sayti" uchun to'liq funksional Django ilovasi.

## Loyiha Tuzilishi

*   **SinfSayti/**: Asosiy loyiha konfiguratsiyasi.
    *   `settings.py`: Loyiha sozlamalari (Tailwind, Media, Static, I18N).
    *   `urls.py`: Asosiy URL marshrutizatsiyasi.
*   **main/**: Asosiy ilova.
    *   `models.py`: O'quvchi, Sharh, Sinf Rahbari, Haftalik Lider modellari.
    *   `views.py`: Barcha sahifalar uchun funksiyalar (Home, Ro'yxat, Profil, Lider).
    *   `urls.py`: Ilova darajasidagi URL marshrutizatsiyasi.
    *   `forms.py`: Sharh qoldirish formasi.
    *   `admin.py`: Admin panel konfiguratsiyasi.
    *   `management/commands/calculate_leader.py`: Haftalik liderni hisoblash uchun boshqaruv buyrug'i.
*   **templates/**: Global HTML shablonlar.
    *   `base.html`: Barcha sahifalar uchun asosiy shablon (Tailwind CSS bilan).
*   **main/templates/main/**: Ilova shablonlari.
    *   `home.html`: Bosh sahifa.
    *   `student_list.html`: O'quvchilar ro'yxati.
    *   `student_detail.html`: O'quvchi profili va sharhlar.
    *   `weekly_leader.html`: Haftalik lider sahifasi.
*   **static/**: Statik fayllar (CSS, JS, Image).
*   **media/**: O'quvchilar rasmlari uchun.

## O'rnatish va Ishga Tushirish

1.  **Virtual muhitni faollashtirish:**
    ```bash
    . venv/bin/activate
    ```

2.  **Kerakli kutubxonalarni o'rnatish:**
    ```bash
    pip install -r requirements.txt
    ```
    *(requirements.txt fayli keyingi bosqichda yaratiladi)*

3.  **Ma'lumotlar bazasini yaratish:**
    ```bash
    python manage.py migrate
    ```

4.  **Superuser yaratish (Admin panel uchun):**
    ```bash
    python manage.py createsuperuser
    ```
    *(Biz avval 'admin' / 'admin' bilan yaratdik, lekin bu buyruqni bilishingiz kerak)*

5.  **Loyiha ishga tushirish:**
    ```bash
    python manage.py runserver
    ```

## Haftalik Liderni Avtomatik Yangilash (Cron Job)

Haftalik liderni avtomatik yangilash uchun siz **cron job** o'rnatishingiz kerak. Bu buyruqni har hafta dushanba kuni soat 00:00 da ishga tushirish tavsiya etiladi.

1.  **Crontabni tahrirlash:**
    ```bash
    crontab -e
    ```

2.  **Quyidagi qatorni qo'shing:**
    *(Eslatma: `PATH_TO_PROJECT` o'rniga loyihangiz joylashgan to'liq yo'lni qo'ying, masalan, `/home/user/SinfSayti`)*

    ```cron
    # Har hafta dushanba kuni soat 00:00 da haftalik liderni hisoblash
    0 0 * * 1 /usr/bin/python3 PATH_TO_PROJECT/manage.py calculate_leader >> PATH_TO_PROJECT/cron.log 2>&1
    ```
    
    Agar virtual muhitdan foydalansangiz, quyidagicha bo'lishi mumkin:
    ```cron
    # Har hafta dushanba kuni soat 00:00 da haftalik liderni hisoblash
    0 0 * * 1 /bin/bash -c "source PATH_TO_PROJECT/venv/bin/activate && python PATH_TO_PROJECT/manage.py calculate_leader" >> PATH_TO_PROJECT/cron.log 2>&1
    ```

## Loyihani Yakunlash

Loyiha to'liq tayyor. Endi uni yakuniy tekshiruvdan o'tkazib, sizga fayllarni taqdim etishimiz mumkin.
