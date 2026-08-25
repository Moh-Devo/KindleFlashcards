import invoker as inv
import window_stuff as win


if __name__ == "__main__":
    while True:
        win.set_focus_window_clipboard_check()

        add_note = inv.fill_anki_card()

        try:
            result = inv.invoke("addNote", add_note)
            print(f"Anki card added! Note ID: {result}\n")

        except Exception as e:
            print(f"Failed to add Anki card: {e}\n")