"""
The database of culture care api
"""

from flask_sqlalchemy import SQLAlchemy

sql_db = SQLAlchemy()

practitioner_gender_table = sql_db.Table('practitioner_gender',
    sql_db.Column('practitioner_id', sql_db.Integer, sql_db.ForeignKey('practitioners.id'), primary_key=True),
    sql_db.Column('gender_id', sql_db.Integer, sql_db.ForeignKey('genders.id'), primary_key=True)
)

practitioner_location_table = sql_db.Table('practitioner_location',
    sql_db.Column('practitioner_id', sql_db.Integer, sql_db.ForeignKey('practitioners.id'), primary_key=True),
    sql_db.Column('location_id', sql_db.Integer, sql_db.ForeignKey('locations.id'), primary_key=True)
)

practitioner_specialization_table = sql_db.Table('practitioner_specialization',
    sql_db.Column('practitioner_id', sql_db.Integer, sql_db.ForeignKey('practitioners.id'), primary_key=True),
    sql_db.Column('specialization_id', sql_db.Integer, sql_db.ForeignKey('specializations.id'), primary_key=True)
)

practitioner_language_table = sql_db.Table('practitioner_language',
    sql_db.Column('practitioner_id', sql_db.Integer, sql_db.ForeignKey('practitioners.id'), primary_key=True),
    sql_db.Column('language_id', sql_db.Integer, sql_db.ForeignKey('languages.id'), primary_key=True)
)

practitioner_network_table = sql_db.Table('practitioner_payment',
    sql_db.Column('practitioner_id', sql_db.Integer, sql_db.ForeignKey('practitioners.id'), primary_key=True),
    sql_db.Column('payment_id', sql_db.Integer, sql_db.ForeignKey('payments.id'), primary_key=True)
)

class EmailContent(sql_db.Model):
    """
    EmailContent Model
    """
    __tablename__ = "emailcontents"

    id = sql_db.Column(sql_db.Integer, primary_key=True, autoincrement = True)
    message = sql_db.Column(sql_db.String)
    practitioner_id = sql_db.Column(sql_db.Integer, sql_db.ForeignKey("practitioners.id"), nullable = False)
    subject = sql_db.Column(sql_db.String)



    def __init__(self, **kwargs):
        """
        Initializes a EmailContent object
        """
        self.message = kwargs.get("message")
        self.subject = kwargs.get("subject")
        self.practitioner_id = kwargs.get("practitioner_id")

    def simple_serialize(self):
        """
        Simple serializes an emailcontent object
        """
        return {
            "id" : self.id,
            "message" : self.message,
            "subject" : self.subject,
            "practitioner_id" : self.practitioner_id
        }
    
    def serialize(self):
        """
        Serializes an emailcontent object
        """
        return {
            "id" : self.id,
            "message" : self.message,
            "subject" : self.subject,
            "practitioner_id" : self.practitioner_id
        }


class Patient(sql_db.Model):
    """
    Patient Model
    """
    __tablename__ = "patients"
    id = sql_db.Column(sql_db.Integer, primary_key = True, autoincrement = True, nullable = False)

    name = sql_db.Column(sql_db.String, nullable = False)
    email_address = sql_db.Column(sql_db.String, nullable = False, unique = True)


    def __init__(self, **kwargs):
        """
        Initializes a Patient object
        """
        self.name = kwargs.get("name")
        self.email_address = kwargs.get("email_address")

    def simple_serialize(self):
        """
        Simple serializes a patient object
        """
        return {
            "id" : self.id,
            "name" : self.name,
            "email_address" : self.email_address,
        }
    
    def serialize(self):
        """
        Serializes a patient 
        """
        return {
            "id" : self.id,
            "name" : self.name,
            "email_address" : self.email_address
        }
    

class Practitioner(sql_db.Model):
    """
    Practitioner Model
    """
    __tablename__ = "practitioners"
    id = sql_db.Column(sql_db.Integer, primary_key = True, autoincrement = True)

    name = sql_db.Column(sql_db.String, nullable = False)
    email_address = sql_db.Column(sql_db.String, nullable = False, unique = True)

    genders = sql_db.relationship("Gender", secondary = practitioner_gender_table, back_populates = "practitioners")  
    languages = sql_db.relationship("Language", secondary = practitioner_language_table, back_populates = "practitioners")  
    locations = sql_db.relationship("Location", secondary = practitioner_location_table, back_populates = "practitioners")  
    specializations = sql_db.relationship("Specialization", secondary = practitioner_specialization_table, back_populates = "practitioners")
    payments = sql_db.relationship("Payment", secondary = practitioner_network_table, back_populates = "practitioners")  
    emailcontents = sql_db.relationship("EmailContent")  

    def __init__(self, **kwargs):
        """
        Initializes a Practitioner object
        """
        self.name = kwargs.get("name")
        self.email_address = kwargs.get("email_address")

    def simple_serialize(self):
        """
        Simple serializes a practitioner object
        """
        return {
            "id" : self.id,
            "name" : self.name,
            "email_address" : self.email_address,
        }
    
    def serialize(self):
        """
        Serializes a practitioner
        """
        return {
            "id" : self.id,
            "name" : self.name,
            "email_address" : self.email_address, 
            "genders" : [gender.simple_serialize() for gender in self.genders],
            "languages" : [language.simple_serialize() for language in self.languages],
            "locations" : [location.simple_serialize() for location in self.locations],
            "specializations" : [specialization.simple_serialize() for specialization in self.specializations],
            "payments" : [payment.simple_serialize() for payment in self.payments]
        }


class Gender(sql_db.Model):
    """
    Gender Model
    """
    __tablename__ = "genders"
    id = sql_db.Column(sql_db.Integer, primary_key = True, autoincrement = True)
    name = sql_db.Column(sql_db.String, nullable = False)
    practitioners = sql_db.relationship("Practitioner", secondary = practitioner_gender_table, back_populates = "genders")  


    def __init__(self, **kwargs):
        """
        Initializes a Gender object
        """
        self.name = kwargs.get("name")

    def simple_serialize(self):
        return {"id" : self.id, "name" : self.name}
    
        
class Language(sql_db.Model):
    """
    Language Model
    """
    __tablename__ = "languages"
    id = sql_db.Column(sql_db.Integer, primary_key = True, autoincrement = True)
    name = sql_db.Column(sql_db.String, nullable = False)
    practitioners = sql_db.relationship("Practitioner", secondary = practitioner_language_table, back_populates = "languages")  

    def __init__(self, **kwargs):
        """
        Initializes a Language object
        """
        self.name = kwargs.get("name")

    def simple_serialize(self):
        """
        Simple serializes a language object
        """
        return {"id" : self.id, "name" : self.name}
    

class Location(sql_db.Model):
    """
    Location Model
    """
    __tablename__ = "locations"
    id = sql_db.Column(sql_db.Integer, primary_key = True, autoincrement = True)
    name = sql_db.Column(sql_db.String, nullable = False)
    practitioners = sql_db.relationship("Practitioner", secondary = practitioner_location_table, back_populates = "locations")  

    def __init__(self, **kwargs):
        """
        Initializes a Location object
        """
        self.name = kwargs.get("name")

    def simple_serialize(self):
        """
        Simple serializes a location object
        """
        return {"id" : self.id, "name" : self.name}
    

class Specialization(sql_db.Model):
    """
    Specialization Model
    """
    __tablename__ = "specializations"
    id = sql_db.Column(sql_db.Integer, primary_key = True, autoincrement = True)
    name = sql_db.Column(sql_db.String, nullable = False)
    practitioners = sql_db.relationship("Practitioner", secondary = practitioner_specialization_table, back_populates = "specializations")  

    def __init__(self, **kwargs):
        """
        Initializes a Specialization object
        """
        self.name = kwargs.get("name")

    def simple_serialize(self):
        """
        Simple serializes a specialization object
        """
        return {"id" : self.id, "name" : self.name}
    
    
class Payment(sql_db.Model):
    """
    Network Model
    """
    __tablename__ = "payments"
    id = sql_db.Column(sql_db.Integer, primary_key = True, autoincrement = True)
    name = sql_db.Column(sql_db.String, nullable = False)
    practitioners = sql_db.relationship("Practitioner", secondary = practitioner_network_table, back_populates = "payments")  

    def __init__(self, **kwargs):
        """
        Initializes a Payment object
        """
        self.name = kwargs.get("name")

    def simple_serialize(self):
        """
        Simple serializes a payment object
        """
        return {"id" : self.id, "name" : self.name}


