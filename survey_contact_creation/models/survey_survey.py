from odoo import fields, models, api


class Survey(models.Model):
    _inherit = 'survey.survey'

    contact_relation_ids = fields.One2many('contact.relation', 'survey_id', string="Contact Relation")
