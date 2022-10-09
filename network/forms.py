from django.forms import ModelForm
from network.models import Post
from django.utils.translation import gettext_lazy as _

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['content']
