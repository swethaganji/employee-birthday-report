
import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from odoo import models, fields, api
from odoo import tools, _
from odoo.exceptions import UserError, ValidationError
from odoo.modules.module import get_module_resource


class birthdayRegisterReport(models.AbstractModel):
    _name = 'report.employee_birthday.register_report'

    @api.model
    def render_html(self,docids,data=None):
        
        if not data.get('form'):
            raise UserError(_("Form content is missing,this report cannot be printed.............."))

        date_from = data['form'].get('date_from')
        date_to = data['form'].get('date_to')
        
        register_ids = self.env.context.get('active_ids', [])
        contrib_registers = self.env['hr.employee'].browse(register_ids)
        docs = self.env['hr.employee'].browse(self.env.context.get('active_id'))

        d_from = datetime.strptime(date_from,'%Y-%m-%d')
        d1 = datetime.strftime(d_from,'%m-%d')
        print d1,"!!!!!!!!!!!!"

        d_to = datetime.strptime(date_to,'%Y-%m-%d')
        d2 = datetime.strftime(d_to,'%m-%d')
        print d2,"|||||||||||||||||||"


        data1 = {}
        bdates1 = self.env['hr.employee'].search(['|', ('birthday', 'like' ,d1), ('birthday','like' , d2)])
        data1['new']=bdates1.read(['name','birthday','work_email','sudo().company_id'])
        lines_data = data1['new']

        docargs = {
            'doc_ids': register_ids,
            'doc_model': 'employee_birthday.wizard.birthday',
            'docs': contrib_registers,
            'data': data,
            'time':time,
            'lines_data': bdates1,
        }
        return self.env['report'].render('employee_birthday.register_report', docargs)

    


    