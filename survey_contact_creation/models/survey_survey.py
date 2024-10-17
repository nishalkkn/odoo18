# -*- coding: utf-8 -*-
from odoo import fields, models


class Survey(models.Model):
    _inherit = 'survey.survey'

    contact_relation_ids = fields.One2many('contact.relation', 'survey_id', string="Contact Relation")


class SurveyUserInput(models.Model):
    _inherit = 'survey.user_input'

    def _mark_done(self):
        res = super(SurveyUserInput, self)._mark_done()
        user_input_line = self.env['survey.user_input.line'].search([('user_input_id', '=', self.id)])
        user_input = {self.env['contact.relation'].search(
            [('question_id', '=', rec.question_id.id)]).contact_field: rec.value_char_box for rec in user_input_line}
        if user_input['name']:
            user_input['from_survey'] = True
            self.env['res.partner'].sudo().create(user_input)
        return res
