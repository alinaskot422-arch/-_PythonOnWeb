import json
import os
from datetime import datetime
from tkinter import *
from tkinter import ttk, messagebox
import random

class FoodItem:
    def __init__(self, name, calories, protein, fat, carbs):
        self.name = name
        self.calories = float(calories)
        self.protein = float(protein)
        self.fat = float(fat)
        self.carbs = float(carbs) 
    def to_dict(self):
        return {
            "name": self.name,
            "calories": self.calories,
            "protein": self.protein,
            "fat": self.fat,
            "carbs": self.carbs
        }   
    @staticmethod
    def from_dict(data):
        return FoodItem(data["name"], data["calories"], data["protein"], data["fat"], data["carbs"])
class MealEntry:
    def __init__(self, food_item, grams, meal_type, date):
        self.food_item = food_item
        self.grams = float(grams)
        self.meal_type = meal_type
        self.date = date  
    def get_nutrients(self):
        multiplier = self.grams / 100
        return {
            "calories": self.food_item.calories * multiplier,
            "protein": self.food_item.protein * multiplier,
            "fat": self.food_item.fat * multiplier,
            "carbs": self.food_item.carbs * multiplier
        }
    def to_dict(self):
        return {
            "food_name": self.food_item.name,
            "grams": self.grams,
            "meal_type": self.meal_type,
            "date": self.date,
            "food_item": self.food_item.to_dict()
        }
    @staticmethod
    def from_dict(data):
        food = FoodItem.from_dict(data["food_item"])
        return MealEntry(food, data["grams"], data["meal_type"], data["date"])
class Database:
    def __init__(self, foods_file="foods.json", diary_file="diary.json"):
        self.foods_file = foods_file
        self.diary_file = diary_file
        self.foods = []
        self.entries = []
        self.load_foods()
        self.load_diary() 
    def load_foods(self):
        if os.path.exists(self.foods_file):
            try:
                with open(self.foods_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.foods = [FoodItem.from_dict(item) for item in data]
            except (json.JSONDecodeError, KeyError):
                self.foods = []
        else:
            self.foods = [] 
    def save_foods(self):
        with open(self.foods_file, "w", encoding="utf-8") as f:
            json.dump([food.to_dict() for food in self.foods], f, ensure_ascii=False, indent=2)
    def load_diary(self):
        if os.path.exists(self.diary_file):
            try:
                with open(self.diary_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.entries = [MealEntry.from_dict(item) for item in data]
            except (json.JSONDecodeError, KeyError):
                self.entries = []
        else:
            self.entries = [] 
    def save_diary(self):
        with open(self.diary_file, "w", encoding="utf-8") as f:
            json.dump([entry.to_dict() for entry in self.entries], f, ensure_ascii=False, indent=2)  
    def add_food(self, food):
        self.foods.append(food)
        self.save_foods() 
    def delete_food(self, index):
        if 0 <= index < len(self.foods):
            del self.foods[index]
            self.save_foods()
            return True
        return False 
    def add_entry(self, entry):
        self.entries.append(entry)
        self.save_diary()    
    def delete_entry(self, index):
        if 0 <= index < len(self.entries):
            del self.entries[index]
            self.save_diary()
            return True
        return False   
    def get_today_stats(self, target_date=None):
        if target_date is None:
            target_date = datetime.now().strftime("%Y-%m-%d")      
        today_entries = [e for e in self.entries if e.date == target_date]       
        total = {"calories": 0, "protein": 0, "fat": 0, "carbs": 0}
        meals = {"breakfast": [], "lunch": [], "dinner": [], "snack": []}        
        for entry in today_entries:
            nutrients = entry.get_nutrients()
            for key in total:
                total[key] += nutrients[key]
            meals[entry.meal_type].append(entry)     
        return total, meals
    def search_foods(self, query):
        return [f for f in self.foods if query.lower() in f.name.lower()]
    def get_total_by_meal_type(self, target_date=None):
        if target_date is None:
            target_date = datetime.now().strftime("%Y-%m-%d")
        today_entries = [e for e in self.entries if e.date == target_date]
        meal_totals = {"breakfast": 0, "lunch": 0, "dinner": 0, "snack": 0}
        for e in today_entries:
            meal_totals[e.meal_type] += e.get_nutrients()['calories']
        return meal_totals
class KBJUApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Трекер КБЖУ - счётчик калорий")
        self.root.geometry("1100x700")
        self.root.resizable(True, True)     
        self.db = Database()     
        self.target_calories = IntVar(value=2000)
        self.target_protein = IntVar(value=150)
        self.target_fat = IntVar(value=67)
        self.target_carbs = IntVar(value=250)   
        self.food_name_var = StringVar()
        self.food_cal_var = StringVar()
        self.food_protein_var = StringVar()
        self.food_fat_var = StringVar()
        self.food_carbs_var = StringVar()   
        self.grams_var = StringVar()
        self.meal_type_var = StringVar(value="breakfast")
        self.selected_food_var = StringVar()      
        self.current_date = datetime.now().strftime("%Y-%m-%d")
        self.search_var = StringVar()
        self.meal_filter_var = StringVar(value="all")
        self.tips_list = [
            "Завтрак должен быть в течение часа после пробуждения",
            "Пейте воду за 20 минут до еды, а не во время",
            "Яблоко вместо печенья - минус 150 ккал",
            "10 минут ходьбы после еды улучшают метаболизм",
            "Половина тарелки - овощи, четверть - белок, четверть - гарнир",
            "Ешьте медленно - мозг получает сигнал сытости через 20 минут",
            "Сон 7-8 часов помогает не переедать на следующий день",
            "Ведите дневник питания - это повышает осознанность"
        ]
        self.current_tip = StringVar(value=random.choice(self.tips_list))
        self.create_widgets()
        self.update_food_list()
        self.update_today_stats()
        self.update_diary_list()
        self.update_progress_bars()
    def update_progress_bars(self):
        total, _ = self.db.get_today_stats(self.current_date)
        cal_percent = (total['calories'] / self.target_calories.get() * 100) if self.target_calories.get() > 0 else 0
        prot_percent = (total['protein'] / self.target_protein.get() * 100) if self.target_protein.get() > 0 else 0
        fat_percent = (total['fat'] / self.target_fat.get() * 100) if self.target_fat.get() > 0 else 0
        carbs_percent = (total['carbs'] / self.target_carbs.get() * 100) if self.target_carbs.get() > 0 else 0
        self.cal_progress['value'] = min(100, cal_percent)
        self.prot_progress['value'] = min(100, prot_percent)
        self.fat_progress['value'] = min(100, fat_percent)
        self.carbs_progress['value'] = min(100, carbs_percent)
        self.cal_label.config(text=f"{total['calories']:.0f} / {self.target_calories.get()} ккал ({cal_percent:.0f}%)")
        self.prot_label.config(text=f"{total['protein']:.0f} / {self.target_protein.get()} г ({prot_percent:.0f}%)")
        self.fat_label.config(text=f"{total['fat']:.0f} / {self.target_fat.get()} г ({fat_percent:.0f}%)")
        self.carbs_label.config(text=f"{total['carbs']:.0f} / {self.target_carbs.get()} г ({carbs_percent:.0f}%)")
    def refresh_tip(self):
        self.current_tip.set(random.choice(self.tips_list))
    def create_widgets(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)     
        foods_frame = Frame(notebook)
        diary_frame = Frame(notebook)
        stats_frame = Frame(notebook)
        settings_frame = Frame(notebook)
        tips_frame = Frame(notebook)
        notebook.add(foods_frame, text="База продуктов")
        notebook.add(diary_frame, text="Дневник питания")
        notebook.add(stats_frame, text="Статистика")
        notebook.add(tips_frame, text="Советы и прогресс")
        notebook.add(settings_frame, text="Настройки")
        self.create_foods_tab(foods_frame)
        self.create_diary_tab(diary_frame)
        self.create_stats_tab(stats_frame)
        self.create_tips_tab(tips_frame)
        self.create_settings_tab(settings_frame)
    def create_tips_tab(self, parent):
        frame = LabelFrame(parent, text="Совет дня", padx=20, pady=20)
        frame.pack(fill="x", padx=20, pady=10)
        tip_label = Label(frame, textvariable=self.current_tip, font=("Arial", 12, "italic"), wraplength=500, fg="purple")
        tip_label.pack(pady=10)
        Button(frame, text="Новый совет", command=self.refresh_tip, bg="purple", fg="white").pack(pady=5)
        progress_frame = LabelFrame(parent, text="Прогресс выполнения целей на сегодня", padx=20, pady=20)
        progress_frame.pack(fill="both", expand=True, padx=20, pady=10)
        Label(progress_frame, text="Калории:", font=("Arial", 10, "bold")).pack(anchor="w", pady=2)
        self.cal_progress = ttk.Progressbar(progress_frame, length=400, mode='determinate')
        self.cal_progress.pack(pady=2)
        self.cal_label = Label(progress_frame, text="0 / 0 ккал (0%)", font=("Arial", 9))
        self.cal_label.pack(anchor="w", pady=2)
        Label(progress_frame, text="Белки:", font=("Arial", 10, "bold")).pack(anchor="w", pady=2)
        self.prot_progress = ttk.Progressbar(progress_frame, length=400, mode='determinate')
        self.prot_progress.pack(pady=2)
        self.prot_label = Label(progress_frame, text="0 / 0 г (0%)", font=("Arial", 9))
        self.prot_label.pack(anchor="w", pady=2)
        Label(progress_frame, text="Жиры:", font=("Arial", 10, "bold")).pack(anchor="w", pady=2)
        self.fat_progress = ttk.Progressbar(progress_frame, length=400, mode='determinate')
        self.fat_progress.pack(pady=2)
        self.fat_label = Label(progress_frame, text="0 / 0 г (0%)", font=("Arial", 9))
        self.fat_label.pack(anchor="w", pady=2)
        Label(progress_frame, text="Углеводы:", font=("Arial", 10, "bold")).pack(anchor="w", pady=2)
        self.carbs_progress = ttk.Progressbar(progress_frame, length=400, mode='determinate')
        self.carbs_progress.pack(pady=2)
        self.carbs_label = Label(progress_frame, text="0 / 0 г (0%)", font=("Arial", 9))
        self.carbs_label.pack(anchor="w", pady=2)
        Button(progress_frame, text="Обновить прогресс", command=self.update_progress_bars, bg="blue", fg="white").pack(pady=10)
    def create_foods_tab(self, parent):
        add_frame = LabelFrame(parent, text="Добавить продукт", padx=10, pady=10)
        add_frame.pack(fill="x", padx=10, pady=5)      
        Label(add_frame, text="Название:").grid(row=0, column=0, sticky="w", padx=5)
        Entry(add_frame, textvariable=self.food_name_var, width=20).grid(row=0, column=1, padx=5)      
        Label(add_frame, text="Калории (100г):").grid(row=0, column=2, sticky="w", padx=5)
        Entry(add_frame, textvariable=self.food_cal_var, width=15).grid(row=0, column=3, padx=5)       
        Label(add_frame, text="Белки (100г):").grid(row=1, column=0, sticky="w", padx=5)
        Entry(add_frame, textvariable=self.food_protein_var, width=15).grid(row=1, column=1, padx=5)      
        Label(add_frame, text="Жиры (100г):").grid(row=1, column=2, sticky="w", padx=5)
        Entry(add_frame, textvariable=self.food_fat_var, width=15).grid(row=1, column=3, padx=5)     
        Label(add_frame, text="Углеводы (100г):").grid(row=1, column=4, sticky="w", padx=5)
        Entry(add_frame, textvariable=self.food_carbs_var, width=15).grid(row=1, column=5, padx=5)      
        Button(add_frame, text="Добавить продукт", command=self.add_food, 
               bg="green", fg="white").grid(row=2, column=0, columnspan=6, pady=10)
        search_frame = Frame(parent)
        search_frame.pack(fill="x", padx=10, pady=5)
        Label(search_frame, text="Поиск:").pack(side=LEFT, padx=5)
        Entry(search_frame, textvariable=self.search_var, width=30).pack(side=LEFT, padx=5)
        Button(search_frame, text="Найти", command=self.search_foods, bg="blue", fg="white").pack(side=LEFT, padx=5)
        Button(search_frame, text="Сброс", command=self.reset_food_list, bg="gray", fg="white").pack(side=LEFT, padx=5)
        list_frame = LabelFrame(parent, text="Список продуктов", padx=10, pady=10)
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)     
        scroll_y = Scrollbar(list_frame, orient=VERTICAL)
        self.foods_tree = ttk.Treeview(list_frame, columns=("name", "cal", "prot", "fat", "carbs"), 
               show="headings", yscrollcommand=scroll_y.set)
        scroll_y.config(command=self.foods_tree.yview)
        scroll_y.pack(side=RIGHT, fill=Y)
        self.foods_tree.pack(fill="both", expand=True)  
        self.foods_tree.heading("name", text="Продукт")
        self.foods_tree.heading("cal", text="Ккал/100г")
        self.foods_tree.heading("prot", text="Белки")
        self.foods_tree.heading("fat", text="Жиры")
        self.foods_tree.heading("carbs", text="Углеводы")  
        self.foods_tree.column("name", width=200)
        self.foods_tree.column("cal", width=100)
        self.foods_tree.column("prot", width=80)
        self.foods_tree.column("fat", width=80)
        self.foods_tree.column("carbs", width=80)     
        Button(list_frame, text="Удалить выбранный продукт", command=self.delete_food, 
               bg="red", fg="white").pack(pady=5)
    def search_foods(self):
        query = self.search_var.get()
        if not query:
            self.reset_food_list()
            return
        for item in self.foods_tree.get_children():
            self.foods_tree.delete(item)
        results = self.db.search_foods(query)
        for i, food in enumerate(results):
            self.foods_tree.insert("", END, iid=i, values=(
                food.name, f"{food.calories:.1f}", f"{food.protein:.1f}", 
                f"{food.fat:.1f}", f"{food.carbs:.1f}"
            ))
    def reset_food_list(self):
        self.search_var.set("")
        self.update_food_list()
    def create_diary_tab(self, parent):
        add_frame = LabelFrame(parent, text="Добавить приём пищи", padx=10, pady=10)
        add_frame.pack(fill="x", padx=10, pady=5)      
        Label(add_frame, text="Продукт:").grid(row=0, column=0, sticky="w", padx=5)
        self.food_combo = ttk.Combobox(add_frame, textvariable=self.selected_food_var, 
                                       state="readonly", width=25)
        self.food_combo.grid(row=0, column=1, padx=5)
        Label(add_frame, text="Вес (грамм):").grid(row=0, column=2, sticky="w", padx=5)
        Entry(add_frame, textvariable=self.grams_var, width=10).grid(row=0, column=3, padx=5)  
        Label(add_frame, text="Приём пищи:").grid(row=0, column=4, sticky="w", padx=5)
        meal_combo = ttk.Combobox(add_frame, textvariable=self.meal_type_var, 
                                  values=["breakfast", "lunch", "dinner", "snack"], 
                                  state="readonly", width=10)
        meal_combo.grid(row=0, column=5, padx=5)   
        Button(add_frame, text="Добавить в дневник", command=self.add_meal_entry, 
               bg="green", fg="white").grid(row=0, column=6, padx=10)
        filter_frame = Frame(add_frame)
        filter_frame.grid(row=1, column=0, columnspan=7, pady=5)
        Label(filter_frame, text="Фильтр по приёму:").pack(side=LEFT, padx=5)
        filter_combo = ttk.Combobox(filter_frame, textvariable=self.meal_filter_var, 
                                    values=["all", "breakfast", "lunch", "dinner", "snack"], 
                                    state="readonly", width=12)
        filter_combo.pack(side=LEFT, padx=5)
        Button(filter_frame, text="Применить", command=self.filter_diary, bg="purple", fg="white").pack(side=LEFT, padx=5)
        date_frame = Frame(add_frame)
        date_frame.grid(row=2, column=0, columnspan=7, pady=10)     
        Label(date_frame, text="Дата (ГГГГ-ММ-ДД):").pack(side=LEFT, padx=5)
        self.date_var = StringVar(value=self.current_date)
        Entry(date_frame, textvariable=self.date_var, width=12).pack(side=LEFT, padx=5)
        Button(date_frame, text="Показать", command=self.change_date, 
               bg="blue", fg="white").pack(side=LEFT, padx=5)
        Button(date_frame, text="Сегодня", command=self.show_today, 
               bg="orange", fg="white").pack(side=LEFT, padx=5) 
        list_frame = LabelFrame(parent, text="Записи за день", padx=10, pady=10)
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)  
        scroll_y = Scrollbar(list_frame, orient=VERTICAL)
        self.diary_tree = ttk.Treeview(list_frame, columns=("meal", "food", "grams", "cal", "prot", "fat", "carbs"),                               
                show="headings", yscrollcommand=scroll_y.set)
        scroll_y.config(command=self.diary_tree.yview)
        scroll_y.pack(side=RIGHT, fill=Y)
        self.diary_tree.pack(fill="both", expand=True)    
        self.diary_tree.heading("meal", text="Приём")
        self.diary_tree.heading("food", text="Продукт")
        self.diary_tree.heading("grams", text="Граммы")
        self.diary_tree.heading("cal", text="Ккал")
        self.diary_tree.heading("prot", text="Белки")
        self.diary_tree.heading("fat", text="Жиры")
        self.diary_tree.heading("carbs", text="Углеводы")  
        self.diary_tree.column("meal", width=80)
        self.diary_tree.column("food", width=200)
        self.diary_tree.column("grams", width=70)
        self.diary_tree.column("cal", width=80)
        self.diary_tree.column("prot", width=80)
        self.diary_tree.column("fat", width=80)
        self.diary_tree.column("carbs", width=80)   
        Button(list_frame, text="Удалить запись", command=self.delete_entry, 
               bg="red", fg="white").pack(pady=5)
    def filter_diary(self):
        self.update_diary_list()
    def create_stats_tab(self, parent):
        self.stats_text = Text(parent, wrap=WORD, font=("Courier", 10))
        self.stats_text.pack(fill="both", expand=True, padx=10, pady=10)   
        Button(parent, text="Обновить статистику", command=self.update_stats_display, 
               bg="blue", fg="white").pack(pady=5)
        Button(parent, text="Детальная статистика по приёмам", command=self.show_meal_details, 
               bg="purple", fg="white").pack(pady=5)
    def show_meal_details(self):
        meal_totals = self.db.get_total_by_meal_type(self.current_date)
        meal_names = {"breakfast": "Завтрак", "lunch": "Обед", "dinner": "Ужин", "snack": "Перекус"}
        details = f"\nДетальная статистика за {self.current_date}:\n\n"
        for meal, total in meal_totals.items():
            details += f"{meal_names[meal]}: {total:.1f} ккал\n"
        messagebox.showinfo("Статистика по приёмам", details)
    def create_settings_tab(self, parent):
        frame = LabelFrame(parent, text="Дневные нормы КБЖУ", padx=20, pady=20)
        frame.pack(fill="both", expand=True, padx=20, pady=20)  
        Label(frame, text="Калории (ккал):").grid(row=0, column=0, sticky="w", pady=10)
        Entry(frame, textvariable=self.target_calories, width=15).grid(row=0, column=1, padx=10)   
        Label(frame, text="Белки (г):").grid(row=1, column=0, sticky="w", pady=10)
        Entry(frame, textvariable=self.target_protein, width=15).grid(row=1, column=1, padx=10)   
        Label(frame, text="Жиры (г):").grid(row=2, column=0, sticky="w", pady=10)
        Entry(frame, textvariable=self.target_fat, width=15).grid(row=2, column=1, padx=10)  
        Label(frame, text="Углеводы (г):").grid(row=3, column=0, sticky="w", pady=10)
        Entry(frame, textvariable=self.target_carbs, width=15).grid(row=3, column=1, padx=10) 
        Button(frame, text="Сохранить нормы", command=self.save_targets, 
               bg="green", fg="white").grid(row=4, column=0, columnspan=2, pady=20)    
        Label(frame, text="Инструкция:\n1. Добавьте продукты в базу\n2. Выберите продукт и укажите вес\n3. Отслеживайте КБЖУ за день", 
              justify=LEFT, fg="gray").grid(row=5, column=0, columnspan=2, pady=20)
    def add_food(self):
        name = self.food_name_var.get().strip()
        if not name:
            messagebox.showerror("Ошибка", "Введите название продукта!")
            return      
        try:
            cal = float(self.food_cal_var.get() or 0)
            prot = float(self.food_protein_var.get() or 0)
            fat = float(self.food_fat_var.get() or 0)
            carbs = float(self.food_carbs_var.get() or 0)   
            if cal < 0 or prot < 0 or fat < 0 or carbs < 0:
                messagebox.showerror("Ошибка", "Значения не могут быть отрицательными!")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные числа!")
            return     
        food = FoodItem(name, cal, prot, fat, carbs)
        self.db.add_food(food)     
        self.food_name_var.set("")
        self.food_cal_var.set("")
        self.food_protein_var.set("")
        self.food_fat_var.set("")
        self.food_carbs_var.set("")    
        self.update_food_list()
        messagebox.showinfo("Успех", f"Продукт '{name}' добавлен!")  
    def delete_food(self):
        selected = self.foods_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите продукт для удаления!")
            return    
        index = int(selected[0])
        food_name = self.db.foods[index].name    
        if messagebox.askyesno("Подтверждение", f"Удалить продукт '{food_name}'?"):
            self.db.delete_food(index)
            self.update_food_list()  
    def update_food_list(self):
        for item in self.foods_tree.get_children():
            self.foods_tree.delete(item)   
        for i, food in enumerate(self.db.foods):
            self.foods_tree.insert("", END, iid=i, values=(
                food.name, f"{food.calories:.1f}", f"{food.protein:.1f}", 
                f"{food.fat:.1f}", f"{food.carbs:.1f}"
            ))   
        food_names = [food.name for food in self.db.foods]
        self.food_combo.config(values=food_names)
        if food_names:
            self.selected_food_var.set(food_names[0]) 
    def add_meal_entry(self):
        grams_str = self.grams_var.get().strip()
        if not grams_str:
            messagebox.showerror("Ошибка", "Введите вес в граммах!")
            return     
        try:
            grams = float(grams_str)
            if grams <= 0:
                messagebox.showerror("Ошибка", "Вес должен быть положительным!")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректный вес!")
            return   
        food_name = self.selected_food_var.get()
        if not food_name:
            messagebox.showerror("Ошибка", "Выберите продукт!")
            return  
        food = next((f for f in self.db.foods if f.name == food_name), None)
        if not food:
            messagebox.showerror("Ошибка", "Продукт не найден!")
            return     
        meal_type = self.meal_type_var.get()      
        entry = MealEntry(food, grams, meal_type, self.current_date)
        self.db.add_entry(entry)       
        self.grams_var.set("")      
        self.update_diary_list()
        self.update_today_stats()
        self.update_stats_display()
        self.update_progress_bars()
        messagebox.showinfo("Успех", "Запись добавлена в дневник!")   
    def delete_entry(self):
        selected = self.diary_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите запись для удаления!")
            return    
        index = int(selected[0])    
        today_entries = [e for e in self.db.entries if e.date == self.current_date]
        if self.meal_filter_var.get() != "all":
            today_entries = [e for e in today_entries if e.meal_type == self.meal_filter_var.get()]
        if 0 <= index < len(today_entries):
            actual_index = self.db.entries.index(today_entries[index])       
            if messagebox.askyesno("Подтверждение", "Удалить запись?"):
                self.db.delete_entry(actual_index)
                self.update_diary_list()
                self.update_today_stats()
                self.update_stats_display()
                self.update_progress_bars()  
    def update_diary_list(self):
        for item in self.diary_tree.get_children():
            self.diary_tree.delete(item)    
        today_entries = [e for e in self.db.entries if e.date == self.current_date]
        if self.meal_filter_var.get() != "all":
            today_entries = [e for e in today_entries if e.meal_type == self.meal_filter_var.get()]
        meal_names = {"breakfast": "Завтрак", "lunch": "Обед", "dinner": "Ужин", "snack": "Перекус"}       
        for i, entry in enumerate(today_entries):
            nutrients = entry.get_nutrients()
            self.diary_tree.insert("", END, iid=i, values=(
                meal_names.get(entry.meal_type, entry.meal_type),
                entry.food_item.name,
                f"{entry.grams:.0f}",
                f"{nutrients['calories']:.1f}",
                f"{nutrients['protein']:.1f}",
                f"{nutrients['fat']:.1f}",
                f"{nutrients['carbs']:.1f}"
            ))
    def update_today_stats(self):
        total, meals = self.db.get_today_stats(self.current_date)     
        self.daily_total = total  
    def update_stats_display(self):
        total, meals = self.db.get_today_stats(self.current_date)   
        cal_percent = (total['calories'] / self.target_calories.get() * 100) if self.target_calories.get() > 0 else 0
        prot_percent = (total['protein'] / self.target_protein.get() * 100) if self.target_protein.get() > 0 else 0
        fat_percent = (total['fat'] / self.target_fat.get() * 100) if self.target_fat.get() > 0 else 0
        carbs_percent = (total['carbs'] / self.target_carbs.get() * 100) if self.target_carbs.get() > 0 else 0 
        stats_str = f"""
════════════════════════════════════════════════════════════════
                    СТАТИСТИКА КБЖУ ЗА ДЕНЬ                    
                      {self.current_date}                        
════════════════════════════════════════════════════════════════
   КАЛОРИИ:    {total['calories']:>6.1f} / {self.target_calories.get()} ккал  ({cal_percent:>5.1f}%)      
   БЕЛКИ:      {total['protein']:>6.1f} / {self.target_protein.get()} г        ({prot_percent:>5.1f}%)      
   ЖИРЫ:       {total['fat']:>6.1f} / {self.target_fat.get()} г        ({fat_percent:>5.1f}%)      
   УГЛЕВОДЫ:   {total['carbs']:>6.1f} / {self.target_carbs.get()} г        ({carbs_percent:>5.1f}%)      
════════════════════════════════════════════════════════════════
  ПО ПРИЁМАМ ПИЩИ:                                             
  Завтрак:      {self.get_meal_sum(meals['breakfast']):>6.1f} ккал                         
  Обед:         {self.get_meal_sum(meals['lunch']):>6.1f} ккал                         
  Ужин:         {self.get_meal_sum(meals['dinner']):>6.1f} ккал                         
  Перекусы:     {self.get_meal_sum(meals['snack']):>6.1f} ккал                         
════════════════════════════════════════════════════════════════
"""
        self.stats_text.delete(1.0, END)
        self.stats_text.insert(1.0, stats_str)  
    def get_meal_sum(self, entries):
        return sum(entry.get_nutrients()['calories'] for entry in entries)    
    def change_date(self):
        new_date = self.date_var.get().strip()
        try:
            datetime.strptime(new_date, "%Y-%m-%d")
            self.current_date = new_date
            self.update_diary_list()
            self.update_today_stats()
            self.update_stats_display()
            self.update_progress_bars()
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты! Используйте ГГГГ-ММ-ДД")
    def show_today(self):
        self.current_date = datetime.now().strftime("%Y-%m-%d")
        self.date_var.set(self.current_date)
        self.update_diary_list()
        self.update_today_stats()
        self.update_stats_display()
        self.update_progress_bars()   
    def save_targets(self):
        messagebox.showinfo("Успех", "Нормы КБЖУ сохранены!")
        self.update_stats_display()
        self.update_progress_bars()
if __name__ == "__main__":
    root = Tk()
    app = KBJUApp(root)
    root.mainloop()