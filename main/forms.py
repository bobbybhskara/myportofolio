from django.forms import ModelForm, NumberInput, Textarea, TextInput, URLInput

from main.models import Experience, Project


class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = [
            "title",
            "description",
            "category",
            "thumbnail",
        ]
        labels = {
            "title": "Experience title",
            "description": "Description",
            "category": "Category",
            "thumbnail": "Thumbnail URL",
        }
        widgets = {
            "title": TextInput(attrs={"placeholder": "Marketing Staff at RISTEK"}),
            "description": Textarea(
                attrs={
                    "placeholder": "Describe the experience and your contribution",
                    "rows": 4,
                }
            ),
            "thumbnail": URLInput(
                attrs={"placeholder": "https://example.com/image.jpg"}
            ),
        }


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "role",
            "description",
            "thumbnail",
            "primary_link_label",
            "primary_link_url",
            "secondary_link_label",
            "secondary_link_url",
            "third_link_label",
            "third_link_url",
            "note",
            "display_order",
        ]
        labels = {
            "title": "Project title",
            "role": "Role",
            "description": "Description",
            "thumbnail": "Thumbnail path or URL",
            "primary_link_label": "Primary link label",
            "primary_link_url": "Primary link URL",
            "secondary_link_label": "Secondary link label",
            "secondary_link_url": "Secondary link URL",
            "third_link_label": "Third link label",
            "third_link_url": "Third link URL",
            "note": "Note",
            "display_order": "Display order",
        }
        widgets = {
            "title": TextInput(attrs={"placeholder": "Portfolio Website"}),
            "role": TextInput(attrs={"placeholder": "Designer & Developer"}),
            "description": Textarea(
                attrs={
                    "placeholder": "Describe the project and your contribution",
                    "rows": 4,
                }
            ),
            "thumbnail": TextInput(
                attrs={
                    "placeholder": "/static/img/project-example.jpg or https://...",
                }
            ),
            "primary_link_label": TextInput(attrs={"placeholder": "GitHub"}),
            "primary_link_url": URLInput(attrs={"placeholder": "https://github.com/..."}),
            "secondary_link_label": TextInput(attrs={"placeholder": "Live Demo"}),
            "secondary_link_url": URLInput(attrs={"placeholder": "https://..."}),
            "third_link_label": TextInput(attrs={"placeholder": "Case Study"}),
            "third_link_url": URLInput(attrs={"placeholder": "https://..."}),
            "note": TextInput(attrs={"placeholder": "Optional note"}),
            "display_order": NumberInput(attrs={"min": 0}),
        }
