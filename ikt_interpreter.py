import random
import webbrowser
import time
import requests

class Interpreter:
    def __init__(self, filename):
        self.filename = filename
        self.state = {}

    def read_file(self):
        with open(self.filename, 'r') as file:
            content = file.read()
        return content
                
    def locate_prof(self):
        link = "link"
        locations = [
            "Last Seen \033[31mNOT\033[0m at Ellen Ochoa Pavillion on 2024-12-05 18:50",
            link, "Mining for Super A's", "Googleplex", "Getting spam Emails from students", 
            "Writing a 100 question final.", "32.7764° N, 117.0719° W", link
        ]
        rand_loc = random.choice(locations)

        if rand_loc == "link":
            url = ["https://www.tiktok.com/@randomspamvideos25/video/7251387037834595630?lang=ent"]
            rand_link = random.choice(url)
            webbrowser.open(rand_link)  
        else:
            for char in rand_loc:
                print(char, end='')
                time.sleep(0.07) 
            print()

    def interpret(self, string):

        def varmap(var):
            return self.state.get(var, None)

        def evaluator(expression):
            output = []
            operators = []
            i = 0

            def precedence(op):
                if op in '+-':
                    return 1
                elif op in '*/%':
                    return 2

            def operator_eval(op):
                right = output.pop()
                left = output.pop()
                if op == '+':
                    output.append(left + right)
                elif op == '-':
                    output.append(left - right)
                elif op == '*':
                    output.append(left * right)
                elif op == '/':
                    output.append(left / right)
                elif op == '%':
                    output.append(left % right)

            while i < len(expression):
                char = expression[i]

                if char == "\"":    #String val's
                    string_val = ''
                    i += 1
                    while i < len(expression) and expression[i] != "\"":
                        string_val += expression[i]
                        i += 1
                    output.append(string_val)
                    continue
                
                if char in 'abcdefghijklmnopqrstuvwxyz':
                    var_name = ''
                    while i < len(expression) and (expression[i] in 'abcdefghijklmnopqrstuvwxyz' or expression[i].isdigit()):
                        var_name += expression[i]
                        i += 1
                    output.append(self.state.get(var_name, 0))  # Access the instance's state
                    continue

                if char.isdigit() or (char == '.' and i + 1 < len(expression) and expression[i + 1].isdigit()): #continue building until end of num
                    num = ''  #build float using num variable
                    while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                        num += expression[i]
                        i += 1
                    output.append(float(num))
                    continue

                # Handling operators
                if char in "+-*/%":
                    while (operators and precedence(operators[-1]) >= precedence(char)):
                        operator_eval(operators.pop())
                    operators.append(char)
                i += 1

            while operators:
                operator_eval(operators.pop())
            return output[0] if output else 0

        def condition_eval(condition):
            ans = False
            condition = condition.strip()

            if "ALPHA" in condition:
                left, right = condition.split("ALPHA", 1)
                ans = condition_eval(left) and condition_eval(right)
            elif "OMEGA" in condition:
                left, right = condition.split("OMEGA", 1)
                ans = condition_eval(left) or condition_eval(right)
            elif "==" in condition:
                left, right = condition.split("==", 1)
                left_val = self.state.get(left, evaluator(left))
                right_val = self.state.get(right, evaluator(right))
                ans = float(left_val) == float(right_val)
            elif "!=" in condition:
                left, right = condition.split("!=", 1)
                left_val = self.state.get(left, evaluator(left))
                right_val = self.state.get(right, evaluator(right))
                ans = float(left_val) != float(right_val)
            elif ">" in condition:
                left, right = condition.split(">", 1)
                left_val = self.state.get(left, evaluator(left))
                right_val = self.state.get(right, evaluator(right))
                ans = float(left_val) > float(right_val)
            elif "<" in condition:
                left, right = condition.split("<", 1)
                left_val = self.state.get(left, evaluator(left))
                right_val = self.state.get(right), evaluator(right)
                ans = float(left_val) < float(right_val)
            return ans

        stmts = string.strip().split('\n')
        i = 0
        
        while i < len(stmts):
            stmt = stmts[i]

            if'Infect' in stmt:
                stmt = stmt.replace("Infect", "").strip()   #eradicate "Infect" but keep rest stmt
                recipient, number = stmt.split(":")
                number, msg = number.split(',')
                
                number = number.strip()

                if len(number) == 10:
                    resp = requests.post('https://textbelt.com/text', {
                    'phone': number,
                    'message': 'Hello, ' + recipient + '. ' + msg,
                    'key': '2e323455d3ca12b3c04d4e71e4ed72d8b338d7cf8uZRSYQABgKYEWALqlanGa9al_test', #append '_test' to not use up texts but test if functional
                    })
                    print(resp.json()) 
                    print('Successfully infected ' + recipient + ' at ' + number)
                else:
                    print("INVALID_PHONE#...REPORTING USER TO AUTHORITIES")
                    break

            if 'encrypt' in stmt: 
                stmt = stmt.replace("encrypt", "").strip()
                var_name, expression = stmt.split(":")
                var_val = evaluator(expression.strip())
                self.state[var_name.strip()] = var_val  # Assign to instance's state
                #print(f"{var_name.strip()} = {var_val}")  # DEBUG

            elif 'initiate_protocol' in stmt:  # Print
                stmt = stmt.replace("initiate_protocol", "").strip()
                if "\"" in stmt:
                    print(stmt.split("\"")[1])
                else:
                    value = varmap(stmt.strip())
                    if value is not None:
                        print(f"Echo {value}")
                    else:
                        print(stmt.strip() + " unverified.")

            elif 'Execute_confirmation_sequence' in stmt:  # If
                stmt = stmt.replace("Execute_confirmation_sequence", "").strip()  
                condition = stmt.strip()  

                if condition_eval(condition):  # If condition is true
                    i += 1

                    print("ACCESS_GRANTED")
                    time.sleep(0.3)

                    while i < len(stmts) and not stmts[i].strip().startswith("Hack_complete"):  
                        self.interpret(stmts[i].strip())  
                        i += 1  
                else:  #bypass
                    user_input = input(f"Error 10011100011010101 : RESTRICTED_INFORMATION ")
                    if user_input == "bypass":  # If bypass is triggered
                        print("Access Granted. Now initiating reflection sequence...")  
                        i += 1
                        time.sleep(0.3)

                        while i < len(stmts) and not stmts[i].strip().startswith("Hack_complete"):  #output !true block
                            self.interpret(stmts[i].strip())  
                            i += 1  
                    else:  # Skip block if not bypassed
                        print("ACCESS_DENIED")  
                        while i < len(stmts) and not stmts[i].strip().startswith("Hack_complete"): 
                            i += 1 

            elif 'locate_Dabish' in stmt:  #I waited an hour in office hours but he cancelled wed classes
                while True:
                    user_input = input("ENTER GEOLOCATOR: ")
                    
                    if user_input == "exit_sequence":
                        print("GEOLOCATOR TERMINATED \n")
                        break
                    elif user_input == "pinpoint_location":
                        self.locate_prof()  #locations
                    else:
                        print("ACCESS_DENIED... ACCESSING USER LOCATION")
                        break

            elif 'override_mainframe' in stmt:  #keyboard spam 30 chars to open link
                user_input = input("ENTER KEY: ")
                
                if len(user_input) >= 30:
                    print("Access granted. Opening super secret environment...")
                    time.sleep(2)
                    webbrowser.open("https://geekprank.com/hacker/")    
                else:
                    print("ACCESS_DENIED.")

            i += 1        
            
interpreter = Interpreter('locate_Dabish.ikt')
file = interpreter.read_file()
interpreter.interpret(file)
