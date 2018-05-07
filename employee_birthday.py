# -*- coding: utf-8 -*-
import logging
import time
from datetime import date,datetime, timedelta
from dateutil import relativedelta

from odoo import models, fields, api
from odoo import tools, _
from odoo.exceptions import UserError, ValidationError
from odoo.modules.module import get_module_resource

class HRemployeeInherit(models.Model):
    _inherit = 'hr.employee'

    birthday = fields.Date("Date Of Birth", groups = 'base.group_user')

class WizardBirthday(models.TransientModel):
    _name = "wizard.birthday"
    # _inherit = 'hr.employee'

    date_from = fields.Date(string='Date From', required=True,
        default=datetime.now().strftime('%Y-%m-01'))
    date_to = fields.Date(string='Date To', required=True,
        default=str(datetime.now() + relativedelta.relativedelta(months=+1, day=1, days=-1))[:10])

    @api.multi
    def print_report(self,context=None):
        bdates = self.env['hr.employee'].search([])
        print "****bday****"
        data={}
        for rec in bdates:
            if rec.sudo().birthday >= self.date_from and rec.sudo().birthday <= self.date_to:
                data['form'] = rec.read(['name','birthday','company_id'])
                b_data1 = data['form']
        active_ids = self.env.context.get('active_ids', [])
        datas = {
            'ids': active_ids,
            'model': 'employee_birthday.wizard.birthday',
            'data':data,
            'form': self.read()[0]
             }
        return self.env['report'].get_action(bdates,'employee_birthday.register_report', data=datas)

    @api.constrains('date_from', 'date_to')
    def _check_dates(self):
        if any(self.filtered(lambda birthday: birthday.date_from > birthday.date_to)):
            raise ValidationError(_("wizard 'Date From' must be before 'Date To'."))

    # @api.constrains('b_data1')
    # def _check_report(self):
    #     for birthday in self.read(b_data1):
    #         if not birthday >= date_from and birthday <= date_to:
    #             raise UserError(_("No matching records,this report cannot be printed.............."))

