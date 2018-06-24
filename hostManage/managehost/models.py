from django.db import models

# Create your models here.


class HostType(models.Model):
    typename = models.CharField(max_length=16)

    def __str__(self):
        return self.typename
    class Meta:
        verbose_name_plural = "主机所属区域"

class HostInfo(models.Model):
    nickname = models.CharField(max_length=16)
    ipaddr = models.GenericIPAddressField()
    uptime = models.CharField(max_length=16,null=True,blank=True)
    cpustat = models.CharField(max_length=16,null=True,blank=True)
    memory = models.CharField(max_length=16,null=True,blank=True)
    rootdisk = models.CharField(max_length=16,null=True,blank=True)
    iostat = models.FloatField(null=True,blank=True)
    network = models.BooleanField(default=True)
    ms = models.CharField(max_length=16,null=True,blank=True)
    hosttype = models.ForeignKey('HostType')
    createdate = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nickname

    class Meta:
        verbose_name_plural = "主机状态列表"

class UserInfo(models.Model):
    """
    code: 为后台验证码，这个用于测试使用，请不要打开admin页面进行修改
    """
    username = models.CharField(max_length=16)
    password = models.CharField(max_length=16)
    code = models.CharField(max_length=16,null=True,blank=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = "用户列表"


