from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    birth_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.username

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"

class Information(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return self.title


class NsaResource(models.Model):
    idx = models.BigAutoField(db_column='idx', primary_key=True)
    id = models.CharField(db_column='id', null=True, max_length=255)
    group = models.CharField(max_length=255,null=True,db_column='group')
    name = models.CharField(max_length=255,null=True,db_column='name')
    hostname = models.CharField(max_length=255,null=True,db_column='hostname')
    ipaddress = models.CharField(max_length=255,null=True,db_column='ipaddress')
    vendor = models.CharField(max_length=255,null=True,db_column='vendor')
    model = models.CharField(max_length=255,null=True,db_column='model')
    osversion = models.CharField(max_length=255,null=True,db_column='osversion')
    crt_dtm = models.DateTimeField(auto_now_add=True,db_column='crt_dtm')
    crt_uid = models.IntegerField(null=True,blank=True,db_column='crt_uid')
    upd_dtm = models.DateTimeField(auto_now=True,null=True,db_column='upd_dtm')
    upd_uid = models.IntegerField(null=True,blank=True,db_column='upd_uid')
    class Meta:
        db_table = 't_nsa_resource'
        managed = False

class NsaResourceInfo(models.Model):
    idx = models.BigAutoField(db_column='idx', primary_key=True)
    t_nsa_resourceidx = models.ForeignKey(NsaResource,db_column='t_nsa_resourceidx', on_delete=models.CASCADE,related_name='ports')
    port_id = models.CharField(max_length=255,null=True,db_column='port_id')
    port_name = models.CharField(max_length=255,null=True,db_column='port_name')
    description = models.TextField(null=True,db_column='description')
    ok = models.CharField(max_length=255,null=True,db_column='ok')
    oper_status = models.CharField(max_length=255,null=True,db_column='oper_status')
    admin_status = models.CharField(max_length=255,null=True,db_column='admin_status')
    mtu = models.CharField(max_length=255,null=True,db_column='mtu')
    type = models.CharField(max_length=255,null=True,db_column='type')
    speed = models.CharField(max_length=255,null=True,db_column='speed')
    ipaddress = models.CharField(max_length=255,null=True,db_column='ipaddress')
    system_name = models.TextField(null=True,db_column='system_name')
    mac = models.CharField(max_length=255,null=True,db_column='mac')
    lldp_alive = models.CharField(max_length=255,null=True,db_column='lldp_alive')
    crt_dtm = models.DateTimeField(auto_now_add=True,db_column='crt_dtm')
    crt_uid = models.IntegerField(null=True,blank=True,db_column='crt_uid')
    upd_dtm = models.DateTimeField(auto_now=True,null=True,db_column='upd_dtm')
    upd_uid = models.IntegerField(null=True,blank=True,db_column='upd_uid')
    class Meta:
        db_table = 't_nsa_resource_info'
        managed = False