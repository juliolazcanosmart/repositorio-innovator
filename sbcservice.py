from flask import Flask
import xmlrpc.client
from flask import request
from flask import jsonify
from datetime import date

from flask_cors import CORS


app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app, resources={r"/eventsearchbyorder": {"origins": "http://localhost:3000"}})


@app.route('/')
def hello_world():
    return ('Hola')

@app.route('/suscripter', methods = ['POST'])
def search_suscripter():
    
    content = request.get_json()


    url = 'https://smartbusinesscorp.odoo.com'
    db = 'luchorck92-smartbusinesscorp-13-0-1796920'
    username = content['user']
    password = content['password']


    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    common.version()

    uid = common.authenticate(db, username, password, {})

    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    
    models.execute_kw(db, uid, password, 'res.partner', 'check_access_rights', ['read'], {'raise_exception': False})

    fields = models.execute_kw(db, uid, password,
    'res.partner', 'search_read',
    [[['id_suscripter', '=', content['id_suscripter']]]],
    {'fields': ['name', 'country_id', 'comment'], 'limit': 5})

    return str(fields)


@app.route('/cratesuscripter', methods = ['POST'])
def crate_suscripter():
    
    content = request.get_json()

    if content['id_suscripter']:


        url = 'https://smartbusinesscorp.odoo.com'
        db = 'luchorck92-smartbusinesscorp-13-0-1796920'
        username = content['user']
        password = content['password']

        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        common.version()

        uid = common.authenticate(db, username, password, {})

        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        models.execute_kw(db, uid, password, 'res.partner', 'check_access_rights', ['read'], {'raise_exception': False})

        partner = models.execute_kw(db, uid, password,
        'res.partner', 'search_read',
        [[['email', '=', content['email']]]],
        {'fields': ['name', 'country_id', 'comment'], 'limit': 5})

        #creamos el partner en Odoo
        if not partner:

            partner_id = models.execute_kw(db, uid, password, 'res.partner', 'create', [{'id_suscripter': content['id_suscripter'], 'name': content['name'],'email': content['email'],'phone': content['phone'],'city': content['city'] , 'comment': 'From Oficina Virtual'}])
            partner = models.execute_kw(db, uid, password,'res.partner', 'search_read',[[['id', '=', partner_id]]],{'fields': ['name', 'country_id', 'comment'], 'limit': 5})

        return str(partner)
    else:
        return False


@app.route('/cratesuscripterinnovator', methods = ['POST'])
def crate_suscripter_innovator():
    
    content = request.get_json()

    if content['name']:


        url = 'https://smartbusinesscorp.odoo.com'
        db = 'luchorck92-smartbusinesscorp-13-0-1796920'
        username = content['user']
        password = content['password']

        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        common.version()

        uid = common.authenticate(db, username, password, {})

        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        models.execute_kw(db, uid, password, 'res.partner', 'check_access_rights', ['read'], {'raise_exception': False})

        partner = models.execute_kw(db, uid, password,
        'res.partner', 'search_read',
        [[['email', '=', content['email']]]],
        {'fields': ['name', 'country_id', 'comment'], 'limit': 5})

        #creamos el partner en Odoo
        if not partner:

            partner_id = models.execute_kw(db, uid, password, 'res.partner', 'create', [{ 'x_innovator':True, 'id_suscripter': '0', 'name': content['name'],'email': content['email'],'city': content['city'], 'comment': 'From Oficina Virtual'}])
            partner = models.execute_kw(db, uid, password,'res.partner', 'search_read',[[['id', '=', partner_id]]],{'fields': ['name', 'country_id', 'comment'], 'limit': 5})

        else:
            for partner_id in partner:
                models.execute_kw(db, uid, password, 'res.partner', 'write', [partner_id['id'], {
                    'x_innovator': True,
                    'comment': 'From Innovator'
                }])

        return str(partner)
    else:
        return False




@app.route('/writesuscripter', methods = ['POST'])
def write_suscripter():

    content = request.get_json()

    if content['id_suscripter']:

        url = 'https://smartbusinesscorp.odoo.com'
        db = 'luchorck92-smartbusinesscorp-13-0-1796920'
        username = content['user']
        password = content['password']

        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        common.version()

        uid = common.authenticate(db, username, password, {})

        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        models.execute_kw(db, uid, password, 'res.partner', 'check_access_rights', ['read'], {'raise_exception': False})

        partner = models.execute_kw(db, uid, password,'res.partner', 'search_read',[[['id_suscripter', '=', content['id_suscripter']]]],{'fields': ['name', 'country_id', 'comment'], 'limit': 5})

        if partner:
            for partner_id in partner:
                models.execute_kw(db, uid, password, 'res.partner', 'write', [partner_id['id'], {
                    'name': content['name']
                }])
            partner = models.execute_kw(db, uid, password,'res.partner', 'search_read',[[['id_suscripter', '=', content['id_suscripter']]]],{'fields': ['name', 'country_id', 'comment'], 'limit': 5})
        return str(partner)

    else:
        return False

@app.route('/saleorder', methods = ['POST'])
def sale_order():

    content = request.get_json()

    today = date.today()


    d2 = today.strftime("%B %d, %Y")

    if content['id_suscripter']:
    
        content = request.get_json()

        url = 'https://smartbusinesscorp.odoo.com'
        db = 'luchorck92-smartbusinesscorp-13-0-1796920'
        username = content['user']
        password = content['password']

        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        common.version()

        uid = common.authenticate(db, username, password, {})

        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        models.execute_kw(db, uid, password, 'res.partner', 'check_access_rights', ['read'], {'raise_exception': False})

        partner = models.execute_kw(db, uid, password,'res.partner', 'search_read',[[['id_suscripter', '=', content['id_suscripter']]]],{'fields': ['name', 'country_id', 'comment'], 'limit': 5})      

        if partner:

            for partner_id in partner:

                orders = models.execute_kw(db, uid, password,'sale.order', 'search_read',[[['partner_id', '=', partner_id['id']]]],{'fields': ['id'], 'limit': 5})

                if len(orders) == 0:

                    order_id = models.execute_kw(db, uid, password, 'sale.order', 'create', [{'partner_id': partner_id['id'],'partner_invoice_id': partner_id['id'],'partner_shipping_id': partner_id['id'], 'date_order': '2021-06-23 22:22:28', }])
                    
                    order_line_id = models.execute_kw(db, uid, password, 'sale.order.line', 'create', [{'product_id': 3,'product_uom_qty': 1,'order_id': order_id}])

                    order = models.execute_kw(db, uid, password,'sale.order', 'search_read',[[['id', '=', order_id]]],{'fields': ['id'], 'limit': 5})
                    
                    return str(order)
                else:
                    return str(orders)
        else:
            return str(False)
    else:
        return str(False)

# Este metodo regresa el listado de eventos activos

@app.route('/eventticket', methods = ['POST'])
def eventticket():

    today = date.today()


    d2 = today.strftime("%B %d, %Y")


    content = request.get_json()


    url = 'https://smartbusinesscorp.odoo.com'
    db = 'luchorck92-smartbusinesscorp-13-0-1796920'
    user = str(request.form['user'])
    password = str(request.form['password'])

    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    common.version()

    uid = common.authenticate(db, username, password, {})

    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    
    models.execute_kw(db, uid, password, 'res.partner', 'check_access_rights', ['read'], {'raise_exception': False})


    fields = models.execute_kw(db, uid, password,
    'event.event', 'search_read',
    [[['state', '=', 'confirm']]],
    {'fields': ['name'], 'limit': 5})

    return str(fields)


# Este metodo regresamos la entrada del evento dependiendo el email, necesitamos el ID del evento y el Email

@app.route('/eventsearchbyeamil', methods = ['POST'])
def eventsearchbyeamil():

    today = date.today()


    d2 = today.strftime("%B %d, %Y")


    content = request.get_json()


    url = 'https://smartbusinesscorp.odoo.com'
    db = 'luchorck92-smartbusinesscorp-13-0-1796920'
    user = str(request.form['user'])
    password = str(request.form['password'])


    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    common.version()

    uid = common.authenticate(db, username, password, {})

    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    
    models.execute_kw(db, uid, password, 'res.partner', 'check_access_rights', ['read'], {'raise_exception': False})


    fields = models.execute_kw(db, uid, password,
    'event.registration', 'search_read',
    [[['email', '=', content['email']], ['event_id', '=', content['event_id']]]],
    {'fields': ['id','name', 'barcode'], 'limit': 5})



    return str(fields)


# Este metodo regresamos la entrada del evento dependiendo el email, necesitamos el Numero de orden

@app.route('/eventsearchbyorder', methods = ['POST'])
def eventsearchbyorder():

    sale_order_id = str(request.form['sale_order_id'])


    user = str(request.form['user'])

    password = str(request.form['password'])


    today = date.today()


    d2 = today.strftime("%B %d, %Y")


    content = request.get_json()

    #sale_order_id = content['sale_order_id']


    url = 'https://www.smartbusinesscorp.info'
    db = 'luchorck92-smartbusinesscorp-13-0-1796920'


    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    common.version()

    uid = common.authenticate(db, user, password, {})

    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    
    models.execute_kw(db, uid, password, 'res.partner', 'check_access_rights', ['read'], {'raise_exception': False})

    #import pdb

    #pdb.set_trace()


    fields = models.execute_kw(db, uid, password,
    'event.registration', 'search_read',
    [[['sale_order_id', '=', sale_order_id]]],
    {'fields': ['id','name', 'barcode', 'sale_order_id'], 'limit': 5})


    response = jsonify(fields)


    return response


if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True, port= 5000)