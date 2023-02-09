from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.
class Coupon(models.Model):
    coupon_name = models.CharField(max_length=100, unique=True)
    coupon_type = models.CharField(max_length=10,choices=[("percentage", "정률"), ("fixed", "정액")])
    discount_rate = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(0.5)])
    discount_amount = models.IntegerField(default=0)
    minimum_amount = models.IntegerField(default=0)
    is_issued = models.BooleanField(default=False)
    is_used = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def clean(self):
        if self.coupon_type == 'fixed' and self.discount_amount > self.minimum_amount:
            raise ValidationError({'discount_amount' : '할인금액은 최소주문금액보다 클 수 없습니다.'})

    def __str__(self):
        return self.coupon_name


