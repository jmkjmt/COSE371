import psycopg2
from flask import Flask, render_template, request

app = Flask(__name__)
connect = psycopg2.connect("dbname=term user=postgres password=whalsrb123")
cur = connect.cursor()

@app.route('/')
def main():
    return render_template("main.html")

@app.route('/return', methods=['post'])
def re_turn():
    whereto=request.form["whereto"]
    if(whereto=="login_success.html"):
        id=request.form['id']
        cur.execute("select subject_name, lecture_name, tutor from enrollment natural join subject group by subject_name, lecture_name, tutor having count(*)=(select count(*) from enrollment natural join subject group by subject_name, lecture_name, tutor order by count(*) desc limit 1);")
        best = cur.fetchall()
        cur.execute("select * from account where id = '{}'".format(id))
        account = cur.fetchall()[0]
        cur.execute("select * from lecture;")
        lectures=cur.fetchall()
        cur.execute("select * from pass_info")
        passinfo=cur.fetchall()
        return render_template(whereto, popular=best, userinfo=account, lectures=lectures, passinfo=passinfo)
    return render_template(whereto)

@app.route('/register', methods=['post'])
def register():
    id = request.form["id"]
    password = request.form["password"]
    send = request.form["send"]
    next_template = ''

    if (send == 'login'):
        cur.execute("SELECT password FROM users WHERE id = '{}' ".format(id))
        result = cur.fetchall()
        if (result == []):
            next_template = "login_fail.html"
        else:
            if (password == result[0][0]):
                cur.execute("select * from account where id = '{}'".format(id))
                account=cur.fetchall()[0]
                cur.execute("select subject_name, lecture_name, tutor from enrollment natural join subject group by subject_name, lecture_name, tutor having count(*)=(select count(*) from enrollment natural join subject group by subject_name, lecture_name, tutor order by count(*) desc limit 1);")
                best=cur.fetchall()
                cur.execute("select * from lecture;")
                lectures=cur.fetchall()
                cur.execute("select * from pass_info")
                passinfo=cur.fetchall()
                next_template = "login_success.html"
                return render_template(next_template, popular=best, userinfo=account,lectures=lectures, passinfo=passinfo)
            else:
                next_template = "login_fail.html"

    elif (send == "sign up"):
        next_template="sign_up.html"

    return render_template(next_template)

@app.route('/signup', methods=['post'])
def signup():
    id=request.form["id"]
    password=request.form["password"]
    role=request.form["role"]


    cur.execute("SELECT id FROM users WHERE id = '{}'".format(id))
    result = cur.fetchall()

    if (result == []):
        cur.execute("INSERT INTO users VALUES ('{}', '{}');".format(id, password))
        cur.execute("insert into account values ('{}', {}, '{}', '{}');".format(id, 10000, 'welcome' , role))
        connect.commit()
        next_template = "signup_success.html"
    else:
        next_template = "ID_collision.html"

    return render_template(next_template);

@app.route('/logout', methods=['post'])
def logout():
    return render_template("main.html")

@app.route('/info',methods=['post'])
def info():
    who=request.form['who_info']
    id=request.form['id']
    if(who=='users info'):
        cur.execute("select * from users natural join account;")
        result = cur.fetchall()
        return render_template("user_info.html", userinfo=result, id=id)
    elif(who=='trades info'):
        cur.execute("select * from enrollment;")
        lec = cur.fetchall()
        cur.execute("select tutee, tutor, price from pass_enroll natural join pass_info;")
        passinfo=cur.fetchall()
        return render_template("trades_info.html", tradeinfo=lec, passinfo=passinfo, id=id)
    elif(who == 'my info'):
        cur.execute("select tutor, price from pass_enroll natural join pass_info where tutee='{}';".format(id))
        passinfo=cur.fetchall()
        cur.execute("select role from account where id='{}';".format(id))
        role=cur.fetchall()[0][0]
        if(role == 'tutee'):
            cur.execute("select subject_name, lecture_name, A.tutor, tutee, price from (lecture natural join subject) as A join enrollment as B on A.name=B.lecture_name and A.code=B.code and A.tutor=B.tutor where tutee='{}';".format(id))
            mylec=cur.fetchall()
            return render_template("view_lecture.html", lecinfo=mylec, id=id, role=role, passinfo=passinfo)
        else:
            cur.execute("select subject_name, name, A.tutor, count(tutee) , price from (lecture natural join subject) as A left outer join enrollment B on A.code=B.code and A.name=B.lecture_name and A.tutor=B.tutor where A.tutor='{}' group by subject_name, name, A.tutor, price;".format(id))
            mylec=cur.fetchall()
            print(mylec)
            cur.execute("select subject_name, lecture_name, tutor, tutee, price from enrollment natural join lecture natural join subject where tutee='{}';".format(id))
            reglec=cur.fetchall()
            return render_template("view_lecture.html", mylec=mylec, reglec=reglec, id=id, role=role, passinfo=passinfo)
    elif(who=='charge info'):
        cur.execute("select * from charge_request;")
        chargeinfo=cur.fetchall()
        return render_template("charge_info.html", id=id, chargeinfo=chargeinfo)

@app.route('/lec_reg', methods=['post'])
def lec_reg():
    code=request.form['code']
    name=request.form['name']
    tutor=request.form['tutor']
    cur.execute("select * from lecture where code='{}' and name='{}' and tutor='{}';".format(code,name,tutor))
    lecture=cur.fetchall()[0]
    id=request.form['id']
    cur.execute("select * from account where id='{}'".format(id))
    userinfo=cur.fetchall()[0]
    cur.execute("select discount from rating_info where rating='{}'".format(userinfo[2]))
    discount=cur.fetchall()[0][0]
    discount=lecture[2]*discount/100
    cur.execute("select * from pass_enroll where tutee='{}' and tutor='{}';".format(id, tutor))
    have_pass=cur.fetchall()
    if(have_pass != []):
        discount=lecture[2]
    return render_template("lec_reg.html",lecture=lecture, userinfo=userinfo, discount=discount, final=int(lecture[2])-discount, have_pass=have_pass)

@app.route('/conf', methods=['post'])
def conf():
    what=request.form['what']
    id=request.form['tutee']
    tutor=request.form['tutor']
    d_price=float(request.form['d_price'])
    if(what=='lec'):
        have_pass=request.form['have_pass']
        name=request.form['name']
        code=request.form['code']
        cur.execute("select * from lecture where code='{}' and name='{}' and tutor='{}';".format(code, name, tutor))
        lecture=cur.fetchall()[0]
        income=lecture[2]
        if(have_pass != []):
            income = 0
        cur.execute("select credit from account where id='{}';".format(id))
        credit=cur.fetchall()[0][0]
        if(credit<d_price):
            return render_template("confirm_fail.html",why='You don\'t have enough money.',id=id)
        if(id==tutor):
            return render_template("confirm_fail.html",why='You are not allowed to take your own course.',id=id)
        cur.execute("select * from enrollment where tutee='{}' and tutor='{}' and code='{}' and lecture_name='{}';".format(id,tutor,code, lecture[1]))
        if(cur.fetchall()!=[]):
            return render_template("confirm_fail.html",why='You cannot apply for a lecture in duplicate.',id=id)
        cur.execute("insert into enrollment values ('{}','{}','{}','{}',{});".format(id,tutor,lecture[0],lecture[1],income))
    else:
        cur.execute("select price from pass_info where tutor='{}';".format(tutor))
        income=cur.fetchall()[0][0]
        cur.execute("select credit from account where id='{}';".format(id))
        credit=cur.fetchall()[0][0]
        if (credit < d_price):
            return render_template("confirm_fail.html", why='You don\'t have enough money.', id=id)
        if (id == tutor):
            return render_template("confirm_fail.html", why='You are not allowed to take your own pass.', id=id)
        cur.execute("select * from pass_enroll where tutee='{}' and tutor='{}';".format(id,tutor))
        if (cur.fetchall() != []):
            return render_template("confirm_fail.html", why='You cannot apply for a pass in duplicate.', id=id)
        cur.execute("insert into pass_enroll values ('{}','{}');".format(tutor,id))

    # 여기부턴 결제 관련
    cur.execute("update account set credit=credit-{} where id='{}';".format(d_price, id))
    cur.execute("update account set credit=credit+{} where id = '{}';".format(income, tutor))
    cur.execute("select condition, rating from rating_info order by condition desc;")
    condition = cur.fetchall()
    cur.execute("select credit from account where id='{}';".format(id))
    tutee_cred = cur.fetchall()[0][0]
    cur.execute("select credit from account where id='{}';".format(tutor))
    tutor_cred = cur.fetchall()[0][0]
    if (tutee_cred >= condition[0][0]):
        tutee_rating = condition[0][1]
    if (tutor_cred >= condition[0][0]):
        tutor_rating = condition[0][1]
    for i in range(0, len(condition) - 1):
        if (tutee_cred < condition[i][0] and tutee_cred >= condition[i + 1][0]):
           tutee_rating = condition[i + 1][1]
        if (tutor_cred < condition[i][0] and tutor_cred >= condition[i + 1][0]):
           tutor_rating = condition[i + 1][1]
    cur.execute("update account set rating='{}' where id='{}'".format(tutee_rating, id))
    cur.execute("update account set rating='{}' where id='{}'".format(tutor_rating, tutor))
    connect.commit()
    return render_template("confirm_success.html", id=id)

@app.route('/add', methods=['post'])
def add():
    id=request.form['id']
    cur.execute("select * from subject;")
    subject=cur.fetchall()
    return render_template("add_lecture.html",id=id,subjects=subject)

@app.route('/add_reg',methods=['post'])
def add_reg():
    id=request.form['id']
    code=request.form['code']
    name=request.form['name']
    price=request.form['price']
    cur.execute("insert into lecture values ('{}','{}',{},'{}');".format(code, name,price, id))
    connect.commit()
    return render_template("add_success.html", id=id)

@app.route('/add_pass',methods=['post'])
def add_pass():
    id=request.form['id']
    return render_template("add_pass.html",id=id)

@app.route('/insert_pass',methods=['post'])
def insert_pass():
    id=request.form['id']
    price=request.form['price']
    cur.execute("insert into pass_info values ('{}','{}');".format(id,price))
    connect.commit()
    return render_template("add_success.html", id=id)


@app.route('/pass_reg',methods=['post'])
def pass_reg():
    tutor=request.form['tutor']
    id=request.form['id']
    cur.execute("select price from pass_info where tutor='{}';".format(tutor))
    income=cur.fetchall()[0][0]
    cur.execute("select * from pass_info where tutor='{}';".format(tutor))
    passinfo=cur.fetchall()[0]
    cur.execute("select * from account where id='{}';".format(id))
    userinfo=cur.fetchall()[0]
    cur.execute("select discount from rating_info where rating='{}'".format(userinfo[2]))
    discount=cur.fetchall()[0][0]
    discount=income*discount/100
    return render_template("pass_reg.html",userinfo=userinfo, passinfo=passinfo,discount=discount, final=int(income)-discount)

@app.route('/charge',methods=['post'])
def charge():
    id=request.form['id']
    cur.execute("select * from account where id='{}';".format(id))
    userinfo=cur.fetchall()[0]
    return render_template("charge.html", userinfo=userinfo)

@app.route('/money_charge_request',methods=['post'])
def money_charge_request():
    id = request.form['id']
    money = request.form['money']
    cur.execute("insert into charge_request values ('{}', {})".format(id,money))
    connect.commit()
    return render_template("request_success.html", id=id)

@app.route('/charge_confirm',methods=['post'])
def charge_confirm():
    id=request.form['id']
    money=request.form['money']
    cur.execute("update account set credit=credit+{} where id='{}';".format(money, id))
    cur.execute("select condition, rating from rating_info order by condition desc;")
    condition = cur.fetchall()
    cur.execute("select credit from account where id='{}';".format(id))
    cred = cur.fetchall()[0][0]
    if (cred >= condition[0][0]):
        rating = condition[0][1]
    for i in range(0, len(condition) - 1):
        if (cred < condition[i][0] and cred >= condition[i + 1][0]):
            rating = condition[i + 1][1]
    cur.execute("update account set rating='{}' where id='{}'".format(rating, id))
    cur.execute("delete from charge_request where id='{}' and money='{}'".format(id,money))
    connect.commit()
    cur.execute("select * from charge_request;")
    chargeinfo=cur.fetchall()
    return render_template("charge_info.html",id=id,chargeinfo=chargeinfo)


if __name__ == '__main__':
   app.run()
