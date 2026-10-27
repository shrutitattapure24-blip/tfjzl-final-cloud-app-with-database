# Final Project: Submission and Evaluation New

This repository contains the Django online course app with exam submission and result evaluation.

## Required public GitHub URLs after pushing to GitHub

Replace `<your-username>` with the GitHub username used for the repository.

- Models: https://github.com/<your-username>/tfjzl-final-cloud-app-with-database/blob/main/onlinecourse/models.py
- Admin: https://github.com/<your-username>/tfjzl-final-cloud-app-with-database/blob/main/onlinecourse/admin.py
- Course detail template: https://github.com/<your-username>/tfjzl-final-cloud-app-with-database/blob/main/templates/onlinecourse/course_details_bootstrap.html
- Views: https://github.com/<your-username>/tfjzl-final-cloud-app-with-database/blob/main/onlinecourse/views.py
- URLs: https://github.com/<your-username>/tfjzl-final-cloud-app-with-database/blob/main/onlinecourse/urls.py

## Screenshot files

- 03-admin-site.png
- 07-final.png

## Notes

- The app uses the `Course`, `Lesson`, `Question`, `Choice`, `Enrollment`, and `Submission` models required by the assignment.
- The exam flow includes `submit` and `show_exam_result`.
- The template includes `{{ course.name }}`, a lesson loop, and Bootstrap styling.
- The result page shows the success message, score, and exam results table.
