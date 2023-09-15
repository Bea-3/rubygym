import json
from flask import Flask,request,session,jsonify
from datetime import datetime
from sqlalchemy import or_
from werkzeug.security import generate_password_hash,check_password_hash

#import local files
from rubygymapp import app,db
from rubygymapp.models import Client,Emergency_contact

@app.route('/')
def homme():
    return "home, please use the URL"

@app.route('/api/adduser', methods=['POST'])
def adduser():
    data = request.get_json()

    pwd_hash = generate_password_hash(data['password'])

    fname = data['first_name']
    lname = data['last_name']
    phone = data['phone']
    add = data['address']
    email = data['email']
    pwd = pwd_hash
    sub = data['subscription']
    prog = data['program']
    #emergency contact info
    firstname = data['emergency_contact_first_name']
    lastname = data['emergency_contact_last_name']
    pnum = data['emergency_contact_phone']
    address = data['emergency_contact_address']


    newuser = Client(client_fname=fname, client_lname=lname, client_phone=phone, client_address=add, client_email=email, client_pwd=pwd,client_subscription=sub, program=prog )
    db.session.add(newuser)
    db.session.commit()
    #saving clientid as the session id
    userid = newuser.client_id
    session['user']=userid
    #populating the emergency contact table
    edata = Emergency_contact(em_fname = firstname, em_lname= lastname, em_phonenum = pnum, em_address = address, clientID=session['user'])
    db.session.add(edata)
    db.session.commit()

    return jsonify({'message' : 'New user created'})



#fetch all users
@app.route('/api/users', methods=['GET'])
def get_all_users():
    allusers = Client.query.join(Emergency_contact).add_columns(Emergency_contact).all()

    output =[]

    for user, info in allusers:
        user_data = {}
        user_data['id'] = user.client_id
        user_data['first_name'] = user.client_fname
        user_data['last_name'] = user.client_lname
        user_data['phone'] = user.client_phone
        user_data['address'] = user.client_address
        user_data['email'] = user.client_email
        user_data['password'] = user.client_pwd
        user_data['subscription'] = user.client_subscription
        user_data['program'] = user.program
        user_data['emergency_contact_first_name'] = info.em_fname
        user_data['emergency_contact_last_name'] = info.em_lname
        user_data['emergency_contact_phone'] = info.em_phonenum
        user_data['emergency_contact_address'] = info.em_address
        output.append(user_data)
    
    return jsonify({'users' : output})


#retrieve db info and display as json
@app.route('/api/user/<user_id>', methods=['GET'])
def fetchuser(user_id):
    # data = Client.query.join(Emergency_contact).add_columns(Emergency_contact).filter(or_(Client.client_id==info,Client.client_fname==info,Client.client_lname==info)).all()
    data = Client.query.join(Emergency_contact).add_columns(Emergency_contact).filter(Client.client_id==user_id).all()

    if not data:
        return jsonify({'message' : 'No user found!'})
    else:      
        user_data = [{
            'id': x.client_id, 
            'first_name': x.client_fname, 
            'last_name': x.client_lname,
            'phone': x.client_phone,
            'address': x.client_address,
            'email': x.client_email,
            'password': x.client_pwd,
            'subscription': x.client_subscription,
            'program': x.program,
            'emergency_contact_first_name': y.em_fname,
            'emergency_contact_last_name': y.em_lname,
            'emergency_contact_phone': y.em_phonenum,
            'emergency_contact_address': y.em_address,
            } for x,y in data ]
        return json.dumps(user_data, indent=4)
    
#update client information
@app.route('/api/update/<userid>', methods = ["PUT"])
def updateuser(userid):
    #query client table, where the id is userid and check if id exists
    getuser = Client.query.filter(Client.client_id==userid).first()
    
    if not getuser:
        return jsonify({'message' : 'No user found!'})
    else:
        data = request.get_json()        

        add = data['address']
        sub = data['subscription']
        prog = data['program']
        em_fname = data['emergency_contact_first_name']
        em_lname = data['emergency_contact_last_name']
        em_phone = data['emergency_contact_phone']
        em_add = data['emergency_contact_address']
        if add != '' and sub != '' and prog != '' and em_fname != '' and em_lname and em_phone and em_add != '' :
            #query an object of EmergencyContact and Client ,get id, assign attributes, commit
            cobj = db.session.query(Client).get(userid)
            cobj.client_address = add
            cobj.client_subscription = sub
            cobj.program = prog
            cobj.emergency_det.em_fname = em_fname
            cobj.emergency_det.em_lname = em_lname
            cobj.emergency_det.em_phonenum = em_phone
            cobj.emergency_det.em_address = em_add
            db.session.commit()
            return jsonify({'message' : 'User Information Updated'})
        else:
            return jsonify({'message' : 'Please supply information'})


#delete a client and all information will be deleted
@app.route('/api/delete/<userid>', methods = ["DELETE"])
def deleteuser(userid):
    getuser = Client.query.filter(Client.client_id==userid).first()
    if not getuser:
        return jsonify({'message' : 'No user found!'})
    else:
        #retrieve client id and delete
        # user = Client.query.get_or_404(userid)
        db.session.delete(getuser)    
        db.session.commit()
        return jsonify({'message' : 'User has been deleted'})
        