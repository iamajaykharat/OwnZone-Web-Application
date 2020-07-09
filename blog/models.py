from django.db import models


# Create your models here.

class Blogpost(models.Model):

    post_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, default="")
    head1 = models.CharField(max_length=100, default="")
    chead1 = models.TextField(default="")
    head2 = models.CharField(max_length=100, default="")
    chead2 = models.TextField(default="")
    head3 = models.CharField(max_length=100, default="")
    chead3 = models.TextField(default="")
    pub_date = models.DateField()
    img = models.ImageField(upload_to='blog/images')

    def __str__(self):
        return self.title
