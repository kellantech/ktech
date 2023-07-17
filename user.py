class user:
  def __init__(self,name,id,passwd,pn,em,ispaid=0,):
    self.name = name
    self.id = id
    self.ispaid = ispaid
    self.phone = pn
    self.email = em
    self.password = passwd
  def __str__(self):
    return f"""-------------------------------------
name: {self.name}
id: {self.id}
ispaid: {self.ispaid == 1}
email: {self.email}
phone number: {self.phone}
-------------------------------------
"""