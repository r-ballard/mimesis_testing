#raw food data here: https://corgis-edu.github.io/corgis/csv/food/

from mimesis import Field, Fieldset, Schema
from mimesis.enums import Gender, TimestampFormat
from mimesis.locales import Locale
from mimesis.random import Numeric
import random
import pandas

numbers = Numeric()
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
    "CustomerID": field("integer_number", start=1, end=1001),
    "OrderDate": field("formatted_date")
    #"TotalAmount": field("price")
} 

order_schema = Schema(schema=order_schema_def, iterations=1000)
order_dict = order_schema.create()

orderdf = pandas.DataFrame.from_dict(order_dict)


fooddf = pandas.read_csv("C:\\Users\\russe\\OneDrive\\Desktop\\class_materials\\DATS6102\\assignments\\erd_star_assignment2\\food.csv")

fooddf = fooddf[['Category','Description']]
fooddf = fooddf.loc[fooddf['Description'].str.len() < 20].reset_index(drop=True)
fooddf.rename(columns={"Description":"ProductName"}, inplace=True)

fdf_rowcount = fooddf.shape[0]

fooddf['Price'] = numbers.floats(start=0, end=500, n=fdf_rowcount, precision=2)


orderdetail_schema_def = lambda: {
    "OrderID": field("integer_number",start=1,end=1001),
    "ProductID": field("integer_number",start=1,end=fdf_rowcount),
    "Quantity": field("integer_number",start=1,end=51)
}

orderdetail_schema = Schema(schema=orderdetail_schema_def, iterations=1000)
orderdetail_dict = orderdetail_schema.create()

orderdetaildf = pandas.DataFrame.from_dict(orderdetail_dict)

orderdetaildf = (pandas.merge(orderdetaildf,fooddf[['Price']],how='left',left_on='ProductID',right_index=True)
                        .rename(columns={"Price":"UnitPrice"}))
                        
orderdf['Total'] =                         
