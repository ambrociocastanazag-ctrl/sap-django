from django.forms import ModelForm
from personas.models import Domicilio, Persona

class PersonaForm(ModelForm):

    class Meta:
        model = Persona
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': field.widget.attrs.get('class', '') + ' input'
            })

PersonaForm.base_fields['domicilio'].empty_label = "Seleccione un domicilio"

class DomicilioForm(ModelForm):

    class Meta:
        model = Domicilio
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'input'
            })