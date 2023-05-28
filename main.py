import tkinter as tk
from tkinter import ttk
import sqlite3
import datetime
from tkcalendar import DateEntry

class Main(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.db = DB()

        self.tree = ttk.Treeview(self, columns=('ID', 'Опис', 'Категорія', 'Ціна'), show='headings')
        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('Опис', width=200, anchor=tk.CENTER)
        self.tree.column('Категорія', width=100, anchor=tk.CENTER)
        self.tree.column('Ціна', width=70, anchor=tk.CENTER)
        self.tree.heading('ID', text='ID')
        self.tree.heading('Опис', text='Опис')
        self.tree.heading('Категорія', text='Категорія')
        self.tree.heading('Ціна', text='Ціна')
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH)

        scroll_y = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll_y.set)

        self.view_records()

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)

        btn_add = ttk.Button(btn_frame, text='Додати', command=self.open_add_dialog)
        btn_add.grid(row=0, column=0)

        btn_edit = ttk.Button(btn_frame, text='Редагувати', command=self.open_edit_dialog)
        btn_edit.grid(row=1, column=0)

        btn_delete = ttk.Button(btn_frame, text='Видалити', command=self.delete_book)
        btn_delete.grid(row=2, column=0)

        btn_search = ttk.Button(btn_frame, text='Пошук', command=self.open_search_dialog)
        btn_search.grid(row=3, column=0)

        btn_generate_report = ttk.Button(btn_frame, text='Згенерувати звіт', command=self.generate_report)
        btn_generate_report.grid(row=4, column=0)

    def generate_report(self):
        report_dialog = ReportDialog(self, self.db)
        report_dialog.generate_report()    

    def view_records(self):
        records = self.db.get_all_records()
        self.tree.delete(*self.tree.get_children())
        for record in records:
            self.tree.insert('', 'end', values=record)

    def search_records(self, search_value):
        records = self.db.search_records(search_value)
        self.tree.delete(*self.tree.get_children())
        for record in records:
            self.tree.insert('', 'end', values=record)

    def open_add_dialog(self):
        AddBookDialog(self, self.db)

    def open_edit_dialog(self):
        selected_item = self.tree.selection()
        if selected_item:
            record_id = self.tree.item(selected_item)['values'][0]
            EditBookDialog(self, self.db, record_id)

    def delete_book(self):
        selected_item = self.tree.selection()
        if selected_item:
            record_id = self.tree.item(selected_item)['values'][0]
            self.db.delete_record(record_id)
        self.view_records()

    def open_search_dialog(self):
        SearchDialog(self, self.db)

    def generate_report(self):
        ReportDialog(self, self.db)


class AddBookDialog(tk.Toplevel):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.parent = parent
        self.db = db

        self.title('Додати книгу')
        self.geometry('300x200')

        lbl_description = ttk.Label(self, text='Опис:')
        lbl_description.pack()
        self.entry_description = ttk.Entry(self)
        self.entry_description.pack()

        lbl_category = ttk.Label(self, text='Категорія:')
        lbl_category.pack()
        self.entry_category = ttk.Entry(self)
        self.entry_category.pack()

        lbl_price = ttk.Label(self, text='Ціна:')
        lbl_price.pack()
        self.entry_price = ttk.Entry(self)
        self.entry_price.pack()

        btn_add = ttk.Button(self, text='Додати', command=self.add_book)
        btn_add.pack(pady=10)

    def add_book(self):
        description = self.entry_description.get()
        category = self.entry_category.get()
        price = float(self.entry_price.get())
        self.db.add_record(description, category, price)
        self.parent.view_records()
        self.destroy()


class EditBookDialog(tk.Toplevel):
    def __init__(self, parent, db, record_id):
        super().__init__(parent)
        self.parent = parent
        self.db = db
        self.record_id = record_id

        self.title('Редагувати книгу')
        self.geometry('300x200')

        lbl_description = ttk.Label(self, text='Опис:')
        lbl_description.pack()
        self.entry_description = ttk.Entry(self)
        self.entry_description.pack()

        lbl_category = ttk.Label(self, text='Категорія:')
        lbl_category.pack()
        self.entry_category = ttk.Entry(self)
        self.entry_category.pack()

        lbl_price = ttk.Label(self, text='Ціна:')
        lbl_price.pack()
        self.entry_price = ttk.Entry(self)
        self.entry_price.pack()

        self.load_record()

        btn_update = ttk.Button(self, text='Оновити', command=self.update_book)
        btn_update.pack(pady=10)

    def load_record(self):
        record = self.db.get_record(self.record_id)
        if record:
            self.entry_description.insert(0, record[1])
            self.entry_category.insert(0, record[2])
            self.entry_price.insert(0, record[3])

    def update_book(self):
        description = self.entry_description.get()
        category = self.entry_category.get()
        price = float(self.entry_price.get())
        self.db.update_record(self.record_id, description, category, price)
        self.parent.view_records()
        self.destroy()


class SearchDialog(tk.Toplevel):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.parent = parent
        self.db = db

        self.title('Пошук')
        self.geometry('300x100')

        lbl_search = ttk.Label(self, text='Значення пошуку:')
        lbl_search.pack()
        self.entry_search = ttk.Entry(self)
        self.entry_search.pack()

        btn_search = ttk.Button(self, text='Пошук', command=self.search)
        btn_search.pack(pady=10)

    def search(self):
        search_value = self.entry_search.get()
        self.parent.search_records(search_value)
        self.destroy()


class ReportDialog(tk.Toplevel):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.parent = parent
        self.db = db

        self.title('Звіт')
        self.geometry('300x150')

        lbl_start_date = ttk.Label(self, text='Початкова дата:')
        lbl_start_date.pack()
        self.entry_start_date = DateEntry(self)  # Используем виджет DateEntry
        self.entry_start_date.pack()

        lbl_end_date = ttk.Label(self, text='Кінцева дата:')
        lbl_end_date.pack()
        self.entry_end_date = DateEntry(self)  # Используем виджет DateEntry
        self.entry_end_date.pack()

        btn_generate = ttk.Button(self, text='Згенерувати', command=self.generate_report)
        btn_generate.pack(pady=10)

    def generate_report(self):
        start_date_str = self.entry_start_date.get()
        end_date_str = self.entry_end_date.get()

        try:
            start_date = datetime.datetime.strptime(start_date_str, '%d.%m.%Y').date()
            end_date = datetime.datetime.strptime(end_date_str, '%d.%m.%Y').date()
        except ValueError:
            tk.messagebox.showerror('Ошибка', 'Некорректный формат даты.')
            return

        report_records = self.db.generate_report(start_date, end_date)
        if report_records:
            report = ''
            for record in report_records:
                report += f'Опис: {record[1]}\nКатегорія: {record[2]}\nЦіна: {record[3]}\n\n'
            tk.messagebox.showinfo('Звіт', report)
        else:
            tk.messagebox.showinfo('Звіт', 'Немає записів за вказаний період.')


class DB:
    def __init__(self):
        self.connection = sqlite3.connect('records.db')
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT,
            category TEXT,
            price REAL,
            date DATE
        )
        '''
        self.cursor.execute(query)
        self.connection.commit()

    def add_record(self, description, category, price):
        query = 'INSERT INTO records (description, category, price) VALUES (?, ?, ?)'
        self.cursor.execute(query, (description, category, price))
        self.connection.commit()

    def get_all_records(self):
        query = 'SELECT * FROM records'
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_record(self, record_id):
        query = 'SELECT * FROM records WHERE id = ?'
        self.cursor.execute(query, (record_id,))
        return self.cursor.fetchone()

    def update_record(self, record_id, description, category, price):
        query = 'UPDATE records SET description = ?, category = ?, price = ? WHERE id = ?'
        self.cursor.execute(query, (description, category, price, record_id))
        self.connection.commit()

    def delete_record(self, record_id):
        query = 'DELETE FROM records WHERE id = ?'
        self.cursor.execute(query, (record_id,))
        self.connection.commit()

    def search_records(self, search_value):
        query = 'SELECT * FROM records WHERE description LIKE ? OR category LIKE ?'
        search_pattern = f'%{search_value}%'
        self.cursor.execute(query, (search_pattern, search_pattern))
        return self.cursor.fetchall()

    def generate_report(self, start_date, end_date):
        query = 'SELECT * FROM records WHERE date BETWEEN ? AND ?'
        self.cursor.execute(query, (start_date, end_date))
        return self.cursor.fetchall()


if __name__ == '__main__':
    root = tk.Tk()
    Main(root).pack()
    root.title('Expense Tracker')
    root.geometry('800x600')
    root.mainloop()
