#raw food data here: https://corgis-edu.github.io/corgis/csv/food/

from mimesis import Field, Fieldset, Schema
from mimesis.enums import Gender, TimestampFormat
from mimesis.locales import Locale
import random

field = Field(Locale.EN, seed=20052)
fieldset = Fieldset(Locale.EN, seed=20052)


customer_schema_def = lambda: {
    "CustomerID": field("increment"),
    "FirstName": field("first_name"),
    "LastName": field("last_name"),
    "Email": field("person.email", domains=["hotmail.com","gmail.com","aol.com","gwmail.gwu.edu"]),
    "Address": field("address"),
    "City": field("city"),
    "Country": field("country")
}

customer_schema = Schema(schema=customer_schema_def, iterations=1000)
customer_dict = customer_schema.create()

#need to calculate total amount as a function of orderdetail...
order_schema_def = lambda: {
    "CustomerID": random.randint(0,1000),
    "OrderDate": field("formatted_date")
    #"TotalAmount": field("price")
} 

order_schema = Schema(schema=order_schema_def, iterations=1000)
order_dict = order_schema.create()