from odoo import fields, models, api


class Survey(models.Model):
    _inherit = 'survey.survey'

    contact_relation_ids = fields.One2many('contact.relation', 'survey_id', string="Contact Relation")


class SurveyUserInputLine(models.Model):
    _inherit = 'survey.user_input.line'


    def create(self, vals_list):
        print("hiiiii")
        res = super(SurveyUserInputLine,self).create(vals_list)
        return res