from django.db import models
import uuid
from datetime import datetime
from django.contrib.auth import get_user_model





class Posts(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_image', blank=True)
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return str(self.user.get_full_name())
    


class Comments(models.Model):
    post = models.ForeignKey(Posts, related_name='details', on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    comment = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.user.get_full_name()
    

class Likes(models.Model):
    user = models.ForeignKey(get_user_model(), related_name='likes', on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, related_name='likes', on_delete=models.CASCADE)





class Group(models.Model):
    pass
    
    