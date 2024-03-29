from mimesis import Field, Fieldset, Schema
from mimesis.enums import Gender, TimestampFormat
from mimesis.locales import Locale

field = Field(Locale.EN, seed=20052)
fieldset = Fieldset(Locale.EN, seed=20052)

schema_definition = lambda: {
    "CustomerID": field("increment"),
    "FirstName": field("first_name"),
    "LastName": field("last_name"),
    "version": field("version"),
    "timestamp": field("timestamp", fmt=TimestampFormat.POSIX),
    "owner": {
        "email": field("person.email", domains=["mimesis.name"]),
        "creator": field("full_name", gender=Gender.FEMALE),
    },
    "apiKeys": fieldset("token_hex", key=lambda s: s[:16], i=3),
}

schema = Schema(schema=schema_definition, iterations=3)
schema.create()


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



order_schema_def = lambda: {
    "CustomerID": field("increment"),
    "FirstName": field("first_name"),
    "LastName": field("last_name"),
    "Email": field("person.email", domains=["hotmail.com","gmail.com","aol.com","gwmail.gwu.edu"]),
    "Address": field("address"),
    "City": field("city"),
    "Country": field("country")
} 






integer_number(start=-1000, end=1000)