import random
from datetime import datetime, timedelta

print("Welcome to MovieMate AI!")

name = input("Enter your name: ")

print("\nChoose Genre:")
print("1. Action")
print("2. Comedy")
print("3. Horror")
print("4. Romance")

choice = int(input("Enter your choice: "))

if choice == 1:
    movies = ["Leo", "Vikram", "Jailer"]
elif choice == 2:
    movies = ["F2", "Jathi Ratnalu", "Mad"]
elif choice == 3:
    movies = ["Kanchana", "Arundhathi", "Masooda"]
elif choice == 4:
    movies = ["Ye Maya Chesave", "Geetha Govindham", "Arya"]
else:
    print("Invalid Choice")
    exit()

print("\nAvailable Movies:")
for i in movies:
    print(i)

movie = input("\nEnter movie: ").lower()

show = ["10:00 AM", "1:00 PM", "4:00 PM", "7:30 PM", "10:00 PM"]
show = input("/nEnter time")

today = datetime.now()
booking_date = today.strftime("%d-%b-%Y")

print("\nBooking Confirmed!")
print("Customer     :", name)
print("Movie        :", movie)
print("Show         :", show)
print("Booking Date :", booking_date)

print("\nEnjoy your movie!")
