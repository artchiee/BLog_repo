
from django import forms

from .models import (MyPosts, Comments)
from datetime import datetime


class Form_Change(forms.ModelForm):
    publish = forms.DateTimeField(
        widget=forms.SelectDateWidget, initial=datetime.now())

    class Meta:
        model = MyPosts
        fields = ['post_title',
                  'post_content',
                  'draft',
                  'category',
                  'publish',
                  'image', ]
        # 'width_field',
        # 'height_field']

    # Making a comment form

class CommentForm(forms.ModelForm):

    # # getting current logged in user
    # def __init__(self, *args, *kwargs):
    #     self.user = self.request.user
    #     super(CommentForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Comments
        fields = [
            'post_name',
            'text'
        ]
