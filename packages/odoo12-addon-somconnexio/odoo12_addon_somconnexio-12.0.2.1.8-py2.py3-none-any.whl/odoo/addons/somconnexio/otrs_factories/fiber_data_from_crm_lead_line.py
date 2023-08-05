from otrs_somconnexio.otrs_models.fiber_data import FiberData

from .broadband_data_from_crm_lead_line import BroadbandDataFromCRMLeadLine


class FiberDataFromCRMLeadLine(BroadbandDataFromCRMLeadLine):

    def build(self):
        fiber_data = super().build()
        fiber_data.update({
            "previous_contract_pon": self.isp_info.previous_contract_pon,
            "previous_contract_fiber_speed": self._previous_contract_fiber_speed(
                self.isp_info.previous_contract_fiber_speed),
            "mobile_pack_contracts": self._mobile_pack_contracts(
                self.isp_info.mobile_pack_contracts
            ),
            "all_grouped_SIMS_recieved": self._have_all_grouped_mbl_SIMS(),
            "has_grouped_mobile_with_previous_owner": (
                self._has_grouped_mobile_with_previous_owner()
            ),
            "technology": fiber_data.get("technology") or "Fibra"
        })
        return FiberData(**fiber_data)

    def _previous_contract_fiber_speed(self, value):
        if value:
            return value.replace(" ", "")
        else:
            return ""

    def _mobile_pack_contracts(self, value):
        return ",".join(code for code in value.mapped("code")) if value else ""

    def _have_all_grouped_mbl_SIMS(self):
        grouped_mobiles_sims_recieved = \
            self.crm_lead_line.lead_id.lead_line_ids.filtered(
                'is_mobile').mapped('mobile_isp_info_has_sim')
        if (grouped_mobiles_sims_recieved
                and all(grouped_mobiles_sims_recieved)):
            return True
        return False

    def _has_grouped_mobile_with_previous_owner(self):
        previous_owners = \
            self.crm_lead_line.lead_id.lead_line_ids.filtered(
                'is_mobile').mapped('mobile_isp_info').mapped(
                    'previous_owner_vat_number')
        if any(previous_owners):
            return True
        return False
