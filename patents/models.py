from django.db import models
from pyArango.connection import Connection
from django.core.validators import MinValueValidator, MaxValueValidator

    
class Patent(models.Model):
    reference_id = models.CharField(max_length=20)
    grant_doc_number = models.CharField(max_length=20)
    record_date = models.DateField()
    patent_holder_id = models.CharField(max_length=20)
    patent_holder = models.CharField(max_length=200)
    patent_seller = models.CharField(max_length=200, blank=True)
    patent_seller_id = models.CharField(max_length=20, blank=True)
    litigation = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    tech_field = models.CharField(max_length=200)
    filing_year = models.DateField()
    type_patent_holder = models.CharField(max_length=200)
    patent_quality = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    patent_value = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    litigation_risk = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    country_patent_holder = models.CharField(max_length=200)
    country_patent_seller = models.CharField(max_length=200, blank=True)
    
    @classmethod
    def search(cls, query):
        conn = Connection(username="patentsearch", password="*Pase00*")
        db = conn["patentrecord"] 
        collection = db["patentcollection"] ## collection name
        print(query) ##time to debug
        results = collection.fetchByExample({
            "patent_holder": {"$regex": query, "$options": "i"}
        })
        return [cls(reference_id=result["refernce_id"], grant_doc_number=result["grant_doc_number"],
            record_date=result["record_date"], patent_holder_id=result["patent_holder_id"],
            patent_holder=result["patent_holder"], patent_seller=result["patent_seller"],
            patent_seller_id=result["patent_seller_id"], litigation=result["litigation"],
            tech_field=result["tech_field"], filing_year=result["filing_year"],
            type_patent_holder=result["type_patent_holder"], patent_quality=result["patent_quality"],
            patent_value=result["patent_value"], litigation_risk=result["litigation_risk"],
            country_patent_holder=result["country_patent_holder"], country_patent_seller=result["country_patent_seller"])
        for result in results]
    






    

