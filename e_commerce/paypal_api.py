from dotenv import load_dotenv, find_dotenv
import os, base64, requests, json

load_dotenv(find_dotenv())

base = os.environ.get("PAYPAL_URL")
auth = base64.b64encode((os.environ.get("CLIENT_ID") + ":" + os.environ.get("APP_SECRET")).encode('ascii')).decode("ascii")

def generateAccessToken():
    response = requests.post(
        base + '/v1/oauth2/token', 
        headers = {
            "Content-Type": "text/plain",
            'Authorization': "Basic " + auth
        }, 
        data = "grant_type=client_credentials"
    )
    data = response.json()
    return data['access_token'];


def createOrder(order_details):
    products = []
    for od in order_details:
        for i in range(od.nu_amount):
            products.append({
                "reference_id": str(od.product.id_product) + "_" + str(i),
                "description": od.product.tx_name,
                "amount": {
                    "currency_code": "MXN",
                    "value": float("{:.2f}".format(od.product.real_price))
                }
            })
    
    access_token = generateAccessToken()
    response = requests.post(
        base + '/v2/checkout/orders', 
        headers = {
            "Content-Type": "application/json",
            'Authorization': "Bearer " + access_token
        }, 
        data = json.dumps({
            'intent': "CAPTURE",
            'purchase_units': products
        })
    )
    return response.json();


def capturePayment(order_id):
    access_token = generateAccessToken()
    response = requests.post(
        base + '/v2/checkout/orders/' + order_id + '/capture', 
        headers = {
            "Content-Type": "application/json",
            'Authorization': "Bearer " + access_token
        }
    )
    return response.json();


# class PaypalOrderResources(Resource):
#     def get(self):
#         order = createOrder()
#         return order, 200
    
# class PaypalPaymentResources(Resource):
#     def get(self, order_id):
#         captureData = capturePayment(order_id)
#         return captureData, 200