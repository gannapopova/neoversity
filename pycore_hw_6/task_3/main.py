import sys
from pathlib import Path
from colorama import Fore, Style, init

init(autoreset=True)

def show_directory(path, level=0):
    try:
        all_items = list(path.iterdir())
        
        all_items.sort(key=lambda x: (x.is_file(), x.name))
        
        for item in all_items:
            indent = "    " * level
            if item.name == 'venv' or item.name == '.git':
             continue
            if item.is_dir():
                print(f"{indent}{Fore.BLUE}📂 {item.name}{Style.RESET_ALL}")
                show_directory(item, level + 1)
            else:
                print(f"{indent}{Fore.GREEN}📜 {item.name}{Style.RESET_ALL}")
    
    except PermissionError:
        indent = "    " * level
        print(f"{indent}{Fore.RED}[No acess]{Style.RESET_ALL}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"{Fore.RED}Error: path to folder is not specified")
        print(f"{Fore.YELLOW}Correct: python3 task_3")
        sys.exit(1)
    
    user_path = sys.argv[1]
    folder = Path(user_path)
    
    if not folder.exists():
        print(f"{Fore.RED}Error: Folder '{user_path}' not exists!")
        sys.exit(1)
    
    if not folder.is_dir():
        print(f"{Fore.RED}Error: '{user_path}' - is not a folder!")
        sys.exit(1)
    
    print(f"{Fore.CYAN}📦 {folder.name}{Style.RESET_ALL}")
    
    show_directory(folder)

    