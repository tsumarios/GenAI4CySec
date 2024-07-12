import sqlite3
import os
import platform
import shutil
import logging
import time
import random
import string

# Configure logging
logging.basicConfig(
    filename="cookie_manipulation.log",
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s",
)

# Paths to cookie databases for different browsers
BROWSER_PATHS = {
    "chrome": {
        "windows": os.path.join(
            os.getenv("LOCALAPPDATA"),
            "Google",
            "Chrome",
            "User Data",
            "Default",
            "Cookies",
        ),
        "mac": os.path.expanduser(
            "~/Library/Application Support/Google/Chrome/Default/Cookies"
        ),
        "linux": os.path.expanduser("~/.config/google-chrome/Default/Cookies"),
    },
    "firefox": {
        "windows": os.path.join(os.getenv("APPDATA"), "Mozilla", "Firefox", "Profiles"),
        "mac": os.path.expanduser("~/Library/Application Support/Firefox/Profiles"),
        "linux": os.path.expanduser("~/.mozilla/firefox"),
    },
    "edge": {
        "windows": os.path.join(
            os.getenv("LOCALAPPDATA"),
            "Microsoft",
            "Edge",
            "User Data",
            "Default",
            "Cookies",
        ),
        "mac": os.path.expanduser(
            "~/Library/Application Support/Microsoft Edge/Default/Cookies"
        ),
        "linux": os.path.expanduser("~/.config/microsoft-edge/Default/Cookies"),
    },
}


def get_cookie_db_path(browser):
    os_type = platform.system().lower()
    paths = BROWSER_PATHS.get(browser, {})
    if os_type.startswith("win"):
        return paths.get("windows")
    elif os_type == "darwin":
        return paths.get("mac")
    elif os_type == "linux":
        return paths.get("linux")
    return None


def backup_database(db_path):
    backup_path = db_path + ".backup"
    try:
        shutil.copy2(db_path, backup_path)
        logging.info(f"Backup created at {backup_path}")
    except Exception as e:
        logging.error(f"Failed to create backup: {e}")
        raise


def restore_database(db_path):
    backup_path = db_path + ".backup"
    try:
        shutil.copy2(backup_path, db_path)
        logging.info(f"Database restored from {backup_path}")
    except Exception as e:
        logging.error(f"Failed to restore backup: {e}")
        raise


def execute_query(db_path, query, params=()):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        cursor.close()
        conn.close()
        logging.info(f"Executed query: {query} with params: {params}")
    except sqlite3.Error as e:
        logging.error(f"SQLite error: {e}")
        raise


def secure_delete_cookie(db_path, name):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT rowid, * FROM cookies WHERE name = ?", (name,))
        rows = cursor.fetchall()
        for row in rows:
            rowid = row[0]
            cursor.execute(
                "UPDATE cookies SET name = ?, value = ? WHERE rowid = ?",
                (randomize_string(name), randomize_string(row[2]), rowid),
            )
        conn.commit()
        cursor.execute("DELETE FROM cookies WHERE name = ?", (randomize_string(name),))
        conn.commit()
        cursor.close()
        conn.close()
        logging.info(f"Securely deleted cookie: {name}")
    except sqlite3.Error as e:
        logging.error(f"SQLite error during secure delete: {e}")
        raise


def randomize_string(original):
    return "".join(
        random.choices(string.ascii_letters + string.digits, k=len(original))
    )


def add_cookie(db_path, name, value, domain, path, expires_utc, is_secure, is_httponly):
    query = """
    INSERT INTO cookies (name, value, host_key, path, expires_utc, is_secure, is_httponly)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    params = (name, value, domain, path, expires_utc, is_secure, is_httponly)
    execute_query(db_path, query, params)


def modify_cookie(
    db_path,
    old_name,
    new_name,
    new_value,
    new_domain,
    new_path,
    new_expires_utc,
    new_is_secure,
    new_is_httponly,
):
    query = """
    UPDATE cookies
    SET name = ?, value = ?, host_key = ?, path = ?, expires_utc = ?, is_secure = ?, is_httponly = ?
    WHERE name = ?
    """
    params = (
        new_name,
        new_value,
        new_domain,
        new_path,
        new_expires_utc,
        new_is_secure,
        new_is_httponly,
        old_name,
    )
    execute_query(db_path, query, params)


def obfuscate_timestamps(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE cookies SET creation_utc = ?, last_access_utc = ?, expires_utc = ?",
            (
                random.randint(0, 9999999999),
                random.randint(0, 9999999999),
                random.randint(0, 9999999999),
            ),
        )
        conn.commit()
        cursor.close()
        conn.close()
        logging.info("Timestamps obfuscated.")
    except sqlite3.Error as e:
        logging.error(f"SQLite error during timestamp obfuscation: {e}")
        raise


def delete_log():
    try:
        os.remove("cookie_manipulation.log")
        print("Log file deleted.")
    except OSError as e:
        print(f"Error deleting log file: {e}")
        logging.error(f"Error deleting log file: {e}")


def randomize_file_timestamps(file_path):
    atime = random.randint(0, int(time.time()))
    mtime = random.randint(0, int(time.time()))
    os.utime(file_path, (atime, mtime))
    logging.info(f"File timestamps randomized for {file_path}")


def fragment_database(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("VACUUM")
        conn.commit()
        cursor.close()
        conn.close()
        logging.info("Database fragmented.")
    except sqlite3.Error as e:
        logging.error(f"SQLite error during database fragmentation: {e}")
        raise


def defragment_database(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA auto_vacuum = FULL")
        cursor.execute("VACUUM")
        conn.commit()
        cursor.close()
        conn.close()
        logging.info("Database defragmented.")
    except sqlite3.Error as e:
        logging.error(f"SQLite error during database defragmentation: {e}")
        raise


# Example usage
if __name__ == "__main__":
    browser = "chrome"  # Can be 'chrome', 'firefox', or 'edge'
    db_path = get_cookie_db_path(browser)

    if db_path and os.path.exists(db_path):
        try:
            backup_database(db_path)

            # Add a cookie
            add_cookie(
                db_path,
                "test_cookie",
                "test_value",
                ".example.com",
                "/",
                9999999999,
                0,
                0,
            )
            print("Cookie added.")

            # Modify a cookie
            modify_cookie(
                db_path,
                "test_cookie",
                "test_cookie_modified",
                "test_value_modified",
                ".example.com",
                "/",
                9999999999,
                0,
                0,
            )
            print("Cookie modified.")

            # Securely delete a cookie
            secure_delete_cookie(db_path, "test_cookie_modified")
            print("Cookie securely deleted.")

            # Obfuscate timestamps
            obfuscate_timestamps(db_path)
            print("Timestamps obfuscated.")

            # Fragment and defragment the database
            fragment_database(db_path)
            defragment_database(db_path)
            print("Database fragmented and defragmented.")

            # Randomize file timestamps
            randomize_file_timestamps(db_path)
            print("File timestamps randomized.")

            # Clean up logs
            delete_log()

        except Exception as e:
            logging.error(f"Operation failed: {e}")
            print(f"An error occurred: {e}")
            restore_database(db_path)
            print("Database restored from backup.")
    else:
        print(f"Cookie database not found for browser: {browser}")
        logging.warning(f"Cookie database not found for browser: {browser}")
