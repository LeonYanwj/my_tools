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
    asset_type = models.CharField(verbose_name='资产类型', choices=asset_type_choices, default='server', max_length=64)
    name = models.CharField(verbose_name='资产名称', max_length=64, unique=True)
    sn = models.CharField('资产编号', max_length=128, unique=True)
    manufactory = models.ForeignKey(to='Manufactory', verbose_name='制造商', null=True, blank=True, max_length=128)
    management_ip = models.GenericIPAddressField(verbose_name='管理ip地址', blank=True, null=True)
    contract = models.ForeignKey(to='Contract', verbose_name='合同', null=True, blank=True)
    trade_date = models.DateField(verbose_name='购买时间', null=True, blank=True)
    expire_date = models.DateField(verbose_name='过保时间', null=True, blank=True)
    price = models.FloatField(verbose_name='硬件价格', null=True, blank=True)
    business_unit = models.ForeignKey(to='BusinessUnit', verbose_name='所属业务线', null=True, blank=True)
    tags = models.CharField(verbose_name='标签', null=True, blank=True,max_length=128)
    admin = models.ForeignKey('UserProfile', verbose_name='资产管理员', null=True, blank=True)
    cabinet = models.ForeignKey(to='Cabinet', verbose_name='IDC机柜', null=True, blank=True)
    status_choices = (
        (0, '在线'),
        (1, '已下线'),
        (2, '故障'),
        (3, '备用'),
        (4, '位置'),
    )
    status = models.SmallIntegerField(choices=status_choices, default=0)
    memo = models.TextField(verbose_name='备注', null=True, blank=True)
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True, auto_now=True)

    class Meta:
        verbose_name = '资产总表'
        # verbose_name_plural = '资产总表'

    def __str__(self):
        return '%s--->%s' % (self.id, self.name)


class Server(models.Model):
    asset = models.OneToOneField('Asset')
    sub_asset_type_choices = (
        (0, 'PC服务器'),
        (1, '刀片机'),
        (2, '小型机'),
    )
    created_by_choices = (
        ('auto', 'Auto'),
        ('menual', 'Manual'),
    )
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choices, verbose_name='服务器类型', default=0)
    created_by = models.CharField(choices=created_by_choices, default='auto',max_length=8)
    hosted_on = models.ForeignKey('self', related_name='hosted_on_server', blank=True, null=True)
    model = models.CharField(verbose_name='型号', max_length=128, null=True, blank=True)
    raid_type = models.CharField(verbose_name='raid类型', max_length=128, blank=True, null=True)
    os_type = models.CharField(verbose_name='操作系统类型', max_length=16, blank=True, null=True)
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
        (0, '防火墙'),
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
    version = models.CharField(verbose_name='软件/系统版本', max_length=64, unique=True, null=True, blank=True)

    def __str__(self):
        return self.version

    class Meta:
        verbose_name = '软件/系统'


class CPU(models.Model):
    """
    一台服务器
    """
    asset = models.ForeignKey('Asset')
    cpu_model = models.CharField(verbose_name='cpu型号', max_length=128, blank=True, null=True)
    cpu_count = models.IntegerField(verbose_name='物理CPU个数')
    cpu_core_count = models.IntegerField(verbose_name='cpu核数')
    memo = models.TextField(verbose_name='备注', null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(blank=True, null=True, auto_now=True)

    def __str__(self):
        return '%s-->%s' % (self.asset.name, self.cpu_model)

    class Meta:
        verbose_name = 'CPU部件'


class RAM(models.Model):
    asset = models.ForeignKey('Asset')
    sn = models.CharField(verbose_name='SN号', max_length=128, blank=True, null=True)
    model = models.CharField(verbose_name='内存型号', max_length=128)
    slot = models.CharField(verbose_name='插槽', max_length=32)
    capacity = models.IntegerField(verbose_name='内存大小（MB）')
    memo = models.TextField(verbose_name='备注', blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return '%s->%s-%s' % (self.asset_id, self.slot, self.capacity)

    class Meta:
        verbose_name = '内存条'
        unique_together = ('asset', 'slot')

    auto_create_fields = ['sn', 'slot', 'model', 'capacity']


class Disk(models.Model):
    asset = models.ForeignKey('Asset')
    sn = models.CharField(verbose_name='SN号', max_length=128, blank=True, null=True)
    slot = models.CharField(u'插槽位', max_length=64)
    model = models.CharField(u'磁盘型号', max_length=128, blank=True, null=True)
    capacity = models.FloatField(u'磁盘容量GB')
    disk_iface_choice = (
        ('SATA', 'SATA'),
        ('SAS', 'SAS'),
        ('SCSI', 'SCSI'),
        ('SSD', 'SSD'),
    )

    iface_type = models.CharField(u'接口类型', max_length=64, choices=disk_iface_choice, default='SAS')
    memo = models.TextField(u'备注', blank=True, null=True)
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True, null=True)
    auto_create_fields = ['sn', 'slot', 'manufactory', 'model', 'capacity', 'iface_type']

    class Meta:
        unique_together = ("asset", "slot")
        verbose_name = '硬盘'
        verbose_name_plural = "硬盘"

    def __str__(self):
        return '%s:slot:%s capacity:%s' % (self.asset_id, self.slot, self.capacity)

    def __str__(self):
        return '%s:slot:%s capacity:%s' % (self.asset_id, self.slot, self.capacity)


class NIC(models.Model):
    """网卡组件"""

    asset = models.ForeignKey('Asset')
    name = models.CharField(u'网卡名', max_length=64, blank=True, null=True)
    sn = models.CharField(u'SN号', max_length=128, blank=True, null=True)
    model = models.CharField(u'网卡型号', max_length=128, blank=True, null=True)
    macaddress = models.CharField(u'MAC', max_length=64, unique=True)
    ipaddress = models.GenericIPAddressField(u'IP', blank=True, null=True)
    netmask = models.CharField(max_length=64, blank=True, null=True)
    bonding = models.CharField(max_length=64, blank=True, null=True)
    memo = models.CharField(u'备注', max_length=128, blank=True, null=True)
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True, auto_now=True, null=True)

    def __str__(self):
        return '%s:%s' % (self.asset_id, self.macaddress)

    class Meta:
        verbose_name = u'网卡'

    auto_create_fields = ['name', 'sn', 'model', 'macaddress', 'ipaddress', 'netmask', 'bonding']


class RaidAdaptor(models.Model):
    """Raid卡"""

    asset = models.ForeignKey('Asset')
    sn = models.CharField(u'SN号', max_length=128, blank=True, null=True)
    slot = models.CharField(u'插口', max_length=64)
    model = models.CharField(u'型号', max_length=64, blank=True, null=True)
    memo = models.TextField(u'备注', blank=True, null=True)
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ("asset", "slot")


class Manufactory(models.Model):
    """厂商"""
    manufactory = models.CharField(u'厂商名称', max_length=64, unique=True)
    support_num = models.CharField(u'支持电话', max_length=30, blank=True)
    memo = models.CharField(u'备注', max_length=128, blank=True)

    def __str__(self):
        return self.manufactory

    class Meta:
        verbose_name = '厂商'
        verbose_name_plural = "厂商"


class BusinessUnit(models.Model):
    """业务线"""
    parent_unit = models.ForeignKey('self', related_name='parent_level', blank=True, null=True)
    name = models.CharField(u'业务线', max_length=64, unique=True)

    # contact = models.ForeignKey('UserProfile',default=None)
    memo = models.CharField(u'备注', max_length=64, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '业务线'
        verbose_name_plural = "业务线"


class Contract(models.Model):
    """合同"""

    sn = models.CharField(u'合同号', max_length=128, unique=True)
    name = models.CharField(u'合同名称', max_length=64)
    memo = models.TextField(u'备注', blank=True, null=True)
    price = models.IntegerField(u'合同金额')
    detail = models.TextField(u'合同详细', blank=True, null=True)
    start_date = models.DateField(blank=True)
    end_date = models.DateField(blank=True)
    license_num = models.IntegerField(u'license数量', blank=True)
    create_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)

    class Meta:
        verbose_name = '合同'
        verbose_name_plural = "合同"

    def __str__(self):
        return self.name


class Cabinet(models.Model):
    """机柜"""
    idc = models.ForeignKey("IDC")
    number = models.CharField(max_length=32)

    def __str__(self):
        return self.number

    class Meta:
        unique_together = ('idc', 'number')


class IDC(models.Model):
    """机房"""

    name = models.CharField(u'机房名称', max_length=64, unique=True)
    memo = models.CharField(u'备注', max_length=128, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '机房'
        verbose_name_plural = "机房"


class Tag(models.Model):
    """资产标签"""

    name = models.CharField('Tag name', max_length=32, unique=True)
    creator = models.ForeignKey('UserProfile')
    create_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class EventLog(models.Model):
    """事件"""

    name = models.CharField(u'事件名称', max_length=100)
    event_type_choices = (
        (1, u'硬件变更'),
        (2, u'新增配件'),
        (3, u'设备下线'),
        (4, u'设备上线'),
        (5, u'定期维护'),
        (6, u'业务上线\更新\变更'),
        (7, u'其它'),
    )
    event_type = models.SmallIntegerField(u'事件类型', choices=event_type_choices)
    asset = models.ForeignKey('Asset')
    component = models.CharField('事件子项', max_length=255, blank=True, null=True)
    detail = models.TextField(u'事件详情')
    date = models.DateTimeField(u'事件时间', auto_now_add=True)
    user = models.ForeignKey('UserProfile', verbose_name=u'事件源')
    memo = models.TextField(u'备注', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '事件纪录'
        verbose_name_plural = "事件纪录"

    def colored_event_type(self):
        if self.event_type == 1:
            cell_html = '<span style="background: orange;">%s</span>'
        elif self.event_type == 2:
            cell_html = '<span style="background: yellowgreen;">%s</span>'
        else:
            cell_html = '<span >%s</span>'
        return cell_html % self.get_event_type_display()

    colored_event_type.allow_tags = True
    colored_event_type.short_description = u'事件类型'


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=32)
    token = models.CharField(max_length=64, blank=True, null=True)
    phone = models.IntegerField()


class NewAssetApprovalZone(models.Model):
    """新资产待审批区"""

    sn = models.CharField(u'资产SN号', max_length=128, unique=True)
    asset_type_choices = (
        ('server', u'服务器'),
        ('switch', u'交换机'),
        ('router', u'路由器'),
        ('firewall', u'防火墙'),
        ('storage', u'存储设备'),
        ('NLB', u'NetScaler'),
        ('wireless', u'无线AP'),
        ('software', u'软件资产'),
        ('others', u'其它类'),
    )
    asset_type = models.CharField(choices=asset_type_choices, max_length=64, blank=True, null=True)
    manufactory = models.CharField(max_length=64, blank=True, null=True)
    model = models.CharField(max_length=128, blank=True, null=True)
    ram_size = models.IntegerField(blank=True, null=True)
    cpu_model = models.CharField(max_length=128, blank=True, null=True)
    cpu_count = models.IntegerField(blank=True, null=True)
    cpu_core_count = models.IntegerField(blank=True, null=True)
    os_distribution = models.CharField(max_length=64, blank=True, null=True)
    os_type = models.CharField(max_length=64, blank=True, null=True)
    os_release = models.CharField(max_length=64, blank=True, null=True)
    data = models.TextField(u'资产数据')
    date = models.DateTimeField(u'汇报日期', auto_now_add=True)
    approved = models.BooleanField(u'已批准', default=False)
    approved_by = models.ForeignKey('UserProfile', verbose_name=u'批准人', blank=True, null=True)
    approved_date = models.DateTimeField(u'批准日期', blank=True, null=True)

    def __str__(self):
        return self.sn

    class Meta:
        verbose_name = '新上线待批准资产'
        verbose_name_plural = "新上线待批准资产"
