'''
REST api used to handle messages being sent from the discord bot
and to send back information about the product

'''
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Setting up the api using Flask
# Setting up the database using SQL
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///product_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class ProductModel(db.Model):
    '''
    Class that contains the information for the product, id is given in url
    '''
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(100), nullable=False)
    lowest_price = db.Column(db.String(100), nullable=False)
    lowest_price_time = db.Column(db.String(100), nullable=False)
    recent_price = db.Column(db.String(100), nullable=False)
    recent_price_time = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Product(product_name = {self.product_name}, lowest_price = {self.lowest_price})"


# Creates the tables
db.create_all()

# All the required arguments for the put request
product_put_args = reqparse.RequestParser()
product_put_args.add_argument(
    "id", type=int, help="Id is required", required=True)
product_put_args.add_argument(
    "product_name", type=str, help="Product Name is required", required=True)
product_put_args.add_argument(
    "url", type=str, help="Url is required", required=True)
product_put_args.add_argument(
    "recent_price", type=str, help="Price is required", required=True)

# All the required arguments for the get requests
product_get_args = reqparse.RequestParser()
product_get_args.add_argument("id", type=int, required=False)
product_get_args.add_argument("product_name", required=False)
product_get_args.add_argument("url", type=str, required=False)
product_get_args.add_argument("recent_price", type=str, required=False)

# Fields in the table
resource_fields = {
    'id': fields.Integer,
    'product_name': fields.String,
    'url': fields.String,
    'lowest_price': fields.String,
    'lowest_price_time': fields.String,
    'recent_price': fields.String,
    'recent_price_time': fields.String
}


class Product(Resource):
    '''
    This calls handles the requests made
    '''
    @marshal_with(resource_fields)
    def get(self, product_name):
        '''
        Get request checks if the product exists. If the product exists,
        then return the lowest price and the time the product was at this lowest
        price.
        '''
        args = product_get_args.parse_args()
        result = ProductModel.query.filter_by(
            product_name=product_name).all()
        print(result[0])
        if not result:
            abort(404, message="Could not find product")
        # NEED TO RETURN PRICE
        return result

    @marshal_with(resource_fields)
    def put(self, product_name):
        '''
        Put requests checks if the product exits. If the product exists,
        checks if the price given is lower than the lowest before,
        if it is lower the lowest_price is now changed to this given price.
        Otherwise, the recent_price is updated. If product is not found, then
        the product is added to the database.
        '''
        dt_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        args = product_put_args.parse_args()
        result = ProductModel.query.filter_by(
            product_name=product_name).first()

        if result:
            # Checks to see if the recent price is acutally lower than lowest_price
            if int(result.lowest_price[1:]) >= int(args["recent_price"][1:]):
                setattr(result, result.lowest_price, args["recent_price"])
                setattr(result, result.lowest_price_time, dt_now)
                setattr(result, result.recent_price, args["recent_price"])
                setattr(result, result.recent_price_time, dt_now)
                db.session.commit()
                return 201
            else:
                setattr(result, result.recent_price,  args["recent_price"])
                setattr(result, result.recent_price_time, dt_now)
                db.session.commit()
                return 201

        # Creates a new ProductModel if the product provided is not found
        product = ProductModel(id=args["id"], product_name=product_name, url=args["url"], lowest_price=args["recent_price"],
                               lowest_price_time=dt_now, recent_price=args["recent_price"], recent_price_time=dt_now)
        db.session.add(product)
        db.session.commit()
        return 201


api.add_resource(Product, "/product/<string:product_name>")

if __name__ == "__main__":
    app.run(debug=True)
