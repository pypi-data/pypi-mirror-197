from odoo import models, fields

class PhotovoltaicPowerStation(models.Model):
    _inherit = "photovoltaic.power.station"

    tecnical_memory_link = fields.Char(string="Enlace memoria técnica")

    eq_family_consumption = fields.Float(
        string='Consumo equivalente en familia',
        compute='_compute_eq_family_consumption',
        tracking=True)

    def _compute_eq_family_consumption(self):
        for record in self:
            record.eq_family_consumption = sum(record.photovoltaic_power_energy_ids.mapped('eq_family_consum'))
