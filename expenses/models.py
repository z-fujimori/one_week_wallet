from django.db import models

# Create your models here.
class Tag(models.Model):
    id = models.AutoField(
        primary_key=True
    )  # わかりやすさ重視でUUIDではなく連番
    name = models.CharField(
        verbose_name=("タグ名(name)")
    )
    image_url = models.CharField(
        max_length=200,
        verbose_name=("画像(image_url)")
    )
    color = models.CharField(
        max_length=100,
        verbose_name=("指定色(color)")
    )

class Expense(models.Model):
    id = models.AutoField(
        primary_key=True
    )  # わかりやすさ重視でUUIDではなく連番
    title = models.CharField(
        verbose_name=("タイトル(title)"),
        max_length=100,
    )
    amount = models.IntegerField(
        verbose_name=("金額(amount)"),
    )
    date = models.DateField(
        verbose_name=("日付(date)")
    )
    tag_id = models.ForeignKey(
        Tag,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    user_id = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE
    )


