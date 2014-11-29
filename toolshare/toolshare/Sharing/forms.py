from django import forms
from django.contrib.auth.models import User
from Sharing.models import Shed, UserShedAssignation
from UserAuth.models import UserProfile
from localflavor.us.forms import USZipCodeField
from localflavor.us.forms import USStateField
from django.forms import ModelForm
from django.core.files.images import get_image_dimensions
import pdb
class ShedCreateForm(forms.ModelForm):
    class Meta:
        model = Shed
        fields = ('name','description')

#May be the form is not required at all but I am adding it because, atleast we get indepedence of different behaviour.
class ShedEditForm(forms.ModelForm):
    user_shed_assignations = forms.ModelMultipleChoiceField(queryset=UserProfile.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)

    # def __init__(self, *args, **kwargs):
    #     super(ShedEditForm, self).__init__(*args, **kwargs)
    #     if kwargs:
    #         shed = kwargs.pop('instance')
    #         self.fields['user_shed_assignations'] = forms.ModelMultipleChoiceField(
    #             required=False,
    #             queryset = shed.user_shed_assignations.all(),
    #             # queryset = UserProfile.objects.all(),
    #             widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Shed
        fields = ('name','description')
