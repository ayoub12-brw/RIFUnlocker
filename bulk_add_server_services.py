import sqlite3

# إعداد الاتصال بقاعدة البيانات
conn = sqlite3.connect('site.db')
c = conn.cursor()

# قائمة الخدمات (الاسم، مدة التسليم، السعر بالدولار)
services = [
    ("ICLOUD REMOVAL COURSE WITH INVOICES ✅ كورس فك الايكلود مع الفواتير", "Minutes", 600),
    ("OXYGEN-UFED-MD NEXT-MAGNET AXIOM - RREMOVE LOCK SCREEN [برنامج ازالة الرمز بدون حذف البيانات]", "Minutes", 20),
    ("ACTIVE UFED V7.70", "Minutes", 20),
    ("ACTIVE MD-NEXT V2.0.3", "Minutes", 20),
    ("ACTIVE MAGNET AXIOM V7.80", "Minutes", 20),
    ("Oxygen Forensic Detective V17.1.0.131", "Minutes", 20),
    ("SK Xiaomi_Auth", "Minutes", 3.84),
    ("Q-UNLOCKER Tool Add Credits to (Exist Username)", "Minutes", 0.763),
    ("Q-UNLOCKER Tool Add Credits to (New Account)", "Minutes", 0.763),
    ("XFP XIAOMI FLASHER PRO Tool Credit Any Qty (AUTH, FRP, FASTBOOT TO EDL) [Existing Account]", "Minutes", 0.745),
    ("BFT - Brutal Forensic tool (1 Account - 20 Credits)", "Minutes", 71.99),
    ("XTP – Xiaomi Tool Pro Credits Refill Package for Existing Users", "Minutes", 0.72),
    ("PhoeProgramFix Tool Activation [1 PC - 1 YEAR]", "Minutes", 34.99),
    ("M-PRO TOOL FRP| FDL | UBL | FLASH Any Quantity [Old/Existing Users] Credits", "Minutes", 0.964),
    ("YCS intelligent Drawing Schematic Bitmap [1 Year - 1 Pc]", "Minutes", 48.99),
    ("NEXTG Auth Tool Credit Any Qty (AUTH, FRP, FASTBOOT TO EDL) [Existing Account]", "Minutes", 0.305),
    ("GsmAuth.com QUALCOMM/MEDIATEK Flash & Frp | Credits Refill | Existing User Only", "Minutes", 0),
    ("Lanrui Gzlanrui Hardware Tool (1 Year - 3 Devices)", "Minutes", 48.49),
    ("UnlockTool 12 Months License", "1-6 Hours", 40.85),
    ("UnlockTool 3 Months License", "1-6 Hours", 16.55),
    ("UnlockTool 6 Months License", "1-6 Hours", 24.45),
    ("EFT Dongle 1 Year (Activation With Dongle )", "Minutes", 21.3),
    ("EFT Dongle Two Year Plan", "1-60 Minutes", 28.35),
    ("EFT Dongle - 12 Months Activation Renew ( WITH DONGLE )", "1-15 Minutes", 21.35),
    ("EFT Pro Activation Without Dongle [1 Year] New User", "1-15 Minutes", 52.29),
    ("EFT Pro Activation Without Dongle [1 Year] Extend Old User", "1-15 Minutes", 34.19),
    ("EFT Dongle Pro (No need Dongle) [1 Month] New User/Old User", "Minutes", 9.6),
    ("EFT Pro Activation Without Dongle [3 Months] New User/Old User", "1-15 Minutes", 21.7),
    ("EFT Pro Activation Without Dongle [6 Months] New User/Old User", "1-15 Minutes", 37),
    ("Chimera Tool Basic Licence 1 Year [ 100 Device ]", "1-60 Minutes", 97.5),
    ("Chimera Tool Professional Licence 1 year [ 1500 Device ]", "1-30 Minutes", 145),
    ("Chimera Tool Premium Licence 1 year [ 5000 Device ]", "1-30 Minutes", 185),
    ("Chimera Tool Credits", "1-30 Minutes", 0.099),
    ("DFT PRO TOOL ACTIVATION [New Users] 1 Year", "1-15 Minutes", 71.95),
    ("DFT PRO TOOL ACTIVATION [Old Users] 1 Year", "1-15 Minutes", 71.95),
    ("DFT PRO TOOL ACTIVATION [New Users] 2 Year", "Minutes", 142.9),
    ("DFT PRO TOOL ACTIVATION [Old Users] 2 Year", "Minutes", 142.9),
    ("DT PRO TOOL ACTIVATION", "1-15 Minutes", 18),
    ("DT PRO Credit For Existing user (Only Activated)", "Minutes", 1.17),
    ("AMT Android Multi Tool - 12 Months", "Minutes", 28.7),
    ("AMT Android Multi Tool (VIVO - XIAOMI - TECNO - INFINIX - ITEL - REALME - OPPO - KARBONN) [FRP - DEMO - FLASH - FDL - FACTORY RESET]", "1-5 Minutes", 0.92),
    ("AMT Android Multi Tool - 3 Months", "Minutes", 11.15),
    ("AMT Android Multi Tool - 6 Months", "Minutes", 18.1),
    ("AWT - AndroidWinTool Credits Qnt", "Minutes", 0.894),
    ("AWT - AndroidWinTool [1 PC | 1 Month]", "Minutes", 15.85),
    ("AWT - AndroidWinTool [1 PC | 1 YEAR]", "Minutes", 34.74),
    ("AWT - AndroidWinTool [1 PC | 3 Months]", "Minutes", 24.35),
    ("BFT - Brutal Forensic tool (1 Account - 20 Credits)", "Minutes", 71.99),
    ("XTP – Xiaomi Tool Pro Credits Refill Package for Existing Users", "Minutes", 0.72),
    ("PhoeProgramFix Tool Activation [1 PC - 1 YEAR]", "Minutes", 34.99),
    ("M-PRO TOOL FRP| FDL | UBL | FLASH Any Quantity [Old/Existing Users] Credits", "Minutes", 0.964),
    ("YCS intelligent Drawing Schematic Bitmap [1 Year - 1 Pc]", "Minutes", 48.99),
    ("NEXTG Auth Tool Credit Any Qty (AUTH, FRP, FASTBOOT TO EDL) [Existing Account]", "Minutes", 0.305),
    ("GsmAuth.com QUALCOMM/MEDIATEK Flash & Frp | Credits Refill | Existing User Only", "Minutes", 0),
    ("Lanrui Gzlanrui Hardware Tool (1 Year - 3 Devices)", "Minutes", 48.49),
    # ... أضف باقي الخدمات هنا بنفس النمط ...
]

for name, delivery_time, price in services:
    c.execute("""
        INSERT INTO services (name, delivery_time, price, category)
        VALUES (?, ?, ?, ?)
    """, (name, delivery_time, price, 'Server Service'))

conn.commit()
conn.close()
print("تمت إضافة الخدمات بنجاح!")
