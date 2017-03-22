from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field
from django import forms

from matches.models import Match
from utils.datetimepicker import UpdatedDateTimePicker


class ImportForm(forms.Form):
    player_name = forms.CharField(max_length=200)
    xws_file = forms.FileField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()

        self.helper.form_id = 'main_form'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-10'

        self.helper.layout = Layout(
            'player_name',
            'xws_file',
            FormActions(
                Submit('run', 'Import'),
            )
        )


class BuildMatch(forms.ModelForm):
    class Meta:
        model = Match
        fields = [
            'squad_one',
            'squad_two',
            'start_time',
            'match_minutes',
        ]
        widgets = {
            'start_time': UpdatedDateTimePicker(
                options={
                    "format": "DD/MM/YYYY HH:mm"
                }
            ),
        }
        localized_fields = ('start_time',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()

        self.helper.form_id = 'main_form'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-8'

        self.helper.layout = Layout(
            Field(
                'squad_one',
                css_class="typeahead",
            ),
            Field(
                'squad_two',
                css_class="typeahead",
            ),
            'start_time',
            'match_minutes',
            FormActions(
                Submit('save', 'Create Match'),
            )
        )


class GenericDeleteForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()

        self.helper.form_id = 'main_form'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-8'

        self.helper.layout = Layout(
            FormActions(
                Submit('save', "Yes, I'm Sure"),
            )
        )
