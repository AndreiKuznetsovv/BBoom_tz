from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .models import User, Post
from .permissions import IsOwnerOrReadOnly
from .serializers import PostSerializer, UserSerializer


class UserListAPIView(ListAPIView):
    '''
    ALLOWED methods: GET
    Return a list of ALL users
    Method Get - only for ADMIN users
    '''
    permission_classes = [IsAdminUser]

    queryset = User.objects.all()
    serializer_class = UserSerializer


class PostListAPIView(ListAPIView):
    '''
    ALLOWED methods: GET
    Return a list of all posts of requested (by id)
    Method Post - only for AUTHENTICATED users
    '''
    permission_classes = [IsAuthenticated]

    # queryset = User.objects.all()
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        user = self.kwargs['user']
        queryset = Post.objects.filter(user_id=user)
        # queryset = User.objects.filter(id=user).prefetch_related('post_set')
        return queryset


class PostRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    ALLOWED METHODS: GET, PUT, PATH, DELETE
    Concrete view for retrieving, updating or deleting a model instance.
    Unsafe methods DELETE, PUT, PATCH only for OWNER of the post
    Safe method GET - for all users
    """
    permission_classes = [IsOwnerOrReadOnly]

    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostCreateAPIView(CreateAPIView):
    """
    ALLOWED methods: POST
    Concrete view for creating a model instance.
    Method Post only for AUTHENTICATED users
    """
    permission_classes = [IsAuthenticated]

    queryset = Post.objects.all()
    serializer_class = PostSerializer
