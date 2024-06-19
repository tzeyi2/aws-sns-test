from django import forms
from .models import RegionConfiguration


class RegionConfigurationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # fields do not exist for read-only (View permission) users on admin page
        if self.fields.get('blocklist') and self.fields.get('allowlist'):
            self.fields['blocklist'].delimiter = '|'
            self.fields['allowlist'].delimiter = '|'

    class Meta:
        model = RegionConfiguration
        fields = '__all__'
