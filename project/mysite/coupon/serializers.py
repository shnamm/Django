from rest_framework import serializers
from .models import Coupon
from django.contrib.auth.models import User

class CouponCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ('coupon_name', 'coupon_type', 'discount_rate', 'discount_amount', 'minimum_amount')

    #둘 중에 하나만 입력해도 POST요청 가능하게 해줌
    discount_rate = serializers.FloatField(required=False, default=0)
    discount_amount = serializers.IntegerField(required=False, default=0)

    #할인율, 할인금액 디폴트 설정
    def create(self, validated_data):
        admin = User.objects.get(username='admin')
        validated_data['user'] = admin
        validated_data.setdefault('discount_rate', 0)
        validated_data.setdefault('discount_rate', 0)
        return super().create(validated_data)
    #쿠폰이름 중복 방지
    def validate_coupon_name(self, value):
        if Coupon.objects.filter(coupon_name=value).exists():
            raise serializers.ValidationError("이미 존재하는 쿠폰 이름입니다.")
        return value
    #할인금액은 양수
    def vaidate_discount_amount(self, value):
        if value < 0:
            raise serializers.ValidationError("할인금액은 0 또는 양수입니다.")
        return value
    #최소주문금액 양수
    def vaidate_minimum_amount(self, value):
        if value < 0:
            raise serializers.ValidationError("최소주문금액은 0 또는 양수입니다.")
        return value

    #정액쿠폰, 정률쿠폰 조건
    def validate(self, attrs):
        coupon_type = attrs.get('coupon_type')
        discount_rate = attrs.get('discount_rate')
        discount_amount = attrs.get('discount_amount')
        minimum_amount = attrs.get('minimum_amount')

        if coupon_type == 'fixed' and discount_amount > minimum_amount:
            raise serializers.ValidationError("할인금액은 최소주문금액보다 클 수 없습니다.")
        if coupon_type == 'percentage' and discount_rate > 0.5:
            raise serializers.ValidationError("할인율은 50%를 초과할 수 없습니다.")
        return attrs

#쿠폰 조회 시리얼라이저
class CouponViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'

    #coupon_type에 따라 할인율이나 할인금액을 빼고 보여주는 함수
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation['coupon_type'] == 'fixed':
            representation.pop('discount_rate', None)
        if representation['coupon_type'] == 'percentage':
            representation.pop('discount_amount', None)
        return representation

#쿠폰발급
class CouponIssueSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    id = serializers.IntegerField()

    #10개 이상이면 에러를 띄우는 함수
    def validate(self, data):
        user_id = data.get('user_id')
        id = data.get('id')

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError("유저가 존재하지 않습니다.")

        try:
            coupon = Coupon.objects.get(id=id)
        except Coupon.DoesNotExist:
            raise serializers.ValidationError("쿠폰이 존재하지 않습니다.")

        if coupon.user != user:
            raise serializers.ValidationError("사용가능한 쿠폰이 아닙니다.")

        if coupon.is_issued:
            raise serializers.ValidationError("이미 발행된 쿠폰입니다..")

        # 10개 이상이면 에러표시
        if Coupon.objects.filter(user=user, is_issued=True, is_used=False, is_deleted=False).count() >= 10:
            raise serializers.ValidationError("쿠폰을 10개 이상 발급받을 수 없습니다.")

        return data

#쿠폰사용
class CouponUseSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    def validate(self, data):
        id = data.get('id')

        try:
            coupon = Coupon.objects.get(id=id)
        except Coupon.DoesNotExist:
            raise serializers.ValidationError("쿠폰이 존재하지 않습니다.")

        if coupon.is_used:
            raise serializers.ValidationError("이미 사용된 쿠폰입니다.")

        return data

#사용자
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password", "email")

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)