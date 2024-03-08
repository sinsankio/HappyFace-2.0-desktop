from tkinter import messagebox


class MessageBoxHelper:
    @staticmethod
    def show_info_message_box(title="showinfo", body="Information") -> None:
        messagebox.showinfo(title, body)

    @staticmethod
    def show_warning_message_box(title="showwarning", body="Warning") -> None:
        messagebox.showwarning(title, body)

    @staticmethod
    def show_error_message_box(title="showerror", body="Error") -> None:
        messagebox.showerror(title, body)

    @staticmethod
    def show_ok_cancel_message_box(title="okcancel", body="Ok or Cancel?") -> bool:
        return messagebox.askokcancel(title, body)
