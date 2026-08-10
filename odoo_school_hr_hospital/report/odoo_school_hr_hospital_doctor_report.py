from odoo import api, fields, models


class OSHrHospitalDoctorReport(models.AbstractModel):
    """Prepare rendering data for the doctor PDF report."""

    _name = 'report.odoo_school_hr_hospital.os_hr_hospital_doctor_report'
    _description = 'Doctor Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        """Collect doctors, visits, and personal patients for the report.

        :param list[int] docids: IDs of doctors included in the report.
        :param dict or None data: Optional report data supplied by Odoo.
        :return: Rendering context for the QWeb report.
        :rtype: dict
        """
        doctors = self.env['os.hr.hospital.doctor'].browse(docids)
        visits = self.env['os.hr.hospital.visit'].search(
            [('doctor_id', 'in', doctors.ids)],
            order='scheduled_datetime desc, id desc',
        )
        patients = self.env['os.hr.hospital.patient'].search(
            [('personal_doctor_id', 'in', doctors.ids)],
            order='name, id',
        )

        visits_by_doctor = {doctor.id: [] for doctor in doctors}
        for visit in visits:
            visits_by_doctor[visit.doctor_id.id].append(visit)

        patients_by_doctor = {doctor.id: [] for doctor in doctors}
        for patient in patients:
            patients_by_doctor[patient.personal_doctor_id.id].append(patient)

        return {
            'doc_ids': docids,
            'doc_model': 'os.hr.hospital.doctor',
            'docs': doctors,
            'company': self.env.company,
            'print_datetime': fields.Datetime.now(),
            'visits_by_doctor': visits_by_doctor,
            'patients_by_doctor': patients_by_doctor,
        }
