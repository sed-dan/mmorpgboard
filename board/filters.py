from django_filters import FilterSet

from board.models import Response, Post


class ResponseFilter(FilterSet):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = kwargs['request']
        self.filters['resp_post'].label = ''
        self.filters['resp_post'].empty_label = 'Все объявления'
        self.filters['resp_post'].queryset = Post.objects.filter(author=self.user)

    class Meta:
        model = Response
        fields = ['resp_post']