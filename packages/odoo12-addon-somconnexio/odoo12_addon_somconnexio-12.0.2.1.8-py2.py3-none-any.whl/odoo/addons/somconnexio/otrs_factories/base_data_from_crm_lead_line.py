class BaseDataFromCRMLeadLine():

    def __init__(self, crm_lead_line):
        self.crm_lead_line = crm_lead_line

    def build(self):
        return {
            "order_id": self.crm_lead_line.id,
            "previous_provider": self.isp_info.previous_provider.code or 'None',
            "previous_owner_vat": self.isp_info.previous_owner_vat_number or '',
            "previous_owner_name": self.isp_info.previous_owner_first_name or '',
            "previous_owner_surname": self.isp_info.previous_owner_name or '',
            "notes": self.crm_lead_line.lead_id.description,
            "iban": self.crm_lead_line.lead_id.iban,
            "email": self.crm_lead_line.lead_id.email_from,
            "product": self.crm_lead_line.product_id.default_code,
            "type": self.isp_info.type,
            "technology": self._get_lead_technology(),
        }

    def _get_lead_technology(self):
        are_lead_lines_mobile = self.crm_lead_line.lead_id.lead_line_ids.mapped(
            'is_mobile')

        if (any(are_lead_lines_mobile) and
                not all(are_lead_lines_mobile)):
            return "Mixta"
        return ""
