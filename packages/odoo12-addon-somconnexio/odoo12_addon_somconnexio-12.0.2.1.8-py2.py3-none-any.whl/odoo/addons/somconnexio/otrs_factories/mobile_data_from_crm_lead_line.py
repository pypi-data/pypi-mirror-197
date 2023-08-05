from otrs_somconnexio.otrs_models.mobile_data import MobileData

from .base_data_from_crm_lead_line import BaseDataFromCRMLeadLine


class MobileDataFromCRMLeadLine(BaseDataFromCRMLeadLine):

    def __init__(self, crm_lead_line):
        super().__init__(crm_lead_line)
        self.isp_info = crm_lead_line.mobile_isp_info

    def build(self):
        mbl_data = super().build()
        mbl_data.update({
            "phone_number": self.isp_info.phone_number,
            "sc_icc": self.isp_info.icc,
            "icc": self.isp_info.icc_donor,
            "has_sim": self.isp_info.has_sim,
            "delivery_street": self.isp_info.delivery_street,
            "delivery_zip_code": self.isp_info.delivery_zip_code,
            "delivery_city": self.isp_info.delivery_city,
            "delivery_state": self.isp_info.delivery_state_id.name,
            "is_grouped_with_fiber": self._has_lead_fiber_service(),
            "technology": mbl_data.get("technology") or "Mobil",
            "fiber_linked": self._get_fiber_code(),
            "sim_delivery_tracking_code": (
                self.crm_lead_line.lead_id.correos_tracking_code
            )
        })
        return MobileData(**mbl_data)

    def _has_lead_fiber_service(self):
        """
        Mobile lead lines from a CRMLead altogether
        with a fiber service
        returns: bool
        """
        lead = self.crm_lead_line.lead_id
        return bool(lead.lead_line_ids.filtered(
            lambda lead_line: lead_line.is_fiber
        ))

    def _get_fiber_code(self):
        if self.isp_info.linked_fiber_contract_id:
            return self.isp_info.linked_fiber_contract_id.code
        return ""
