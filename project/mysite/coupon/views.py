from django.http import Http404
from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication
from .models import Coupon
from .serializers import CouponCreateSerializer, CouponViewSerializer, CouponIssueSerializer, CouponUseSerializer, UserSerializer
from django.contrib.auth.models import User
from django.db import transaction

# Create your views here.
#쿠폰 생성 및 조회
class CouponListAPI(APIView):
    authentication_classes = [SessionAuthentication]
    #쿠폰 생성
    def post(self, request, format=None):
        # 관리자만 가능
        admin = request.user
        if not admin.is_staff:
            return Response({"error": "괸리자가 아닙니다."})

        serializer = CouponCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 쿠폰 목록 조회
    def get(self, request):
        # 관리자만 가능
        admin = request.user
        if not admin.is_staff:
            return Response({"error": "괸리자가 아닙니다."})

        queryset = Coupon.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 5
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = CouponViewSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

#쿠폰 삭제
class CouponDetailAPI(APIView):
    authentication_classes = [SessionAuthentication]
    def get_object(self, pk):
        try:
            return Coupon.objects.get(pk=pk)
        except Coupon.DoesNotExist:
            raise Http404

    #쿠폰 조회
    def get(self, request, pk):
        # 관리자만 가능
        admin = request.user
        if not admin.is_staff:
            return Response({"error": "괸리자가 아닙니다."})

        coupon = self.get_object(pk)
        serializer = CouponViewSerializer(coupon)
        return Response(serializer.data)

    #쿠폰 삭제
    def delete(self, request, pk):
        # 관리자만 가능
        admin = request.user
        if not admin.is_staff:
            return Response({"error": "괸리자가 아닙니다."})

        coupon = self.get_object(pk)
        coupon.is_deleted = True
        coupon.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

#쿠폰 발행 API
class CouponIssueAPI(APIView):
    authentication_classes = [SessionAuthentication]
    #쿠폰 발급
    def post(self, request, format=None):
        #관리자만 가능
        admin = request.user
        if not admin.is_staff:
            return Response({"error": "괸리자가 아닙니다."})

        id = request.data.get('id')
        user_id = request.data.get('user_id')
        try:
            coupon = Coupon.objects.get(id=id)
        except Coupon.DoesNotExist:
            return Response({"error": "쿠폰을 찾을 수 없습니다."},status=status.HTTP_404_NOT_FOUND)
        coupon.is_issued = True
        coupon.user = User.objects.get(id=user_id)
        coupon.save()
        serializer = CouponIssueSerializer(coupon)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # 쿠폰 목록 조회
    def get(self, request):
        # 관리자만 가능
        admin = request.user
        if not admin.is_staff:
            return Response({"error": "괸리자가 아닙니다."})

        queryset = Coupon.objects.all()
        serializer = CouponIssueSerializer(queryset, many=True)
        return Response(serializer.data)

#쿠폰 사용 API
class CouponUserAPI(APIView):
    authentication_classes = [SessionAuthentication]
    #쿠폰 사용
    def post(self, request, format=None):
        serializer = CouponUseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        id = serializer.validated_data.get('id')
        coupon = Coupon.objects.get(id=id)

        if request.user != coupon.user:
            return Response({"error": "쿠폰을 사용할 수 없는 유저입니다."}, status=status.HTTP_400_BAD_REQUEST)

        #동시 사용 방지를 위한 트랜잭션 처리
        with transaction.atomic():
            coupon.is_used = True
            coupon.save()

        return  Response({"success": "쿠폰이 사용되었습니다."}, status=status.HTTP_201_CREATED)

    # 쿠폰 사용 목록 조회
    def get(self, request):
        user = request.user
        queryset = Coupon.objects.filter(is_used=True, user=user)
        serializer = CouponUseSerializer(queryset, many=True)
        return Response(serializer.data)

#회원가입 API
class SignupAPI(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def post(self, request):
        user = request.data

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)