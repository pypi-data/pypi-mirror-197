from ..sc_test_case import SCTestCase


class TestProductTemplate(SCTestCase):

    def test_product_template_root_categ_mobile(self):
        product = self.browse_ref('somconnexio.100MinSenseDades')
        self.assertEquals(
            product.root_categ_id, self.browse_ref('somconnexio.mobile_service')
        )

    def test_product_template_root_categ_ba(self):
        product = self.browse_ref('somconnexio.Fibra100Mb')
        self.assertEquals(
            product.root_categ_id, self.browse_ref('somconnexio.broadband_service')
        )
