
def count_msg(a):
    """to count the messages"""
    print(f'the total length is:{len(a)}')
    
def  unq_user(b):
    """Unique users in chat"""
    s=set()
    for i in b:
        name=i.split(':')[0]
        s.add(name)
    print( f'the unique users are:{s}')


def total_words(c):
    """Total words in the chat"""
    count=0
    for i in c:
        words=i.split(":")[1]
        text=words.split()
        count+=len(text)   
    print(f"the total words :{count}")      

def avg_words(d):
    """Average words for messagae """
    count=0
    for i in d:
        words=i.split(":")[1]
        text=words.split()
        count+=len(text)   
    avg=count/len(d)
    print( f'the average words per msg :{avg}')


def long_msg(e):
    """"Longest messsage sent"""
    long=""
    for i in e:
        text=i.split(':')[1]
        if len(long)<len(text):
            long=i
    print(f'longest msg is:{long}')        
    

def active_user(f):
    """"Most active user"""
    active={}
    for i in f:
        words=i.split(':')[0]
        if words in active:
            active[words]+=1

        else:
            active[words]=1
    print(f'most active user is :{active}')            
        


def msg_count(g):
    """Message count for a specific person""" 
    count=0
    person=input("Enter the specific person name:")
    for i in g:
        name=i.split(':')[0]
        if name==person:
            count+=1
     
    print(f'Message sent by{person}:{count}')           
        

def freq_word(h):
    """""most frequent word used by spcific user"""
    person = input("Enter the user name: ")
    count = {}
    for i in h:
        name, text = i.split(":", 1)
        if name == person:
            words = text.split()
            for word in words:
                if word in count:
                    count[word] += 1
                else:
                    count[word] = 1
    max_word = ""
    max_count = 0
    for word in count:
        if count[word] > max_count:
            max_count = count[word]
            max_word = word
    print(f"Most frequent word used by {person}: {max_word}")

def frstlast_msg(k):
    """First and last message"""
    print(f'the first messgae is {k[0]}')
    print(f'the last message is :{k[-1]}')


def user_present(l):
    """User present in a chat"""
    n=input("Enter the user name:")
    found=False
    for i in l:
        name=i.split(':')[0]
        if n==name:
            found=True
            break
    if found==True:
        print(f'User {n} was found')
    else:
        print(f'User {n} was not found')       



def common_words(m):
    """Common words repteadly"""
    common={}
    for i in m:
        name=i.split(':')[1]
        words=name.split()
        for j in words:
            if j in common:
                common[j]+=1
            else:
                common[j]=1    
    common_word=set()
    for k in common:
        if common[k]>1:
            common_word.add(k)
    print(f'the common word is{common_word}')      

def longavg_msg(n):
    """The user with the longest avg message length"""
    total = {}
    count = {}
    for msg in n:
        name, text = msg.split(":", 1)
        if name not in total:
            total[name] = 0
            count[name] = 0
        total[name] += len(text.split())
        count[name] += 1
    max_user = ""
    max_avg = 0
    for name in total:
        avg = total[name] / count[name]
        if avg > max_avg:
            max_avg = avg
            max_user = name
    print(max_user, "(avg", round(max_avg, 1), "words)")

def mentions(o):
    """ No of Mentions  by specific user"""
    n=input("enter the name of user:")
    count=0
    for i in o:
        text=i.split(':')[1]
        if n.lower() in text.lower():
            count+=1
      
    print(f'Messages mentionings {n}:{count}')            


def rmv_dup(p):
    """Remove duplicates messages"""
    count=set()
    for i in p:
        text=i.split(':')[1]
        count.add(text)
    print(f'unique message count{len(count)}')    


def sort_msg(q):
    """Sort the msgs aplhabatically"""
    msg=sorted(q)
    print("The sorted order is :")
    for i in msg:
        print(i)

def exract_qun(r):
    """Extract the all questions asked"""
    
    for i in r:
        text=i.split(':')[1]
        if "?" in text:
            print(f'messages contain with"?"{i}')
         

def ratio_bw2(s):
    """Reply ratio between two users"""
    usr1=input("Enter the name1:")
    usr2=input("enter the name2:")
    count=0
    for i in s:
        name,text=i.split(':')
        if name==usr1:
            if usr2 in text:
                count+=1

    print(f'the ratio blw {usr1} and {usr2} is :{count} replies')

count=0

def del_themsg(v):
    """To delete the message"""
    global count
    n=input("Enter the message to delete:")
    for i in v:
        text=i.split(':')[0]
        if text==n:
            v.remove(i)
            count+=1
            break
    print(f'the message was deleted:{text}')         
    

def del_msg(t):
    """Deleted messages"""
    global count
    print(f'the deleted count is:{count}')
  