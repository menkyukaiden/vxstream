from django.forms import ModelForm

from app.models import InterfaceConfiguration


class InterfaceConfigurationForm(ModelForm):
    class Meta:
        model = InterfaceConfiguration
        fields = ['sat_name', 'delivery_system', 'frequency', 'symbole_rate', 'polarisation', 'modulation', 'fec',
                  'rolloff', 'pilot', 'lnb_type', 'lnb_lof_standard', 'lnb_slof', 'lnb_lof_low', 'lnb_lof_high']
