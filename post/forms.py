from django import forms
from .models import PostData

class PostDataForm(forms.ModelForm):
    class Meta:
        model = PostData
        fields = ('caption', 'image')

    def __init__(self, *args, **kwargs):
        super(PostDataForm, self).__init__(*args, **kwargs)
        for field in (self.fields['caption'], self.fields['image']):
            field.widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form-control-file'})