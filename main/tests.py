import json
import uuid

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Experience, Project


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(
            response,
            f'href="{reverse("main:show_experience")}"',
        )

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")
        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Part-Time")
        self.assertContains(response, "Ongoing")
        self.assertContains(
            response,
            f'href="{reverse("main:show_main")}"',
        )

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))
        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))
        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "Done")
        self.assertNotContains(response, "Ongoing")

    def test_create_experience_page_is_accessible(self):
        response = self.client.get(reverse("main:create_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience_form.html")
        self.assertContains(response, "Add Experience")
        self.assertContains(response, "csrfmiddlewaretoken")
        self.assertEqual(
            list(response.context["form"].fields),
            ["title", "description", "category", "thumbnail"],
        )

    def test_create_experience_with_valid_data(self):
        response = self.client.post(
            reverse("main:create_experience"),
            {
                "title": "Product Design Intern",
                "description": "Designed and tested product flows.",
                "category": "internship",
                "thumbnail": "https://example.com/internship.jpg",
            },
            follow=True,
        )

        self.assertRedirects(response, reverse("main:show_experience"))
        self.assertTrue(
            Experience.objects.filter(title="Product Design Intern").exists()
        )
        self.assertContains(response, "Experience added successfully!")

    def test_create_experience_with_invalid_data(self):
        experience_count = Experience.objects.count()
        response = self.client.post(
            reverse("main:create_experience"),
            {
                "title": "",
                "description": "Missing a required title.",
                "category": "internship",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience_form.html")
        self.assertContains(response, "This field is required.")
        self.assertEqual(Experience.objects.count(), experience_count)

    def test_update_experience_page_is_prefilled(self):
        response = self.client.get(
            reverse("main:update_experience", args=[self.experience.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience_form.html")
        self.assertContains(response, "Update Experience")
        self.assertContains(response, f'value="{self.experience.title}"')

    def test_update_experience_with_valid_data(self):
        experience_count = Experience.objects.count()
        response = self.client.post(
            reverse("main:update_experience", args=[self.experience.id]),
            {
                "title": "Teaching Assistant PBP",
                "description": "Helped students learn Django.",
                "category": "part-time",
                "thumbnail": "https://example.com/teaching.jpg",
            },
            follow=True,
        )

        self.experience.refresh_from_db()
        self.assertRedirects(response, reverse("main:show_experience"))
        self.assertEqual(Experience.objects.count(), experience_count)
        self.assertEqual(self.experience.title, "Teaching Assistant PBP")
        self.assertEqual(self.experience.description, "Helped students learn Django.")
        self.assertContains(response, "Experience updated successfully!")

    def test_update_experience_returns_404_for_unknown_id(self):
        response = self.client.get(
            reverse("main:update_experience", args=[uuid.uuid4()])
        )

        self.assertEqual(response.status_code, 404)

    def test_experience_page_shows_thumbnail_and_actions(self):
        self.experience.thumbnail = "https://example.com/experience.jpg"
        self.experience.save()

        response = self.client.get(reverse("main:show_experience"))
        update_url = reverse("main:update_experience", args=[self.experience.id])

        self.assertContains(response, self.experience.thumbnail)
        self.assertContains(response, f'href="{reverse("main:create_experience")}"')
        self.assertContains(response, f'href="{update_url}"')

    def test_experiences_json_endpoint(self):
        response = self.client.get(reverse("main:get_experiences_json"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")

        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["model"], "main.experience")
        self.assertEqual(data[0]["pk"], str(self.experience.id))
        self.assertEqual(data[0]["fields"]["title"], self.experience.title)
        self.assertEqual(data[0]["fields"]["category"], "part-time")

    def test_experiences_json_endpoint_returns_empty_list(self):
        Experience.objects.all().delete()

        response = self.client.get(reverse("main:get_experiences_json"))

        self.assertEqual(json.loads(response.content), [])

    def test_experience_page_uses_deserialized_objects(self):
        response = self.client.get(reverse("main:show_experience"))
        experience_list = response.context["experience_list"]

        self.assertIsInstance(experience_list, list)
        self.assertEqual(len(experience_list), 1)
        self.assertIsInstance(experience_list[0], Experience)
        self.assertEqual(experience_list[0].id, self.experience.id)


class ProjectTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            title="VETO",
            role="Concept · Design · Direction",
            description="API-first ODOL middleware.",
            thumbnail="/static/img/project-veto.jpg",
            primary_link_label="GitHub",
            primary_link_url="https://github.com/6avier/veto",
            display_order=1,
        )

    def test_project_model(self):
        self.assertEqual(str(self.project), "VETO")
        self.assertEqual(self.project.display_order, 1)

    def test_projects_url_is_accessible(self):
        response = self.client.get(reverse("main:show_projects"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects.html")

    def test_project_data_appears(self):
        response = self.client.get(reverse("main:show_projects"))
        self.assertContains(response, self.project.title)
        self.assertContains(response, self.project.role)
        self.assertContains(response, self.project.description)

    def test_empty_projects_page(self):
        Project.objects.all().delete()
        response = self.client.get(reverse("main:show_projects"))
        self.assertContains(response, "Belum ada proyek yang ditambahkan.")

    def test_main_page_links_to_projects(self):
        response = self.client.get(reverse("main:show_main"))
        self.assertContains(
            response,
            f'href="{reverse("main:show_projects")}"',
        )

    def test_create_project_page_is_accessible(self):
        response = self.client.get(reverse("main:create_project"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects_form.html")
        self.assertContains(response, "Add New Project")
        self.assertContains(response, "csrfmiddlewaretoken")

    def test_create_project_with_valid_data(self):
        response = self.client.post(
            reverse("main:create_project"),
            {
                "title": "New Portfolio",
                "role": "Designer & Developer",
                "description": "A new portfolio project.",
                "thumbnail": "/static/img/project-comprof.jpg",
                "primary_link_label": "GitHub",
                "primary_link_url": "https://github.com/example/portfolio",
                "display_order": 2,
            },
            follow=True,
        )

        self.assertRedirects(response, reverse("main:show_projects"))
        self.assertTrue(Project.objects.filter(title="New Portfolio").exists())
        self.assertContains(response, "Project added successfully!")

    def test_create_project_with_invalid_data(self):
        project_count = Project.objects.count()
        response = self.client.post(
            reverse("main:create_project"),
            {
                "title": "",
                "role": "Developer",
                "description": "Missing a required title.",
                "thumbnail": "/static/img/project-comprof.jpg",
                "display_order": 2,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects_form.html")
        self.assertContains(response, "This field is required.")
        self.assertEqual(Project.objects.count(), project_count)

    def test_projects_json_endpoint(self):
        response = self.client.get(reverse("main:get_projects_json"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")

        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["pk"], str(self.project.id))
        self.assertEqual(data[0]["fields"]["title"], "VETO")

    def test_projects_json_can_filter_by_title(self):
        Project.objects.create(
            title="Unrelated Alpha",
            role="Developer",
            description="Another project.",
            thumbnail="/static/img/project-comprof.jpg",
            display_order=2,
        )

        response = self.client.get(
            reverse("main:get_projects_json"),
            {"title": "veto"},
        )

        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["fields"]["title"], "VETO")

    def test_projects_page_can_filter_by_title(self):
        Project.objects.create(
            title="Unrelated Alpha",
            role="Developer",
            description="Another project.",
            thumbnail="/static/img/project-comprof.jpg",
            display_order=2,
        )

        response = self.client.get(
            reverse("main:show_projects"),
            {"title": "veto"},
        )

        self.assertContains(response, self.project.title)
        self.assertNotContains(response, "Unrelated Alpha")
        self.assertContains(response, 'value="veto"')

    def test_projects_page_shows_search_empty_state(self):
        response = self.client.get(
            reverse("main:show_projects"),
            {"title": "missing"},
        )

        self.assertContains(response, 'No projects found for "missing".')

    def test_projects_page_contains_delete_confirmation(self):
        response = self.client.get(reverse("main:show_projects"))
        delete_url = reverse("main:delete_project", args=[self.project.id])

        self.assertContains(response, "Delete Project?")
        self.assertContains(response, f'action="{delete_url}"')
        self.assertContains(response, "csrfmiddlewaretoken")

    def test_delete_project_with_post(self):
        response = self.client.post(
            reverse("main:delete_project", args=[self.project.id]),
            follow=True,
        )

        self.assertRedirects(response, reverse("main:show_projects"))
        self.assertFalse(Project.objects.filter(pk=self.project.id).exists())
        self.assertContains(response, "Project deleted successfully!")

    def test_delete_project_rejects_get(self):
        response = self.client.get(
            reverse("main:delete_project", args=[self.project.id]),
        )

        self.assertEqual(response.status_code, 405)
        self.assertTrue(Project.objects.filter(pk=self.project.id).exists())

    def test_delete_project_returns_404_for_unknown_id(self):
        response = self.client.post(
            reverse("main:delete_project", args=[uuid.uuid4()]),
        )

        self.assertEqual(response.status_code, 404)
