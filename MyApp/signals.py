# from django.contrib.auth.models import Group
# from django.db.models.signals import post_migrate
# from django.dispatch import receiver
# from .models import permissionLightIntensity
#
#
# @receiver(post_migrate)
# def assign_permissions_light_intensity(sender, **kwargs):
#     # Assign view_light_intensity permission to light_intensities_viewer group
#     group = Group.objects.get(name='light_intensities_viewer')
#     group.permissions.add(permissionLightIntensity)
