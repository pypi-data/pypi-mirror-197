from datetime import date, datetime, timedelta

from mock import patch

from ....services.contract_process.fiber import FiberContractProcess
from ...helpers import crm_lead_create
from .base_test_contract_process import BaseContractProcessTestCase


@patch("pyopencell.resources.subscription.Subscription.get")
@patch(
    "odoo.addons.somconnexio.models.contract.CRMAccountHierarchyFromContractCreateService"  # noqa
)
class TestFiberContractProcess(BaseContractProcessTestCase):
    def setUp(self):
        super().setUp()
        self.data = {
            "partner_id": self.partner.ref,
            "email": self.partner.email,
            "service_address": self.service_address,
            "service_technology": "Fiber",
            "service_supplier": "Vodafone",
            "vodafone_fiber_contract_service_info": {
                "phone_number": "654123456",
                "vodafone_offer_code": "offer",
                "vodafone_id": "123",
            },
            "fiber_signal_type": "NEBAFTTH",
            "contract_lines": [
                {
                    "product_code": (
                        self.browse_ref("somconnexio.Fibra100Mb").default_code
                    ),
                    "date_start": "2020-01-01 00:00:00",
                }
            ],
            "iban": self.iban,
            "ticket_number": self.ticket_number,
        }

    def test_create_fiber(self, *args):
        content = FiberContractProcess(self.env).create(**self.data)
        contract = self.env["contract.contract"].browse(content["id"])
        self.assertEquals(
            contract.name,
            self.data["vodafone_fiber_contract_service_info"]["phone_number"]
        )

    def test_create_fiber_wo_vodafone_offer_code(self, *args):
        self.data["vodafone_fiber_contract_service_info"]["vodafone_offer_code"] = ""

        content = FiberContractProcess(self.env).create(**self.data)
        contract = self.env["contract.contract"].browse(content["id"])
        self.assertTrue(contract)

    @patch(
        "odoo.addons.somconnexio.services.contract_process.fiber.UnblockMobilePackTicket"  # noqa
    )
    @patch(
        "odoo.addons.somconnexio.services.contract_process.fiber.SetFiberContractCodeMobileTicket"  # noqa
    )
    def test_create_fiber_unblock_mobile_ticket(
        self, SetFiberContractCodeMock, UnblockMobilePackTicketMock, *args
    ):
        pack_code = self.browse_ref(
            "somconnexio.TrucadesIllimitades20GBPack"
        ).default_code
        new_ticket_number = "123454321"
        crm_lead = crm_lead_create(
            self.env, self.partner, "fiber", portability=False, pack=True
        )
        for line in crm_lead.lead_line_ids:
            if line.product_id.default_code == pack_code:
                line.ticket_number = new_ticket_number
            else:
                line.ticket_number = self.ticket_number
        content = FiberContractProcess(self.env).create(**self.data)
        contract = self.env["contract.contract"].browse(content["id"])
        self.assertEquals(
            contract.name,
            self.data["vodafone_fiber_contract_service_info"]["phone_number"]
        )
        activation_date = self._get_activation_date()
        introduced_date = self._get_introduced_date(activation_date)

        UnblockMobilePackTicketMock.assert_called_once_with(
            new_ticket_number,
            activation_date=activation_date.strftime("%Y-%m-%d"),
            introduced_date=introduced_date.strftime("%Y-%m-%d")
        )
        UnblockMobilePackTicketMock.return_value.run.assert_called_once_with()

        SetFiberContractCodeMock.assert_called_once_with(
            new_ticket_number,
            fiber_contract_code=contract.code
        )

    @patch(
        "odoo.addons.somconnexio.services.contract_process.fiber.date",
        spec=["today"],
    )
    @patch(
        "odoo.addons.somconnexio.services.contract_process.fiber.UnblockMobilePackTicket"  # noqa
    )
    @patch(
        "odoo.addons.somconnexio.services.contract_process.fiber.SetFiberContractCodeMobileTicket"  # noqa
    )
    def test_create_fiber_unblock_mobile_ticket_with_holidays(
        self, SetFiberContractCodeMock, UnblockMobilePackTicketMock, MockDate, *args
    ):
        """
        2022-11-11 -> Friday
        + 8 days -> 2022-11-19 -> Saturday
        + 1 days -> 2022-11-20 -> Sunday
        + 1 days -> 2022-11-21 -> Monday (Workday) (Holiday)
        + 1 days -> 2022-11-22 -> Workday
        Introduced day -> 2022-11-22
        """
        MockDate.today.return_value = date(2022, 11, 11)
        hl_year = self.env["hr.holidays.public"].create(
            {
                "year": 2022,
            }
        )
        self.env["hr.holidays.public.line"].create(
            {
                "name": "Holiday Demo",
                "date": date(2022, 11, 21),
                "year_id": hl_year.id,
            },
        )
        self.env["hr.holidays.public.line"].create(
            {
                "name": "Holiday Demo before",
                "date": date(2022, 11, 18),
                "year_id": hl_year.id,
            },
        )

        pack_code = self.browse_ref(
            "somconnexio.TrucadesIllimitades20GBPack"
        ).default_code
        new_ticket_number = "123454321"
        crm_lead = crm_lead_create(
            self.env, self.partner, "fiber", portability=False, pack=True
        )
        for line in crm_lead.lead_line_ids:
            if line.product_id.default_code == pack_code:
                line.ticket_number = new_ticket_number
            else:
                line.ticket_number = self.ticket_number
        content = FiberContractProcess(self.env).create(**self.data)
        contract = self.env["contract.contract"].browse(content["id"])
        self.assertEquals(
            contract.name,
            self.data["vodafone_fiber_contract_service_info"]["phone_number"],
        )
        # 19 and 20 from november 22 are weekend dates, 18 and 22 hoolidays
        UnblockMobilePackTicketMock.assert_called_once_with(
            new_ticket_number,
            activation_date="2022-11-22",
            introduced_date="2022-11-17"
        )
        UnblockMobilePackTicketMock.return_value.run.assert_called_once_with()

        SetFiberContractCodeMock.assert_called_once_with(
            new_ticket_number,
            fiber_contract_code=contract.code
        )

    @patch(
        "odoo.addons.somconnexio.services.contract_process.fiber.UnblockMobilePackTicket"  # noqa
    )
    @patch(
        "odoo.addons.somconnexio.services.contract_process.fiber.SetFiberContractCodeMobileTicket"  # noqa
    )
    def test_create_fiber_unblock_mobile_ticket_without_set_fiber_contract_code(
        self, SetFiberContractCodeMock, UnblockMobilePackTicketMock, *args
    ):
        no_pack_product = self.browse_ref(
            "somconnexio.TrucadesIllimitades20GB"
        )
        new_ticket_number = "123454321"
        crm_lead = crm_lead_create(
            self.env, self.partner, "fiber", portability=False, pack=True
        )
        for line in crm_lead.lead_line_ids:
            if line.is_mobile:
                line.product_id = no_pack_product.id
                line.ticket_number = new_ticket_number
            else:
                line.ticket_number = self.ticket_number

        content = FiberContractProcess(self.env).create(**self.data)
        contract = self.env["contract.contract"].browse(content["id"])
        self.assertEquals(
            contract.name,
            self.data["vodafone_fiber_contract_service_info"]["phone_number"]
        )
        UnblockMobilePackTicketMock.return_value.run.assert_called_once_with()

        SetFiberContractCodeMock.assert_not_called()

    def _get_activation_date(self):
        create_date = date.today()
        activation_date = create_date + timedelta(days=8)
        while not activation_date.weekday() < 5:  # 5 Sat, 6 Sun
            activation_date = activation_date + timedelta(days=1)
        return activation_date

    def _get_introduced_date(self, activation_date):
        introduced_date = activation_date - timedelta(days=2)
        while not introduced_date.weekday() < 5:  # 5 Sat, 6 Sun
            introduced_date = introduced_date - timedelta(days=1)
        return introduced_date

    def test_create_fiber_relate_with_mobile_pack(self, *args):
        # Crear un Contrato de mobil
        contract_product = self.env.ref("somconnexio.TrucadesIllimitades20GBPack")
        mobile_contract_service_info = self.env["mobile.service.contract.info"].create(
            {"phone_number": "654987654", "icc": "123"}
        )
        contract_line = {
            "name": contract_product.name,
            "product_id": contract_product.id,
            "date_start": datetime.now() - timedelta(days=12),
        }
        vals_contract = {
            "name": "Test Contract Mobile",
            "code": "12345",
            "partner_id": self.partner.id,
            "invoice_partner_id": self.partner.id,
            "service_technology_id": self.ref("somconnexio.service_technology_mobile"),
            "service_supplier_id": self.ref("somconnexio.service_supplier_masmovil"),
            "mobile_contract_service_info_id": mobile_contract_service_info.id,
            "contract_line_ids": [(0, 0, contract_line)],
            "email_ids": [(6, 0, [self.partner.id])],
        }
        mobile_contract = self.env["contract.contract"].create(vals_contract)

        # Añadir al data el contrato vinculado
        data = self.data.copy()
        data["mobile_pack_contracts"] = mobile_contract.code

        content = FiberContractProcess(self.env).create(**data)
        contract = self.env["contract.contract"].browse(content["id"])

        # Revisar que el contrato de fibra tiene como childs al contrato de mobil
        self.assertEquals(
            mobile_contract,
            contract.children_pack_contract_ids,
        )
