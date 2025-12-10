from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    # Yulduzcha berish uchun maxsus maydon
    rating = forms.IntegerField(
        label="Bahoyingiz (1-5 yulduzcha)",
        widget=forms.NumberInput(attrs={'min': 1, 'max': 5, 'class': 'w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'}),
        min_value=1,
        max_value=5
    )
    
    class Meta:
        model = Comment
        fields = ['author_name', 'text', 'rating']
        widgets = {
            'author_name': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500', 'placeholder': "Ismingiz"}),
            'text': forms.Textarea(attrs={'class': 'w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500', 'rows': 4, 'placeholder': "Sharhingizni yozing..."}),
        }
        labels = {
            'author_name': "Ism",
            'text': "Sharh Matni",
        }
