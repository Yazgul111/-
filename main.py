import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

class TrainingPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner")
        self.trainings = []
        self.load_data()

        # Поля ввода
        self.date_label = tk.Label(root, text="Дата (ГГГГ-ММ-ДД):")
        self.date_label.grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = tk.Entry(root)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        self.type_label = tk.Label(root, text="Тип тренировки:")
        self.type_label.grid(row=1, column=0, padx=5, pady=5)
        self.type_entry = tk.Entry(root)
        self.type_entry.grid(row=1, column=1, padx=5, pady=5)

        self.duration_label = tk.Label(root, text="Длительность (мин):")
        self.duration_label.grid(row=2, column=0, padx=5, pady=5)
        self.duration_entry = tk.Entry(root)
        self.duration_entry.grid(row=2, column=1, padx=5, pady=5)

        self.add_button = tk.Button(root, text="Добавить тренировку", command=self.add_training)
        self.add_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Таблица
        self.tree = ttk.Treeview(root, columns=("date", "type", "duration"), show='headings')
        self.tree.heading("date", text="Дата")
        self.tree.heading("type", text="Тип")
        self.tree.heading("duration", text="Длительность")
        self.tree.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        # Фильтрация
        self.filter_type_label = tk.Label(root, text="Фильтр по типу:")
        self.filter_type_label.grid(row=5, column=0, padx=5, pady=5)
        self.filter_type_entry = tk.Entry(root)
        self.filter_type_entry.grid(row=5, column=1, padx=5, pady=5)

        self.filter_date_start_label = tk.Label(root, text="Дата с:")
        self.filter_date_start_label.grid(row=6, column=0, padx=5, pady=5)
        self.filter_date_start_entry = tk.Entry(root)
        self.filter_date_start_entry.grid(row=6, column=1, padx=5, pady=5)

        self.filter_date_end_label = tk.Label(root, text="Дата по:")
        self.filter_date_end_label.grid(row=7, column=0, padx=5, pady=5)
        self.filter_date_end_entry = tk.Entry(root)
        self.filter_date_end_entry.grid(row=7, column=1, padx=5, pady=5)

        self.apply_filter_button = tk.Button(root, text="Применить фильтр", command=self.apply_filter)
        self.apply_filter_button.grid(row=8, column=0, columnspan=2, pady=10)

        self.reset_filter_button = tk.Button(root, text="Сбросить фильтр", command=self.reset_filter)
        self.reset_filter_button.grid(row=9, column=0, columnspan=2, pady=10)

        self.update_table()

    def add_training(self):
        date = self.date_entry.get()
        type_ = self.type_entry.get()
        duration = self.duration_entry.get()

        if not self.validate_date(date):
            messagebox.showerror("Ошибка", "Дата должна быть в формате ГГГГ-ММ-ДД")
            return
        if not duration.isdigit() or int(duration) <= 0:
            messagebox.showerror("Ошибка", "Длительность должна быть положительным числом")
            return

        self.trainings.append({"date": date, "type": type_, "duration": int(duration)})
        self.save_data()
        self.update_table()

    def validate_date(self, date):
        try:
            datetime.strptime(date, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def update_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for t in self.trainings:
            self.tree.insert("", "end", values=(t["date"], t["type"], t["duration"]))

    def apply_filter(self):
        filter_type = self.filter_type_entry.get().lower()
        date_start = self.filter_date_start_entry.get()
        date_end = self.filter_date_end_entry.get()

        filtered = self.trainings

        if filter_type:
            filtered = [t for t in filtered if filter_type in t["type"].lower()]

        if date_start and self.validate_date(date_start):
            filtered = [t for t in filtered if t["date"] >= date_start]

        if date_end and self.validate_date(date_end):
            filtered = [t for t in filtered if t["date"] <= date_end]

        for i in self.tree.get_children():
            self.tree.delete(i)
        for t in filtered:
            self.tree.insert("", "end", values=(t["date"], t["type"], t["duration"]))

    def reset_filter(self):
        self.filter_type_entry.delete(0, tk.END)
        self.filter_date_start_entry.delete(0, tk.END)
        self.filter_date_end_entry.delete(0, tk.END)
        self.update_table()

    def save_data(self):
        with open("trainings.json", "w", encoding="utf-8") as f:
            json.dump(self.trainings, f, ensure_ascii=False, indent=4)

    def load_data(self):
        try:
            with open("trainings.json", "r", encoding="utf-8") as f:
                self.trainings = json.load(f)
                # Сортируем по дате (новые сверху)
                self.trainings.sort(key=lambda x: x["date"], reverse=True)
                return True
        except FileNotFoundError:
            return False

if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingPlanner(root)
    root.mainloop()