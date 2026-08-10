=======================
Odoo School HR Hospital
=======================

Odoo School HR Hospital is an Odoo 19 module for managing doctors, patients,
visits, disease classifications, personal doctor assignments, reports, and
role-based access to medical visits.

Features
========

* Manage doctors, qualifications, interns, and mentor assignments.
* Maintain patient records and personal doctor assignment history.
* Organize diseases in a hierarchical classifier.
* Schedule visits and track scheduled, completed, and cancelled states.
* Review visits in list, form, calendar, pivot, and graph views.
* Filter visits by doctor, patient, disease, period, and status.
* Reassign a personal doctor for multiple patients.
* Generate visit and disease selections with dedicated wizards.
* Print PDF reports containing a doctor's visits and personal patients.
* Control visit access with Patient, Intern, Doctor, Manager, and
  Administrator roles.
* Use the module in English or Ukrainian.

Installation
============

To install this module, you need to:

#. Copy the ``odoo_school_hr_hospital`` directory to an Odoo addons path.
#. Add the parent directory to the ``addons_path`` option in the Odoo
   configuration file.
#. Restart the Odoo server.
#. Update the Apps list.
#. Install **Odoo School HR Hospital**.

Configuration
=============

#. Open **Settings** and assign an HR Hospital access level to each user.
#. Link patient and doctor records to their corresponding system users when
   visit access must be restricted by user.
#. Review the predefined doctor qualifications and add other qualifications
   when required.
#. Enable demo data during database creation if sample hospital records are
   needed.

Usage
=====

Doctors and Patients
--------------------

Create doctor and patient records from the **HR Hospital** menu. Assign a
qualification to every doctor as needed. A mentor can be assigned only to an
intern, and an intern cannot mentor another intern.

Assign a personal doctor to a patient to maintain the current assignment. Use
the mass reassignment action when several patients must be assigned to a new
personal doctor on the same date.

Diseases
--------

Create parent and child diseases to maintain a hierarchical disease
classifier. Recursive disease hierarchies are rejected automatically.

Visits
------

Create a visit for a patient and doctor, then provide its scheduled date,
disease, description, and status. Completed visits may contain the actual date
and medical summary.

Completed visits cannot be archived, and their doctor or dates cannot be
changed. Only an HR Hospital Administrator can delete completed visits.

Reports
-------

Use the visit report wizard to filter visits by doctors, patients, dates,
completion status, and disease. Use the disease report wizard to group matching
visits by disease.

Open a doctor record or select doctors in the list view and use the print action
to generate a PDF report with visit history and personal patients.

Access Rights
-------------

The HR Hospital roles inherit one another in this order:

* **Patient** can read only visits linked to the user's patient record.
* **Intern** can read and edit visits assigned to the intern.
* **Doctor** can read and edit the doctor's visits and visits assigned to the
  doctor's interns.
* **Manager** can read all visits.
* **Administrator** has full access to all module data.

Credits
=======

Authors
-------

* `Odoo School Student <https://odoo.school/>`_
