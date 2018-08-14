from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Asset(models.Model):
    asset_type_choices = (
        ('server', '服务器'),
        ('networkdevice', '网络设备'),
        ('storagedevice', '存储设备'),
        ('securitydevice', '安全设备'),
        ('idcdevice', '机房设备'),
        ('accescories', '备件'),
        ('software', '软件资产')
    )
    asset_type = models.CharField(verbose_name='资产类型',choices=asset_type_choices,default='server',max_length=64)
    name = models.CharField(verbose_name='资产名称',max_length=64,unique=True)
    sn = models.CharField('资产编号',max_length=128,unique=True)
    manufactory = models.ForeignKey(to='Manufactory',verbose_name='制造商',null=True,blank=True,max_length=128)
    management_ip = models.GenericIPAddressField(verbose_name='管理ip地址',blank=True,null=True)
    contract = models.ForeignKey(to='Contract',verbose_name='合同',null=True,blank=True)
    trade_date = models.DateField(verbose_name='购买时间',null=True,blank=True)
    expire_date = models.DateField(verbose_name='过保时间',null=True,blank=True)
    price  = models.FloatField(verbose_name='硬件价格',null=True,blank=True)
    business_unit = models.ForeignKey(to='BusinessUnit',verbose_name='所属业务线',null=True,blank=True)
    tags = models.CharField(verbose_name='标签',null=True,blank=True)
    admin = models.ForeignKey('UserProfile',verbose_name='资产管理员',null=True,blank=True)
    cabinet = models.ForeignKey(to='Cabinet',verbose_name='IDC机柜',null=True,blank=True)
    status_choices = (
        (0,'在线'),
        (1,'已下线'),
        (2,'故障'),
        (3,'备用'),
        (4,'位置'),
    )
    status = models.SmallIntegerField(choices=status_choices,default=0)
    memo = models.TextField(verbose_name='备注',null=True,blank=True)
    create_date = models.DateTimeField(blank=True,auto_now_add=True)
    update_date = models.DateTimeField(blank=True,auto_now=True)

    class Meta:
        verbose_name = '资产总表'
        # verbose_name_plural = '资产总表'

    def __str__(self):
        return '%s--->%s'%(self.id,self.name)


class Server(models.Model):
    asset = models.OneToOneField('Asset')
    sub_asset_type_choices = (
        (0,'PC服务器'),
        (1,'刀片机'),
        (2,'小型机'),
    )
    created_by_choices = (
        ('auto','Auto'),
        ('menual','Manual'),
    )
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choices,verbose_name='服务器类型',default=0)
    created_by = models.CharField(choices=created_by_choices,default='auto')
    hosted_on = models.ForeignKey('self',related_name='hosted_on_server',blank=True,null=True)
    model = models.CharField(verbose_name='型号',max_length=128,null=True,blank=True)
    raid_type = models.CharField(verbose_name='raid类型',max_length=128,blank=True,null=True)
    os_type = models.CharField(verbose_name='操作系统类型',max_length=16,blank=True,null=True)
    os_distribution = models.CharField(u'发型版本', max_length=64, blank=True, null=True)
    os_release = models.CharField(u'操作系统版本', max_length=64, blank=True, null=True)

    class Meta:
        verbose_name = '服务器'
        verbose_name_plural = "服务器"
        # together = ["sn", "asset"]

    def __str__(self):
        return '%s sn:%s' % (self.asset.name, self.asset.sn)



class SecurityDevice(models.Model):
    asset = models.OneToOneField('Asset')
    sub_assset_type_choices = (
        (0,'防火墙'),
        (1, '入侵检测设备'),
        (2, '互联网网关'),
        (4, '运维审计系统'),
    )
    sub_asset_type = models.SmallIntegerField(choices=sub_assset_type_choices, verbose_name="服务器类型", default=0)
    def __str__(self):
        return self.asset.id

class NetworkDevice(models.Model):
    asset = models.OneToOneField('Asset')
    sub_assset_type_choices = (
        (0, '路由器'),
        (1, '交换机'),
        (2, '负载均衡'),
        (4, 'VPN设备'),
    )
    sub_asset_type = models.SmallIntegerField(choices=sub_assset_type_choices, verbose_name="服务器类型", default=0)

    vlan_ip = models.GenericIPAddressField(u'VlanIP', blank=True, null=True)
    intranet_ip = models.GenericIPAddressField(u'内网IP', blank=True, null=True)
    model = models.CharField(u'型号', max_length=128, null=True, blank=True)
    firmware = models.ForeignKey('Software', blank=True, null=True)
    port_num = models.SmallIntegerField(u'端口个数', null=True, blank=True)
    device_detail = models.TextField(u'设备详细配置', null=True, blank=True)
    class Meta:
        verbose_name = '网络设备'
        verbose_name_plural = "网络设备"


class Software(models.Model):
    asset = models.OneToOneField('Asset')
    sub_assset_type_choices = (
        (0, 'OS'),
        (1, '办公\开发软件'),
        (2, '业务软件'),
    )
    sub_asset_type = models.SmallIntegerField(choices=sub_assset_type_choices, verbose_name="服务器类型", default=0)
    license_num = models.IntegerField(verbose_name="授权数")