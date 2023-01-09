from django.db import models
import uuid
from datetime import datetime
from django.contrib.auth import get_user_model





class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_image', blank=True)
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_likes = models.IntegerField(default=0)
    
    
    def __str__(self):
        return str(self.user.get_full_name())
    
    
class Group(models.Model):
    pass
    
    