from django.contrib.auth.decorators import user_passes_test                                                                                                                         
 
def in_beheer_group(user):
    return user.is_authenticated and user.groups.filter(name="beheer").exists()
 
beheer_required = user_passes_test(in_beheer_group)
