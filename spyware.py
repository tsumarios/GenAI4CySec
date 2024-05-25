import time
import daemonize
import pygetwindow as gw
import keyboard


# Function to record URL to the 'history' file
def record_url(url):
    with open("history.txt", "a") as history_file:
        history_file.write(f"{url}\n")


# Main function to monitor browser activity and record URLs
def main():
    while True:
        try:
            # Check if the browser window is active
            active_window = gw.getActiveWindow()
            if active_window and "browser" in active_window.title.lower():
                # Assuming 'Ctrl + L' is used to focus on the browser address bar
                keyboard.press_and_release("ctrl + l")
                time.sleep(0.5)  # Allow time for the address bar to be in focus
                keyboard.press_and_release(
                    "ctrl + c"
                )  # Copy the URL from the address bar
                url_to_record = keyboard.read_event().name  # Read the clipboard content
                # Record the URL
                record_url(url_to_record)
        except Exception as e:
            # Handle exceptions (e.g., missing libraries, window title not found)
            print(f"Error: {e}")
        # Sleep for a while before checking again
        time.sleep(2)


if __name__ == "__main__":
    # Define the paths for the daemon process
    pid = "url_recorder.pid"
    stdout = "url_recorder.log"
    stderr = "url_recorder_error.log"
    # Create the daemon context
    daemon = daemonize.Daemonize(
        app="url_recorder", pid=pid, action=main, keep_fds=[1, 2]
    )
    # Start the daemon
    daemon.start()
