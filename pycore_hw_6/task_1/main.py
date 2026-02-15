def total_salary(path):
    try:
        total = 0
        count = 0
        
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                
                if not line:
                    continue
                
                parts = line.split(',')
                
                if len(parts) == 2:
                    try:
                        salary = int(parts[1])
                        total += salary
                        count += 1
                    except ValueError:
                        print(f"Error: salary not correct'{line}'")
                        continue
        
        if count > 0:
            average = total / count
            return total, average
        else:
            print("File do not correct data")
            return 0, 0
    
    except FileNotFoundError:
        print(f"Error: file '{path}' can not be reached")
        return 0, 0
    except Exception as e:
        print(f"Error: {e}")
        return 0, 0

total, average = total_salary("salary_file.txt")
print(f"Загальна сума заробітної плати: {total}, Середня заробітна плата: {average}")