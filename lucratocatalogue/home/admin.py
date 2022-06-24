from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy
from .forms import *
from .models import CatalogueUser
from .models import Label
from .models import Item
from django.contrib.auth.models import Group
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

# admin.site.register(CatalogueUser)
admin.site.register(Label)
admin.site.register(Item)


class CatalogueUserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = CatalogueUser
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CatalogueUserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CatalogueUser
        fields = ('email',)


class CatalogueUserAdmin(UserAdmin):
    # The forms to add and change user instances
    add_form = CatalogueUserCreationForm
    form = CatalogueUserChangeForm

    list_display = ('email', 'first_name', 'last_name', 'is_editor', 'is_seller', 'company')
    list_filter = ('is_editor', 'is_seller', 'company',)
    fieldsets = (
        (None, {'fields': ('email', 'is_editor', 'is_seller',)}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'company',)}),
        ('Permissions', {'fields': ('is_superuser',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            "classes":("wide"),
            'fields': ('email', 'first_name', 'last_name', 'is_editor', 'is_seller', 'company', 'password1','password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(CatalogueUser, CatalogueUserAdmin)

admin.site.unregister(Group)


class TINTAdminSite(AdminSite):
    admin.site.site_header = 'Beheer'
    AdminSite.site_title = 'Technology catalogue'
    AdminSite.index_title = 'Beheer'


admin_site = TINTAdminSite()
