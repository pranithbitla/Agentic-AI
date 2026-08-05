print("Welcome")
balance=10000
attempt=0
pin=1234
transcations=[]
while attempt<3:
    user_pin=int(input("Enter the pin:"))
    if user_pin==pin:
       while True:
        print("Choose the option:")
        print("1.Check Balance\n2.Deposit\n3.Withdraw\n4.Ministatement\n5.Change PIN\n6.Exit")
        inp1=int(input("Enter what to do now:"))
        if inp1==6:
          print("Thank you for Using ATM")
          break
        elif inp1==1:
          print(balance)
          
        elif inp1==2:
          deposit=int(input("Enter the Amount to deposit:"))
          balance+=deposit
          transcations.append(f"Despisted ${deposit}")
          print(f"Updated balance:{balance}")
          
        elif inp1==3:
          withdraw=int(input("Enter amount to withdraw:"))
          if withdraw<=balance:
            balance-=withdraw
            transcations.append(f"Withdawn amount ${withdraw}")
            print(f"Transaction Succesful! the balance amount:{balance}")
            
        elif inp1==4:
          print("\n-------------Mini Statement-----------------")
          if len(transcations)==-1:
             print("No trancations found!")
             
          else: 
             for i in range(len(transcations)):
                print(f"{i+1}.{transcations[i]}")
        elif inp1==5:
           pin2=int(input("Enter Current pin:"))
           if pin==pin2:
              new_pin=int(input("Enter the New PIN:"))
              pin=new_pin
              print("PIN changed Succesfully")
              print(f"The New pin was{new_pin}")
           else:
              print("Wrong PIN")   
          
    else:
        attempt+=1
        print("Wrong PIN")
if attempt==3:
    print("Card blocked")    