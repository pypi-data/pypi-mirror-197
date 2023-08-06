import json
import os
def append_new_data(filename , your_data):
    if os.path.exists(filename):
        print('ok')
    else:
        with open(filename , 'w') as w:
            w.write('[]')

    with open(filename) as f:
        data = json.load(f)

    data.append(your_data)
    with open(filename, 'w') as f:
        json.dump(data, f,indent=2)

    f.close()


def update_data(filename , reference , matching_text , update_reference , update_text):
    with open(filename, "r") as file:
        data = json.load(file)
        # Find the person named "John"
    person = [p for p in data if p[reference] == matching_text][0]
    person[update_reference] = update_text
    with open(filename, "w") as file:
        json.dump(data, file,indent=2)


def login_check(filename , username , password):
    with open(filename , "r") as file:
        data = json.load(file)
    username_check = [p for p in data if p["username"] == username]
    password_check = [p for p in data if p["password"] == password]
    
    if username_check and password_check:
        status = 'ok'
    else:
        status = "notok"
    return status
    
def signup_validator(filename , username , email):
    with open(filename , "r") as file:
        data = json.load(file)
    username_check = [p for p in data if p["username"] == username]
    email_check = [p for p in data if p["email"] == email]
    if username_check:
        status = 'username_already_exist  '
    elif email_check:
        status = "email_already_exist"
    elif "@gmail.com" in email:
        status = "all_ok"
    else:
        status = "only_use_gmail"
    return status


