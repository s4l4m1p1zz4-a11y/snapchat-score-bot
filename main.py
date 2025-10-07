import os
import time
import random
from typing import Optional, List

from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

load_dotenv()

SNAP_USERNAME = os.getenv("SNAP_USERNAME", "")
SNAP_PASSWORD = os.getenv("SNAP_PASSWORD", "")
DEVICE_ID     = os.getenv("DEVICE_ID", "emulator-5554")
APPIUM_SERVER = os.getenv("APPIUM_SERVER", "http://127.0.0.1:4723")

PACKAGE = "com.snapchat.android"
LAUNCH_ACTIVITY = "com.snap.mushroom.MainActivity"

# ---------- Helpers ----------

def human_delay(a: float = 0.6, b: float = 1.8):
    time.sleep(random.uniform(a, b))

def jitter(n: int, p: float = 0.07) -> int:
    """Add small randomness to coordinates/steps."""
    return int(n * (1 + random.uniform(-p, p)))

def connect_driver() -> webdriver.Remote:
    caps = {
        "platformName": "Android",
        "automationName": "UiAutomator2",
        "deviceName": DEVICE_ID,
        "udid": DEVICE_ID,
        "appPackage": PACKAGE,
        "appActivity": LAUNCH_ACTIVITY,
        "noReset": True,        # keep sessions when possible
        "newCommandTimeout": 240,
        "autoGrantPermissions": True,
    }
    driver = webdriver.Remote(APPIUM_SERVER, caps)
    driver.implicitly_wait(2)
    return driver

def wait_for(driver, by, value, timeout=15):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )

def try_find(driver, by, value, timeout=5):
    try:
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
    except Exception:
        return None

def swipe_up(driver, dur=450):
    size = driver.get_window_size()
    x = size["width"] // 2
    start_y = int(size["height"] * 0.78)
    end_y   = int(size["height"] * 0.22)
    driver.swipe(jitter(x), jitter(start_y), jitter(x), jitter(end_y), dur)

def tap_xy(driver, x_ratio: float, y_ratio: float):
    size = driver.get_window_size()
    x = int(size["width"] * x_ratio)
    y = int(size["height"] * y_ratio)
    driver.tap([(jitter(x), jitter(y))], 60)

# ---------- Core flows (update selectors via Appium Inspector) ----------

def login(driver, username: str, password: str) -> bool:
    """
    Attempts login if Snapchat shows the login screen.
    Return True if logged in/already logged in.
    """
    # Heuristic: detect camera screen (already logged in)
    camera = try_find(driver, AppiumBy.ACCESSIBILITY_ID, "Take a Snap", timeout=5)
    if camera:
        return True

    # Common login screen buttons (may vary by version/locale)
    login_btn = try_find(driver, AppiumBy.ANDROID_UIAUTOMATOR,
                         'new UiSelector().textContains("Log In")')
    if not login_btn:
        # Tap "I already have an account" or similar
        have_acc = try_find(driver, AppiumBy.ANDROID_UIAUTOMATOR,
                            'new UiSelector().textContains("Already")')
        if have_acc:
            have_acc.click()
            human_delay()
        login_btn = try_find(driver, AppiumBy.ANDROID_UIAUTOMATOR,
                             'new UiSelector().textContains("Log In")')

    if login_btn:
        login_btn.click()
        human_delay(0.8, 1.6)

    # Username & Password fields (IDs can change; adjust as needed)
    user_field = try_find(driver, AppiumBy.CLASS_NAME, "android.widget.EditText", 8)
    if not user_field:
        # Sometimes two fields appear; find by index
        fields = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.EditText")
        if len(fields) >= 1:
            user_field = fields[0]

    if user_field:
        user_field.click()
        user_field.clear()
        user_field.send_keys(username)
        human_delay()

    # Next or Continue
    next_btn = try_find(driver, AppiumBy.ANDROID_UIAUTOMATOR,
                        'new UiSelector().textContains("Next")', 6)
    if not next_btn:
        next_btn = try_find(driver, AppiumBy.ANDROID_UIAUTOMATOR,
                            'new UiSelector().textContains("Continue")', 6)
    if next_btn:
        next_btn.click()
        human_delay(1.0, 2.0)

    # Password
    pwd_field = try_find(driver, AppiumBy.CLASS_NAME, "android.widget.EditText", 8)
    if not pwd_field:
        fields = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.EditText")
        if len(fields) >= 1:
            pwd_field = fields[-1]

    if pwd_field:
        pwd_field.click()
        pwd_field.clear()
        pwd_field.send_keys(password)
        human_delay()

    # Log In confirm
    final_login = try_find(driver, AppiumBy.ANDROID_UIAUTOMATOR,
                           'new UiSelector().textContains("Log In")', 6)
    if final_login:
        final_login.click()
        human_delay(2.0, 3.0)

    # Handle potential 2FA prompt (manual/OTP service step—customize here)
    code_field = try_find(driver, AppiumBy.CLASS_NAME, "android.widget.EditText", 6)
    if code_field:
        print("[WARN] 2FA code required. Enter it manually or integrate an SMS API.")
        # You can integrate SMSMan/5SIM/etc. here.

    # Validate camera presence as "logged in"
    camera = try_find(driver, AppiumBy.ACCESSIBILITY_ID, "Take a Snap", timeout=12)
    return camera is not None

def view_stories(driver, count: int = 8):
    """
    Opens the Stories/Spotlight screen and watches a few items with human-like timing.
    """
    print("[INFO] Opening Stories…")
    # Swipe left from camera to open Stories/Discover (depends on UI version)
    size = driver.get_window_size()
    start_x = int(size["width"] * 0.85)
    end_x   = int(size["width"] * 0.15)
    y       = int(size["height"] * 0.5)
    driver.swipe(jitter(start_x), jitter(y), jitter(end_x), jitter(y), 300)
    human_delay(1.0, 1.7)

    watched = 0
    while watched < count:
        human_delay(2.0, 4.5)
        # Tap the first story tile region (approx). Update with a proper selector if possible.
        tap_xy(driver, 0.25, 0.25)
        human_delay(5.0, 9.0)  # watch duration
        # Close story (tap top-left/back gesture)
        tap_xy(driver, 0.08, 0.08)
        watched += 1
        # Scroll feed a bit
        swipe_up(driver, 300)
        print(f"[INFO] Watched story #{watched}")

def add_friends(driver, usernames: List[str], max_add: int = 5):
    """
    Opens search, enters usernames, and taps Add.
    """
    print("[INFO] Adding friends…")
    # From camera: tap search (top-left) — this may vary; adjust selector.
    # Fallback: swipe down to open search.
    driver.swipe(jitter(500), jitter(200), jitter(500), jitter(1400), 250)
    human_delay(0.8, 1.4)

    added = 0
    for u in usernames:
        if added >= max_add:
            break
        # Find search field
        search = try_find(driver, AppiumBy.CLASS_NAME, "android.widget.EditText", 6)
        if not search:
            # Try tapping approximate search box area
            tap_xy(driver, 0.5, 0.12)
            search = try_find(driver, AppiumBy.CLASS_NAME, "android.widget.EditText", 6)
        if not search:
            print("[WARN] Could not find search field; skipping.")
            continue

        search.click()
        search.clear()
        search.send_keys(u)
        human_delay(1.0, 1.8)

        # Tap the user result (approx area for first result)
        tap_xy(driver, 0.5, 0.24)
        human_delay(0.8, 1.4)

        # Tap Add button (text can be 'Add', 'Add Friend', etc.)
        add_btn = try_find(driver, AppiumBy.ANDROID_UIAUTOMATOR,
                           'new UiSelector().textContains("Add")', 5)
        if add_btn:
            add_btn.click()
            added += 1
            print(f"[INFO] Sent friend request to: {u}")
        else:
            print(f"[WARN] Add button not found for {u}")

        # Go back to search list
        driver.back()
        human_delay(0.7, 1.3)
        driver.back()
        human_delay(0.7, 1.1)

def send_chat_message(driver, to_username: str, message: str):
    """
    Opens chat and sends a simple text message to a user.
    """
    print(f"[INFO] Sending chat to {to_username}…")
    # From camera, swipe right to open chat list
    size = driver.get_window_size()
    start_x = int(size["width"] * 0.15)
    end_x   = int(size["width"] * 0.85)
    y       = int(size["height"] * 0.5)
    driver.swipe(jitter(start_x), jitter(y), jitter(end_x), jitter(y), 300)
    human_delay(0.8, 1.3)

    # Tap search in chat list, enter username
    tap_xy(driver, 0.9, 0.10)  # top-right search icon region (approx)
    human_delay(0.6, 1.0)

    search = try_find(driver, AppiumBy.CLASS_NAME, "android.widget.EditText", 6)
    if search:
        search.click()
        search.clear()
        search.send_keys(to_username)
        human_delay(1.0, 1.8)
        # Tap first result
        tap_xy(driver, 0.5, 0.25)
        human_delay(0.8, 1.2)

        # Type message (chat input is usually an EditText at bottom)
        input_field = try_find(driver, AppiumBy.CLASS_NAME, "android.widget.EditText", 6)
        if input_field:
            input_field.click()
            input_field.send_keys(message)
            human_delay(0.5, 0.9)
            # Tap send (paper plane) approx area at bottom-right
            tap_xy(driver, 0.93, 0.94)
            print("[INFO] Chat sent.")
        else:
            print("[WARN] Could not find chat input field.")
    else:
        print("[WARN] Could not open chat search.")

# ---------- Orchestrator ----------

def run_flow():
    driver = connect_driver()
    try:
        if not login(driver, SNAP_USERNAME, SNAP_PASSWORD):
            print("[ERROR] Login failed.")
            return

        # Randomize task order to look human
        tasks = [
            lambda: view_stories(driver, count=random.randint(5, 9)),
            lambda: add_friends(driver, usernames=["testuser1", "alice_snap", "bob_snap"], max_add=3),
            lambda: send_chat_message(driver, to_username="testuser1", message="Hey! 👋")
        ]
        random.shuffle(tasks)
        for t in tasks:
            t()
            human_delay(1.5, 3.0)

        print("[INFO] Done.")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_flow()
