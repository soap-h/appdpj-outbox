import Member
import Product
import Orderhistory
import shelve
import Question
import Admin
import FeedbackSimpleDB

from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
import datetime
from werkzeug.utils import secure_filename
from FeedbackSimpleDB import add_question
from Question import Question


from forms import CreateMemberForm, CreateProductForm, CreateQuestionForm, CreateLoginForm, CreateCardForm, CreateAdminForm

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'
app.secret_key = 'PKfEKJh0'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    create_login_form = CreateLoginForm(request.form)

    db = shelve.open('database.db', 'r')
    login_list = db["Members"]
    admin_list = db["Admin"]
    if request.method == "POST" and create_login_form.validate():
        email = create_login_form.email.data
        password = create_login_form.password.data
        for member_id, member in login_list.items():
            if member.get_email() == email and member.get_password() == password:
                session['name'] = member.get_first_name() + " " + member.get_last_name()
                session['member_id'] = member_id
                flash("Login successful", "success")
                return redirect(url_for('outbox'))
            else:
                for admin_id, admin in admin_list.items():
                    if admin.get_email() == email and admin.get_password() == password:
                        session['name'] = admin.get_first_name() + " " + admin.get_last_name()
                        session['member_id'] = admin_id
                        session['admin'] = "active"
                        flash("Admin Login successful" , "success")
                        return redirect(url_for('admin'))
        flash("Invalid email or password. Please try again", "error")

    return render_template('login.html', form=create_login_form)

@app.route("/profile")
def profile():
    if "name" in session:
        name = session["name"]
        id = session["member_id"]

        member_dict = {}
        db = shelve.open('database.db', 'r')
        member_dict = db['Members']
        user_info = member_dict[id]
        order_hist = db['OrderHist']
        member_orderhist = []
        for order_id in order_hist:
            if order_hist[order_id].get_name() == name:
                member_orderhist.append(order_hist[order_id])
    return render_template('profile.html', name=name, id=id, user=user_info, history=member_orderhist)

@app.route("/logout")
def logout():
    session.pop('name', None)
    session.pop('member_id', None)
    if 'admin' in session:
        session.pop('admin', None)
    return redirect(url_for('homepage'))

@app.route('/outbox')
def outbox():
    if request.method == 'POST':
        return redirect(url_for('filter_outbox'))
    # Retrieve products from inventory
    inventory_dict = {}
    db_inventory = shelve.open('database.db', 'r')
    inventory_dict = db_inventory['Inventory']
    db_inventory.close()

    categories = set(product.get_category() for product in inventory_dict.values())
    return render_template('outbox.html', outbox_products=inventory_dict.values(), categories = categories)


@app.route('/view_cart')
def view_cart():
    outbox_dict = {}
    db_outbox = shelve.open('database.db', 'r')
    outbox_dict = db_outbox['Outbox']
    db_outbox.close()

    outbox_list = list(outbox_dict.values())
    cart_list = session.get('cart', [])
    return render_template('viewcart.html', count=len(cart_list), outbox_list=outbox_list)


@app.route('/add_to_outbox/<int:product_id>')
def add_to_outbox(product_id):
    inventory_dict = {}
    db_inventory = shelve.open('database.db', 'r')
    inventory_dict = db_inventory['Inventory']
    db_inventory.close()

    selected_product = inventory_dict.get(product_id)

    outbox_dict = {}
    db_outbox = shelve.open('database.db', 'c')
    try:
        outbox_dict = db_outbox['Outbox']
    except:
        print("Error in retrieving products from database.db")

    if 'cart' not in session:
        session['cart'] = []

    session['cart'].append(product_id)
    session.modified = True

    outbox_dict[selected_product.get_product_id()] = selected_product
    db_outbox['Outbox'] = outbox_dict
    db_outbox.close()
    flash("Item successfully added to cart.", "success")
    return redirect(url_for('outbox'))

@app.route('/deleteitem/<int:id>', methods=['POST'])
def delete_cart(id):
    cart_dict = {}
    db = shelve.open('database.db', 'w')
    cart_dict = db['Outbox']
    cart_dict.pop(id)
    db['Outbox'] = cart_dict
    db.close()
    cart_list = session.get('cart', [])
    if id in cart_list:
        cart_list.remove(id)

    session['cart'] = cart_list
    session.modified = True

    return redirect(url_for('view_cart'))




@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart_list = session.get('cart', [])
    if not cart_list:
        flash("Your cart is empty. Add items to your cart before proceeding to checkout.", "warning")
        return redirect(url_for('view_cart'))

    create_card_form = CreateCardForm(request.form)
    db = shelve.open("database.db", "c")
    checkout_dict = {}
    checkout_dict = db['Outbox']

    total_price = sum(float(item.get_price()) for item in checkout_dict.values())
    if request.method == "POST" and create_card_form.validate():
        order_dict = {}
        order_dict = db['OrderHist']
        if 'name' in session:
            id = session['member_id']
            memberdb = db['Members']
            product = []
            for i in checkout_dict:
                product.append(checkout_dict[i].get_name())
            date = datetime.date.today()
            order_hist = Orderhistory.OrderHistory(session['name'], memberdb[id].get_email(),
                                      product, date, memberdb[id].get_phone(),
                                      total_price)
            if len(order_dict) == 0:
                my_key = 1
            else:
                my_key = len(order_dict.keys()) + 1
            order_hist.set_order_id(my_key)
            order_dict[my_key] = order_hist
            db['OrderHist'] = order_dict
            # date.strftime("%d/%m/%y")
        else:
            product = []
            for i in checkout_dict:
                product.append(checkout_dict[i].get_name())
            date = datetime.date.today()
            order_hist = Orderhistory.OrderHistory("Guest", "Null",
                                                   product, date, "Null",
                                                   total_price)
            if len(order_dict) == 0:
                my_key = 1
            else:
                my_key = len(order_dict.keys()) + 1
            order_hist.set_order_id(my_key)
            order_dict[my_key] = order_hist
            db['OrderHist'] = order_dict


        for id in checkout_dict:
            if id in cart_list:
                cart_list.remove(id)

        session['cart'] = cart_list
        session.modified = True

        nothing = {}
        db['Outbox'] = nothing
        db.close()
        return render_template("homepage.html")

    db.close()
    return render_template('checkout.html',
                           cart_items=checkout_dict.values(), total_price=total_price, form=create_card_form)


@app.route('/orderhistory')
def orderhistory():
    db = shelve.open("database.db", "c")
    order_dict = db['OrderHist']
    order_list = []

    for key in order_dict:
        orderid = order_dict.get(key)
        order_list.append(orderid)

    db.close()
    return render_template("orderhistory.html", count=len(order_dict), order_list=order_list)
@app.route('/deleteorder/<int:id>', methods=['POST'])
def delete_order(id):
    order_dict = {}
    db = shelve.open('database.db', 'w')
    order_dict = db['OrderHist']
    order_dict.pop(id)
    db['OrderHist'] = order_dict
    db.close()
    return redirect(url_for('orderhistory'))




@app.route('/admin')
def admin():
    if 'admin' in session:
        name = session['name']
        return render_template('admin.html', name=name)
    else:
        flash("UNAUTHORISED ACCESS. LOG IN TO ACCESS", category='error')
        return redirect(url_for('login'))


@app.route("/addadmin", methods=['GET', 'POST'])
def addadmin():
    create_admin_form = CreateAdminForm(request.form)
    if request.method == 'POST' and create_admin_form.validate():
        admin_dict = {}
        db = shelve.open('database.db', 'c')
        try:
            admin_dict = db['Admin']
        except:
            print("Error in retrieving admins from database.db")

        admin = Admin.Admin(create_admin_form.first_name.data, create_admin_form.last_name.data,
                            create_admin_form.email.data, create_admin_form.password.data)

        if len(admin_dict) == 0:
            my_key = 1
        else:
            my_key = len(admin_dict.keys()) + 1

        admin.set_member_id(my_key)
        admin_dict[my_key] = admin
        db['Admin'] = admin_dict
        db.close()
        return redirect(url_for('admin'))

    return render_template('registeradmin.html', form=create_admin_form)

@app.route('/viewadmins')
def viewadmins():
    admin_dict = {}
    db = shelve.open('database.db', 'r')
    admin_dict = db['Admin']
    db.close()

    admin_list = []
    for key in admin_dict:
        admin = admin_dict.get(key)
        admin_list.append(admin)
    return render_template('viewadmins.html', count = len(admin_list), admin_list=admin_list)


@app.route('/updateadmin/<int:id>/', methods=['GET', 'POST'])
def update_admin(id):
    update_admin_form = CreateAdminForm(request.form)
    if request.method == 'POST' and update_admin_form.validate():
        admin_dict = {}
        db = shelve.open('database.db', 'w')
        admin_dict = db['Admin']
        admin = admin_dict.get(id)

        admin.set_first_name(update_admin_form.first_name.data)
        admin.set_last_name(update_admin_form.last_name.data)
        admin.set_email(update_admin_form.email.data)
        admin.set_password(update_admin_form.password.data)

        db['Admin'] = admin_dict
        db.close()
        return redirect(url_for('viewadmins'))
    else:
        admin_dict = {}
        db = shelve.open('database.db', 'w')
        admin_dict = db['Admin']
        db.close()

        admin = admin_dict.get(id)
        update_admin_form.first_name.data = admin.get_first_name()
        update_admin_form.last_name.data = admin.get_last_name()
        update_admin_form.email.data = admin.get_email()
        update_admin_form.password.data = admin.get_password()
        return render_template('updateAdmin.html', form=update_admin_form)


@app.route('/deleteadmin/<int:id>/', methods=['POST'])
def delete_admin(id):
    admin_dict = {}
    db = shelve.open('database.db', 'w')
    admin_dict = db['Admin']
    admin_dict.pop(id)
    db['Admin'] = admin_dict
    db.close()
    return redirect(url_for('viewadmins'))


@app.route('/register', methods=['GET', 'POST'])
def create_member():
    create_member_form = CreateMemberForm(request.form)
    if request.method == 'POST' and create_member_form.validate():
        members_dict = {}
        db = shelve.open('database.db', 'c')
        try:
            members_dict = db['Members']
        except:
            print("Error in retrieving members from database.db")

        email_list = []
        member_list = db['Members']
        for i in member_list:
            email_list.append(member_list[i].get_email())
        if create_member_form.email.data in email_list:
            flash('email already exists. Please choose a different one.', 'error')
        else:
            member = Member.Member(create_member_form.first_name.data, create_member_form.last_name.data,
                                   create_member_form.email.data, create_member_form.phone.data,
                                   create_member_form.password.data)
            if len(members_dict) == 0:
                my_key = 1
            else:
                my_key = len(members_dict.keys()) + 1
            member.set_member_id(my_key)
            members_dict[my_key] = member
            db['Members'] = members_dict
            db.close()
            return redirect(url_for('admin'))

    return render_template('adminmembers.html', form=create_member_form)


@app.route('/members')
def members():
    return render_template('adminmembers.html')


@app.route('/members/viewmembers')
def view_members():
    member_dict = {}
    db = shelve.open('database.db', 'r')
    member_dict = db['Members']
    db.close()

    member_list = []
    for key in member_dict:
        member = member_dict.get(key)
        member_list.append(member)
    return render_template('adminviewmembers.html', count=len(member_list), member_list=member_list)


@app.route('/updatemember/<int:id>/', methods=['GET', 'POST'])
def update_user(id):
    update_member_form = CreateMemberForm(request.form)
    if request.method == 'POST' and update_member_form.validate():
        members_dict = {}
        db = shelve.open('database.db', 'w')
        members_dict = db['Members']
        member = members_dict.get(id)
        member.set_first_name(update_member_form.first_name.data)
        member.set_last_name(update_member_form.last_name.data)
        member.set_email(update_member_form.email.data)
        member.set_phone(update_member_form.phone.data)
        member.set_password(update_member_form.password.data)
        db['Members'] = members_dict
        db.close()
        return redirect(url_for('view_members'))
    else:
        members_dict = {}
        db = shelve.open('database.db', 'r')
        members_dict = db['Members']
        db.close()
        member = members_dict.get(id)
        update_member_form.first_name.data = member.get_first_name()
        update_member_form.last_name.data = member.get_last_name()
        update_member_form.email.data = member.get_email()
        update_member_form.phone.data = member.get_phone()
        update_member_form.password.data = member.get_password()
        return render_template('adminupdatemember.html', form=update_member_form)


@app.route('/deletemember/<int:id>', methods=['POST'])
def delete_user(id):
    member_dict = {}
    db = shelve.open('database.db', 'w')
    member_dict = db['Members']
    member_dict.pop(id)
    db['Members'] = member_dict
    db.close()
    return redirect(url_for('view_members'))


# my input
@app.route('/addproduct', methods=['GET', 'POST'])
def create_product():
    create_product_form = CreateProductForm(request.form)
    if request.method == 'POST' and create_product_form.validate():
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            inventory_dict = {}
            db = shelve.open('database.db', 'c')
            try:
                inventory_dict = db['Inventory']
            except:
                print("Error in retrieving products from database.db")
            product = Product.Product(create_product_form.name.data, create_product_form.price.data,
                                      create_product_form.category.data, create_product_form.remarks.data,
                                      create_product_form.drinks.data, filename)
            if len(inventory_dict) == 0:
                my_key = 1
            else:
                my_key = len(inventory_dict.keys()) + 1
            product.set_product_id(my_key)
            inventory_dict[my_key] = product
            db['Inventory'] = inventory_dict
            db.close()

            return redirect(url_for('admin'))
    return render_template('admininventory.html', form=create_product_form)


@app.route('/inventory')
def inventory():
    return render_template('admininventory.html')


@app.route('/inventory/viewinventory')
def view_inventory():
    inventory_dict = {}
    db = shelve.open('database.db', 'r')
    inventory_dict = db['Inventory']
    db.close()

    inventory_list = []
    for key in inventory_dict:
        product = inventory_dict.get(key)
        inventory_list.append(product)
    return render_template('adminviewinventory.html', count=len(inventory_list), inventory_list=inventory_list)


@app.route('/updateproduct/<int:id>/', methods=['GET', 'POST'])
def update_product(id):
    update_product_form = CreateProductForm(request.form)
    if request.method == 'POST' and update_product_form.validate():
        inventory_dict = {}
        db = shelve.open('database.db', 'w')
        inventory_dict = db['Inventory']
        product = inventory_dict.get(id)
        product.set_name(update_product_form.name.data)
        product.set_price(update_product_form.price.data)
        product.set_category(update_product_form.category.data)
        product.set_remarks(update_product_form.remarks.data)
        product.set_drinks(update_product_form.drinks.data)
        db['Inventory'] = inventory_dict
        db.close()
        return redirect(url_for('view_inventory'))
    else:
        inventory_dict = {}
        db = shelve.open('database.db', 'r')
        inventory_dict = db['Inventory']
        db.close()
        product = inventory_dict.get(id)
        update_product_form.name.data = product.get_name()
        update_product_form.price.data = product.get_price()
        update_product_form.category.data = product.get_category()
        update_product_form.remarks.data = product.get_remarks()
        update_product_form.drinks.data = product.get_drinks()
        return render_template('adminupdateproduct.html', form=update_product_form)


@app.route('/deleteproduct/<int:id>', methods=['POST'])
def delete_product(id):
    inventory_dict = {}
    db = shelve.open('database.db', 'w')
    inventory_dict = db['Inventory']
    inventory_dict.pop(id)
    db['Inventory'] = inventory_dict
    db.close()
    return redirect(url_for('view_inventory'))

#Forum vvv


@app.route('/createQuestion', methods=['GET', 'POST'])
def create_question():
    create_question_form = CreateQuestionForm(request.form)
    # need to get data from  create_user_form and save to shelve database
    if request.method == 'POST' and create_question_form.validate():
        question = Question(create_question_form.email.data,
                            create_question_form.title.data,
                            create_question_form.question.data,
                            create_question_form.date_posted.data,
                            create_question_form.overall.data,
                            create_question_form.feedback.data)
        add_question(question)
        return redirect(url_for('homepage'))
    return render_template('createQuestion.html', form=create_question_form)


@app.route('/viewQuestion')
def retrieve_questions():
    questions_dict = {}
    db = shelve.open('database.db', 'r')
    questions_dict = db['Question']
    db.close()
    questions_list = []
    for key in questions_dict:
        question = questions_dict.get(key)
        questions_list.append(question)
    return render_template('retrieveQuestion.html', count=len(questions_list), questions_list=questions_list)

@app.route('/cviewQuestion')
def cretrieve_questions():
    questions_dict = {}
    db = shelve.open('database.db', 'r')
    questions_dict = db['Question']
    db.close()
    questions_list = []
    for key in questions_dict:
        question = questions_dict.get(key)
        questions_list.append(question)
    return render_template('customerforum.html', count=len(questions_list), questions_list=questions_list)


@app.route('/updateQuestion/<int:id>/', methods=['GET', 'POST'])
def update_question(id):
    update_question_form = CreateQuestionForm(request.form)
    if request.method == 'POST' and update_question_form.validate():
        print("updating question")
        db = shelve.open('database.db', 'w')
        questions_dict = db['Question']
        question = questions_dict.get(id)
        question.set_email(update_question_form.email.data)
        question.set_title(update_question_form.title.data)
        question.set_question(update_question_form.question.data)
        question.set_date_posted(update_question_form.date_posted.data)
        question.set_overall(update_question_form.overall.data)
        question.set_feedback(update_question_form.feedback.data)
        db['Question'] = questions_dict
        db.close()
        return redirect(url_for('retrieve_questions'))

    else:
        questions_dict = {}
        db = shelve.open('database.db', 'r')
        questions_dict = db['Question']
        db.close()
        question = questions_dict.get(id)
        update_question_form.email.data = question.get_email()
        update_question_form.date_posted.data = question.get_date_posted()
        update_question_form.title.data = question.get_title()
        update_question_form.question.data = question.get_question()
        update_question_form.overall.data = question.get_overall()
        update_question_form.feedback.data = question.get_feedback()

        return render_template('updateQuestion.html', form=update_question_form)

@app.route('/deleteQuestion/<int:id>', methods=['POST'])
def delete_questions(id):
    questions_dict = {}
    db = shelve.open('database.db', 'w')
    questions_dict = db['Question']

    questions_dict.pop(id)

    db['Question'] = questions_dict
    db.close()
    return redirect(url_for('retrieve_questions'))


@app.route('/filter_outbox', methods=['GET', 'POST'])
def filter_outbox():
    # Retrieve products from inventory
    inventory_dict = {}
    db_inventory = shelve.open('database.db', 'r')
    inventory_dict = db_inventory['Inventory']
    db_inventory.close()

    categories = set(product.get_category() for product in inventory_dict.values())

    selected_category = request.form.get('category')  # Change to request.form for POST
    if selected_category:
        filtered_products = {k: v for k, v in inventory_dict.items() if v.get_category() == selected_category}
    else:
        filtered_products = inventory_dict

    return render_template('outbox.html', outbox_products=filtered_products.values(), categories=categories)

if __name__ == '__main__':
    app.run(debug=True)
