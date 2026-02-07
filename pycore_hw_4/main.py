#Task_1
from datetime import datetime

def get_days_from_today(date):
    try:
        given_date = datetime.strptime(date, '%Y-%m-%d').date()
        today = datetime.today().date()
        difference = today - given_date
        return difference.days
    
    except ValueError:
        print("Error: unexepted format. Try 'YYYY-MM-DD'")
        return None
    
print(get_days_from_today("2020-10-09"))

#Task_2

import random

def get_numbers_ticket(min, max, quantity):
    if min < 1 or max > 1000 or quantity < 1:
        return []
    
    if min > max or quantity > (max - min + 1):
        return []
    
    numbers = random.sample(range(min, max + 1), quantity)
    
    return sorted(numbers)


lottery_numbers = get_numbers_ticket(1, 49, 6)
print("Ваші лотерейні числа:", lottery_numbers)

print(get_numbers_ticket(1, 36, 5))

#Task_3

import re

def normalize_phone(phone_number):
    cleaned = re.sub(r'[^\d+]', '', phone_number)
    
    if cleaned.startswith('+'):
        return cleaned
    
    if cleaned.startswith('380'):
        return '+' + cleaned
    
    return '+38' + cleaned

raw_numbers = [
  "    +38(050)123-32-34",
"     0503451234",
"(050)8889900",
"38050-111-22-22",
"38050 111 22 11   ",
]

sanitized_numbers = [normalize_phone(num) for num in raw_numbers]
print("Normalized phone numbers:", sanitized_numbers)

#Task_4

from datetime import datetime, timedelta

def get_upcoming_birthdays(users):
    today = datetime.today().date()
    upcoming = []
    
    for user in users:
        birthday = datetime.strptime(user["birthday"], "%Y.%m.%d").date()
        
        birthday_this_year = birthday.replace(year=today.year)
        
        if birthday_this_year < today:
            birthday_this_year = birthday_this_year.replace(year=today.year + 1)
        
        days_until_birthday = (birthday_this_year - today).days
        
        if 0 <= days_until_birthday <= 7:
            congratulation_date = birthday_this_year
            
            weekday = congratulation_date.weekday()
            
            if weekday == 5:
                congratulation_date += timedelta(days=2)
            elif weekday == 6:
                congratulation_date += timedelta(days=1)
            
            upcoming.append({
                "name": user["name"],
                "congratulation_date": congratulation_date.strftime("%Y.%m.%d")
            })
    
    return upcoming

users = [
    {"name": "John Doe", "birthday": "1985.02.13"},
    {"name": "Jane Smith", "birthday": "1990.01.27"}
]

upcoming_birthdays = get_upcoming_birthdays(users)
print("Список привітань на цьому тижні:", upcoming_birthdays)

users2 = [
    {"name": "Petro Marchenko", "birthday": "2026.02.07"},
    {"name": "Anna Popova", "birthday": "1991.02.08"},  
    {"name": "Maks Popov", "birthday": "1989.03.17"},
]

upcoming_birthdays2 = get_upcoming_birthdays(users2)
print("Дні народження з суб та воскр :", upcoming_birthdays2)
