from django.shortcuts import render
# django.views.genericからTemplateView, ListViewをインポート
from django.views.generic import TemplateView, ListView
# django.views.genericからCreateViewをインポート
from django.views.generic import CreateView
# django.urlsからreverse_lazyをインポート
from django.urls import reverse_lazy
# formsモジュールからPhotoPsotFormをインポート
from .forms import PhotoPostForm
# method_decoratorをインポート
from django.utils.decorators import method_decorator
# login_requiredをインポート
from django.contrib.auth.decorators import login_required
# modelsモジュールからモデルPhotoPostをインポート
from .models import PhotoPost

from django.views.generic import DetailView

class IndexView(ListView):
    '''トップページビュー
    '''
    # index.htmlをレタリングする
    template_name ='index.html'
    # モデルBlogPostのオブジェクトにorder_by()を適用して
    # 投稿日時の降順で並び替える
    queryset = PhotoPost.objects.order_by('-posted_at')
    # 1ページに表示するレコードの件数
    paginate_by = 9
    
@method_decorator(login_required, name='dispatch')
class CreatePhotoView(CreateView):

    form_class = PhotoPostForm
    
    template_name = "post_photo.html"

    success_url = reverse_lazy('photo:post_done')

    def form_valid(self, form):
        
        postdata = form.save(commit=False)

        postdata.user = self.request.user
        
        postdata.save()

        return super().form_valid(form)
    
class PostSuccessView(TemplateView):
    
    template_name = 'post_success.html'

class CategoryView(ListView):

    template_name = 'index.html'

    paginate_by = 9

    def get_queryset(self):

        category_id = self.kwargs['category']

        categories = PhotoPost.objects.filter(
            category=category_id).order_by('-posted_at')

        return categories
    
class UserView(ListView):
    
    template_name = 'index.html'

    paginate_by = 9
    
    def get_queryset(self):
        
        user_id = self.kwargs['user']

        user_list = PhotoPost.objects.filter(
            user=user_id).order_by('-posted_at')

        return user_list

class DetailView(DetailView):
    
    template_name = 'datail.html'

    model = PhotoPost
    
class MypageView(ListView):
    
    template_name = 'mypage.html'

    pagenate_by = 9
    
    def get_queryset(self):
        
        queryset = PhotoPost.objects.filter(
            user=self.request.user).order_by('-posted_at')
        
# Create your views here.
