# Campus Exchange

**Campus Exchange** is a web-based marketplace designed to connect Bob Jones University students, enabling them to buy, sell, and exchange items safely and conveniently within their campus community. Built with modern web technologies, this project demonstrates full-cycle product development—from requirements gathering and user experience design to implementation, deployment, and maintenance.

## 🎯 Project Overview

- **Problem:** Students often struggle to find a trusted and centralized platform for campus-specific transactions, leading to friction and safety concerns when using general classifieds sites.
- **Solution:** Campus Exchange offers an exclusive, authenticated environment where students can create listings, chat directly with peers, and handle transactions in person.

## 🔑 Key Features

- **User Authentication & Profiles:** Secure sign-up, email verification, and personalized dashboards.
- **Listing Management:** Create, edit, and remove item listings with up to six images each, featuring drag-and-drop uploads and instant previews.
- **Image Handling:** Cloud-based media storage and delivery (Cloudinary) to ensure fast, reliable image loading.
- **Search & Filters:** Browse items by category or keyword search.
- **In-App Messaging:** Real-time chat between buyers and sellers to negotiate and coordinate exchanges.
- **Notifications:** Email updates powered by SendGrid for new messages, offers, and account alerts.

## 👤 My Role & Contributions

- **Lead Developer:** Architected the Django backend, defined database models, and implemented RESTful APIs.
- **Frontend Integration:** Designed and developed the user interface using HTML5, CSS3, and JavaScript, integrating Dropzone.js for intuitive image uploads.
- **DevOps & Deployment:** Automated CI/CD pipelines and deployed the application to Render, ensuring high availability and free custom-domain support.
- **Third-Party Integrations:** Configured Cloudinary for media storage, SendGrid for email delivery, and Stripe for payments, balancing user experience with security best practices.

## 🛠️ Technology Stack

| Layer             | Technologies                                 |
| ----------------- | -------------------------------------------- |
| **Backend**       | Python 3.10, Django 5.1                      |
| **Frontend**      | HTML5, CSS3, JavaScript, Dropzone.js         |
| **Database**      | PostgreSQL (Render-hosted)                   |
| **Media Storage** | Cloudinary                                   |
| **Email Service** | SendGrid                                     |
| **Payments**      | Stripe                                       |
| **Deployment**    | Render (Web Service, Postgres), GitHub CI/CD |
| **Dev Tools**     | Git, GitHub, python-decouple                 |

## 🌟 Impact & Results

- **Performance:**  Fast page loads (<1s) and 99.9% uptime on Render’s free tier.
- **Scalability:** Easily accommodates images and listings without local storage constraints, using Cloudinary’s CDN.


---

*For questions or collaboration inquiries, please reach out to **Cole (col3mill3r7@gmail.com)** or view the live site at **https://campus-exchange-rhcm.onrender.com**.*
