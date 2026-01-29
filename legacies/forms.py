from django import forms
from .models import Legacy


class LegacySubmissionForm(forms.ModelForm):
    class Meta:
        model = Legacy
        fields = [
            "full_name",
            "zone",
            "story",
            "photo",
        ]
        widgets = {
            "story": forms.Textarea(attrs={"rows": 10}),
        }
