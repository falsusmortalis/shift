from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from datetime import datetime, timedelta
from collections import defaultdict

class Employee:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.vacation_days = []

class ShiftScheduler:
    def __init__(self):
        self.employees = []
        self.assigned_shifts = []
        self.unassigned_shifts = []
        self.employee_stats = defaultdict(lambda: {'shifts_count': 0, 'occupied_days': set(), 'monthly_slots': 15})
    
    def add_employee(self, name, vacation_days=None):
        employee_id = len(self.employees) + 1
        employee = Employee(employee_id, name)
        if vacation_days:
            employee.vacation_days = vacation_days
        self.employees.append(employee)
        return employee_id

    def generate_schedule(self, daily_shifts):
        self.assigned_shifts = []
        self.unassigned_shifts = []
        
        for employee in self.employees:
            self.employee_stats[employee.id] = {'shifts_count': 0, 'occupied_days': set(), 'monthly_slots': 15}
        
        all_shifts = []
        for date, shift_types in daily_shifts.items():
            for shift_type in shift_types:
                all_shifts.append({'date': date, 'type': shift_type})
        
        all_shifts.sort(key=lambda x: x['date'])
        
        for shift in all_shifts:
            available_employees = self._get_available_employees(shift)
            
            if available_employees:
                available_employees.sort(key=lambda emp: self.employee_stats[emp.id]['shifts_count'])
                employee = available_employees[0]
                
                self.assigned_shifts.append({
                    'date': shift['date'],
                    'type': shift['type'],
                    'employee_id': employee.id
                })
                
                self.employee_stats[employee.id]['shifts_count'] += 1
                
                shift_days = [shift['date'], shift['date'] + timedelta(days=1)]
                self.employee_stats[employee.id]['occupied_days'].update(shift_days)
                
                if shift['type'] in [1, 2, 3, 4, 5, 7]:
                    self.employee_stats[employee.id]['monthly_slots'] -= 1
            else:
                self.unassigned_shifts.append(shift)
    
    def _get_available_employees(self, shift):
        available = []
        shift_days = [shift['date'], shift['date'] + timedelta(days=1)]
        
        for employee in self.employees:
            # Проверка отпуска
            vacation_conflict = False
            for day in shift_days:
                for vacation in employee.vacation_days:
                    if vacation.date() == day.date():
                        vacation_conflict = True
                        break
                if vacation_conflict:
                    break
            
            if vacation_conflict:
                continue
                
            # Проверка лимита
            if shift['type'] in [1, 2, 3, 4, 5, 7] and self.employee_stats[employee.id]['monthly_slots'] <= 0:
                continue
                
            # Проверка занятости
            busy = any(day in self.employee_stats[employee.id]['occupied_days'] for day in shift_days)
            if busy:
                continue
                    
            available.append(employee)
            
        return available

class VahotApp(App):
    def build(self):
        self.scheduler = ShiftScheduler()
        self.daily_shifts = {}
        
        # Основной интерфейс
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Заголовок
        title = Label(text='Распределение нарядов', size_hint_y=0.1, font_size='20sp')
        layout.add_widget(title)
        
        # Область для ввода сотрудников
        self.employees_input = TextInput(
            hint_text='Введите сотрудников:\nИванов:01.01.2024,02.01.2024\nПетров:\nСидоров:15.01.2024',
            size_hint_y=0.3
        )
        layout.add_widget(self.employees_input)
        
        # Область для ввода расписания
        self.schedule_input = TextInput(
            hint_text='Введите расписание:\n01.01.2024;1,2,3\n02.01.2024;4,5\n03.01.2024;6,7',
            size_hint_y=0.3
        )
        layout.add_widget(self.schedule_input)
        
        # Кнопка расчета
        calc_btn = Button(text='Рассчитать расписание', size_hint_y=0.1)
        calc_btn.bind(on_press=self.calculate_schedule)
        layout.add_widget(calc_btn)
        
        # Область результатов
        scroll = ScrollView(size_hint_y=0.2)
        self.results_label = Label(text='Результаты появятся здесь', size_hint_y=None, text_size=(None, None))
        self.results_label.bind(texture_size=self.results_label.setter('size'))
        scroll.add_widget(self.results_label)
        layout.add_widget(scroll)
        
        return layout
    
    def calculate_schedule(self, instance):
        try:
            # Парсим сотрудников
            self.scheduler = ShiftScheduler()
            employees_text = self.employees_input.text.strip()
            for line in employees_text.split('\n'):
                if ':' in line:
                    name, vacations_str = line.split(':', 1)
                    name = name.strip()
                    if name:
                        vacation_days = []
                        for date_str in vacations_str.split(','):
                            date_str = date_str.strip()
                            if date_str:
                                try:
                                    date = datetime.strptime(date_str, "%d.%m.%Y")
                                    vacation_days.append(date)
                                except ValueError:
                                    pass
                        self.scheduler.add_employee(name, vacation_days)
            
            # Парсим расписание
            self.daily_shifts = {}
            schedule_text = self.schedule_input.text.strip()
            for line in schedule_text.split('\n'):
                if ';' in line:
                    date_str, shifts_str = line.split(';', 1)
                    date_str = date_str.strip()
                    shifts_str = shifts_str.strip()
                    
                    if date_str:
                        try:
                            date = datetime.strptime(date_str, "%d.%m.%Y")
                            shift_types = []
                            for shift_str in shifts_str.split(','):
                                shift_type = int(shift_str.strip())
                                if 1 <= shift_type <= 7:
                                    shift_types.append(shift_type)
                            self.daily_shifts[date] = shift_types
                        except ValueError:
                            pass
            
            # Генерируем расписание
            self.scheduler.generate_schedule(self.daily_shifts)
            
            # Показываем результаты
            result_text = "✅ РАСПРЕДЕЛЕНИЕ ЗАВЕРШЕНО\n\n"
            result_text += f"📊 Всего нарядов: {sum(len(shifts) for shifts in self.daily_shifts.values())}\n"
            result_text += f"✅ Распределено: {len(self.scheduler.assigned_shifts)}\n"
            result_text += f"⚠️ Нераспределено: {len(self.scheduler.unassigned_shifts)}\n\n"
            
            result_text += "👥 СТАТИСТИКА ПО СОТРУДНИКАМ:\n"
            for employee in self.scheduler.employees:
                stats = self.scheduler.employee_stats[employee.id]
                vacation_count = len(employee.vacation_days)
                result_text += f"• {employee.name}: {stats['shifts_count']} нарядов, отпусков: {vacation_count}, осталось слотов: {stats['monthly_slots']}\n"
            
            if self.scheduler.unassigned_shifts:
                result_text += f"\n🚫 НЕРАСПРЕДЕЛЕННЫЕ НАРЯДЫ:\n"
                for shift in self.scheduler.unassigned_shifts[:10]:
                    result_text += f"- {shift['date'].strftime('%d.%m.%Y')}: наряд {shift['type']}\n"
            
            self.results_label.text = result_text
            
        except Exception as e:
            self.results_label.text = f"❌ Ошибка: {str(e)}"

if __name__ == '__main__':
    VahotApp().run()
