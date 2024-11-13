from rest_framework import viewsets
from rest_framework import permissions
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from .serializers import UserSerializer, UserUpdateSerializer, LoginSerializer, CustomTokenObtainPairSerializer,CategorySerializer,PostSerializer,CommentSerializer,InformationSerializer
from .models import CustomUser, Category, Post, Comment, Information
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import viewsets, permissions
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from django.db.models import Q
from datetime import datetime
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.db import connections
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100

# 커스텀 권한 클래스를 파일 상단으로 이동
class IsAuthenticatedForAllMethods(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view)

# Create your views here.
class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            serializer = CustomTokenObtainPairSerializer(data=request.data)
            if serializer.is_valid():
                return Response({
                    'refresh': serializer.validated_data['refresh'],
                    'access': serializer.validated_data['access'],
                    'user': UserSerializer(user).data
                }, status=status.HTTP_200_OK)
        return Response({'error': '로그인 실패'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "로그아웃 성공"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "잘못된 토큰"}, status=status.HTTP_400_BAD_REQUEST)

class RefreshTokenView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh')
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                access_token = str(token.access_token)
                return Response({'access': access_token}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': '유효하지 않은 refresh 토큰'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'refresh 토큰이 제공되지 않았습니다.'}, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(APIView):
    def get(self, request):
        return Response({'message': 'Hello, World!'}, status=status.HTTP_200_OK)
    def put(self, request):
        return Response({'message': 'Hello, World!'}, status=status.HTTP_200_OK)
    def delete(self, request):
        return Response({'message': 'Hello, World!'}, status=status.HTTP_200_OK)
    
class UpdateProfileView(APIView):
    def put(self, request):
        return Response({'message': 'Hello, World!'}, status=status.HTTP_200_OK)

class DeleteProfileView(APIView):
    def delete(self, request):
        return Response({'message': 'Hello, World!'}, status=status.HTTP_200_OK)

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['category__name']
    ordering_fields = ['date', 'title','author','category']  # 정렬 가능한 필드 지정
    search_fields = ['title', 'content']  # 검색 가능한 필드 지정

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        queryset = Post.objects.all()
        category = self.request.query_params.get('category', None)
        author = self.request.query_params.get('author', None)
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        search = self.request.query_params.get('search', None)

        if category:
            queryset = queryset.filter(category__name=category)
        if author:
            queryset = queryset.filter(author__username=author)
        if start_date and end_date:
            try:
                start = datetime.strptime(start_date, '%Y-%m-%d').date()
                end = datetime.strptime(end_date, '%Y-%m-%d').date()
                queryset = queryset.filter(date__date__range=[start, end])
            except ValueError:
                pass  # 날짜 형식이 잘못된 경우 무시
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(content__icontains=search)
            )
        return queryset

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['post']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        queryset = Comment.objects.filter(parent=None)  # 최상위 댓글만 가져옵니다
        post = self.request.query_params.get('post', None)
        if post is not None:
            queryset = queryset.filter(post__id=post)
        return queryset

class InformationViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    # 목록 조회
    def list(self, request):
        queryset = Information.objects.all()
        page = self.paginate_queryset(queryset)
        serializer = InformationSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)
    
    # 상세 조회
    def retrieve(self, request, pk=None):
        information = get_object_or_404(Information, pk=pk)
        information.views += 1
        information.save()
        serializer = InformationSerializer(information)
        return Response(serializer.data)
    
    # 생성
    def create(self, request):
        serializer = InformationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # 수정
    def update(self, request, pk=None):
        information = get_object_or_404(Information, pk=pk)
        if information.author != request.user:
            return Response({"error": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = InformationSerializer(information, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # 부분 수정
    def partial_update(self, request, pk=None):
        information = get_object_or_404(Information, pk=pk)
        if information.author != request.user:
            return Response({"error": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = InformationSerializer(information, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # 삭제
    def destroy(self, request, pk=None):
        information = get_object_or_404(Information, pk=pk)
        if information.author != request.user:
            return Response({"error": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        
        information.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class NsaResourceView(APIView):
    # connection = pymysql.connect(host='localhost', user='root', password='7F5c2c3c4@!#', db='kkotest', charset='utf8')
    
    
    def my_custom_sql_function(self):
        connection = connections['default']
        sql = "SELECT * FROM post"
        params = ['post']  # SQL 인젝션 방지를 위해 파라메터 사용

        with connection.cursor() as cursor:
            cursor.execute(sql)
            results = cursor.fetchall()
        print(f'results: {results}')        
        return results
# connection = connctions['default']
    def get(self, request):
        self.my_custom_sql_function()
        return Response({'message': 'Hello, World!'}, status=status.HTTP_200_OK)