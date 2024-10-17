# -*- coding: utf-8 -*-
from odoo import fields, models


class ContactRelation(models.Model):
    _name = "contact.relation"
    _description = "Contact Relation"

    question_id = fields.Many2one('survey.question')
    contact_field = fields.Selection(
        [('name', 'Name'), ('phone', 'Phone'), ('email', 'Email')], required=True)
    survey_id = fields.Many2one('survey.survey', required=True)
