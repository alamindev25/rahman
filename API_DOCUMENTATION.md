# Alrahman87 Healthcare Platform - API Documentation

> **Base URL:** `http://127.0.0.1:8000/api/`  
> **Protocol:** HTTP / HTTPS  
> **Data Format:** JSON (`application/json`)  
> **Authentication:** Bearer Token (`Authorization: Bearer <access_token>`) & Secure HTTP-only Cookies

---

## 📑 সূচিপত্র (Table of Contents)
1. [গ্লোবাল কনফিগারেশন ও অথেনটিকেশন](#1-গ্লোবাল-কনফিগারেশন-ও-অথেনটিকেশন)
2. [অথেনটিকেশন ও ইউজার প্রোফাইল API](#2-অথেনটিকেশন-ও-ইউজার-প্রোফাইল-api)
3. [ক্লিনিক ও পার্টনার ম্যানেজমেন্ট API](#3-ক্লিনিক-ও-পার্টনার-ম্যানেজমেন্ট-api)
4. [অ্যাপয়েন্টমেন্ট ও শিডিউলিং API](#4-অ্যাপয়েন্টমেন্ট-ও-শিডিউলিং-api)
5. [সাবস্ক্রিপশন ও পেমেন্ট গেটওয়ে API](#5-সাবস্ক্রিপশন-ও-পেমেন্ট-গেটওয়ে-api)
6. [নোটিফিকেশন ও পুশ নোটিফিকেশন API](#6-নোটিফিকেশন-ও-পুশ-নোটিফিকেশন-api)
7. [ব্লগ, CMS ও রিসোর্স API](#7-ব্লগ-cms-ও-রিসোর্স-api)
8. [স্ট্যান্ডার্ড রেসপন্স ও এরর কোড](#8-স্ট্যান্ডার্ড-রেসপন্স-ও-এরর-কোড)

---

## 1. গ্লোবাল কনফিগারেশন ও অথেনটিকেশন

### Headers
প্রটেক্টেড বা অথোরাইজড এন্ডপয়েন্টগুলোতে নিচের হেডার পাঠানো বাধ্যতামূলক:
```http
Content-Type: application/json
Authorization: Bearer <your_jwt_access_token>
```

### স্ট্যান্ডার্ড রেসপন্স ফরম্যাট
```json
{
  "status": 200,
  "success": true,
  "message": "Operation completed successfully.",
  "data": { ... },
  "errors": null
}
```

---

## 2. অথেনটিকেশন ও ইউজার প্রোফাইল API

### ২.১ ইউজার রেজিস্ট্রেশন (Sign Up)
- **URL:** `/api/signup/`
- **Method:** `POST`
- **Auth:** None
- **Request Body:**
```json
{
  "email": "patient@example.com",
  "password": "StrongPassword123!",
  "confirm_password": "StrongPassword123!",
  "role": "patient" // "patient", "clinic_owner"
}
```
- **Response (201 Created):**
```json
{
  "status": 201,
  "success": true,
  "message": "User registered successfully. Please verify your OTP.",
  "data": { "email": "patient@example.com", "user_id": 1 }
}
```

### ২.২ লগইন (Sign In)
- **URL:** `/api/signin/`
- **Method:** `POST`
- **Auth:** None
- **Request Body:**
```json
{
  "email": "patient@example.com",
  "password": "StrongPassword123!",
  "remember_me": true
}
```
- **Response (200 OK):**
```json
{
  "status": 200,
  "success": true,
  "message": "Login successful.",
  "data": {
    "access_token": "eyJhbGciOi...",
    "refresh_token": "eyJhbGciOi...",
    "user": {
      "id": 1,
      "email": "patient@example.com",
      "role": "patient"
    }
  }
}
```

### ২.৩ গুগল সোশ্যাল লগইন (Google Auth)
- **URL:** `/api/google-auth/`
- **Method:** `POST`
- **Auth:** None
- **Request Body:**
```json
{
  "id_token": "<google_oauth_id_token>"
}
```

### ২.৪ OTP প্রেরণ (Send OTP)
- **URL:** `/api/send-otp/`
- **Method:** `POST`
- **Request Body:**
```json
{
  "email": "patient@example.com"
}
```

### ২.৫ OTP যাচাই (Verify OTP)
- **URL:** `/api/verify-otp/`
- **Method:** `POST`
- **Request Body:**
```json
{
  "email": "patient@example.com",
  "otp": "123456"
}
```

### ২.৬ পুনরায় OTP পাঠানো (Resend OTP)
- **URL:** `/api/resend-otp/`
- **Method:** `POST`
- **Request Body:**
```json
{
  "email": "patient@example.com"
}
```

### ২.৭ পাসওয়ার্ড রিসেট (Reset Password)
- **URL:** `/api/reset-password/`
- **Method:** `POST`
- **Request Body:**
```json
{
  "email": "patient@example.com",
  "otp": "123456",
  "password": "NewStrongPassword123!",
  "confirm_password": "NewStrongPassword123!"
}
```

### ২.৮ পাসওয়ার্ড পরিবর্তন (Change Password)
- **URL:** `/api/change-password/`
- **Method:** `POST`
- **Auth:** Bearer Token
- **Request Body:**
```json
{
  "old_password": "OldPassword123!",
  "new_password": "NewStrongPassword123!",
  "confirm_password": "NewStrongPassword123!"
}
```

### ২.৯ প্রোফাইল দেখা (Get Profile)
- **URL:** `/api/profile-get/`
- **Method:** `GET`
- **Auth:** Bearer Token

### ২.১০ প্রোফাইল আপডেট (Update Profile)
- **URL:** `/api/profile-update/`
- **Method:** `PUT`
- **Auth:** Bearer Token
- **Request Body:**
```json
{
  "first_name": "Alamin",
  "last_name": "Hossain",
  "phone": "+8801700000000",
  "address": "Dhaka, Bangladesh"
}
```

### ২.১১ প্রোফাইল ছবি আপলোড (Avatar Update)
- **URL:** `/api/avatar-update/`
- **Method:** `POST`
- **Auth:** Bearer Token
- **Content-Type:** `multipart/form-data`
- **Body:** `avatar` (Image File)

### ২.১২ টোকেন রিফ্রেশ ও ভেরিফাই
- `POST /api/token/refresh/` - Refresh Token পাঠিয়ে নতুন Access Token পাওয়া
- `POST /api/token/verify/` - বর্তমান টোকেনের সক্রিয়তা যাচাই করা

### ২.১৩ লগআউট (Sign Out)
- **URL:** `/api/signout/`
- **Method:** `POST`
- **Auth:** Bearer Token
- **Request Body:**
```json
{
  "refresh_token": "eyJhbGciOi..."
}
```

---

## 3. ক্লিনিক ও পার্টনার ম্যানেজমেন্ট API

### ৩.১ ক্লিনিক ওনার সাইনআপ (Clinic Owner Register)
- **URL:** `/api/auth/clinic-owner/signup/` বা `/api/clinics/owner-register/`
- **Method:** `POST`
- **Request Body:**
```json
{
  "email": "owner@clinic.com",
  "password": "Password123!",
  "confirm_password": "Password123!",
  "role": "clinic_owner"
}
```

### ৩.২ ক্লিনিক রেজিস্ট্রেশন / অনবোর্ডিং (Clinic Register)
- **URL:** `/api/clinics/register/`
- **Method:** `GET`, `POST`, `PUT`, `PATCH`
- **Auth:** Bearer Token
- **Content-Type:** `multipart/form-data`
- **Fields:** `clinic_name`, `email`, `phone`, `country`, `city`, `address`, `postal_code`, `license_number`, `treatments`, `facilities`, `images`, ইত্যাদি।

### ৩.৩ ক্লিনিক অ্যাপ্লিকেশন স্ট্যাটাস চেক
- **URL:** `/api/clinics/submission-status/`
- **Method:** `GET`
- **Auth:** Bearer Token
- **Response:** `pending`, `approved`, বা `rejected`

### ৩.৪ ক্লিনিক তালিকা ও সার্চ (Public Clinic Search)
- **URL:** `/api/clinics/`
- **Method:** `GET`
- **Query Params:** `?search=dhaka&treatment=dialysis&page=1`
- **URL:** `/api/clinic/search/`
- **Method:** `GET`
- **Query Params:** `?location=Dhaka&date=2026-11-01`

### ৩.৫ নির্দিষ্ট ক্লিনিকের বিস্তারিত
- **URL:** `/api/clinics/<int:pk>/`
- **Method:** `GET`

### ৩.৬ ক্লিনিক রিভিউ ও রেটিং
- **URL:** `/api/clinics/rating/`
- **Method:** `POST`
- **Auth:** Bearer Token
- **Request Body:**
```json
{
  "clinic": 1,
  "rating": 5,
  "comment": "Excellent medical care and friendly staff."
}
```

### ৩.৭ ট্রিটমেন্ট তালিকা
- **URL:** `/api/clinics/treatments/` অথবা `/api/treatments/`
- **Method:** `GET`

### ৩.৮ পার্টনার ক্লিনিক ড্যাশবোর্ড ও অ্যাপয়েন্টমেন্ট
- `GET /api/clinics/dashboard/` - ক্লিনিক ওনারের অ্যাডমিন ড্যাশবোর্ড ডাটা
- `GET /api/clinics/dashboard/appointments/` - ক্লিনিকের সব অ্যাপয়েন্টমেন্ট
- `PATCH /api/clinics/dashboard/appointments/<int:pk>/` - অ্যাপয়েন্টমেন্ট স্ট্যাটাস আপডেট (`confirmed`, `completed`, `cancelled`)

### ৩.৯ অ্যাডমিন অনুমোদন / রিজেকশন এন্ডপয়েন্ট
- `GET, PATCH /api/clinic/<int:pk>/approve/` - অ্যাডমিন দ্বারা অনুমোদন
- `PATCH /api/clinic/<int:pk>/reject/` - অ্যাডমিন দ্বারা বাতিল
- `GET /api/clinic/email-approve/<uuid:token>/` - ইমেইল লিংকের মাধ্যমে অনুমোদন
- `POST /api/clinic/email-reject/<uuid:token>/` - ইমেইল লিংকের মাধ্যমে বাতিল

---

## 4. অ্যাপয়েন্টমেন্ট ও শিডিউলিং API

### ৪.১ ফাঁকা স্লট অনুসন্ধান (Check Available Slots)
- **URL:** `/api/available-slots/`
- **Method:** `GET`
- **Query Params:** `?clinic_id=1&date=2026-11-05`
- **Response:**
```json
{
  "status": 200,
  "success": true,
  "data": {
    "date": "2026-11-05",
    "slots": [
      { "time": "09:00 AM", "available": true, "capacity_left": 3 },
      { "time": "10:00 AM", "available": false, "capacity_left": 0 }
    ]
  }
}
```

### ৪.২ বুক হওয়া স্লট দেখা
- **URL:** `/api/appointments/booked-slots/`
- **Method:** `GET`
- **Query Params:** `?clinic_id=1&date=2026-11-05`

### ৪.৩ অ্যাপয়েন্টমেন্ট বুকিং (Create Appointment)
- **URL:** `/api/appointments/`
- **Method:** `POST`
- **Auth:** Bearer Token
- **Content-Type:** `multipart/form-data` বা `application/json`
- **Request Body:**
```json
{
  "clinic": 1,
  "appointment_date": "2026-11-05",
  "appointment_time": "09:00:00",
  "treatment_type": "Hemodialysis",
  "patient_name": "Rahim Khan",
  "patient_phone": "+8801800000000",
  "health_status": "Stable",
  "medical_report": "<file>"
}
```

### ৪.৪ অ্যাপয়েন্টমেন্ট দেখা ও বাতিল/পরিবর্তন
- `GET /api/appointments/<int:pk>/` - অ্যাপয়েন্টমেন্টের বিস্তারিত
- `PUT, PATCH /api/appointments/<int:pk>/` - তথ্য বা সময় পরিবর্তন
- `DELETE /api/appointments/<int:pk>/` - অ্যাপয়েন্টমেন্ট বাতিল করা

### ৪.৫ ইউজার বুকিং হিস্ট্রি
- **URL:** `/api/booking-history/`
- **Method:** `GET`
- **Auth:** Bearer Token

### ৪.৬ ক্লিনিক শিফট, ক্যাপাসিটি ও ছুটির দিন সেটিংস (ওনার প্যানেল)
- `GET, POST, PUT, PATCH /api/availability-shifts/` - ক্লিনিকের সাপ্তাহিক শিফট সময় নির্ধারণ
- `GET, POST, PUT, DELETE /api/appointmentper-slot/` - প্রতি স্লটে সর্বোচ্চ রোগী সংখ্যা
- `GET, POST, PUT, DELETE /api/slot-capacity/<int:pk>/` - নির্দিষ্ট স্লট ক্যাপাসিটি মডিফাই
- `GET, POST, DELETE /api/blackout-dates/` - ক্লিনিকের ছুটির দিন / অফ-ডে যুক্ত করা
- `GET, POST, DELETE /api/blackout-dates/<int:pk>/` - নির্দিষ্ট ছুটির দিন ডিলিট করা

---

## 5. সাবস্ক্রিপশন ও পেমেন্ট গেটওয়ে API

### ৫.১ সাবস্ক্রিপশন প্যাকেজ তালিকা
- **URL:** `/api/subscription/packages/`
- **Method:** `GET`

### ৫.২ বর্তমান সক্রিয় সাবস্ক্রিপশন প্ল্যান
- **URL:** `/api/current/subscription/`
- **Method:** `GET`
- **Auth:** Bearer Token

### ৫.৩ সাবস্ক্রিপশনের জন্য Stripe চেকআউট
- **URL:** `/api/stripe/checkout/`
- **Method:** `POST`
- **Auth:** Bearer Token
- **Request Body:**
```json
{
  "package_id": 2,
  "success_url": "https://frontend.com/subscription/success",
  "cancel_url": "https://frontend.com/subscription/cancel"
}
```
- **Response:**
```json
{
  "status": 200,
  "success": true,
  "data": { "checkout_url": "https://checkout.stripe.com/c/pay/cs_..." }
}
```

### ৫.৪ সাবস্ক্রিপশন বাতিল
- **URL:** `/api/cancel/subscription/`
- **Method:** `POST`
- **Auth:** Bearer Token

### ৫.৫ অ্যাপয়েন্টমেন্ট বুকিং ফি পেমেন্ট (Stripe Checkout)
- **URL:** `/api/checkout/appointment/`
- **Method:** `POST`
- **Auth:** Bearer Token
- **Request Body:**
```json
{
  "appointment_id": 10,
  "success_url": "https://frontend.com/appointment/success",
  "cancel_url": "https://frontend.com/appointment/cancel"
}
```

### ৫.৬ পেমেন্ট হিস্ট্রি
- **URL:** `/api/history/`
- **Method:** `GET`
- **Auth:** Bearer Token

### ৫.৭ Stripe Webhook
- **URL:** `/api/stripe/webhook/` (অথবা `/api/webhook/stripe/`)
- **Method:** `POST`
- Stripe সার্ভার থেকে পেমেন্ট কনফার্মেশনের জন্য স্বয়ংক্রিয় ব্যাকএন্ড রুট।

---

## 6. নোটিফিকেশন ও পুশ নোটিফিকেশন API

### ৬.১ নোটিফিকেশন তালিকা
- **URL:** `/api/notification-list/`
- **Method:** `GET`
- **Auth:** Bearer Token

### ৬.২ বিগত ৩০ দিনের নোটিফিকেশন
- **URL:** `/api/last-30-days/`
- **Method:** `GET`
- **Auth:** Bearer Token

### ৬.৩ নোটিফিকেশন পঠিত (Mark Read)
- `POST /api/mark-read/<int:notification_id>/` - নির্দিষ্ট নোটিফিকেশন Read করা
- `POST /api/mark-all-read/` - সব নোটিফিকেশন একসাথে Read করা

### ৬.৪ নোটিফিকেশন ডিলিট
- `DELETE /api/delete/<int:notification_id>/` - নির্দিষ্ট নোটিফিকেশন মুছে ফেলা
- `DELETE /api/delete-all/` - সমস্ত নোটিফিকেশন মুছে ফেলা

### ৬.৫ FCM পুশ ডিভাইস টোকেন রেজিস্টার
- **URL:** `/api/device-token/`
- **Method:** `POST`
- **Auth:** Bearer Token
- **Request Body:**
```json
{
  "fcm_token": "fcm_device_token_string_here"
}
```

### ৬.৬ পুশ নোটিফিকেশন টেস্ট
- **URL:** `/api/test-push/`
- **Method:** `POST`
- **Auth:** Bearer Token

---

## 7. ব্লগ, CMS ও রিসোর্স API

### ৭.১ ব্লগ পোস্ট
- `GET /api/blogs/` - ব্লগের তালিকা (ফিল্টারিং ও পেজিনেশন সহ)
- `GET /api/blogs/<int:pk>/` - নির্দিষ্ট ব্লগের পূর্ণাঙ্গ কনটেন্ট

### ৭.২ CMS পেজ
- `GET /api/cms/` - CMS ডাটা (Privacy Policy, Terms of Service ইত্যাদি)
- `POST /api/cms/` - CMS ডাটা আপডেট (অ্যাডমিন)

### ৭.৩ FAQ (সচরাচর জিজ্ঞাসিত প্রশ্ন)
- `GET /api/faqs/` - FAQ তালিকা

### ৭.৪ রিসোর্স ও গাইড
- `GET /api/resources/` - রিসোর্স আইটেমের তালিকা
- `GET /api/resources/<int:pk>/` - নির্দিষ্ট রিসোর্সের বিস্তারিত

### ৭.৫ সিস্টেম ও কন্টাক্ট ইনফো
- `GET /api/about-us/` - আমাদের সম্পর্কে (About Us) তথ্য
- `GET /api/about-system/` - সিস্টেম ও প্ল্যাটফর্মের সাধারণ তথ্য
- `GET /api/contact-info/` - যোগাযোগের ফোন নম্বর, ইমেইল, ঠিকানা
- `POST /api/contact-submit/` - সাধারণ ইউজার বা রোগীর মেসেজ সাবমিট করা
  ```json
  {
    "name": "Kamal Hossain",
    "email": "kamal@gmail.com",
    "subject": "Treatment Inquiry",
    "message": "Do you have dialysis slots available next week?"
  }
  ```

### ৭.৬ ভাষা সেটিংস (Localization)
- `GET /api/languages/` - সিস্টেমে সমর্থিত ভাষার তালিকা (English, Arabic, ইত্যাদি)
- `GET /api/languages/default/` - ডিফল্ট সক্রিয় ভাষা

---

## 8. স্ট্যান্ডার্ড রেসপন্স ও এরর কোড

| HTTP Status | অর্থ | কারণ |
| :--- | :--- | :--- |
| `200 OK` | সফল | রিকোয়েস্ট সঠিকভাবে সম্পন্ন হয়েছে |
| `201 Created` | তৈরি হয়েছে | নতুন ইউজার, ক্লিনিক বা অ্যাপয়েন্টমেন্ট সফলভাবে তৈরি হয়েছে |
| `400 Bad Request` | ভুল তথ্য | প্রয়োজনীয় ফিল্ড বাদ পড়েছে বা ভ্যালিডেশন ফেইল করেছে |
| `401 Unauthorized` | লগইন প্রয়োজন | টোকেন পাঠানো হয়নি বা টোকেন মেয়াদোত্তীর্ণ |
| `403 Forbidden` | অ্যাক্সেস নেই | ব্যবহারকারীর এই একশনে অনুমতি নেই (যেমন: নন-ওনারের একশন) |
| `404 Not Found` | পাওয়া যায়নি | আইডি বা রিসোর্স সিস্টেমে অনুপস্থিত |
| `500 Server Error` | সার্ভার সমস্যা | ইন্টারনাল সার্ভার সমস্যা |
