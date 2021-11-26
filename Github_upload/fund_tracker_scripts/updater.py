import json
EM = input("E Or M? (E/M) :")
if EM == 'E':       
    with open("/home/pi/pythonbotProject1/fundinfo.txt",'r') as file:
            funds=json.load(file)
if EM == 'M':
    with open("/home/pi/pythonbotProjectM/fundinfo.txt",'r') as file:
            funds=json.load(file)         
while True:
    update=input("View Funds? (Y/N) :")


    if update == 'Y':
        print(funds)

    AR=input("Add, Remove Or Update? (A/R/U) :")

    if AR == 'R':
        remove= input("Which Fund? :")
        funds.pop(remove)

    if AR == 'A':
        typ = input("What Type? (fund/share/unit/cash/etf) :")
        if typ == 'fund':
            code = input("What Is The Code? https://markets.ft.com/data/funds/tearsheet/summary?s= :" )
        if typ == 'unit':
            code = input(" What Is The Code? https://www.share.com/investments/shares/{code}#prices-and-trades :")
        if typ == 'etf':
            code = input("What Is The Code? https://markets.ft.com/data/etfs/tearsheet/summary?s= :")
        if typ == 'share':
            code = input("What Is The Code? https://markets.ft.com/data/equities/tearsheet/summary?s= :")
        if typ == 'cash':
            code = None
        else:
            print("Invalid")
            break
        qty = input("How Many? :")
        pp = input("Pounds Or Pence? (£/p) :")
        if pp == 'p':
                    qty= round(qty*(100)**(-1),2)
        else:
            print("Invalid")
            break
        name = input("Name It :")
        
        funds[name]={"code": code, "shareqty":qty, "type": typ, 'shareprice':1}
        
    if AR == 'U':
        name = input("Which One? :")
        field = input("Update What? :")
        value = input("Value :")
        funds[name][field]= value
    else:
        print("Invalid")
        break
    done = input("Anything Else? (Y/N):")
    if done == 'N':
            break
print("Done")

if EM == 'E':       
    with open("/home/pi/pythonbotProject1/fundinfo.txt",'w') as file:
            json.dump(funds,file)
if EM == 'M':
    with open("/home/pi/pythonbotProjectM/fundinfo.txt",'w') as file:
            json.dump(funds,file) 

quit()
                    
    
        



