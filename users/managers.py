from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True
    
    def _create_user(self, email, first_name, other_name, last_name, username, password, **extra_fields):
        
        if not email:
            raise ValueError(_('User needs to provide an Email address...'))
        
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, other_name=other_name, last_name=last_name, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    
    
    def create_superuser(self, email, first_name, other_name, last_name, username, password, **extra_fields):
        
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_admin', True)
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('superuser must be assigned to is_superuser=True')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('superuser must be assigned to is_staff=True')
        
        if extra_fields.get('is_admin') is not True:
            raise ValueError('superuser must be assigned to is_admin=True')
        
        return self._create_user(email, first_name, other_name, last_name, username, password, **extra_fields)