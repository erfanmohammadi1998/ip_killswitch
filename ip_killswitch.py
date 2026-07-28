"""
IP Kill-Switch
--------------
هر چند ثانیه یک‌بار IP عمومی سیستم را چک می‌کند. اگر این IP با
TARGET_IP فرق داشت (مثلاً وی‌پی‌ان قطع شد)، همه‌ی پراسس‌های
مرورگر را می‌بندد تا از لو رفتن IP واقعی جلوگیری شود.

نصب پیش‌نیازها:
    pip install requests psutil

اجرا:
    python ip_killswitch.py
"""

import time
import sys
import requests
import psutil

# ---------------- تنظیمات ----------------
TARGET_IP = "82.115.17.77"      # IP‌ای که انتظار داری همیشه همینو داشته باشی
CHECK_INTERVAL = 0.5            # فاصله زمانی بین چک‌ها (ثانیه)
IP_CHECK_URL = "https://ifconfig.me/ip"
REQUEST_TIMEOUT = 5             # ثانیه
FAIL_THRESHOLD = 2              # بعد از این‌همه خطای پشت‌سرهم در گرفتن IP، مرورگر بسته می‌شود

# نام پراسس‌هایی که باید بسته بشن (حروف بزرگ/کوچک مهم نیست، خودکار نرمال می‌شه)
BROWSER_PROCESS_NAMES = [
    "chrome.exe",
    "msedge.exe",
    "firefox.exe",
    "brave.exe",
    "opera.exe",
    "iexplore.exe",
    "vivaldi.exe",
    "Code.exe",      # VS Code
]
BROWSER_PROCESS_NAMES = [n.lower() for n in BROWSER_PROCESS_NAMES]
# -------------------------------------------


def get_public_ip() -> str | None:
    """IP عمومی فعلی سیستم را برمی‌گرداند، یا None اگر نشد بگیرد."""
    try:
        resp = requests.get(IP_CHECK_URL, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        return resp.text.strip()
    except requests.RequestException as e:
        print(f"[!] خطا در گرفتن IP: {e}")
        return None


def close_browsers() -> None:
    """همه‌ی پراسس‌های مرورگر شناخته‌شده را می‌بندد."""
    closed_any = False
    for proc in psutil.process_iter(["pid", "name"]):
        try:
            name = (proc.info["name"] or "").lower()
            if name in BROWSER_PROCESS_NAMES:
                proc.kill()
                closed_any = True
                print(f"[x] بسته شد: {name} (PID {proc.info['pid']})")
        except psutil.NoSuchProcess:
            continue
        except psutil.AccessDenied:
            print(f"[!] دسترسی کافی برای بستن {proc.info.get('name')} نیست -> با Run as Administrator اجرا کن")
            continue
    if not closed_any:
        print("[i] هیچ پراسس مرورگر بازی پیدا نشد.")


def main() -> None:
    print(f"[i] IP هدف: {TARGET_IP}")
    print(f"[i] بازه چک: هر {CHECK_INTERVAL} ثانیه")
    print("[i] برای توقف: Ctrl+C\n")

    consecutive_failures = 0

    while True:
        current_ip = get_public_ip()

        if current_ip is None:
            consecutive_failures += 1
            print(f"[!] عدم دریافت IP ({consecutive_failures}/{FAIL_THRESHOLD})")
            if consecutive_failures >= FAIL_THRESHOLD:
                print("[!] چند بار پشت‌سرهم نتونستیم IP رو چک کنیم -> فرض بر قطع اتصال امن")
                close_browsers()
                consecutive_failures = 0
            time.sleep(CHECK_INTERVAL)
            continue

        consecutive_failures = 0

        if current_ip != TARGET_IP:
            print(f"[!] تغییر IP شناسایی شد: {current_ip} (باید {TARGET_IP} باشه)")
            close_browsers()
        else:
            print(f"[✓] IP سالمه: {current_ip}")

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[i] متوقف شد.")
        sys.exit(0)
