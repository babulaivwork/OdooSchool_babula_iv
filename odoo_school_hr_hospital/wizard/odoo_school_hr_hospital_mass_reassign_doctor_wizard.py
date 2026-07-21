from odoo import fields, models
from odoo.exceptions import UserError


class OSHrHospitalMassReassignDoctorWizard(models.TransientModel):
    _name = 'os.hr.hospital.mass.reassign.doctor.wizard'
    _description = 'Mass Reassign Personal Doctor'

    new_doctor_id = fields.Many2one(
        comodel_name='os.hr.hospital.doctor',
        string='New Doctor',
        required=True,
    )
    change_date = fields.Date(
        string='Change Date',
        default=fields.Date.today,
    )

    def action_reassign_doctor(self):
        self.ensure_one()
        if not self.change_date:
            raise UserError('Change Date is required to update personal doctor history.')

        if self.env.context.get('active_model') != 'os.hr.hospital.patient':
            raise UserError('This action can only be used for patients.')

        patients = self.env['os.hr.hospital.patient'].browse(self.env.context.get('active_ids', [])).exists()
        if not patients:
            raise UserError('Please select at least one patient.')

        patients_to_reassign = patients.filtered(lambda patient: patient.personal_doctor_id != self.new_doctor_id)
        if not patients_to_reassign:
            return {'type': 'ir.actions.act_window_close'}

        open_histories = self.env['os.hr.hospital.doctor.history'].search(
            [
                ('patient_id', 'in', patients_to_reassign.ids),
                ('active', '=', True),
                ('change_date', '=', False),
            ]
        )
        open_histories.write({'change_date': self.change_date})

        patients_to_reassign.write({'personal_doctor_id': self.new_doctor_id.id})
        self.env['os.hr.hospital.doctor.history'].create(
            [
                {
                    'patient_id': patient.id,
                    'doctor_id': self.new_doctor_id.id,
                    'assignment_date': self.change_date,
                    'active': True,
                }
                for patient in patients_to_reassign
            ]
        )

        return {'type': 'ir.actions.act_window_close'}
