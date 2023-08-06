"""Admin site for `app`:ajax.
"""

# pylint:disable=R0904
# R0904: too many public methods in ModelAdmin.

from .models import Fylke, Kommune, PostSted
from django.contrib import admin


class FylkeOptions(admin.ModelAdmin):
    "Admin options for `model`:dknorway.Fylke."
    list_display = 'navn nr active note'.split()
    list_filter = ['active']


class PostStedOptions(admin.ModelAdmin):
    "Admin options for `model`:dknorway.PostSted."
    list_display = 'postnummer poststed kommune lat lng'.split()
    list_filter = ['kommune']
    search_fields = 'postnummer poststed'.split()


class KommuneOptions(admin.ModelAdmin):
    "Admin options for `model`:dknorway.Kommune."
    list_display = 'kode navn fylke'.split()
    search_fields = 'kode navn'.split()


admin.site.register(Fylke, FylkeOptions)
admin.site.register(PostSted, PostStedOptions)
admin.site.register(Kommune, KommuneOptions)
