# 💬 Realtime Messenger — پیام‌رسان Real-time با Django + Docker

یک پیام‌رسان کامل و Real-time با **Django Channels** و **WebSocket** که از چت خصوصی، چت گروهی، ارسال/ویرایش/حذف لحظه‌ای پیام، و احراز هویت با OTP پشتیبانی می‌کند.

کل پروژه با **Docker** کانتینری شده و از **PostgreSQL** به‌عنوان دیتابیس اصلی استفاده می‌کند.

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-4.2+-092E20?style=for-the-badge&logo=django&logoColor=white)
![Channels](https://img.shields.io/badge/Django%20Channels-4.0+-blueviolet?style=for-the-badge)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-7+-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

---

## 📌 درباره پروژه

**Realtime Messenger** یک پیام‌رسان کامل است که با هدف تمرین و نمایش توانمندی‌های **Django**، **Django Channels** و **Docker** ساخته شده. تمرکز اصلی این پروژه روی **Backend**، **Real-time Communication**، **معماری Async** و **کانتینری‌سازی** است.

### ✨ چرا این پروژه؟

- ✅ پیاده‌سازی کامل **WebSocket** با `AsyncWebsocketConsumer`
- ✅ ارتباط **Real-time** بین چند کاربر همزمان
- ✅ **احراز هویت با OTP** (بدون نیاز به رمز عبور)
- ✅ **Dockerize شده** با `docker-compose` (App + PostgreSQL + Redis)
- ✅ **PostgreSQL** به عنوان دیتابیس اصلی
- ✅ **Redis** به عنوان Channel Layer در production
- ✅ معماری تمیز و ماژولار Django

---

## 🚀 شروع سریع با Docker

### پیش‌نیاز
- [Docker](https://www.docker.com/products/docker-desktop) نصب باشد
- [Docker Compose](https://docs.docker.com/compose/install/) (معمولاً همراه Docker Desktop هست)

### دستورات راه‌اندازی

```bash
# 1. ساخت و اجرای کانتینرها
docker compose up --build

# 2. ساخت کاربر ادمین (در ترمینال جداگانه)
docker compose exec app python manage.py createsuperuser