from odoo import fields, models


class Survey(models.Model):
    _inherit = 'survey.survey'

    contact_relation_ids = fields.One2many('contact.relation', 'survey_id', string="Contact Relation")


class SurveyUserInput(models.Model):
    _inherit = 'survey.user_input'

    def _mark_done(self):
        res = super(SurveyUserInput, self)._mark_done()
        user_input = {}
        contact_relation = []
        var = self.env['survey.user_input.line'].search([('user_input_id', '=', self.id)])
        for rec in var:
            contact_field = rec.env['contact.relation'].search([('question_id', '=', rec.question_id.id)]).contact_field
            user_input[contact_field] = rec.value_char_box
            contact_relation.append(contact_field)
        if 'name' in contact_relation:
            user_input['from_survey'] = True
            self.env['res.partner'].sudo().create(user_input)
        return res
