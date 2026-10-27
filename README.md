# Final Project: Submission and Evaluation New

This repository contains the Django online course app with exam submission and result evaluation.

## Required public GitHub URLs

These are the exact public repository paths expected by the assignment feedback.

- Models: https://github.com/shrutitattapure24-blip/tfjzl-final-cloud-app-with-database/blob/main/onlinecourse/models.py
- Admin: https://github.com/shrutitattapure24-blip/tfjzl-final-cloud-app-with-database/blob/main/onlinecourse/admin.py
- Course detail template: https://github.com/shrutitattapure24-blip/tfjzl-final-cloud-app-with-database/blob/main/templates/onlinecourse/course_details_bootstrap.html
- Views: https://github.com/shrutitattapure24-blip/tfjzl-final-cloud-app-with-database/blob/main/onlinecourse/views.py
- URLs: https://github.com/shrutitattapure24-blip/tfjzl-final-cloud-app-with-database/blob/main/onlinecourse/urls.py

## Screenshot files

- 03-admin-site.png
- 07-final.png

## Notes

- The app uses the `Course`, `Lesson`, `Question`, `Choice`, `Enrollment`, and `Submission` models required by the assignment.
- The exam flow includes `submit` and `show_exam_result`.
- The template explicitly includes `{{ course.name }}`, a lesson loop with `{% for lesson in lessons %}`, and Bootstrap styling.
- The result page includes the success message, score, and exam results table.
