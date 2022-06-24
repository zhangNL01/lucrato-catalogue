# from django import forms
# from django.contrib.auth.forms import ReadOnlyPasswordHashField
# from django.core.exceptions import ValidationError
# from .models import CatalogueUser
#
#
# class NewUser(forms.ModelForm):
#     email = forms.CharField(label="email", max_length=128)
#     first_name = forms.CharField(label="first_name", max_length=128)
#     last_name = forms.CharField(label="last_name", max_length=128)
#     company = forms.CharField(label="company", max_length=128)
#     is_editor = forms.BooleanField()
#     is_seller = forms.BooleanField()
#     password = forms.CharField(label='password', widget=forms.PasswordInput)
#
#     class Meta:
#         model = CatalogueUser
#         fields = ('email', 'first_name', 'last_name', 'company', 'is_editor', 'is_seller',)
#
#     def save(self, commit=True):
#         # Save the provided password in hashed format
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data["password"])
#         if commit:
#             user.save()
#         return user
#
#
# class CUCreationForm(forms.ModelForm):
#     """A form for creating new users. Includes all the required fields, plus a repeated password."""
#     password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
#     password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
#     is_editor = forms.BooleanField()
#     is_seller = forms.BooleanField()
#
#     class Meta:
#         model = CatalogueUser
#         fields = ('email', 'first_name', 'last_name', 'company', 'is_editor', 'is_seller',)
#
#     def clean_password2(self):
#         # Check that the two password entries match
#         password1 = self.cleaned_data.get("password1")
#         password2 = self.cleaned_data.get("password2")
#         if password1 and password2 and password1 != password2:
#             raise ValidationError("Passwords don't match")
#         return password2
#
#     def save(self, commit=True):
#         # Save the provided password in hashed format
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data["password1"])
#         if commit:
#             user.save()
#         return user
#
#
# class CUChangeForm(forms.ModelForm):
#     """A form for updating users. Includes all the fields on
#     the user, but replaces the password field with admin's
#     disabled password hash display field.
#     """
#     password = ReadOnlyPasswordHashField()
#     is_editor = forms.BooleanField()
#     is_seller = forms.BooleanField()
#
#     class Meta:
#         model = CatalogueUser
#         fields = ('email', 'password', 'first_name', 'last_name', 'company',)
