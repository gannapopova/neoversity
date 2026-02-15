def get_cats_info(path):
    try:
        cats_list = []
        
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                
                if not line:
                    continue
                
                parts = line.split(',')
                
                if len(parts) == 3:
                    cat_info = {
                        "id": parts[0],
                        "name": parts[1],
                        "age": parts[2]
                    }
                    cats_list.append(cat_info)
                else:
                    print(f"Error: wrong line '{line}'")
        
        return cats_list
    
    except FileNotFoundError:
        print(f"Error: file '{path}' can not found")
        return []
    except Exception as e:
        print(f"Error: {e}")
        return []

cats_info = get_cats_info("cats_file.txt")
print(cats_info)