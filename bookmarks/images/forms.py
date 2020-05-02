from urllib import request

from django import forms
from django.core.files.base import ContentFile
from django.utils.text import slugify

from .models import Image


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'url', 'description')
        # User should not enter URL directly bug we will provide javascript to retrieve the URL by a selected image
        # the url-input widget is hidden
        widgets = {
            'url': forms.HiddenInput,
        }

    # for all fieldnames we can define 'clean_*' functions that are evaluated by the forms 'is_valid()'
    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg', 'png']
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError(f'The given url is not providing a supported image format: {valid_extensions}')
        return url

    def save(self, force_insert=False, force_update=False, commit=True):
        """
        You could, for example, use the view that handles the form to download the image file.
        Instead, let's take a more general approach by overriding the save() method of your model form to
        perform this task every time the form is saved.
        """
        image = super().save(commit=False)  # save returns image object if commit=False
        image_url = self.cleaned_data['url']
        name = slugify(image.title)
        extension = image_url.rsplit('.', 1)[1].lower()
        image_name = f'{name}.{extension}'

        # download image from url
        response = request.urlopen(image_url)
        # ContentFile: In this way, you save the file to the media directory of your project
        # You pass the save=False parameter to avoid saving the object to the database yet
        image.image.save(image_name, ContentFile(response.read()), save=False)

        if commit: image.save()  # only save if commit=True to respect the ModelForm.save() interface
        return image
