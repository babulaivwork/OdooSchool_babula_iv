.. _changelog:

Changelog
=========

`19.0.13.0.0`
---------------

* Added automated tests for age computation, disease hierarchy validation,
  and completed visit write restrictions.
* Added Python docstrings for all custom classes and methods.
* Added the module README and complete version history.
* Added an HTML module description for the module form and Odoo Apps.

`19.0.12.0.0`
---------------

* Added the Ukrainian translation for the interface, reports, messages,
  security groups, qualifications, and disease classifier.
* Made disease names, disease descriptions, and qualification names
  translatable.
* Added pneumonia and allergic rhinitis to the demo disease classifier.
* Made Python and QWeb user-facing messages translation-ready.

`19.0.11.0.0`
---------------

* Added inherited Patient, Intern, Doctor, Manager, and Administrator roles.
* Restricted patients to reading their own visits.
* Allowed interns to read and edit their assigned visits.
* Allowed doctors to read and edit their visits and their interns' visits.
* Allowed managers to read all visits.
* Granted administrators full access to all module data.
* Linked patient and doctor records to system users.

`19.0.10.0.0`
---------------

* Improved borders and spacing in the doctor PDF report tables.
* Improved the printed presentation of visit and patient information.

`19.0.9.0.0`
--------------

* Added edit and delete actions to doctor kanban cards.
* Displayed doctor qualifications and assigned interns in kanban view.

`19.0.8.0.0`
--------------

* Added a QWeb PDF report for doctors.
* Included visit history and personal patients in the report.
* Added company information, print details, and visit status highlighting.

`19.0.7.0.0`
--------------

* Added a disease report wizard with doctor, disease, and period filters.
* Added calendar, pivot, graph, and advanced search views for visits.
* Added visit counters and smart actions for diseases and patients.
* Added actions for opening prefilled visit forms from doctor and patient
  records.
* Added an extended doctor kanban view and additional demo records.

`19.0.6.0.0`
--------------

* Added a wizard for mass reassignment of patients' personal doctors.
* Added automatic updates to personal doctor assignment history.
* Added a visit report wizard with doctor, patient, date, disease, and status
  filters.

`19.0.5.0.0`
--------------

* Added a hierarchical disease classifier.
* Added parent and child disease relations and hierarchical display names.
* Added validation that prevents recursive disease hierarchies.
* Added disease classifier demo data.

`19.0.4.0.0`
--------------

* Added doctor qualifications, intern detection, mentors, and visit relations.
* Added scheduled, completed, and cancelled visit states.
* Added visit dates, diseases, descriptions, and medical summaries.
* Prevented invalid changes, archiving, and deletion of completed visits.
* Added visit demo data.

`19.0.3.0.0`
--------------

* Added a reusable abstract model for medical information.
* Added blood group, gender, birth date, and computed age fields.
* Applied shared medical information to doctor and patient records.

`19.0.2.0.0`
--------------

* Added doctor qualification records and configuration views.
* Added personal doctor assignment history.
* Added assignment date validation and history display names.
* Added qualification and history demo data.

`19.0.1.0.0`
--------------

* Added the initial HR Hospital module.
* Added doctor, patient, disease, and visit models.
* Added list and form views, menus, access rights, and demo data.
