from flask import \
Flask,render_template,request,make_response

from kellanb_cryptography import hash
import user,send,pickle


phone = "4076769053"
admin_password = "6f7d59b8d218b73c1ad1a0ae9a6d85bd2a2f122ed1824311067cb59b4340eb6f"
home_btn = '''
<br>
<a href="/">home</a>
'''

app = Flask(__name__,static_folder='./static',)
try:
  with open("users.pickle",'rb') as lpf:
    users= pickle.load(lpf)
except FileNotFoundError:
  users = {}

def val(id,pwd):
  usr = users[id]
  return (pwd == usr.password)
  

  
@app.route("/")
def index():
  u = request.cookies.get("UID")
  if u == None or u == "":
    return render_template("index_nologin.html",uid=u)
    
  else:
    if val(u,request.cookies.get("phash")):
      return render_template("index_login.html",uid=u,name=users[u].name)
    else:
      return render_template("index_nologin.html",uid=u)


@app.route("/pay")
def pay():
  u = request.args.get("UID")
  p = request.args.get("pwd")
  if hash.sha256(p) == admin_password:
    user = users[u]
    user.ispaid=1
    with open("users.pickle",'wb') as pf2:
      pickle.dump(users,pf2)
    return ""
  return f"access denied {home_btn}"
@app.route("/unpay")
def unpay():
  u = request.args.get("UID")
  p = request.args.get("pwd")
  if hash.sha256(p) == admin_password:
    user = users[u]
    user.ispaid=0
    with open("users.pickle",'wb') as pf2:
      pickle.dump(users,pf2)
    return ""
  return f"access denied {home_btn}"


@app.route("/login")
def login():
  return render_template("login.html")

@app.route("/login_internal")
def loginint():
  uid = request.args.get("uid")
  pwd = request.args.get("pwd")
  try: _ = users[uid]
  except KeyError:
    return f"invalad id {home_btn}"
  res = make_response(f'logged in! {home_btn}')
  res.set_cookie("UID", value=uid)
  res.set_cookie("phash", value=hash.sha256(pwd))
  
  return res
  
@app.route("/logout")
def logout():
  return render_template("logout.html")




@app.route('/issue')
def issue():
  uid = request.cookies.get("UID")
  
  if uid == None or uid == "":
      return f"you need to login {home_btn}"
    
  if users[uid].ispaid == 1:
    if val(uid,request.cookies.get("phash")):
      return render_template("issue.html",name=users[uid].name)
    else: 
      return 'access denied'
  else:
      return f'You need to pay!!!!!!!!{home_btn}'
  
    

@app.route('/issue-internal')
def isint():
  des= request.args.get("desc")
  name=users[request.cookies.get("UID")].name
  p=users[request.cookies.get("UID")].phone
  print(f"{name}\n{des}\n\n")
  send.send_message('4076769053',f"""
name: {name}
problem: {des}
phone #: {p}
  """)
  return render_template("issue_responce.html")



@app.route("/signup")
def signup():
  return render_template("signup.html")


@app.route("/signup-int")
def signup_int():
  name = request.args.get("name")
  phn = request.args.get("phn")
  eml = request.args.get("eml")
  pwd = hash.sha256(request.args.get("pwd"))
  
  id = name
  users[id] = user.user(name,id,pwd,phn,eml)
  
  with open("users.pickle",'wb') as pf:
    pickle.dump(users,pf)
  send.send_message("4076769053",f"""
new user!
name: {name}
phone number:{phn}
email:{eml}
""")
  return home_btn 

@app.route("/veiw")
def veiw():
  s = ""
  pwd = request.args.get("pwd")
  if hash.sha256(pwd) != admin_password:
    return "access denied"
  for _,v in users.items():
    s += str(v).replace("\n","<br>")
  return s
app.run(host='0.0.0.0', port=81)
