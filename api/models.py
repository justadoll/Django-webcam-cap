from django.db import models

class Uri_link(models.Model):
    name = models.CharField(max_length=30)
    url = models.CharField(max_length=15)
    ip = models.CharField(max_length=15, blank=True,null=True)
    create_date=models.DateTimeField(auto_now_add=True,db_index=True)

    class Meta:
        verbose_name_plural="Links"
        verbose_name="link"
        ordering=['-create_date']
