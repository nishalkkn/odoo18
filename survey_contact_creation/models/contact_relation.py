from odoo import fields,models


class ContactRelation(models.Model):
    _name = "contact.relation"
    _description = "Contact Relation"

    question_id = fields.Many2one('survey.question', required=True)
    contact_id = fields.Many2one('res.partner', required=True)
    survey_id = fields.Many2one('survey.survey', required=True)
