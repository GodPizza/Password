import random
import time


def optionsmenu(name):
  print("")
  print("Options:")
  print("1-Play")
  print("2-See your best games")
  print("3-Score leaders")
  print("")

  sel = input()
  valid = ["1", "2", "3"]

  while sel not in valid:
    print("Type a valid option")
    sel = input()

  if str(sel) == "1":
    return

  if sel == "2":
    getuserscore(name)
    print("")
    optionsmenu(name)

  if sel == "3":
    scoreleadertable()
    print("")
    optionsmenu(name)


#/////////////////////////////////////////////////////////
def scoreleadertable():
  scores = []
  with open("records_table.txt", "r") as f:
    for line in f:
      if line.startswith("$"):
        name_end_index = line.find("$", 1)
        if name_end_index != -1:
          name = line[1:name_end_index]
          score_start_index = line.find("=", name_end_index)
          if score_start_index != -1:
            score_str = line[score_start_index + 1:].strip()
            score = int(score_str)
            scores.append((name, score))

  if scores:
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)[:10]
    print("The top scores are:")
    for i, (name, score) in enumerate(sorted_scores, start=1):
      print(f"{i}. {name}: {score}")

    return sorted_scores
  else:
    print("No records found.")
    return []


#/////////////////////////////////////////////////////////
def getuserscore(name):
  scores = []
  username = "$" + name + "$"
  with open("records_table.txt", "r") as f:
    for line in f:
      if username in line:
        score = int(line.split("=")[-1].strip())
        scores.append(score)

  if scores:
    sorted_scores = sorted(scores, reverse=True)[:3]
    print(f"The three highest scores for {name} are:")
    for i, score in enumerate(sorted_scores, start=1):
      print(f"{i}. {score}")
  else:
    print(f"No records found for '{name}'.")


#/////////////////////////////////////////////////////////
def writerecord(name, attemps, clock_start):
  f = open("records_table.txt", "a")

  score = (10000 / (attemps)) - time_calculation(clock_start)
  record = "$" + name + "$" + str(attemps) + "/" + str(
      time_calculation(clock_start)) + "=" + str(int(score))
  f.write(record + "\n")
  f.close()


#/////////////////////////////////////////////////////////
def time_calculation(clock_start):

  final_time = int(time.time() - clock_start)

  return final_time


#/////////////////////////////////////////////////////////
def password_creator():  #create a random number with 4

  a = ""
  b = ""
  c = ""
  d = ""

  while a == b or a == c or a == d or b == c or b == d or c == d:
    a = str(random.randint(1, 9))

    b = str(random.randint(1, 9))

    c = str(random.randint(1, 9))

    d = str(random.randint(1, 9))

  return a + b + c + d


#/////////////////////////////////////////////////////////
def check_password(numb, password):  #check password for the game

  correct_pos = 0
  correct_num = 0

  for i in numb:
    for c in password:
      if i == c:
        correct_num += 1
        if numb.index(i) == password.index(c):
          correct_pos += 1

  return correct_num, correct_pos


#/////////////////////////////////////////////////////////
def valid_numb(numb):  #check the number input
  list = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]  #list of valid digits

  no_repeat = True
  in_range = True
  correct_len = True

  if len(numb) != 4:  #check the lenght of the number ==4
    correct_len = False
    print("Enter a 4 digit number")
    print("")
    return False

  else:
    correct_len = True

  for i in numb:
    if i in list:  #check the digits range 1-9
      in_range = True
    else:
      print(i, "is not a number between 1 and 9")
      print("")
      in_range = False
      return False

  temp = []  #check if the digits are repeated
  for i in numb:
    if i not in temp:
      no_repeat = True
      temp.append(i)

    else:
      no_repeat = False
      print(i, "it's repeated!")
      print("")
      return False

  return no_repeat and in_range and correct_len


#/////////////////////////////////////////////////////////
def game():
  print("Welcome to Guess The Password")
  print("""The rules are simple:
  -You will have to guess the four-digit password six times.
  -The digits will be between 1 and 9
  -There are no repeated numbers in the password
  -After each attempt the program will give you how many numbers are correct and how many are in the correct position.
  """)
  print("Good luck")
  print("")
  print("First enter your name(It will be saved in the records table)")

  user_name = input()

  optionsmenu(user_name)

  print("Now try to guess the password")

  correct_password = password_creator()  #storage the correct password

  clock_start = time.time()  #start clock
  attempts = 5  #number of attemps
  user_number = input()  #user guess

  while user_number != correct_password and attempts != 1:
    while valid_numb(
        user_number) == False:  #Try again loop since a correct number
      print("Try again")
      user_number = input()

    attempts -= 1  #attemp counter
    hint = check_password(user_number,
                          correct_password)  #Check Password for game

    print("You have:")
    print(hint[0], "correct number(s).")
    print(hint[1], "in position")
    print("And", attempts, "attemp(s)")
    print("")
    user_number = input()

  if attempts == 1:
    print("")
    print("0 attemps left, the password was", correct_password)
    print("----------YOU LOSE!----------")
  else:
    print("")
    print(correct_password, "You got it in", 6 - attempts, "attemp(s)")
    print("----------CONGRATS!----------")
    writerecord(user_name, 6 - attempts, clock_start)

  print("")
  print("")
  print("")


#Game
game()
