import pyperclip
import win32gui
import win32con
import time
from pynput.keyboard import Key, Controller


def get_foreground_window():
    return win32gui.GetForegroundWindow()


def get_window_title(window_handle):
    return win32gui.GetWindowText(window_handle)


def find_window_by_title(title):
    return win32gui.FindWindow(None, title)


def set_foreground_window_by_title(title):
    window_handle = find_window_by_title(title)
    if window_handle:
        win32gui.ShowWindow(window_handle, win32con.SW_RESTORE)
        win32gui.BringWindowToTop(window_handle)
        time.sleep(0.1)
        win32gui.SetForegroundWindow(window_handle)
        return True
    else:
        print(f"Window with title '{title}' not found.")
        return False


def set_foreground_window(window_handle):
    win32gui.ShowWindow(window_handle, win32con.SW_RESTORE)
    win32gui.BringWindowToTop(window_handle)
    win32gui.SetForegroundWindow(window_handle)
    return


def find_window_by_partial_title(partial_title):
    def callback(hwnd, hwnd_list):
        title = win32gui.GetWindowText(hwnd)
        if partial_title.lower() in title.lower():
            hwnd_list.append(hwnd)
        return True

    hwnd_list = []
    win32gui.EnumWindows(callback, hwnd_list)
    return hwnd_list


def set_foreground_window_by_partial_title(partial_title):
    window_handles = find_window_by_partial_title(partial_title)

    if window_handles:
        kbd = Controller()
        window_handle = window_handles[0]
        kbd.press(Key.alt)
        try:
            win32gui.SetForegroundWindow(window_handle)
        finally:
            kbd.release(Key.alt)
        return True
    else:
        print(f"Window with partial title '{partial_title}' not found.")
        return False


def clipboard_change_check():
    pass


def set_focus_window_clipboard_check():
    previous_clipboard_content = pyperclip.paste()

    while True:
        target_window_title = 'giga_finder.exe'
        current_clipboard_content = pyperclip.paste()
        if current_clipboard_content != previous_clipboard_content:
            window_handle = get_foreground_window()
            window_title = get_window_title(window_handle)

            previous_clipboard_content = current_clipboard_content

            if 'Mohameds Kindle für PC' in window_title:
                print(f"Window Handle: {window_handle}")
                print(f"Window Title: {window_title}")

                set_foreground_window_by_partial_title(target_window_title)
                return True

        time.sleep(1)
