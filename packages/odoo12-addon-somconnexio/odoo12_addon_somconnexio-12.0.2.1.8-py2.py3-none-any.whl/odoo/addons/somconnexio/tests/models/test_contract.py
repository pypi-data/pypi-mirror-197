from datetime import datetime, timedelta

from mock import Mock, patch
from odoo.exceptions import ValidationError

from ...helpers.date import date_to_str, first_day_next_month
from ..sc_test_case import SCComponentTestCase


@patch("odoo.addons.somconnexio.models.res_partner.SomOfficeUser")
@patch("odoo.addons.somconnexio.models.contract.OpenCellConfiguration")
@patch("odoo.addons.somconnexio.models.contract.SubscriptionService")
@patch("odoo.addons.somconnexio.models.contract.CRMAccountHierarchyFromContractCreateService")  # noqa
@patch("odoo.addons.somconnexio.models.contract.CRMAccountHierarchyFromContractUpdateService")  # noqa
class TestContract(SCComponentTestCase):

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.Contract = self.env['contract.contract']
        self.product_1 = self.env.ref('product.product_product_1')
        self.router_product = self.env['product.product'].search(
            [
                ("default_code", "=", "NCDS224WTV"),
            ]
        )
        self.router_lot = self.env['stock.production.lot'].create({
            'product_id': self.router_product.id,
            'name': '123',
            'router_mac_address': '12:BB:CC:DD:EE:90'
        })
        self.mobile_contract_service_info = self.env[
            'mobile.service.contract.info'
        ].create({
            'phone_number': '654987654',
            'icc': '123'
        })
        self.adsl_contract_service_info = self.env[
            'adsl.service.contract.info'
        ].create({
            'phone_number': '654987654',
            'administrative_number': '123',
            'router_product_id': self.router_product.id,
            'router_lot_id': self.router_lot.id,
            'ppp_user': 'ringo',
            'ppp_password': 'rango',
            'endpoint_user': 'user',
            'endpoint_password': 'password'
        })
        self.vodafone_fiber_contract_service_info = self.env[
            'vodafone.fiber.service.contract.info'
        ].create({
            'phone_number': '654321123',
            'vodafone_id': '123',
            'vodafone_offer_code': '456',
        })
        self.partner = self.browse_ref('somconnexio.res_partner_2_demo')
        self.service_partner = self.env['res.partner'].create({
            'parent_id': self.partner.id,
            'name': 'Service partner',
            'type': 'service'
        })

    def test_service_contact_wrong_type(self, *args):
        partner_id = self.partner.id
        service_partner = self.env['res.partner'].create({
            'parent_id': partner_id,
            'name': 'Partner not service'
        })
        vals_contract = {
            'name': 'Test Contract Broadband',
            'partner_id': partner_id,
            'service_partner_id': service_partner.id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref(
                "somconnexio.service_technology_adsl"
            ),
            "service_supplier_id": self.ref(
                "somconnexio.service_supplier_jazztel"
            ),
            'adsl_service_contract_info_id': (
                self.adsl_contract_service_info.id
            ),
            'bank_id': self.partner.bank_ids.id
        }
        self.assertRaises(
            ValidationError,
            self.env['contract.contract'].create,
            (vals_contract,)
        )

    def test_service_contact_right_type(self, *args):
        partner_id = self.partner.id
        vals_contract = {
            'name': 'Test Contract Broadband',
            'partner_id': partner_id,
            'service_partner_id': self.service_partner.id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref(
                "somconnexio.service_technology_fiber"
            ),
            'service_supplier_id': self.ref(
                "somconnexio.service_supplier_vodafone"
            ),
            'vodafone_fiber_service_contract_info_id': (
                self.vodafone_fiber_contract_service_info.id
            ),
            'bank_id': self.partner.bank_ids.id
        }
        self.assertTrue(self.env['contract.contract'].create(vals_contract))

    def test_contact_without_code(self, *args):
        partner_id = self.partner.id
        vals_contract = {
            'name': 'Test Contract Broadband',
            'partner_id': partner_id,
            'service_partner_id': self.service_partner.id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref(
                "somconnexio.service_technology_fiber"
            ),
            'service_supplier_id': self.ref(
                "somconnexio.service_supplier_vodafone"
            ),
            'vodafone_fiber_service_contract_info_id': (
                self.vodafone_fiber_contract_service_info.id
            ),
            'bank_id': self.partner.bank_ids.id
        }
        contract_code = self.browse_ref(
            'somconnexio.sequence_contract'
        ).number_next_actual
        contract = self.env['contract.contract'].create(vals_contract)
        self.assertEquals(contract.code, str(contract_code))

    def test_contact_with_empty_code_manual_UI_creation(self, *args):
        partner_id = self.partner.id
        vals_contract = {
            'code': False,
            'name': 'Test Contract Broadband',
            'partner_id': partner_id,
            'service_partner_id': self.service_partner.id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref(
                "somconnexio.service_technology_fiber"
            ),
            'service_supplier_id': self.ref(
                "somconnexio.service_supplier_vodafone"
            ),
            'vodafone_fiber_service_contract_info_id': (
                self.vodafone_fiber_contract_service_info.id
            ),
            'bank_id': self.partner.bank_ids.id
        }
        contract_code = self.browse_ref(
            'somconnexio.sequence_contract'
        ).number_next_actual
        contract = self.env['contract.contract'].create(vals_contract)
        self.assertEquals(contract.code, str(contract_code))

    def test_contact_with_code(self, *args):
        partner_id = self.partner.id
        vals_contract = {
            'code': 1234,
            'name': 'Test Contract Broadband',
            'partner_id': partner_id,
            'service_partner_id': self.service_partner.id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref(
                "somconnexio.service_technology_fiber"
            ),
            'service_supplier_id': self.ref(
                "somconnexio.service_supplier_vodafone"
            ),
            'vodafone_fiber_service_contract_info_id': (
                self.vodafone_fiber_contract_service_info.id
            ),
            'bank_id': self.partner.bank_ids.id
        }
        contract = self.env['contract.contract'].create(vals_contract)
        self.assertEquals(contract.code, '1234')

    def test_service_contact_wrong_parent(self, *args):
        partner_id = self.partner.id
        service_partner = self.env['res.partner'].create({
            'parent_id': self.ref('somconnexio.res_partner_1_demo'),
            'name': 'Partner wrong parent',
            'type': 'service'
        })
        vals_contract = {
            'name': 'Test Contract Broadband',
            'partner_id': partner_id,
            'service_partner_id': service_partner.id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref(
                "somconnexio.service_technology_adsl"
            ),
            'adsl_service_contract_info_id': (
                self.adsl_contract_service_info.id
            ),
            'service_supplier_id': self.ref(
                'somconnexio.service_supplier_jazztel'
            ),
            'bank_id': self.partner.bank_ids.id
        }
        self.assertRaises(
            ValidationError,
            self.env['contract.contract'].create,
            (vals_contract,)
        )

    def test_service_contact_wrong_parent_not_broadband(self, *args):
        partner_id = self.partner.id
        service_partner = self.env['res.partner'].create({
            'parent_id': self.ref('somconnexio.res_partner_1_demo'),
            'name': 'Partner wrong parent',
            'type': 'service'
        })
        vals_contract = {
            'name': 'Test Contract Mobile',
            'partner_id': partner_id,
            'service_partner_id': service_partner.id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref("somconnexio.service_technology_mobile"),
            'service_supplier_id': self.ref("somconnexio.service_supplier_masmovil"),
            'mobile_contract_service_info_id': self.mobile_contract_service_info.id,
            'bank_id': self.partner.bank_ids.id
        }
        self.assertTrue(self.env['contract.contract'].create(vals_contract))

    def test_service_contact_wrong_type_not_broadband(self, *args):
        partner_id = self.partner.id
        service_partner = self.env['res.partner'].create({
            'parent_id': partner_id,
            'name': 'Partner not service'
        })
        vals_contract = {
            'name': 'Test Contract Mobile',
            'partner_id': partner_id,
            'service_partner_id': service_partner.id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref("somconnexio.service_technology_mobile"),
            'service_supplier_id': self.ref("somconnexio.service_supplier_masmovil"),
            'mobile_contract_service_info_id': self.mobile_contract_service_info.id,
            'bank_id': self.partner.bank_ids.id
        }
        self.assertTrue(self.env['contract.contract'].create(vals_contract))

    def test_email_not_partner_not_child_wrong_type(self, *args):
        partner_id = self.partner.id
        wrong_email = self.env['res.partner'].create({
            'name': 'Bad email',
            'email': 'hello@example.com'
        })
        vals_contract = {
            'name': 'Test Contract Mobile',
            'partner_id': partner_id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref("somconnexio.service_technology_mobile"),
            'service_supplier_id': self.ref("somconnexio.service_supplier_masmovil"),
            'mobile_contract_service_info_id': self.mobile_contract_service_info.id,
            'bank_id': self.partner.bank_ids.id,
            'email_ids': [(6, 0, [wrong_email.id])]
        }
        self.assertRaises(
            ValidationError,
            self.env['contract.contract'].create,
            (vals_contract,)
        )

    def test_email_not_partner_not_child_right_type(self, *args):
        partner_id = self.partner.id
        wrong_email = self.env['res.partner'].create({
            'name': 'Bad email',
            'email': 'hello@example.com',
            'type': 'contract-email',
        })
        vals_contract = {
            'name': 'Test Contract Mobile',
            'partner_id': partner_id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref("somconnexio.service_technology_mobile"),
            'service_supplier_id': self.ref("somconnexio.service_supplier_masmovil"),
            'mobile_contract_service_info_id': self.mobile_contract_service_info.id,
            'bank_id': self.partner.bank_ids.id,
            'email_ids': [(6, 0, [wrong_email.id])]
        }
        self.assertRaises(
            ValidationError,
            self.env['contract.contract'].create,
            (vals_contract,)
        )

    def test_email_same_partner_not_contract_email_type(self, *args):
        partner_id = self.partner.id
        vals_contract = {
            'name': 'Test Contract Mobile',
            'partner_id': partner_id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref("somconnexio.service_technology_mobile"),
            'service_supplier_id': self.ref("somconnexio.service_supplier_masmovil"),
            'mobile_contract_service_info_id': self.mobile_contract_service_info.id,
            'bank_id': self.partner.bank_ids.id,
            'email_ids': [(6, 0, [partner_id])]
        }
        self.assertTrue(self.env['contract.contract'].create(vals_contract))

    def test_email_child_partner_wrong_type(self, *args):
        partner_id = self.partner.id
        child_email = self.env['res.partner'].create({
            'name': 'Bad email',
            'email': 'hello@example.com',
            'parent_id': partner_id,
            'type': 'delivery'
        })
        vals_contract = {
            'name': 'Test Contract Mobile',
            'partner_id': partner_id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref("somconnexio.service_technology_mobile"),
            'service_supplier_id': self.ref("somconnexio.service_supplier_masmovil"),
            'mobile_contract_service_info_id': self.mobile_contract_service_info.id,
            'bank_id': self.partner.bank_ids.id,
            'email_ids': [(6, 0, [child_email.id])]
        }
        self.assertRaises(
            ValidationError,
            self.env['contract.contract'].create,
            (vals_contract,)
        )

    def test_email_child_partner_right_type(self, *args):
        partner_id = self.partner.id
        child_email = self.env['res.partner'].create({
            'name': 'Right email',
            'email': 'hello@example.com',
            'parent_id': partner_id,
            'type': 'contract-email'
        })
        vals_contract = {
            'name': 'Test Contract Mobile',
            'partner_id': partner_id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref("somconnexio.service_technology_mobile"),
            'service_supplier_id': self.ref("somconnexio.service_supplier_masmovil"),
            'mobile_contract_service_info_id': self.mobile_contract_service_info.id,
            'bank_id': self.partner.bank_ids.id,
            'email_ids': [(6, 0, [child_email.id])]
        }
        self.assertTrue(self.env['contract.contract'].create(vals_contract))

    def test_contact_create_call_opencell_integration(
            self,
            _,
            CRMAccountHierarchyFromContractCreateServiceMock,
            __,
            OpenCellConfigurationMock,
            ___):
        partner_id = self.partner.id
        vals_contract = {
            'name': 'Test Contract Broadband',
            'partner_id': partner_id,
            'service_partner_id': self.service_partner.id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref(
                "somconnexio.service_technology_fiber"
            ),
            'service_supplier_id': self.ref(
                "somconnexio.service_supplier_vodafone"
            ),
            'vodafone_fiber_service_contract_info_id': (
                self.vodafone_fiber_contract_service_info.id
            ),
            'bank_id': self.partner.bank_ids.id
        }
        CRMAccountHierarchyFromContractCreateServiceMock.return_value = Mock(spec=["run"])  # noqa
        OpenCellConfigurationMock.return_value = object

        contract = self.env['contract.contract'].create(vals_contract)

        CRMAccountHierarchyFromContractCreateServiceMock.assert_called_once_with(
            contract,
            OpenCellConfigurationMock.return_value
        )
        CRMAccountHierarchyFromContractCreateServiceMock.return_value.run.assert_called_once_with(  # noqa
            force=False)

    def test_sequence_in_creation(self, *args):
        partner_id = self.partner.id
        child_email = self.env['res.partner'].create({
            'name': 'Right email',
            'email': 'hello@example.com',
            'parent_id': partner_id,
            'type': 'contract-email'
        })
        vals_contract = {
            'name': 'Test Contract Mobile',
            'partner_id': partner_id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref("somconnexio.service_technology_mobile"),
            'service_supplier_id': self.ref("somconnexio.service_supplier_masmovil"),
            'mobile_contract_service_info_id': self.mobile_contract_service_info.id,
            'bank_id': self.partner.bank_ids.id,
            'email_ids': [(6, 0, [child_email.id])]
        }
        contract_code = self.browse_ref(
            'somconnexio.sequence_contract'
        ).number_next_actual
        contract = self.env['contract.contract'].create(vals_contract)
        self.assertEquals(contract.code, str(contract_code))

    def test_code_in_creation(self, *args):
        partner_id = self.partner.id
        child_email = self.env['res.partner'].create({
            'name': 'Right email',
            'email': 'hello@example.com',
            'parent_id': partner_id,
            'type': 'contract-email'
        })
        vals_contract = {
            'code': '1234',
            'name': 'Test Contract Mobile',
            'partner_id': partner_id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref("somconnexio.service_technology_mobile"),
            'service_supplier_id': self.ref("somconnexio.service_supplier_masmovil"),
            'mobile_contract_service_info_id': self.mobile_contract_service_info.id,
            'bank_id': self.partner.bank_ids.id,
            'email_ids': [(6, 0, [child_email.id])]
        }
        contract = self.env['contract.contract'].create(vals_contract)
        self.assertEquals(contract.code, '1234')

    def test_set_previous_id_vodafone(self, *args):
        partner_id = self.partner.id
        vals_contract = {
            'code': '1234',
            'name': 'Test Contract Vodafone Fiber',
            'partner_id': partner_id,
            'service_partner_id': self.service_partner.id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref("somconnexio.service_technology_fiber"),
            'service_supplier_id': self.ref("somconnexio.service_supplier_vodafone"),
            'vodafone_fiber_service_contract_info_id': (
                self.vodafone_fiber_contract_service_info.id
            ),
            'bank_id': self.partner.bank_ids.id,
        }
        contract = self.env['contract.contract'].create(vals_contract)
        contract.previous_id = 'vf123'
        self.assertEquals(
            self.vodafone_fiber_contract_service_info.previous_id,
            'vf123'
        )

    def test_set_vodafone_id_in_submodel(self, *args):
        partner_id = self.partner.id
        vals_contract = {
            'code': '1234',
            'name': 'Test Contract Vodafone Fiber',
            'partner_id': partner_id,
            'service_partner_id': self.service_partner.id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref("somconnexio.service_technology_fiber"),
            'service_supplier_id': self.ref("somconnexio.service_supplier_vodafone"),
            'vodafone_fiber_service_contract_info_id': (
                self.vodafone_fiber_contract_service_info.id
            ),
            'bank_id': self.partner.bank_ids.id,
        }
        contract = self.env['contract.contract'].create(vals_contract)
        self.vodafone_fiber_contract_service_info.vodafone_id = 'vf123'
        self.assertEquals(
            contract.vodafone_id,
            'vf123'
        )

    def test_set_vodafone_offer_code_in_submodel(self, *args):
        partner_id = self.partner.id
        vals_contract = {
            'code': '1234',
            'name': 'Test Contract Vodafone Fiber',
            'partner_id': partner_id,
            'service_partner_id': self.service_partner.id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref("somconnexio.service_technology_fiber"),
            'service_supplier_id': self.ref("somconnexio.service_supplier_vodafone"),
            'vodafone_fiber_service_contract_info_id': (
                self.vodafone_fiber_contract_service_info.id
            ),
            'bank_id': self.partner.bank_ids.id,
        }
        contract = self.env['contract.contract'].create(vals_contract)
        self.vodafone_fiber_contract_service_info.vodafone_offer_code = 'vf123'
        self.assertEquals(
            contract.vodafone_offer_code,
            'vf123'
        )

    def test_set_previous_id_and_name_and_icc_router_4G(self, *args):
        partner_id = self.partner.id
        router_4g_service_contract_info = self.env[
            'router.4g.service.contract.info'
        ].create({
            'vodafone_id': 'VD123',
            'vodafone_offer_code': '456',
            'icc': '2222'
        })
        vals_contract = {
            'code': '1234',
            'name': 'Test Contract Vodafone Fiber',
            'partner_id': partner_id,
            'service_partner_id': self.service_partner.id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref(
                "somconnexio.service_technology_4G"),
            'service_supplier_id': self.ref("somconnexio.service_supplier_vodafone"),
            'router_4G_service_contract_info_id': (
                router_4g_service_contract_info.id
            ),
        }
        contract = self.env['contract.contract'].create(vals_contract)

        self.assertFalse(contract.previous_id)
        self.assertEquals(contract.icc, '2222')
        contract.previous_id = 'vf123'
        contract.icc = '333'
        self.assertEquals(
            router_4g_service_contract_info.previous_id,
            'vf123'
        )
        self.assertEquals(
            router_4g_service_contract_info.icc,
            '333'
        )
        self.assertEquals(contract.name, '-')

    def test_set_previous_id_masmovil(self, *args):
        partner_id = self.partner.id
        masmovil_fiber_contract_service_info = self.env[
            'mm.fiber.service.contract.info'
        ].create({
            'phone_number': '654321123',
            'mm_id': '123',
        })
        vals_contract = {
            'code': '1234',
            'name': 'Test Contract Mas Movil Fiber',
            'partner_id': partner_id,
            'invoice_partner_id': partner_id,
            'service_partner_id': self.service_partner.id,
            'service_technology_id': self.ref("somconnexio.service_technology_fiber"),
            'service_supplier_id': self.ref("somconnexio.service_supplier_masmovil"),
            'mm_fiber_service_contract_info_id': (
                masmovil_fiber_contract_service_info.id
            ),
            'bank_id': self.partner.bank_ids.id,
        }
        contract = self.env['contract.contract'].create(vals_contract)
        contract.previous_id = 'mm123'
        self.assertEquals(masmovil_fiber_contract_service_info.previous_id, 'mm123')

    def test_set_previous_id_adsl(self, *args):
        partner_id = self.partner.id
        vals_contract = {
            'name': 'Test Contract Broadband',
            'partner_id': partner_id,
            'service_partner_id': self.service_partner.id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref(
                "somconnexio.service_technology_adsl"
            ),
            'adsl_service_contract_info_id': (
                self.adsl_contract_service_info.id
            ),
            'service_supplier_id': self.ref(
                'somconnexio.service_supplier_jazztel'
            ),
            'bank_id': self.partner.bank_ids.id,
        }
        contract = self.env['contract.contract'].create(vals_contract)
        contract.previous_id = 'adsl123'
        self.assertEquals(self.adsl_contract_service_info.previous_id, 'adsl123')

    def test_set_previous_id_xoln(self, *args):
        partner_id = self.partner.id
        xoln_fiber_service_contract_info = self.env[
            'xoln.fiber.service.contract.info'
        ].create({
            'phone_number': '654321123',
            'external_id': '123',
            'project': 'laBorda',
            'id_order': '456',
            'router_product_id': self.router_product.id,
            'router_lot_id': self.router_lot.id,
        })
        vals_contract = {
            'name': 'Test Contract Broadband',
            'partner_id': partner_id,
            'service_partner_id': self.service_partner.id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref(
                "somconnexio.service_technology_fiber"
            ),
            'xoln_fiber_service_contract_info_id': (
                xoln_fiber_service_contract_info.id
            ),
            'service_supplier_id': self.ref(
                'somconnexio.service_supplier_xoln'
            ),
            'bank_id': self.partner.bank_ids.id,
        }
        contract = self.env['contract.contract'].create(vals_contract)
        contract.previous_id = 'xoln123'
        self.assertEquals(xoln_fiber_service_contract_info.previous_id, 'xoln123')

    def test_set_icc_mobile(self, *args):
        partner_id = self.partner.id
        mobile_service_contract_info = self.env[
            'mobile.service.contract.info'
        ].create({
            'phone_number': '654321123',
            'icc': '123',
        })
        vals_contract = {
            'name': 'Test Contract Mobile',
            'partner_id': partner_id,
            'service_partner_id': self.service_partner.id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref(
                "somconnexio.service_technology_mobile"
            ),
            'mobile_contract_service_info_id': (
                mobile_service_contract_info.id
            ),
            'service_supplier_id': self.ref(
                'somconnexio.service_supplier_masmovil'
            )
        }
        contract = self.env['contract.contract'].create(vals_contract)
        self.assertEquals(contract.icc, '123')
        contract.icc = '333'
        self.assertEquals(mobile_service_contract_info.icc, '333')

    def adsl_contract_service_info_wo_phone_number(self, *args):
        adsl_contract_service_info = self.env[
            'adsl.service.contract.info'
        ].create({
            'administrative_number': '123',
            'router_product_id': self.router_product.id,
            'router_lot_id': self.router_lot.id,
            'ppp_user': 'ringo',
            'ppp_password': 'rango',
            'endpoint_user': 'user',
            'endpoint_password': 'password'
        })
        self.assertEqual(adsl_contract_service_info.phone_number, '-')

    def test_children_pack_contract_ids(self, *args):
        partner_id = self.partner.id
        vals_contract = {
            'name': 'Test Contract Broadband',
            'partner_id': partner_id,
            'service_partner_id': self.service_partner.id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref(
                "somconnexio.service_technology_fiber"
            ),
            'service_supplier_id': self.ref(
                "somconnexio.service_supplier_vodafone"
            ),
            'vodafone_fiber_service_contract_info_id': (
                self.vodafone_fiber_contract_service_info.id
            ),
            'bank_id': self.partner.bank_ids.id
        }
        parent_contract = self.env['contract.contract'].create(vals_contract)
        vals_contract['parent_pack_contract_id'] = parent_contract.id
        contract = self.env['contract.contract'].create(vals_contract)
        self.assertEquals(contract.parent_pack_contract_id, parent_contract)
        self.assertEquals(parent_contract.children_pack_contract_ids, contract)
        self.assertEquals(parent_contract.number_contracts_in_pack, 2)
        self.assertTrue(parent_contract.has_vinculated_contracts)
        self.assertTrue(contract.has_vinculated_contracts)
        self.assertTrue(contract.is_pack)
        self.assertTrue(parent_contract.is_pack)

    def test_not_pack_contract_id(self, *args):
        partner_id = self.partner.id
        vals_contract = {
            'name': 'Test Contract Broadband',
            'partner_id': partner_id,
            'service_partner_id': self.service_partner.id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref(
                "somconnexio.service_technology_fiber"
            ),
            'service_supplier_id': self.ref(
                "somconnexio.service_supplier_vodafone"
            ),
            'vodafone_fiber_service_contract_info_id': (
                self.vodafone_fiber_contract_service_info.id
            ),
        }
        contract = self.env['contract.contract'].create(vals_contract)
        self.assertFalse(contract.parent_pack_contract_id)
        self.assertEquals(contract.number_contracts_in_pack, 0)
        self.assertFalse(contract.has_vinculated_contracts)
        self.assertFalse(contract.is_pack)

    @patch("odoo.addons.somconnexio.models.contract.ChangeTariffTicket")
    def test_break_contracts_in_pack(self, MockChangeTariffTicket, *args):
        partner_id = self.partner.id
        parent_contract_product = self.env.ref("somconnexio.Fibra100Mb")
        parent_contract_line = {
            "name": parent_contract_product.name,
            "product_id": parent_contract_product.id,
            "date_start": datetime.now() - timedelta(days=12),
        }
        parent_vals_contract = {
            'name': 'Test Contract Broadband',
            'partner_id': partner_id,
            'service_partner_id': self.service_partner.id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref(
                "somconnexio.service_technology_fiber"
            ),
            'service_supplier_id': self.ref(
                "somconnexio.service_supplier_vodafone"
            ),
            'vodafone_fiber_service_contract_info_id': (
                self.vodafone_fiber_contract_service_info.id
            ),
            "contract_line_ids": [(0, 0, parent_contract_line)],
        }
        parent_contract = self.env["contract.contract"].create(parent_vals_contract)
        contract_product = self.env.ref("somconnexio.TrucadesIllimitades20GBPack")
        contract_line = {
            "name": contract_product.name,
            "product_id": contract_product.id,
            "date_start": datetime.now() - timedelta(days=12),
        }
        vals_contract = {
            'name': 'Test Contract Mobile',
            'partner_id': partner_id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref("somconnexio.service_technology_mobile"),
            'service_supplier_id': self.ref("somconnexio.service_supplier_masmovil"),
            'mobile_contract_service_info_id': self.mobile_contract_service_info.id,
            "contract_line_ids": [(0, 0, contract_line)],
            "email_ids": [(6, 0, [self.partner.id])],
        }
        contract = self.env["contract.contract"].create(vals_contract)
        contract.parent_pack_contract_id = parent_contract.id

        self.assertTrue(parent_contract.is_pack)
        self.assertTrue(contract.is_pack)

        parent_contract.break_packs()

        self.assertFalse(parent_contract.is_pack)
        self.assertFalse(contract.is_pack)

        MockChangeTariffTicket.assert_called_once_with(
            self.partner.vat,
            self.partner.ref,
            {
                "phone_number": contract.phone_number,
                "new_product_code": self.env.ref(
                    "somconnexio.TrucadesIllimitades20GB"
                ).default_code,
                "current_product_code": contract.current_tariff_product.default_code,  # noqa
                "effective_date": date_to_str(first_day_next_month()),
                "fiber_linked": "",
                "subscription_email": self.partner.email,
                "language": self.partner.lang,
            },
        )
        MockChangeTariffTicket.return_value.create.assert_called_once()
