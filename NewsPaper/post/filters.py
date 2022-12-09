from django_filters import FilterSet
from .models import Post


class PostFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
            'time': ['gt'],
            'title': ['icontains'],
            'author': ['exact'],
        }

    def __init__(self, *args, **kwargs):
        super(PostFilter, self).__init__(*args, **kwargs)
        # При первом вызове не отображать никаких результатов
        if self.data == {}:
            self.queryset = self.queryset.none()
