from django.forms import ModelForm
from network.models import Post
from django.utils.translation import gettext_lazy as _

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['content']
        labels = {
            'content': _('New Post')
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget.attrs.update({'id': 'newposttext'})
