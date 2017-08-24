from flask import Flask, render_template, request, redirect
from flask import jsonify, url_for, flash, make_response
from flask import session as login_session
from werkzeug import secure_filename
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from catalog_setup import Base, User, Category, Item
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import os
import random
import string
import httplib2
import json
import requests

path = os.path.dirname(__file__)

app = Flask(__name__)

# Folder to upload catalog images to
app.config['UPLOAD_FOLDER'] = 'static/img'
# Extensions that are accepted
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg'])
# Limit image size and dimensions
app.config['MAX_CONTENT_LENGTH'] = 1 * 250 * 250

# Connect to Database and create database session
engine = create_engine('postgresql://catalog:pa$$word@localhost/catalog')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create a random state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# Sign In with Facebook
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    app_id = json.loads(open(path+'/fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open(path+'/fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_' \
        'exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' \
        % (app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    userinfo_url = "https://graph.facebook.com/v2.8/me"
    token = result.split(',')[0].split(':')[1].replace('"', '')
    url = 'https://graph.facebook.com/v2.8/me?access_token=%s&fields=name,' \
        'id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]
    login_session['access_token'] = token
    url = 'https://graph.facebook.com/v2.8/me/picture?access_token=%s&' \
        'redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    login_session['picture'] = data["data"]["url"]
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
    output = ''
    output += '<h2>Welcome, '
    output += login_session['username']
    output += '!</h2>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 250px; height: 250px;border-radius:' \
        ' 125px;-webkit-border-radius: 125px;-moz-border-radius: 125px;"> '
    flash("You are logged in as %s" % login_session['username'])
    return output


def fbdisconnect():
    facebook_id = login_session['facebook_id']
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' \
        % (facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


# Sign In with Google
CLIENT_ID = json.loads(
    open(path+'/client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog App"


@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data
    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response
    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()
    login_session['provider'] = 'google'
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
    output = ''
    output += '<h2>Welcome, '
    output += login_session['username']
    output += '!</h2>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 250px; height: 250px;border-radius: 125px;' \
        '-webkit-border-radius: 125px;-moz-border-radius: 125px;"> '
    flash("You are logged in as %s" % login_session['username'])
    return output


def gdisconnect():
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials.access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] != '200':
        response = make_response(
            json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


# User functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# JSON Endpoints
# All categories
@app.route('/catalog/JSON')
def catalogJSON():
    categories = session.query(Category).all()
    return jsonify(categories=[c.serialize for c in categories])


# All items in the catalog
@app.route('/catalog/items/JSON')
def itemsJSON():
    items = session.query(Item).all()
    return jsonify(items=[i.serialize for i in items])


# Items for a specific category
@app.route('/catalog/<int:category_id>/items/JSON')
def categoryItemsJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id).all()
    return jsonify(category=category.serialize,
                   items=[i.serialize for i in items])


# Specific item by id
@app.route('/catalog/item/<int:item_id>/JSON')
def categoryItemJSON(item_id):
    category_item = session.query(Item).filter_by(id=item_id).one()
    return jsonify(category_item=category_item.serialize)


# Users of the catalog app
@app.route('/catalog/users/JSON')
def userJSON():
    members = session.query(User).all()
    return jsonify(members=[m.serialize for m in members])


# Main catalog page
@app.route('/')
@app.route('/catalog')
def showCatalog():
    categories = session.query(Category).all()
    items = session.query(Item).filter_by(category_id=Category.id).all()
    if 'username' not in login_session:
        return render_template('publiccatalog.html', categories=categories,
                               items=items)
    else:
        return render_template('catalog.html', categories=categories,
                               items=items)


# Category and the items in that category page
@app.route('/catalog/<int:category_id>/')
@app.route('/catalog/<int:category_id>/items')
def showItems(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id).order_by("time_created desc").all()  # NOQA
    creator = getUserInfo(category.user_id)
    if 'username' not in login_session:
        return render_template('publicitems.html', category=category,
                               items=items, creator=creator)
    else:
        return render_template('items.html', category=category, items=items,
                               creator=creator)


# Single selected item page
@app.route('/catalog/item/<int:item_id>')
def showItem(item_id):
    category_item = session.query(Item).filter_by(id=item_id).one()
    creator = getUserInfo(category_item.user_id)
    if 'username' not in login_session or creator.id != login_session['user_id']:  # NOQA
        return render_template('publicitem.html', category_item=category_item,
                               creator=creator)
    else:
        return render_template('item.html', category_item=category_item,
                               creator=creator)


# Add a new item in a category page
@app.route('/catalog/<int:category_id>/item/new', methods=['GET', 'POST'])
def newCategoryItem(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    if 'username' not in login_session:
        flash('You are not allowed to add items until you login!')
        return redirect('/login')
    if request.method == 'POST':
        if request.files['file']:
            image = request.files['file']
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        newItem = Item(name=request.form['name'],
                       description=request.form['description'],
                       price=request.form['price'], picture=filename,
                       category_id=category.id,
                       user_id=login_session['user_id'])
        session.add(newItem)
        flash('Item successfully added to %s.' % category.name)
        session.commit()
        return redirect(url_for('showItems', category_id=category_id))
    else:
        return render_template('newitem.html')
        flash('Something went wrong, please try again!')


# Edit an item created by the current user
@app.route('/catalog/item/<int:item_id>/edit', methods=['GET', 'POST'])
def editItem(item_id):
    editedItem = session.query(Item).filter_by(id=item_id).one()
    creator = getUserInfo(editedItem.user_id)
    if 'username' not in login_session:
        flash('You are not allowed to edit items until you login!')
        return redirect('/login')
    if login_session['user_id'] != editedItem.user_id:
        flash('You are not allowed to edit items created by other users!')
        return redirect(url_for('showCatalog'))
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['price']:
            editedItem.price = request.form['price']
        if request.files['file']:
            image = request.files['file']
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            editedItem.picture = filename
        session.add(editedItem)
        session.commit()
        flash('%s item successfully updated' % editedItem.name)
        return redirect(url_for('showItem', item_id=item_id))
    else:
        return render_template('edititem.html', item_id=item_id,
                               item=editedItem)


# Delete an item created by the current user
@app.route('/catalog/item/<int:item_id>/delete', methods=['GET', 'POST'])
def deleteItem(item_id):
    deletedItem = session.query(Item).filter_by(id=item_id).one()
    creator = getUserInfo(deletedItem.user_id)
    if 'username' not in login_session:
        flash('You are not allowed to delete items until you login!')
        return redirect('/login')
    if login_session['user_id'] != deletedItem.user_id:
        flash('You are not allowed to delete items created by other users!')
        return redirect(url_for('showCatalog'))
    if request.method == 'POST':
        session.delete(deletedItem)
        flash('%s Successfully Deleted!' % deletedItem.name)
        session.commit()
        return redirect(url_for('showItems',
                                category_id=deletedItem.category_id))
    else:
        return render_template('deleteitem.html', item_id=item_id,
                               item=deletedItem)


# Disconnect the user based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showCatalog'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showCatalog'))

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
