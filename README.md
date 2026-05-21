<div align="center">

# 🍱 SPPG Management System

**Custom ERPNext / Frappe Application**  
Sistem Operasional Satuan Pelaksana Program Gizi (SPPG) & Makan Bergizi Gratis (MBG)

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/USERNAME/sppg_management/releases)
[![ERPNext](https://img.shields.io/badge/ERPNext-v14%20%7C%20v15-green.svg)](https://erpnext.com)
[![Frappe](https://img.shields.io/badge/Frappe-v14%20%7C%20v15-orange.svg)](https://frappeframework.com)
[![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://python.org)

</div>

---

## 📋 Daftar Isi

- [Tentang Modul](#-tentang-modul)
- [Versi & Changelog](#-versi--changelog)
- [Persyaratan Sistem](#-persyaratan-sistem)
- [Fitur Lengkap](#-fitur-lengkap)
- [Alur Operasional](#-alur-operasional)
- [Doctype yang Tersedia](#-doctype-yang-tersedia)
- [Instalasi di ERPNext Self-Hosted](#-instalasi-di-erpnext-self-hosted)
- [Instalasi di Frappe Cloud](#-instalasi-di-frappe-cloud)
- [Konfigurasi Awal Setelah Install](#-konfigurasi-awal-setelah-install)
- [Role & Hak Akses](#-role--hak-akses)
- [REST API](#-rest-api)
- [Integrasi ERPNext Standard](#-integrasi-erpnext-standard)
- [Troubleshooting](#-troubleshooting)
- [Kontribusi](#-kontribusi)
- [Lisensi](#-lisensi)

---

## 🍽 Tentang Modul

**SPPG Management System** adalah custom ERPNext application yang dirancang khusus untuk mendukung operasional **dapur penyedia Makan Bergizi Gratis (MBG)** secara end-to-end.

Modul ini mengintegrasikan seluruh rantai operasional mulai dari:

> **Kontrak** → **Menu Plan** → **Kebutuhan Bahan** → **Stok & Pembelian** → **Produksi Dapur** → **Quality Check** → **Pemorsian** → **Distribusi** → **Cost Control** → **Dashboard Owner**

Dirancang untuk dijalankan di atas ERPNext v14 / v15 dengan memanfaatkan modul standar Stock, Buying, Selling, Accounting, dan HRMS.

---

## 🏷 Versi & Changelog

### Version 1.0.0 — MVP Release *(Current)*
> Tanggal Rilis: 2025

**New Features:**
- ✅ 30 Doctype custom (master data, transaksi, child tables)
- ✅ 6 Workflow otomatis (Kontrak, Menu, Produksi, Delivery, Purchase, QC)
- ✅ Auto-calculate kebutuhan bahan dari Menu Plan
- ✅ Auto-generate Stock Forecast & Purchase Planning saat Menu Plan dikonfirmasi
- ✅ Auto-generate Delivery Plan saat Pemorsian selesai
- ✅ Kalkulasi HPP / Cost Per Portion otomatis
- ✅ Validasi Angka Kecukupan Gizi (AKG) pada Master Menu
- ✅ 3 Script Report (Menu Plan Harian, Cost Per Portion, Stok Kritis)
- ✅ Workspace SPPG Management dengan 35+ shortcut terorganisir
- ✅ 11 Role dengan permission matrix lengkap
- ✅ 8 REST API endpoint (mobile-ready)
- ✅ Client Script untuk UX (warning stok, auto-fetch, custom buttons)
- ✅ Integrasi: Stock Entry, Material Request, Purchase Order, Sales Order

**Known Limitations v1.0.0:**
- Dashboard Number Card & Chart belum di-generate otomatis (perlu dibuat manual di ERPNext setelah install)
- Integrasi payroll HRMS masih manual (belum otomatis pull dari Payroll Entry)
- GPS tracking driver belum real-time (field tersedia, implementasi perlu mobile app terpisah)

---

**Roadmap Version 1.1.0** *(Planned)*
- [ ] Number Card & Dashboard Chart JSON fixtures
- [ ] Laporan tambahan: Variance Produksi, P&L Kontrak, Supplier Evaluation
- [ ] Auto-complete contract via scheduler
- [ ] Kalender Menu MBG (rotasi menu bulanan)
- [ ] Notifikasi email alert stok kritis & expired

---

**Roadmap Version 2.0.0** *(Planned)*
- [ ] Mobile App API lengkap (driver app, dapur app)
- [ ] Multi-SPPG Unit dashboard konsolidasi
- [ ] Integrasi HRMS payroll otomatis ke Cost Per Portion
- [ ] Price comparison & supplier evaluation otomatis
- [ ] Export laporan ke Excel/PDF

---

## 💻 Persyaratan Sistem

| Komponen | Versi Minimum | Versi Direkomendasikan |
|---|---|---|
| **ERPNext** | v14.0.0 | v15.x (latest) |
| **Frappe Framework** | v14.0.0 | v15.x (latest) |
| **Python** | 3.10 | 3.11+ |
| **MariaDB** | 10.6 | 10.11+ |
| **Node.js** | 16.x | 18.x |
| **Redis** | 6.x | 7.x |

**Modul ERPNext yang Harus Aktif:**
- ✅ Stock (wajib)
- ✅ Buying (wajib)
- ✅ Selling (direkomendasikan)
- ✅ Accounts (direkomendasikan)
- ⬜ HRMS (opsional — untuk integrasi payroll)

---

## ✨ Fitur Lengkap

### 1. 🏢 Master Data Management

| Fitur | Deskripsi |
|---|---|
| **SPPG Unit** | Data unit/cabang operasional dapur, mapping ke Cost Center & Warehouse ERPNext |
| **Konsumen MBG** | Data sekolah/lembaga penerima dengan PIC, area distribusi, koordinat GPS |
| **Sasaran Penerima MBG** | Kelompok usia (PAUD, SD, SMP, SMA) beserta rentang usia |
| **Angka Kecukupan Gizi (AKG)** | Standar gizi per kelompok sasaran & tipe layanan (pagi/siang/malam) |
| **Kategori Produk MBG** | Kategori bahan baku dan masakan (lauk, sayur, buah, dll) |
| **Produk MBG** | Master bahan baku dengan nilai gizi per 100g, link ke Item ERPNext |
| **Produk Hasil Masakan** | Produk jadi dengan komposisi gizi, yield %, prosedur masak |
| **Standar Porsi MBG** | Berat standar porsi per produk per kelompok sasaran |
| **Area Distribusi** | Zona pengiriman dengan estimasi jarak & waktu tempuh |
| **Driver & Vehicle** | Data pengemudi dan kendaraan pengiriman |

---

### 2. 📄 Manajemen Kontrak

| Fitur | Deskripsi |
|---|---|
| **Kontrak Penyediaan MBG** | Kontrak resmi dengan konsumen; periode, harga/porsi, tipe layanan |
| **Detail Penerima Manfaat** | Daftar penerima per kelompok sasaran dalam satu kontrak |
| **Jadwal Layanan** | Hari dan jam layanan per kontrak |
| **Auto-generate Sales Order** | Saat kontrak disubmit, otomatis membuat Sales Order di ERPNext |
| **Workflow 5-step** | Draft → Diajukan → Dikonfirmasi → Kontrak Berjalan → Selesai |
| **Auto-complete by scheduler** | Kontrak yang melewati end_date otomatis berubah Selesai |

---

### 3. 🥗 Master Menu & Validasi Gizi

| Fitur | Deskripsi |
|---|---|
| **Master Menu MBG** | Kumpulan produk masakan untuk satu kali saji |
| **Auto-calculate Nilai Gizi** | Total energi, protein, lemak, karbohidrat, natrium dihitung otomatis |
| **Validasi vs AKG** | Status gizi: Sesuai / Kurang / Melebihi / Perlu Review Ahli Gizi |
| **Toleransi AKG** | Batas toleransi atas/bawah persen yang bisa dikonfigurasi |
| **Workflow Approval** | Draft → Review Ahli Gizi → Disetujui → Aktif |
| **Menu Substitution** | Doctype untuk penggantian menu darurat |

---

### 4. 📅 Menu Plan Harian

| Fitur | Deskripsi |
|---|---|
| **Menu Plan MBG** | Rencana menu operasional harian per kontrak |
| **Auto-calculate Kebutuhan Bahan** | Standar porsi × jumlah penerima = total kebutuhan per bahan (kg) |
| **Auto-fetch Harga Bahan** | Estimasi biaya bahan dari valuation rate Item ERPNext |
| **Cek Stok Otomatis** | Bandingkan kebutuhan vs stok tersedia di warehouse |
| **Status Stok** | Stock Available / Stock Shortage dengan indikator visual merah/hijau |
| **Generate Stock Forecast** | Saat submit, otomatis membuat Stock Forecast MBG |
| **Generate Purchase Planning** | Jika stok kurang, otomatis membuat Purchase Planning MBG |
| **Generate Production Plan** | Tombol custom untuk membuat Production Plan dari Menu Plan |
| **Estimasi HPP** | Estimated Cost Per Portion tampil real-time |

---

### 5. 📦 Stok & Pembelian

| Fitur | Deskripsi |
|---|---|
| **Stock Forecast MBG** | Proyeksi kebutuhan bahan dari Menu Plan, per item per tanggal |
| **Purchase Planning MBG** | Rencana pembelian otomatis dari shortage stok |
| **Auto Material Request** | Saat Purchase Planning disubmit, otomatis buat Material Request di ERPNext |
| **Link ke Purchase Order** | Purchase Planning bisa dilanjutkan ke PO via flow ERPNext standard |
| **Monitoring Stok Kritis** | Laporan & alert harian untuk item di bawah reorder level |
| **Monitoring Expired** | Scheduler harian cek batch mendekati expired (≤7 hari), kirim email alert |

---

### 6. 🔥 Produksi Dapur

| Fitur | Deskripsi |
|---|---|
| **Production Plan MBG** | Rencana produksi harian dengan shift dan kepala dapur |
| **Auto Stock Entry** | Saat Production Plan submit, otomatis buat Stock Entry Material Issue |
| **Cooking Batch MBG** | Eksekusi masak per batch: waktu mulai/selesai, suhu, chef, bahan |
| **Quality Check MBG** | Pengecekan suhu, visual, bau, tekstur, rasa sebelum pemorsian |
| **Workflow QC** | QC Passed → Siap Pemorsian; QC Failed → kembali ke produksi |
| **Waste Food MBG** | Pencatatan waste per kategori (bahan baku, produksi, distribusi) |

---

### 7. 🥡 Pemorsian

| Fitur | Deskripsi |
|---|---|
| **Pemorsian MBG** | Pencatatan porsi aktual yang berhasil dibuat |
| **Tracking Variance** | Selisih target vs aktual porsi dicatat otomatis |
| **Detail per Sasaran** | Porsi per kelompok sasaran (PAUD, SD, dll) |
| **Auto-update Menu Plan** | Actual portion otomatis diperbarui di Menu Plan |
| **Auto-generate Delivery Plan** | Saat pemorsian submit, otomatis membuat Delivery Plan MBG |

---

### 8. 🚚 Distribusi & Pengiriman

| Fitur | Deskripsi |
|---|---|
| **Delivery Plan MBG** | Rencana pengiriman dengan driver, kendaraan, rute |
| **Route Delivery** | Multi-titik tujuan dalam satu pengiriman dengan urutan & target waktu |
| **Update Status per Titik** | Lacak status per konsumen: Menunggu / Dalam Perjalanan / Diterima / Gagal |
| **Proof of Delivery** | Upload foto penerimaan + nama penerima (siap mobile app) |
| **Delivery Issue** | Pencatatan masalah pengiriman dengan tipe dan tindakan |
| **Workflow 6-step** | Draft → Siap Kirim → Dalam Perjalanan → Diterima → Selesai |
| **Alert Bermasalah** | Status "Bermasalah" wajib isi Delivery Issue dan eskalasi ke Manager |

---

### 9. 💰 Cost Control & Finance

| Fitur | Deskripsi |
|---|---|
| **Cost Per Portion MBG** | Kalkulasi HPP aktual per porsi per hari |
| **Komponen Biaya Lengkap** | Bahan baku + packaging + gas + transport + tenaga kerja + waste + overhead |
| **HPP Plan vs Aktual** | Bandingkan target HPP dengan realisasi, tampilkan variance |
| **Gross Margin** | Hitung margin keuntungan dari harga jual kontrak |
| **Auto-trigger** | Cost Per Portion dihitung otomatis saat Menu Plan selesai |
| **Link ke GL ERPNext** | Data bisa disinkronkan dengan Cost Center di Accounting ERPNext |

---

### 10. 📊 Laporan

| Laporan | Tipe | Deskripsi |
|---|---|---|
| **Laporan Menu Plan Harian** | Script Report | Detail menu plan per tanggal/unit/konsumen |
| **Laporan Cost Per Portion** | Script Report | HPP plan vs aktual, margin, variance per periode |
| **Laporan Stok Kritis** | Script Report | Item di bawah reorder level di semua warehouse |

---

### 11. 🔌 REST API (Mobile-Ready)

8 endpoint whitelisted untuk integrasi mobile app driver & dapur:

```
GET  /api/method/sppg_management.sppg_management.api.get_owner_dashboard_summary
GET  /api/method/sppg_management.sppg_management.api.get_today_menu_plan
GET  /api/method/sppg_management.sppg_management.api.get_today_production_tasks
GET  /api/method/sppg_management.sppg_management.api.get_driver_delivery_tasks
POST /api/method/sppg_management.sppg_management.api.update_delivery_status
POST /api/method/sppg_management.sppg_management.api.submit_pod
GET  /api/method/sppg_management.sppg_management.api.get_stock_shortage
POST /api/method/sppg_management.sppg_management.api.calculate_cost_per_portion
```

---

## 🔄 Alur Operasional

```
[Setup Master Data]
     SPPG Unit → Konsumen MBG → Sasaran → AKG → Produk → Standar Porsi → Master Menu
           ↓
[Kontrak]
     Kontrak Penyediaan MBG (Draft → Kontrak Berjalan)
           ↓
[Menu Plan Harian]
     Menu Plan MBG → Auto-check stok → Stock Forecast → Purchase Planning
           ↓                                                    ↓
[Pembelian]                                          Material Request → Purchase Order
           ↓
[Produksi]
     Production Plan MBG → Cooking Batch → Quality Check
           ↓
[Pemorsian]
     Pemorsian MBG → Auto-create Delivery Plan
           ↓
[Distribusi]
     Delivery Plan → Dalam Perjalanan → Proof of Delivery → Selesai
           ↓
[Cost Control]
     Cost Per Portion MBG (Auto-calc HPP Aktual vs Plan)
```

---

## 📁 Doctype yang Tersedia

<details>
<summary><b>Master Data (10 Doctype)</b></summary>

| Doctype | Naming Series | Keterangan |
|---|---|---|
| SPPG Unit | `SPPG-.YYYY.-.#####` | Unit/cabang operasional |
| Konsumen MBG | `KONS-.YYYY.-.#####` | Sekolah/lembaga penerima |
| Sasaran Penerima MBG | `SAR-.#####` | Kelompok usia sasaran |
| Angka Kecukupan Gizi | `AKG-.#####` | Standar gizi per sasaran |
| Kategori Produk MBG | field:category_name | Kategori produk |
| Produk MBG | `PROD-.#####` | Bahan baku |
| Produk Hasil Masakan | `MAS-.#####` | Produk jadi/masakan |
| Standar Porsi MBG | `SPR-.#####` | Berat porsi standar |
| Area Distribusi | field:area_name | Zona distribusi |
| Driver | `DRV-.#####` | Data driver |
| Vehicle | `VHL-.#####` | Data kendaraan |

</details>

<details>
<summary><b>Kontrak (3 Doctype + 2 Child Table)</b></summary>

| Doctype | Naming Series | Keterangan |
|---|---|---|
| Kontrak Penyediaan MBG | `KMBG-.YY.MM.-.####` | Kontrak utama *(Submittable)* |
| Detail Penerima Manfaat | — | Child table penerima |
| Detail Jadwal Layanan MBG | — | Child table jadwal |

</details>

<details>
<summary><b>Menu Plan (3 Doctype + 2 Child Table)</b></summary>

| Doctype | Naming Series | Keterangan |
|---|---|---|
| Master Menu MBG | `MENU-.YYYY.-.#####` | Kumpulan menu *(Submittable)* |
| Detail Menu MBG | — | Child: produk dalam menu |
| Menu Plan MBG | `MNU-.YY.MM.-.####` | Rencana harian *(Submittable)* |
| Detail Menu Plan | — | Child: kebutuhan bahan |

</details>

<details>
<summary><b>Stok & Pembelian (3 Doctype + 2 Child Table)</b></summary>

| Doctype | Naming Series | Keterangan |
|---|---|---|
| Stock Forecast MBG | `SF-.YY.MM.-.####` | Proyeksi kebutuhan stok |
| Stock Forecast Detail | — | Child: per item |
| Purchase Planning MBG | `PPM-.YY.MM.-.####` | Rencana pembelian *(Submittable)* |
| Purchase Planning Item MBG | — | Child: item yang dibeli |

</details>

<details>
<summary><b>Produksi (5 Doctype + 2 Child Table)</b></summary>

| Doctype | Naming Series | Keterangan |
|---|---|---|
| Production Plan MBG | `PRD-.YY.MM.-.####` | Rencana produksi *(Submittable)* |
| Cooking Batch MBG | `CB-.YY.MM.-.####` | Eksekusi masak *(Submittable)* |
| Detail Batch Produksi | — | Child: bahan per batch |
| Quality Check MBG | `QC-.YY.MM.-.####` | QC checklist *(Submittable)* |
| Waste Food MBG | `WF-.YY.MM.-.####` | Pencatatan waste *(Submittable)* |

</details>

<details>
<summary><b>Pemorsian (2 Doctype + 1 Child Table)</b></summary>

| Doctype | Naming Series | Keterangan |
|---|---|---|
| Pemorsian MBG | `POR-.YY.MM.-.####` | Proses pemorsian *(Submittable)* |
| Detail Pemorsian | — | Child: per kelompok sasaran |

</details>

<details>
<summary><b>Distribusi (5 Doctype + 1 Child Table)</b></summary>

| Doctype | Naming Series | Keterangan |
|---|---|---|
| Delivery Plan MBG | `DLV-.YY.MM.-.####` | Rencana kirim *(Submittable)* |
| Route Delivery | — | Child: titik tujuan |
| Proof of Delivery | `POD-.YY.MM.-.####` | Bukti terima *(Submittable)* |
| Delivery Issue | `DI-.YY.MM.-.####` | Masalah pengiriman |

</details>

<details>
<summary><b>Finance & Cost (1 Doctype)</b></summary>

| Doctype | Naming Series | Keterangan |
|---|---|---|
| Cost Per Portion MBG | `CPP-.YY.MM.-.####` | Kalkulasi HPP aktual |

</details>

---

## 🚀 Instalasi di ERPNext Self-Hosted

### Prasyarat

Pastikan ERPNext sudah berjalan dengan bench. Cek versi:

```bash
bench version
# Output harus menampilkan frappe v14/v15 dan erpnext v14/v15
```

---

### Metode 1 — Instalasi via GitHub (Direkomendasikan)

**Langkah 1: Masuk ke folder bench**
```bash
cd /home/frappe/frappe-bench
# atau sesuai lokasi bench Anda
```

**Langkah 2: Download app dari GitHub**
```bash
bench get-app https://github.com/USERNAME/sppg_management
# Atau jika repo private dengan SSH:
bench get-app git@github.com:USERNAME/sppg_management.git
```

**Langkah 3: Install ke site**
```bash
bench --site [nama-site-anda] install-app sppg_management
# Contoh:
bench --site mysite.localhost install-app sppg_management
```

**Langkah 4: Jalankan migrasi database**
```bash
bench --site [nama-site-anda] migrate
```

**Langkah 5: Clear cache dan restart**
```bash
bench --site [nama-site-anda] clear-cache
bench --site [nama-site-anda] clear-website-cache
bench restart
```

**Langkah 6: Verifikasi instalasi**
```bash
bench --site [nama-site-anda] list-apps
# Output harus menampilkan: sppg_management
```

---

### Metode 2 — Instalasi via ZIP (Tanpa GitHub)

**Langkah 1: Upload dan extract ZIP**
```bash
# Upload sppg_management.zip ke server
# Extract ke folder apps bench
cd /home/frappe/frappe-bench/apps
unzip sppg_management.zip
mv sppg_repo sppg_management
```

**Langkah 2: Install Python package**
```bash
cd /home/frappe/frappe-bench
./env/bin/pip install -e apps/sppg_management
```

**Langkah 3: Install ke site & migrate**
```bash
bench --site [nama-site-anda] install-app sppg_management
bench --site [nama-site-anda] migrate
bench restart
```

---

### Metode 3 — Development Mode (Docker)

```bash
# Jika menggunakan frappe_docker
git clone https://github.com/USERNAME/sppg_management apps/sppg_management
docker compose exec backend bench get-app /workspace/development/apps/sppg_management
docker compose exec backend bench --site dev.localhost install-app sppg_management
docker compose exec backend bench --site dev.localhost migrate
```

---

## ☁️ Instalasi di Frappe Cloud

### Prasyarat Frappe Cloud
- Akun aktif di [frappecloud.com](https://frappecloud.com)
- Repository GitHub **Public** (untuk akun Free/Trial)
- Repository GitHub **Private** didukung pada plan berbayar

---

### Step-by-Step Frappe Cloud

**Step 1: Upload repo ke GitHub**

```bash
# Di komputer lokal / server development
cd sppg_repo

git init
git add .
git commit -m "feat: SPPG Management System v1.0.0"
git branch -M main

# Buat repo baru di github.com lalu:
git remote add origin https://github.com/USERNAME/sppg_management.git
git push -u origin main
```

**Step 2: Login ke Frappe Cloud**

Buka [frappecloud.com](https://frappecloud.com) → Login

**Step 3: Tambahkan App ke Site**

```
Dashboard → Pilih Site Anda → Tab "Apps" → Klik "Add App"
```

**Step 4: Isi form Add App**

| Field | Nilai |
|---|---|
| Source | GitHub |
| Repository URL | `https://github.com/USERNAME/sppg_management` |
| Branch | `main` |
| App Name | `sppg_management` |

Klik **Add App** → Tunggu proses deploy (biasanya 2-5 menit)

**Step 5: Verifikasi**

Setelah deploy selesai, app akan muncul di daftar Apps site Anda.

Buka ERPNext → cari menu **SPPG Management** di sidebar.

---

### Frappe Cloud — Private Repository

Jika repo GitHub bersifat Private:

1. Di Frappe Cloud Dashboard → **Integrations** → **GitHub**
2. Authorize Frappe Cloud untuk akses repo Anda
3. Ulangi Step 3-5 di atas, repo private akan terdeteksi

---

## ⚙️ Konfigurasi Awal Setelah Install

Lakukan langkah berikut secara berurutan setelah app berhasil terinstall:

### 1. Import Workflow

```bash
# Jalankan di bench (self-hosted)
bench --site [site] import-doc apps/sppg_management/sppg_management/sppg_management/fixtures/workflow_kontrak_penyediaan_mbg.json
bench --site [site] import-doc apps/sppg_management/sppg_management/sppg_management/fixtures/workflow_master_menu_mbg.json
bench --site [site] import-doc apps/sppg_management/sppg_management/sppg_management/fixtures/workflow_menu_plan_mbg.json
bench --site [site] import-doc apps/sppg_management/sppg_management/sppg_management/fixtures/workflow_production_plan_mbg.json
bench --site [site] import-doc apps/sppg_management/sppg_management/sppg_management/fixtures/workflow_delivery_plan_mbg.json
bench --site [site] import-doc apps/sppg_management/sppg_management/sppg_management/fixtures/workflow_purchase_planning_mbg.json
```

Atau via UI: **ERPNext → Settings → Import Data** → Upload file JSON dari folder `fixtures/`

### 2. Buat Item Layanan MBG di ERPNext

```
Stock → Items → New
Item Code  : MBG-SERVICE
Item Name  : Layanan MBG
Item Group : Services
Is Stock Item : No (uncheck)
```

Item ini digunakan saat auto-generate Sales Order dari Kontrak.

### 3. Setup Master Data (Urutan Wajib)

```
1. SPPG Unit          → Buat unit dapur Anda
2. Area Distribusi    → Buat zona pengiriman
3. Konsumen MBG       → Daftarkan sekolah/lembaga
4. Sasaran Penerima   → Buat kelompok usia (PAUD, SD, SMP, SMA)
5. Angka Kecukupan Gizi → Isi standar AKG per sasaran & tipe layanan
6. Kategori Produk    → Buat kategori (Lauk, Sayur, Buah, dll)
7. Produk MBG         → Daftarkan bahan baku (link ke Item ERPNext)
8. Produk Hasil Masakan → Daftarkan masakan dengan nilai gizi
9. Standar Porsi MBG  → Isi berat porsi per masakan per sasaran
10. Master Menu MBG   → Buat menu dan aktifkan setelah review gizi
```

### 4. Assign Role ke User

```
ERPNext → Settings → User → Pilih user → Tab Roles
```

Assign role sesuai fungsi:

| User | Role yang Diberikan |
|---|---|
| Pemilik/Owner | SPPG Owner |
| Manager Operasional | SPPG Manager |
| Admin/Staff Admin | Admin SPPG |
| Nutrisionis | Ahli Gizi |
| Kepala Dapur | Kepala Dapur |
| Staff Masak | Staff Dapur |
| Staff Gudang | Staff Gudang |
| Tim Purchasing | Purchasing SPPG |
| Tim Finance | Finance SPPG |
| Driver | Driver Logistik |
| Tim QC | Quality Control SPPG |

### 5. Konfigurasi Warehouse

Pastikan Warehouse untuk setiap SPPG Unit sudah ada di ERPNext:
```
Stock → Warehouse → New
Masukkan warehouse name dan assign ke Company
```

Kemudian update field **Warehouse Utama** di setiap SPPG Unit.

### 6. Setup Cost Center (Opsional — untuk Cost Control)

```
Accounts → Chart of Accounts → Cost Center
Buat Cost Center per SPPG Unit
Update field Cost Center di SPPG Unit
```

---

## 👥 Role & Hak Akses

| Role | Akses Utama | Bisa Submit? |
|---|---|---|
| **SPPG Owner** | Read all, Approve Kontrak & Menu | Amend |
| **SPPG Manager** | Read/Write semua modul operasional | Submit Kontrak, Menu Plan |
| **Admin SPPG** | Create/Write transaksi operasional | Submit Menu Plan |
| **Ahli Gizi** | Master Menu, AKG, Gizi | Submit Master Menu |
| **Kepala Dapur** | Production Plan, Cooking Batch, QC | Submit Produksi |
| **Staff Dapur** | Cooking Batch, Pemorsian | Submit Batch & Pemorsian |
| **Staff Gudang** | Stock, Purchase Receipt, Expired Monitoring | — |
| **Purchasing SPPG** | Purchase Planning, PO, Supplier | Submit Purchase Planning |
| **Finance SPPG** | Cost Per Portion, Invoice, Budget | — |
| **Driver Logistik** | Delivery Plan (milik sendiri), POD | Submit POD |
| **Quality Control SPPG** | Quality Check, Waste | Submit QC |

---

## 🔌 Integrasi ERPNext Standard

| Custom Doctype | ERPNext Doctype | Jenis Integrasi |
|---|---|---|
| Konsumen MBG | Customer | Field link, auto-mapping |
| Produk MBG / Hasil Masakan | Item | Field link ke item_code |
| Kontrak Penyediaan MBG | Sales Order | Auto-generate saat submit |
| Purchase Planning MBG | Material Request | Auto-generate saat submit |
| Production Plan MBG | Stock Entry (Material Issue) | Auto-generate saat submit |
| SPPG Unit | Cost Center | Field link |
| SPPG Unit | Warehouse | Field link main_warehouse |
| Driver, Kepala Dapur | Employee | Field link |

---

## 🛠 Troubleshooting

### App tidak muncul di sidebar setelah install

```bash
bench --site [site] clear-cache
bench --site [site] clear-website-cache
bench restart
# Refresh browser dengan Ctrl+Shift+R
```

### Workflow tidak aktif

1. Buka **ERPNext → Settings → Workflow**
2. Cari workflow SPPG (Kontrak, Menu Plan, dll)
3. Pastikan **Is Active = ✅**
4. Jika tidak ada, import manual dari folder `fixtures/`

### Error `ModuleNotFoundError: sppg_management`

```bash
# Reinstall Python package
cd /home/frappe/frappe-bench
./env/bin/pip install -e apps/sppg_management
bench restart
```

### Error saat `bench migrate`

```bash
# Lihat log detail
bench --site [site] migrate --verbose 2>&1 | tail -50
# Pastikan MariaDB berjalan
sudo service mariadb status
```

### Workspace SPPG Management tidak muncul

```bash
# Reimport workspace
bench --site [site] import-doc \
  apps/sppg_management/sppg_management/sppg_management/workspace/sppg_management/sppg_management.json
bench --site [site] clear-cache
```

### Error `Item MBG-SERVICE not found` saat submit Kontrak

Buat Item dengan kode `MBG-SERVICE` di ERPNext → Stock → Items (lihat bagian Konfigurasi Awal)

### Stok tidak terhitung saat Menu Plan dikonfirmasi

Pastikan field **Warehouse** di Menu Plan MBG diisi sebelum konfirmasi.

---

## 🤝 Kontribusi

Kontribusi sangat disambut! Silakan:

1. Fork repository ini
2. Buat branch fitur: `git checkout -b feature/nama-fitur`
3. Commit perubahan: `git commit -m 'feat: tambah fitur X'`
4. Push ke branch: `git push origin feature/nama-fitur`
5. Buat Pull Request

**Konvensi commit:**
- `feat:` — fitur baru
- `fix:` — perbaikan bug
- `docs:` — perubahan dokumentasi
- `refactor:` — refactoring kode
- `test:` — penambahan test

---

## 📜 Lisensi

MIT License — lihat file [LICENSE](license.txt) untuk detail lengkap.

---

<div align="center">

**SPPG Management System v1.0.0**  
Dibangun dengan ❤️ di atas [Frappe Framework](https://frappeframework.com) & [ERPNext](https://erpnext.com)

*Mendukung Program Makan Bergizi Gratis Indonesia 🇮🇩*

</div>
