import invoker as inv
import window_stuff as win


if __name__ == "__main__":
    while True:
        win.set_focus_window_clipboard_check()
        add_note = inv.fill_anki_card()
        inv.invoke('addNote', add_note)  # maybe put error handling here? i.e store the invoke return as variable
        print("Anki card added!\n")

