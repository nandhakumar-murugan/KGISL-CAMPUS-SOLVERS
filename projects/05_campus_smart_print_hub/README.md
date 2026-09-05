# 🖨️ Subproject #5: KiTE Campus Smart Print Queue & Token Hub

> **A student-centric digital pre-print queue and token generator for central campus print facilities across KiTE, KGCAS, and IIM.**

---

## 📌 The Campus Problem
During lunch hours and examination submission deadlines, hundreds of students converge at the central campus printing shops. Long queues, delays, manual USB-drive handling, and payment friction lead to lost study time and missed deadlines.

## 💡 The Solution
This web portal allows students to upload documents securely from their phones or laptops during classes, customize print preferences (A4/A3, B&W/Color, single/double-sided, page range), and receive an instant **6-digit Print Claim ID and QR Code**.

The print operator prepares the batch in advance. Students simply present their QR code at the express pickup counter and collect their documents in seconds!

---

## 👥 Contributors & Roles
* **Bala** ([@Bala050814](https://github.com/Bala050814), ECE/VLSI) — *Problem Proposal, Campus Operational Logistics, Print Options & Pricing Architecture*
* **Prabakar A** ([@prabakar09](https://github.com/prabakar09), AI&DS) — *Streamlit UI, Session Queue State, Co-Author & Mentor*

---

## 🚀 Quickstart

```bash
# 1. Navigate to the project directory
cd projects/05_campus_smart_print_hub

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the web application
streamlit run app.py
```

---

## 🛠️ Roadmap & Future Enhancements
- [x] Streamlit file upload and document parameter configuration
- [x] Live 6-digit claim token and scannable QR code generator
- [ ] Push notification / status indicator (e.g., "Printing", "Ready for Pickup")
- [ ] Campus UPI payment integration (Google Pay / PhonePe)
- [ ] Operator Dashboard view for bulk printing
