import Member
import Product
import shelve

from flask import Flask, render_template, request, redirect, url_for

from forms import CreateMemberForm, CreateProductForm

app = Flask(__name__)


@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/outbox')
def outbox():
    return render_template('outbox.html')


@app.route('/register', methods=['GET', 'POST'])
def create_member():
    create_member_form = CreateMemberForm(request.form)
    if request.method == 'POST' and create_member_form.validate():
        members_dict = {}
        db = shelve.open('member.db', 'c')
        try:
            members_dict = db['Members']
        except:
            print("Error in retrieving members from Members.db")
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


@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route('/members')
def members():
    return render_template('adminmembers.html')


# @app.route('/members/createmembers', methods=['GET', 'POST'])
# def create_member():
#     create_member_form = CreateMemberForm(request.form)
#     if request.method == 'POST' and create_member_form.validate():
#         members_dict = {}
#         db = shelve.open('member.db', 'c')
#         try:
#             members_dict = db['Members']
#         except:
#             print("Error in retrieving members from Members.db")
#         member = Member.Member(create_member_form.first_name.data, create_member_form.last_name.data,
#                                create_member_form.email.data, create_member_form.phone.data,
#                                create_member_form.password.data)
#         members_dict[member.get_member_id()] = member
#         db['Members'] = members_dict
#
#         db.close()
#
#         return redirect(url_for('admin'))
#     return render_template('adminmembers.html', form=create_member_form)


@app.route('/members/viewmembers')
def view_members():
    member_dict = {}
    db = shelve.open('member.db', 'r')
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
        db = shelve.open('member.db', 'w')
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
        db = shelve.open('member.db', 'r')
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
    db = shelve.open('member.db', 'w')
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
        inventory_dict = {}
        db = shelve.open('inventory.db', 'c')
        try:
            inventory_dict = db['Inventory']
        except:
            print("Error in retrieving products from Inventory.db")
        product = Product.Product(create_product_form.name.data, create_product_form.price.data,
                                  create_product_form.category.data, create_product_form.remarks.data,
                                  create_product_form.drinks.data)
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
    db = shelve.open('inventory.db', 'r')
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
        db = shelve.open('inventory.db', 'w')
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
        db = shelve.open('inventory.db', 'r')
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
    db = shelve.open('inventory.db', 'w')
    inventory_dict = db['Inventory']
    inventory_dict.pop(id)
    db['Inventory'] = inventory_dict
    db.close()
    return redirect(url_for('view_inventory'))


if __name__ == '__main__':
    app.run(debug=True)
