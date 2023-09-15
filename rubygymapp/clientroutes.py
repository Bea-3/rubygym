import json
from flask import Flask,request,session,jsonify
from datetime import datetime
from sqlalchemy import or_


#import local files
from rubygymapp import app,db
from rubygymapp.models import Client,Emergency_contact

@app.route('/')
def homme():
    return "home, please use the URL"

@app.route('/user')
def user():
    fname = "Lizzy"
    lname = "Asa"
    phone = "08123456789"
    add = "16 Gimpo lagos"
    email = "lizzy@asa.com"
    pwd = "liz123"
    sub = "3 months"
    prog = "self"
    #emergency contact info
    firstname = "Jude"
    lastname ="Miracle"
    pnum = "08234567890"
    address = "50 orange town ikeja"


    cdata = Client(client_fname=fname, client_lname=lname, client_phone=phone, client_address=add, client_email=email, client_pwd=pwd,client_subscription=sub, program=prog )
    db.session.add(cdata)
    db.session.commit()
    #saving clientid as the session id
    userid = cdata.client_id
    session['user']=userid
    #populating the emergency contact table
    edata = Emergency_contact(em_fname = firstname, em_lname= lastname, em_phonenum = pnum, em_address = address, clientID=session['user'])
    db.session.add(edata)
    db.session.commit()
    return "done inserting"

#delete a client and all information will be deleted
@app.route('/delete/api/<userid>')
def deleteuser(userid):
    userid = session.get('user')
    if userid == None:
        return "no session detected"
    else:
        #retrieve client id and delete
        getuser = Client.query.get_or_404(userid)
        db.session.delete(getuser)    
        db.session.commit()
        return "user"
    
#retrieve db info and display as json
@app.route('/fetch/api/<info>')
def fetchuser(info):
    data = Client.query.join(Emergency_contact).add_columns(Emergency_contact).filter(or_(Client.client_id==info,Client.client_fname==info,Client.client_lname==info)).all()
    user_data = [{
        'id': x.client_id, 
        'first_name': x.client_fname, 
        'last_name': x.client_lname,
        'phone': x.client_phone,
        'address': x.client_address,
        'email': x.client_email,
        'subscription': x.client_subscription,
        'program': x.program,
        'emergency_contact_first_name': y.em_fname,
        'emergency_contact_last_name': y.em_lname,
        'emergency_contact_phone': y.em_phonenum,
        'emergency_contact_address': y.em_address,
        } for x,y in data ]
    return json.dumps(user_data, indent=4)
    
#update client information
@app.route('/update/api/<userid>')
def updateuser(userid):
    userid = session.get('user')
    if userid ==None:
        return "no session detected"
    else:
        #query client table, where the id is userid and update any information
        add = request.args.get('client_address')
        email = request.args.get('client_email')
        pwd = request.args.get('client_pwd')
        sub = request.args.get('client_subscription')
        prog = request.args.get('program')
        em_fname = request.args.get('em_fname')
        em_lname = request.args.get('em_lname')
        em_phone = request.args.get('em_phonenum')
        em_add = request.args.get('em_address')
        if add != '' and email != '' and pwd != '' and sub != '' and prog != '' and em_fname != '' and em_lname and em_phone and em_add != '' :
            #query an object of EmergencyContact and Client ,get id, assign attributes, commit
            cobj = db.session.query(Client).get(userid)
            cobj.client_address = add
            cobj.client_email = email
            cobj.client_pwd = pwd
            cobj.client_subscription = sub
            cobj.program = prog
            cobj.emergency_det.em_fname = em_fname
            cobj.emergency_det.em_lname = em_lname
            cobj.emergency_det.em_phonenum = em_phone
            cobj.emergency_det.em_address = em_add
            db.session.commit()
            return "updated"
        else:
            return "please supply information"



        