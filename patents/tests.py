from django.test import TestCase
from datetime import date
from .models import Patent

class PatentTestCase(TestCase):
    def setUp(self):
        Patent.objects.create(
            reference_id="1234",
            grant_doc_number="5678",
            record_date=date.today(),
            patent_holder_id="ABCD",
            patent_holder="John Smith",
            patent_seller="",
            patent_seller_id="",
            litigation=0,
            tech_field="Software",
            filing_year=date.today(),
            type_patent_holder="Individual",
            patent_quality=8,
            patent_value=7,
            litigation_risk=5,
            country_patent_holder="USA",
            country_patent_seller=""
        )

    def test_search(self):
        results = Patent.search("john")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].patent_holder, "John Smith")




   
