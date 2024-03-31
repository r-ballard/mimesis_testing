#raw food data here: https://corgis-edu.github.io/corgis/csv/food/

from mimesis import Field, Fieldset, Schema
from mimesis.enums import Gender, TimestampFormat
from mimesis.locales import Locale
from mimesis import Numeric
import random
import pandas

numbers = Numeric()
field = Field(Locale.EN, seed=20052)
fieldset = Fieldset(Locale.EN, seed=20052)

out_path = "C:\\Users\\russe\\OneDrive\\Desktop\\class_materials\\DATS6102\\assignments\\erd_star_assignment2\\synthetic_data\\"

#------

#Create erd_customer synthetic data
customer_schema_def = lambda: {
    "FirstName": field("first_name"),
    "LastName": field("last_name"),
    "Email": field("person.email", domains=["hotmail.com","gmail.com","aol.com","gwmail.gwu.edu"]),
    "Address": field("address"),
    "City": field("city"),
    "Country": field("country")
}

customer_schema = Schema(schema=customer_schema_def, iterations=1000)
customer_dict = customer_schema.create()

#Create dataframe, convert index into CustomerID column, reorder columns to have CustomerID leftmost/index 0
customerdf = pandas.DataFrame.from_dict(customer_dict)
customerdf['CustomerID'] = customerdf.index + 1
col = customerdf.pop('CustomerID')
customerdf.insert(0,col.name,col)
customerdf.to_csv(path_or_buf=f"{out_path}erd_customers.csv",
                index=False)

#------

#create erd_order synthetic data
#need to calculate total amount as a function of orderdetail...

order_schema_def = lambda: {
    "CustomerID": field("integer_number", start=1, end=1001),
    "OrderDate": field("formatted_date")
    #"TotalAmount": field("price")
} 

order_schema = Schema(schema=order_schema_def, iterations=1000)
order_dict = order_schema.create()

orderdf = pandas.DataFrame.from_dict(order_dict)

orderdf['OrderID'] = orderdf.index + 1
col = orderdf.pop('OrderID')
orderdf.insert(0,col.name,col)
#Add order total in orderdetails, save in that section

#---

#erd_product

fooddf = pandas.read_csv("C:\\Users\\russe\\OneDrive\\Desktop\\class_materials\\DATS6102\\assignments\\erd_star_assignment2\\food.csv")

fooddf = fooddf[['Category','Description']]
fooddf = fooddf.loc[fooddf['Description'].str.len() < 20].reset_index(drop=True)
fooddf.rename(columns={"Description":"ProductName"}, inplace=True)

fdf_rowcount = fooddf.shape[0]

fooddf['Price'] = numbers.floats(start=0, end=500, n=fdf_rowcount, precision=2)
fooddf['ProductID'] = fooddf.index + 1
col = fooddf.pop('ProductID')
fooddf.insert(0,col.name,col)
fooddf.to_csv(path_or_buf=f"{out_path}erd_products.csv",
                index=False)

#-------

#create erd_orderdetail synthetic data
order_rowcount = orderdf.shape[0]

orderdetail_schema_def = lambda: {
    "OrderID": field("integer_number",start=0,end=1000),
    "ProductID": field("integer_number",start=1,end=fdf_rowcount+1),
    "Quantity": field("integer_number",start=1,end=51)
}

orderdetail_schema = Schema(schema=orderdetail_schema_def, iterations=20000)
orderdetail_dict = orderdetail_schema.create()

orderdetaildf = pandas.DataFrame.from_dict(orderdetail_dict)

orderdetaildf = (pandas.merge(orderdetaildf,fooddf[['Price']],how='left',left_on='ProductID',right_index=True)
                       .rename(columns={"Price":"UnitPrice"}))
                        
orderdetail2 = orderdetaildf.copy()
orderdetail2['detailsum'] = orderdetail2['UnitPrice']*orderdetail2['Quantity']   
orderdetailpivot = (orderdetail2.drop(axis=1,columns=['ProductID','UnitPrice','Quantity'])
                                .pivot_table(index='OrderID',aggfunc='sum'))

orderdetaildf['OrderDetailID'] = orderdetaildf.index + 1
col = orderdetaildf.pop('OrderDetailID')
orderdetaildf.insert(0,col.name,col)
orderdetaildf.to_csv(path_or_buf=f"{out_path}erd_orderdetails.csv",
                index=False)


orderdf = (pandas.merge(orderdf,orderdetailpivot,how='left',left_index=True,right_index=True)
                 .rename(columns={"detailsum":"TotalAmount"}))

#Once we have total, we then write orderdf to file
orderdf.to_csv(path_or_buf=f"{out_path}erd_orders.csv",
                index=False)