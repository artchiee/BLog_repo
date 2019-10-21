from django.conf.urls import url
from . import views as pv

# Register Your url here 

urlpatterns = [
    #   For fV 
    url(r'^', pv.IndexView, name= 'Index'),
    url(r'^(?P<pk>\d+)/$', pv.DetailHome.as_view(),  name='post_detail'),
    url(r'^create_a_post/$',pv.CreateForm.as_view(),  name='Create_post'),
    url(r'^update_a_post/(?P<pk>\d+)/$',pv.Update_Posts.as_view(),  name='UpdatePosts'),
    url(r'^delete_a_post/(?P<pk>\d+)/$',pv.Delete_Your_Post.as_view(),  name='delete_your_post'),
        # Category list url 
    url(r'^(?P<pk>\d+)/category/$',pv.CategoryHomeView.as_view(), name='category_list'),

    # Comments Views 
    url(r'^(?P<pk>\d+)/addcomment/$', pv.Add_Comments.as_view(), name='add_comment'),
    url(r'^update_your_comment/(?P<pk>\d+)/$', pv.UpdateOwnComment.as_view() , name='update_comment'),
    url(r'^(?P<pk>\d+)/delete_your_comment/$', pv.DeleteOwnComment.as_view(), name='delete_own_comment')


]














