import json
import os

FILENAME = "bmi_records.json"

records = []

if os.path.exists(FILENAME):
    with open(FILENAME, "r", encoding="utf-8") as f:
        records = json.load(f)

red = "\033[91m"
green = "\033[92m"
yellow = "\033[93m"
blue = "\033[94m"
purple = "\033[95m"
color_reset = "\033[0m"

while True:
    print(f"{blue}====== BMI Calculator ======{color_reset}")
    print(f"{blue}1.Enter your information{color_reset}")
    print(f"{blue}2.View history{color_reset}")
    print(f"{blue}3.Search records by name{color_reset}")
    print(f"{blue}4.Sort records{color_reset}")
    print(f"{red}6.Clear all records{color_reset}")
    print(f"{red}7.Quit{color_reset}")
    print(f"{blue}   Enter number 1 to 7{color_reset}") 
    print(f"{blue}={color_reset}" * 28)
    
    choice = input("Enter the option you want: ").strip()
    print("")
    
    if choice == "1":
        while True:
            date = input("Enter your measurement date.(MMDD, e.g., 0105) : ").strip()
            
            if date.isdigit() and len(date) == 4:
                month = date[:2]
                day = int(date[2:])
                
                days_in_month = {
                    "01": 31, "02": 28, "03": 31, "04": 30,
                    "05": 31, "06": 30, "07": 31, "08": 31,
                    "09": 30, "10": 31, "11": 30, "12": 31
                }
                
                if month in days_in_month:
                    max_day = days_in_month[month] # 在days_in_month中 你輸入的month那個月份的資料
                    
                    if 1 <= day <= max_day:
                        break
                    else:
                        print("")
                        print(f"{red}Invaild day! Month {month} only has 1 to {max_day} days.{color_reset}\n")
                else:
                    print("")
                    print(f"{red}Invalid month! Please enter a month between 01 to 12.{color_reset}\n")           
            else:
                print("")
                print(f"{red}Invalid format! Please enter exactly 4 digits (e.g., 0105 for January 5th).{color_reset}\n")
            
        name = input("Enter your name: ").strip()
        
        while True:
            h = input("Enter your height(M): ").strip()
            if h.replace(".", "", 1).isdigit():
                height = float(h)
                if height >= 2.5 or height <= 0.5:
                    print("")
                    print(f"{red}Please enter your real height(M)!{color_reset}\n")
                else:
                    break
            else:
                print("")
                print(f"{red}Enter the correct number, please!(if your height is 170 cm. Enter 1.7.){color_reset}\n")
        
        while True:
            w = input("Enter your weight(KG): ").strip()
            if w.replace(".", "", 1).isdigit():
                weight = float(w)
                if weight >= 300 or weight <= 20:
                    print("")
                    print(f"{red}Please enter your real weight(KG)!{color_reset}\n")
                else:
                    break
            else:
                print("")
                print(f"{red}Enter the correct number, please!(if your weight is 60 kg. Enter 60.){color_reset}\n")
        
        bmi = weight / height ** 2
        
        print("")
        print(f"{green}Your BMI is: {bmi:.2f}{color_reset}")
        
        if bmi < 18.5:
            print(f"{yellow}Too thin{color_reset}\n")
        elif bmi > 18.5 and bmi < 24:
            print(f"{green}Normal{color_reset}\n")
        else:
            print(f"{red}Overweight{color_reset}\n")
        
        r = {}
        r['date'] = date
        r['name'] = name
        r['height'] = height
        r['weight'] = weight
        r['bmi'] = bmi
        records.append(r)
        
        with open(FILENAME, "w", encoding="utf-8") as f:
            json.dump(records, f, ensure_ascii=False, indent=4)
    
    elif choice == "2":
        if len(records) == 0:
            print(f"{yellow}No records found yet!{color_reset}\n")
        else:
            print(f"{'Date':<12}{'Name':<12}{'Height':<12}{'Weight':<12}{'BMI':<12}")
            print("-" * 60)
            
            for r in records: # 從records中 一筆一筆拿出來
                print(f"{r['date']:<12}{r['name']:<12}{r['height']:<12.2f}{r['weight']:<12.1f}{r['bmi']:<12.2f}\n")
                
    elif choice == "3":
        if len(records) == 0:
            print(f"{yellow}No records found yet!{color_reset}\n")
        else:
            search_name = input("Enter the name you want to search: ").strip()
            print("")
            
            found = False # 預設沒找到人 found相當於一個開關

            for r in records:
                if r['name'].lower() == search_name.lower():
                    # 第一次如果有有找到人會是True 第二輪開始就變False了
                    if not found:
                        print(f"{'Date':<12}{'Name':<12}{'Height':<12}{'Weight':<12}{'BMI':<12}")
                        print("-" * 60)
                        found = True # 找到人後變True 之後的迴圈就不會一直重複了
                    
                    print(f"{r['date']:<12}{r['name']:<12}{r['height']:<12.2f}{r['weight']:<12.1f}{r['bmi']:<12.2f}\n")\
                        
            if not found: # "if not"會導致found變成True 就等於if found == False:
                print(f"{red}No records found for '{search_name}'.{color_reset}\n")
                    
            else:
                print("")

    elif choice == "4":
        if len(records) == 0:
            print(f"{yellow}No records found yet!{color_reset}\n")
        else:
            while True:
                print("")
                print(f"{blue}====== Sort Option ======={color_reset}")
                print(f"{blue}1.Sort by date(earliest to lastest){color_reset}")
                print(f"{blue}2.Sort by BMI(lowest to highest){color_reset}")
                print(f"{blue}3.Sort by BMI(highest to lowest){color_reset}")
                print(f"{blue}4.Back to main menu{color_reset}")
                print(f"{blue}={color_reset}" * 28)
                
                sort_choice = input("Enter the option you want: ").strip()
                
                if sort_choice == "1":
                    sorted_records = sorted(records, key=lambda x: x['date']) # dict沒法排序 所以要先把records的每一個dict暫時命名為x x['date']就是把date這個欄位的值抽出來
                    print(f"{green}---- Sorted by date(earliest to lastest) ----{color_reset}\n")
                    break
                    
                elif sort_choice == "2":
                    sorted_records = sorted(records, key=lambda x: x['bmi'])
                    print(f"{green}---- Sorted by BMI(lowest to highest) ----{color_reset}\n")
                    break
                    
                elif sort_choice == "3":
                    sorted_records = sorted(records, key=lambda x: x['bmi'], reverse = True)
                    print(f"{green}---- Sorted by BMI(highest to lowest) ----{color_reset}\n")
                    break

                elif sort_choice == "4":
                    break
                
                else:
                    print(f"{red}Invaild option! Please try again.{color_reset}\n")
                    
            if sort_choice in ["1", "2", "3"]: # ["1", "2", "3"]是多個選項 所以不能用==    
                print(f"{'Date':<12}{'Name':<12}{'Height':<12}{'Weight':<12}{'BMI':<12}")
                print("-" * 60)
                for r in sorted_records:
                    print(f"{r['date']:<12}{r['name']:<12}{r['height']:<12.2f}{r['weight']:<12.1f}{r['bmi']:<12.2f}\n")
                            
    elif choice == "6":
        records.clear()
        
        with open(FILENAME, "w", encoding="utf-8") as f:
            json.dump(records, f, ensure_ascii=False, indent=4)
            
        print(f"{yellow}All records have been cleared!{color_reset}\n")
        
    elif choice == "7":
        print(f"{blue}Goodbye!{color_reset}\n")
        break
    
    else:
        print(f"{red}Invalid option! Please try again.{color_reset}\n")