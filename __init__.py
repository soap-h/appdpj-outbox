import Member
import Product
import shelve
import Question

from flask import Flask, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
from forms import CreateMemberForm, CreateProductForm, CreateQuestionForm

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

@app.route('/outbox')
def outbox():
    # Retrieve products from inventory
    inventory_dict = {}
    db_inventory = shelve.open('database.db', 'r')
    inventory_dict = db_inventory['Inventory']
    db_inventory.close()

    return render_template('outbox.html', outbox_products=inventory_dict.values())

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

    outbox_dict[selected_product.get_product_id()] = selected_product
    db_outbox['Outbox'] = outbox_dict
    db_outbox.close()

    return redirect(url_for('outbox'))

@app.route('/view_cart')
def view_cart():
    outbox_dict = {}
    db_outbox = shelve.open('database.db', 'r')
    outbox_dict = db_outbox['Outbox']
    db_outbox.close()

    outbox_list = list(outbox_dict.values())
    return render_template('viewcart.html', count=len(outbox_list), outbox_list=outbox_list)

@app.route('/deleteitem/<int:id>', methods=['POST'])
def delete_cart(id):
    cart_dict = {}
    db = shelve.open('database.db', 'w')
    cart_dict = db['Outbox']
    cart_dict.pop(id)
    db['Outbox'] = cart_dict
    db.close()
    return redirect(url_for('view_cart'))

@app.route('/admin')
def admin():
    return render_template('admin.html')

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
            inventory_dict[product.get_product_id()] = product
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

@app.route('/createQuestion', methods=['GET', 'POST'])
def create_question():
    create_question_form = CreateQuestionForm(request.form)
    # need to get data from  create_user_form and save to shelve database
    if request.method == 'POST' and create_question_form.validate():
        question = Question(create_question_form.email.data,
                            create_question_form.title.data,
                            create_question_form.question.data,
                            create_question_form.date_posted.data)
        # first_name is a data filled object so need to retrieve data
        add_question(question)
        return redirect(url_for('homepage'))
    return render_template('createQuestion.html', form=create_question_form)


@app.route('/retrieveQuestion')
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

if __name__ == '__main__':
    app.run(debug=True)
