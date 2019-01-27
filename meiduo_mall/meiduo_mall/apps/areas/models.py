from django.db import models


class Area(models.Model):
    """
    行政区划
    """

    name = models.CharField(max_length=20, verbose_name="名称")
    # 自关联字段的外键指向自身，所以ForeignKey('self')
    # 通过on_delete选项指明主表删除数据时，对于外键引用表数据如何处理,SET_NULL 设置为NULL，仅在该字段null=True允许为null时可用
    # 需要使用related_name指明查询一个行政区划的所有下级行政区划时，使用哪种语法查询，
    # 如本模型类中指明通过Area模型类对象.subs查询所有下属行政区划，而不是使用Django默认的Area模型类对象.area_set语法
    # null如果为True，表示允许为空，默认值是False
    # blank如果为True，则该字段允许为空白，默认值是False
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, related_name="subs", null=True, blank=True, verbose_name="上级行政区划")

    class Meta:
        db_table = "tb_areas"
        verbose_name = "行政区划"
        verbose_name_plural = "行政区划"

    def __str__(self):
        return self.name
