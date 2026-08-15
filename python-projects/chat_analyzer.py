while True:
    try:
        n = int(input("Enter the no of messages:"))
        break
    except ValueError:
        print("Invalid number! Try again")

message = []

for i in range(n):
    msg = input()
    message.append(msg)

print(message)

import chat_utils

while True:
    print("--------------MENU OF ANALYSIS----------------")
    print("1.Count messages\n2.Identify unique users in the chat\n3.Count total words in the chat\n4.Calculate average words per message\n5.Find the longest message sent\n6.Find the most active user\n7.Get message count for a specific user\n8.Find the most frequent word used by a specific user\n9.Retrieve the first and last message by a user\n10.Check if a user is present in the chat\n11.Find commonly repeated words\n12.Identify the user with the longest average message length\n13.Count how many messages mention a specific user\n14.Remove duplicate messages\n15.Sort messages alphabetically\n16.Extract all questions asked in the chat\n17.Calculate the reply ratio between two users\n18.Delete the message\n19.Check for deleted messages\n20.Exit")
    print("-------------------")
    try:
        inp = int(input("Enter the above number to do task:"))
    except ValueError:
        print("Invalid number! Try again")
        continue

    if inp == 20:
        break
    elif inp == 1:
        chat_utils.count_msg(message)
    elif inp == 2:
        chat_utils.unq_user(message)
    elif inp == 3:
        chat_utils.total_words(message)
    elif inp == 4:
        chat_utils.avg_words(message)
    elif inp == 5:
        chat_utils.long_msg(message)
    elif inp == 6:
        chat_utils.active_user(message)
    elif inp == 7:
        chat_utils.msg_count(message)
    elif inp == 8:
        chat_utils.freq_word(message)
    elif inp == 9:
        chat_utils.frstlast_msg(message)
    elif inp == 10:
        chat_utils.user_present(message)
    elif inp == 11:
        chat_utils.common_words(message)
    elif inp == 12:
        chat_utils.longavg_msg(message)
    elif inp == 13:
        chat_utils.mentions(message)
    elif inp == 14:
        chat_utils.rmv_dup(message)
    elif inp == 15:
        chat_utils.sort_msg(message)
    elif inp == 16:
        chat_utils.exract_qun(message)
    elif inp == 17:
        chat_utils.ratio_bw2(message)
    elif inp == 18:
        chat_utils.del_themsg(message)
    elif inp == 19:
        chat_utils.del_msg(message)
