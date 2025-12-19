import time
import json
import random

currentUser = ""
points = 0
level = 0
xp=0
unlocked = set()
"""
Study Buddy Guide
Answer questions to earn buddy points
Trade buddy points for cosmetics

There are two buyable cosmetics:
  v        (Head gear cosmetic)
[•‿•]      (Face expression cosmetic)
 /^\

Points and cosmetics get saved to your account data
Create your own quiz, or modify an existing quiz!
"""

"""
Test Functions At The Bottom!
"""

def clear():
  """
  Gives a screen clear effect by printing a bunch of new lines
  """
  print('\n'*25)

def pressEnter(msg = "To Continue"):
  """
  Prompt the user to press enter
  """
  input(f"[Press Enter {msg}]")

def prompt(msg, choices):
  """
  Prompts the user with input validation
  """
  choices = choices.split(',')
  print(msg)
  for c in choices:
    print(f"> {c}")
  response = input("Your input: ")
  for c in choices:
    if c.lower() == response.lower():
      return c

  print("Invalid Response")
  pressEnter()
  clear()
  print(','.join(choices))
  return prompt(msg, ','.join(choices))

def wakePrint(animation):
  """
  Wake up animation
  """
  sleepy = ".  z  Z"
  temp = 3
  for a in animation:
    print("     " + sleepy[:temp])
    temp+=3
    if temp == 12:
      temp = 0
    print(" __           __")
    print("|               | ") 
    print(a)
    print("|__           __|")
    time.sleep(0.75)
    clear()
animation = [
  "|   __     __   |",
  "|   ~~     __   |",
  "|   ⬤      __   |",
  "|   ⬤      ~~   |",
  "|   ⬤      ⬤    |" , 
  "|   __     __   |",
  "|   ⬤      ⬤    |"]

def signUp():
  """
  Allows the user to sign up
  Adds new user data to the user.json file
  """
  clear()
  print("~ Study Budy Sign Up ~")
  username = input("Create your username: ")
  password = input("Create your password: ")

  user = {}
  try:# prevent crashout if user.json file doesn't exist
    with open("user.json", 'r') as f:
      try:
        user = json.load(f)
      except:
        user = {} #make user blank if user.json is empty
  except:
    pass
  with open('user.json', 'w') as f:
    user[username] = {
        "password":password,
        "level":1,
        "xp":0,
        "points":0,
        "buddy":{
          "hat":"v",
          "expression":"[•‿•]",
          "item":"",
          "unlocked":[("[•‿•]","Expressions",0),("v","Hats",0)]
        }
      }
    
    json.dump(user, f, indent = 2)
  login()

def login():
  """
  Gets username and password, confirms the account exists, 
  checks the password, then logs the user in
  """
  global currentUser, points, level, unlocked
  clear()
  print("~ Study Buddy Login ~")
  username = input("Enter your username: ")
  password = input("Enter your password: ")

  with open('user.json', 'r') as f:
    try:
      user = json.load(f)
    except:
      user = {}

  if username not in user:
    print("An account under this username doesn't exist!")
    res = prompt("Do you want to sign up instead?", "Login,Sign Up")
    if res == "Sign Up":
      signUp()
    else:
      login()
  else:
    if user[username]["password"] != password:
      print("Incorrect password!")
      pressEnter()
      login()
    else:
      clear()
      print("You have been successfully logged in!")
      currentUser = username
      points = user[username]["points"]
      level = user[username]["level"]
      xp = user[username]["xp"]
      unlocked = set()
      for x in user[username]["buddy"]["unlocked"]:
        unlocked.add(tuple(x))
      # unlocked = set(tuple(user[username]["buddy"]["unlocked"]))
      pressEnter()
      # dashboard()

def updateUser():
  """
  Update user.json with any modified values to store long term
  """
  global currentUser, points, level
  with open('user.json', 'r') as f:
    user = json.load(f)
  with open('user.json', 'w') as f:
    user[currentUser]["points"] = points
    user[currentUser]["level"] = level 
    user[currentUser]["xp"] = xp
    user[currentUser]["buddy"]["unlocked"] = list(unlocked)

    json.dump(user, f, indent = 2)

def printBuddy(item = "none"):
  """
  Prints a buddy with the proper cosmetics
  'Items' can be put defined and held by the buddy
  """
  with open("user.json", 'r') as f:
    user = json.load(f)
    buddy = user[currentUser]["buddy"]
    blanks = (len(buddy["expression"]) - len(buddy["hat"]))//2
    hat = item if item != 'none' else ''
    print(" "*blanks+buddy["hat"] + "  " +hat)
    head = '/' if item != 'none' else ''
    print(buddy["expression"]+head)
    if buddy["item"] == '' and item == 'none':
      print(" /^\\")
    else:
      print(" /^")

def load(course):
  """
  Lodas the questions from a course
  """
  with open('questions.json', 'r') as f:
    data = json.load(f)
    return data[course]
    
def play(course):
  """
  Plays the selected course
  Outputs final statistics
  Update user.json file with gained points
  """
  questions = list(load(course).items())
  random.shuffle(questions)

  stats = {}
  
  for q,info in questions:
    response = promptQuestion(q,info)

    if response.lower() == info['answer'].lower():
      clear()
      print("Correct!")
      if info["unit"] in stats:
        stats[info["unit"]] = [stats[info["unit"]][0]+1, stats[info["unit"]][1]+1]
      else:
        stats[info["unit"]] = [1,1]
      pressEnter()
    else:
      clear()
      print("Not quite. The correct answer is", info["answer"] + "!")
      if info["unit"] in stats:
        stats[info["unit"]] = [stats[info['unit']][0], stats[info['unit']][1]+1]
      else:
        stats[info["unit"]] = [0,1]
      pressEnter()

  clear()
  print("Stats"+"_"*44)
  print(' '*24+'|')

  units = sorted(list(stats))
  accuracy = 0
  for unit in units:
    unitAccuracy = int((stats[unit][0] / stats[unit][1])*100)
    accuracy+=stats[unit][0]
    tempText = f" Unit {unit}: {unitAccuracy}% Accurate" + " "*24
    tempText = tempText[:23]
    print(tempText + ' | ',end = '')
    print("Looking good!" if unitAccuracy >= 80 else "Could use review.")
    print(' '*24 + '|')

  print("_"*24 + '|' + '_'*24)


  gainedPoints = accuracy*100
  gainedXp = accuracy//10
  accuracy = int((accuracy / len(questions))*100)
  print()
  print(f"Overall Accuracy: {accuracy}%")

  print(f"You gained {gainedPoints} Buddy Points!")
  global points, xp 
  xp+=gainedXp 
  points+=gainedPoints
  updateUser()
  print()
  printBuddy("Well Done!")
  print("Want to review your answers? Scroll up to view questions and answers!")
  res = prompt("Choose an action:","Replay,Dashboard")
  if res == "Replay":
    play(course)
  else:
    dashboard()

def promptQuestion(q,info, options=[], randomize = True):
  """
  Prompts quiz questions
  Can either ask FRQ and MCQ questions
  """
  clear()
  print(q)
  options = info['options']
  r = eval(info['randomize'])
  questionType = info['type']
  if questionType == "MCQ":
    if randomize and r: 
      random.shuffle(options)
    print(f"a.{options[0]}{' '*(len(max(options, key = len))+4-len(options[0]))}b.{options[1]}")
    print(f"c.{options[2]}{' '*(len(max(options, key = len))+4-len(options[2]))}d.{options[3]}")
    response = input("Your answer: ")
    if 'a' <= response.lower() <= 'd':
      response = options[ord(response[0])-97]
    else:
      print("Invalid Response")
      pressEnter()
      return promptQuestion(q,info,options, False)
  else:
    response = input("Your answer: ")
  return response
  
def getCosmetics():
  """
  Fetches cosmetics from cosmetics.txt
  Parses then returns it
  """
  costs = []
  lines = [x.strip() for x in open('cosmetics.txt')]
  types = []
  rarities = []
  vals = []

  temp = []
  rarity = False 
  for l in lines:
    if 'Buddy Point' in l:
      t, p = l.split(' - ')
      p = p.split()
      costs.append(int(p[0]))
      types.append(t)
    if l == '':
      rarity = False
      vals.append(temp)
      temp = []
    elif l == l.capitalize() and rarity == False:
      rarity = True 
      rarities.append(l)
    elif l == l.capitalize() and rarity == True:
      temp.append(l)

  d = {}
  t = {}
  i=0
  for e in range(len(types)):
    for j in range(3):
      print(t, vals[i+j])
      t[rarities[i+j]] = vals[i+j]
    i+=3
    d[types[e]] = t 
    d[types[e]]["Cost"] = costs[e]
    t={}
  return d
  
def shop():
  """
  Fetches all cosmetics
  Prompts purchase
  If its purchasable
  Randomly chooses a cosmetic
  Unlocks the cosmetic in user.json
  Subtracts points
  Otherwise can't buy
  """
  global points
  cosmetics = getCosmetics()
  clear()
  print(f"You have {points} buddy points!")
  print(f"There are {len(cosmetics)} available cosmetics:")
  for x in cosmetics:
    print(f"{x} - {cosmetics[x]['Cost']} Buddy Points")
  res = prompt("Which would you like to purchase?", ",".join([x for x in cosmetics])+",Back")
  if res == "Back":
    dashboard() 
  else:
    for x in cosmetics:
      if x == res:
        if points >= cosmetics[x]['Cost']:
          #can be purchased
          yourCosmetic = random.choice(cosmetics[x]['Common'] + cosmetics[x]['Rare'] + cosmetics[x]['Legendary']) #randomly pick rarity
          cosmeticRarity = 2
          if yourCosmetic in cosmetics[x]['Common']:
            cosmeticRarity = 0
          elif yourCosmetic in cosmetics[x]['Rare']:
            cosmeticRarity = 1
          unlocked.add((yourCosmetic,x,cosmeticRarity))
          r = {0:'common', 1:'rare',2:"legendary"}
          print(f"You rolled a {r[cosmeticRarity]} {x[:-1].lower()}: {yourCosmetic}")
          points-=cosmetics[x]['Cost']
          updateUser()
          pressEnter()
          shop()
        else:
          print("That's too expensive for you to afford! Earn more Buddy Points by answering quiz questions!")
          pressEnter()
          shop()

def createQuiz():
  """
  Asks a series of questions that gets put together into a quiz 
  Quiz added to questions.json to be played
  """
  clear()
  quizName = input("Name your quiz: ")
  updateQuestions(promptNewQuestions(), quizName)
  clear()
  print("Your quiz has been created!")
  pressEnter()
  quiz()
  
def promptNewQuestions():
  """
  Will prompt user for a question until the user is a finished
  """
  questions = {}
  questionType = ""
  while True:
    clear()
    res = prompt("Do you want to add a question or finish?", "Add,Finish")
    if res == "Finish":
      break 
    questionName, questionData = actualQuestionPrompt()
    questions[questionName] = questionData
  return questions
    
def actualQuestionPrompt():
  """
  Actually asks the user the question data
  """
  questionData = {}
  clear()
  question = input("Enter the question: ")
  if len(question.split()) == 0:
    print("Question can not be blank!")
    pressEnter()
    actualQuestionPrompt()
  unit = input("What unit is it from: ")
  if unit.isnumeric():
    unit = int(unit)
  else:
    print(f'Unit can not be "{unit}"! Defaulting to 0"')
    unit = 0 
  clear()
  res = prompt("What type of question is this, frq/mcq", "FRQ,MCQ")
  randomize = "False"
  if res == "FRQ":
    questionType = "FRQ"
    options = "none"
    ans = input("Enter the correct answer: ")
    
  else:
    questionType = "MCQ"
    print("Add question options:")
    print("Press enter to leave the option blank")
    options = [""]*4
    print(options)
    for i in range(4):
      options[i] = input(f"Option {i+1}: ")
    t=""
    for index, option in enumerate(options, start=1):
      t += f'{index}. "{option}", '

    randomize = input("Would you like to randomize the options, yes/no: ")
    if 'y' in randomize:
      randomize = "True" 
    else:
      randomize = "False"
    print(t[:-2])
    ans = input("Enter the index of the correct answer: ")
    if ans.isnumeric():
      if 0 < int(ans) <=4:
        ans = int(ans)-1
      else:
        ans=0 
    else:
      ans=0

    ans = options[ans]
    print("Your selected answer was:",ans)
  questionData = {
    "unit":unit,
    "type":questionType,
    "options":options,
    "answer":ans,
    "randomize" : randomize
  }
    
  return question, questionData

def editIndividualQuestions(selectedCourse):
  """
  Allows users to enter index of questions and modify them
  """
  clear()
  course = []
  with open('questions.json', 'r') as f:
    course = json.load(f)

    for index,questionName in enumerate(course[selectedCourse],start=1):
      print(f"{index}. {questionName}")
    res = input("Enter the index of the question you want to edit (enter 'done' to finish): ")
    if res.isnumeric():
      res = int(res)
      if 1 <= res <= len(course[selectedCourse]):
        pass 
      else:
        res = 1
    else:
      modifyQuiz()
    selectedQuestion = list(course[selectedCourse])[res-1]
    print("SELECTED QUESTION:",selectedQuestion)
    questionName, questionData = actualQuestionPrompt()
    questions = course[selectedCourse]
    questions.pop(selectedQuestion)
    questions[questionName] = questionData

    course.pop(selectedCourse)
    course[selectedCourse] = questions 
  with open('questions.json', 'w') as f:
    json.dump(course, f, indent = 2)
    
def updateQuestions(questions,quizName):
  """
  Update questions.json once values have been edited`
  """
  with open("questions.json", 'r') as f:
    try:
      q = json.load(f)
    except:
      q = {}
  with open('questions.json', 'w') as f:
    q[quizName] = questions
    json.dump(q,f,indent=2)
    
def modifyQuiz():
  """
  Prompts courses to modify
  """
  clear()
  with open("questions.json",'r') as f:
    courses = json.load(f)
    c=[]
    for course,_ in list(courses.items()):
      c.append(course)
    res = prompt('Which course do you want to modify?',','.join(c)+",Back")
    if res == "Back":
      quiz() 
    else:
      edit(res,courses)

def edit(selectedCourse, courses):
  """
  Prompts actions in modifying quiz questions
  """
  clear()
  res = prompt('Select from the following actions:', 'Delete,Rename,Edit,Back')
  if res == 'Rename':
    quizName = input("Rename your quiz: ")
    courses[quizName] = courses[selectedCourse]
    courses.pop(selectedCourse)
  elif res == "Back":
    modifyQuiz()
  elif res == "Delete":
    clear()
    if 'y' in input(f'Are you sure you want delete the following quiz: "{selectedCourse}"? \nYour actions can not be undone, yes/no: '):
      courses.pop(selectedCourse)
      clear()
      print(f"{selectedCourse} has been deleted.")
  elif res == "Edit":
    clear()
    res = prompt("Do you want to add or edit existing questions: ", 'Add,Edit')
    if res == "Add":
      q=[]
      with open('questions.json', 'r') as f:
        q = json.load(f)
      # with open('questions.json', 'w'):
        questions = promptNewQuestions()
        q[selectedCourse] = questions | q[selectedCourse]
      with open('questions.json', 'w') as f:
        json.dump(q,f,indent = 2)
      pressEnter()
      modifyQuiz()
    else: 
      editIndividualQuestions(selectedCourse)
      pressEnter()
      editIndividualQuestions(selectedCourse)
  with open("questions.json", 'w') as f:
    json.dump(courses, f, indent=2)
  pressEnter()
  modifyQuiz()
      
def customize():
  """
  Interface for editing cosmetics
  """
  global unlocked, currentUser
  clear()
  print("Lets customize your buddy!")
  printBuddy()
  print("You have the following unlocked:")

  un = sorted(unlocked, key = lambda item: (item[1], item[2]))
  r = {0:"Common", 1:"Rare", 2:"Legendary"}
  temp = []
  for i,cos in enumerate(un, start = 1):
    print(f"{i}. {cos[0]} - {r[cos[2]]} {cos[1][:-1]}")
    temp.append((cos[0],cos[1]))
  print("> Back")

  res = input("Enter the number next to the cosmetic that you want to update to: ")
  if res.lower() == "back":
    dashboard()
  if res.isnumeric() and 0 < int(res) <= len(un):
    res = int(res)
    user = ""
    with open('user.json', 'r') as f:
      user = json.load(f)

    with open('user.json', 'w') as f:
      print(temp[res-1][1], temp[res-1][0])
      user[currentUser]["buddy"][temp[res-1][1][:-1].lower()] = temp[res-1][0]
      json.dump(user, f, indent = 2)
    clear()
    print("Your new buddy!")
    printBuddy()
    res = prompt("Do you want to continue customizing or return to dashboard?","Customize,Dashboard")
    if res == "Customize":
      customize()
    else:
      dashboard()
  else:
    print("Please enter a valid response")
    pressEnter()
    customize()

def dashboard():
  """
  Dashboard interface that leads to everything else
  """
  clear()
  msgs = ["Hello","Welcome","Wassup"]
  printBuddy(f"{random.choice(msgs)}, {currentUser}!")
  res = prompt("What would you like to do today?", "Quiz,Shop,Customize,Log Out")
  if res == "Shop":
    shop()
  elif res == "Customize":
    customize()
  elif res == "Log Out":
    run()
  else:
    clear()
    quiz()
    
def quiz():
  """
  Prompts actions for quizes
  """
  clear()
  res=prompt("Do you want to play, create, or modify a quiz?","Play,Create,Modify,Back")
  if res == "Create":
    createQuiz()
  elif res == "Modify":
    modifyQuiz()
  elif res == "Back":
    dashboard()
  else:
    clear()
    with open('questions.json', 'r') as f:
      courses = json.load(f)
      c=[]
      for course,_ in list(courses.items()):
        c.append(course)
      play(prompt("Which course do you want to practice today?", ','.join(c)))#play the course that they select

def run():
  """
  Plays animation
  Prompts login or sign up
  Leads to the dashboard
  """
  clear()
  wakePrint(animation)
  print(" __           __    Welcome!")
  print("|               |  /")
  print("|   ⬤   U  ⬤    | / ")
  print("|__           __|/")
  pressEnter("To Proceed To Login Page")
  clear()
  res = prompt("Do you want to","Login,Sign Up")
  if res == "Sign Up":
    signUp()
  elif res == "Login":
    login()

  #skip login for now lol
  dashboard()




#Test functions!
run() #starts the whole thing
# print("User selected:",prompt("Pick one","One,Two"))
# play("Computer Science")

# currentUser = "bernie"
# printBuddy("🎉")