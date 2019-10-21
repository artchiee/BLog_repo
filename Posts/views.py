from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView, DeleteView
)
from django.shortcuts import render, get_object_or_404, Http404, redirect, render_to_response
from .models import (MyPosts, Comments, Category)
from django.utils import timezone
from django.urls import reverse_lazy

# These imports for pagination
from django.db.models import Q
from django.core.paginator import (
    Paginator,
    PageNotAnInteger, EmptyPage
)
from .forms import (Form_Change, CommentForm)

# i use generic views here
# Create your views here.




# Making view page with functions 


def IndexView(request):
    template_name = 'Index.html'
    today_date = timezone.now().date()
    queryset = MyPosts.objects.active()

       #Search post if its exists

    query = request.GET.get("query_post")
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query)|
            Q(content__icontains =query)|
            Q(user__email__icontains = query)
        ).distinct()


    context = {
        'myposts' : queryset,
        'today_date' : today_date,
        "title": "List",

               }
    return render(request, template_name, context)



# Making a class BV for Detail view
class DetailHome(DetailView):
    model = MyPosts
    template_name = 'Detail_page.html'
    #ontext_object_name = 'instance'

    # define a get context data
    def get_context_data(self, *args, **kwargs):
        contx = super(DetailHome, self).get_context_data(**kwargs)
        contx['instance'] = get_object_or_404(MyPosts, pk=self.kwargs['pk'])
        return contx


# Create Posts View

class CreateForm(CreateView):
    form_class = Form_Change
    model = MyPosts
    template_name = 'form_page.html'

# import daterime  datetime.date.today()

    # define get request
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    # def a Post request to handle the form
    def post(self, request, *args, **kwargs):
        form = self.form_class(self.request.POST, self.request.FILES)
        # process form valid
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    # Process if the form.is_valid

    def form_valid(self, form, **kwargs):
        # dic = self.get_context_data(**kwargs)
        # dic ['form'] = form
        instance = form.save(commit=False)
        print(form.cleaned_data.get('post_title , \n,  post_content'))
        instance.user = self.request.user
        instance.save()
        return redirect('/Index')
        return render(self.request, self.template_name)

    # IF the form is not valid
    def form_invalid(self, request, form):
        # dic = self.get_context_data(**kwargs)
        # dic ['form'] = form
        print('You have an invalid form data')
        return render(request, template_name, dic)


# Update the posts here

class Update_Posts(UpdateView):
    form_class = Form_Change
    model = MyPosts
    template_name = 'form_page.html'

    # Define a post method
    def post(self, request, pk):
        if self.request.user.admin_user or self.request.user.staff_user or self.request.user.active_user:
            instance = get_object_or_404(MyPosts, pk=pk)
            form = self.form_class(
                self.request.POST, self.request.FILES or None, instance=instance)
            if form.is_valid():
                return self.form_valid(form)
            else:
                print('this data isn\'t Valid')

    # Check if the form is valid

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.save()
        print('Your post has been successfuly updated ')
        return redirect('/Index')

        # Delete users oxn posts


class Delete_Your_Post(DeleteView):
    model = MyPosts
    # LAter try to use the same template as delete comments with slightly
    # diffrent text
    template_name = 'delete_your_post.html'
    success_url = '/Index'

    # implementing a content to show post content before removing it
    def get_context_data(self, **kwargs):
        context = super(Delete_Your_Post, self).get_context_data(**kwargs)
        context['getpost'] = get_object_or_404(MyPosts, pk=self.kwargs['pk'])
        #context['post'] = get_object_or_404(MyPosts, pk=self.kwargs['pk'])
        return context

# Creating a view to add a comments


class Add_Comments(CreateView):
    model = Comments
    form_class = CommentForm
    template_name = 'add_comment.html'

    # get queryset to see if the post requested is correct
    # def get_queryset(self, pk ):
    #     post =  get_object_or_404(MyPosts, pk=pk)
    #     return post

    # def get_context_data(self,*args, **kwargs):
    #     context = super(Add_Comments, self).get_context_data(**kwargs)
    #     context['get_post'] = Comments.objects.raw('select Posts_myposts.id from Posts_mypost where id = post_title)
    #     return context

    # define a post method
    def post(self, *args, **kwargs):
        form = self.form_class(self.request.POST, self.request.user)
        if form.is_valid():
            return self.form_valid(form)
        else:
            print('Form Invalid ')

    def form_valid(self, form):
        post_comment = form.save(commit=False)
        post_comment.user = self.request.user
        # post_comment.post_name = self.posts  # i tried getting the selected post
        post_comment.save()
        print('Your comment have been saved ')
        return redirect('/Index')

        # View for updating each user's comments


class UpdateOwnComment(Update_Posts):
    model = Comments
    # this is the same template as the one used above but in here it will render
    # only one comment to update
    template_name: 'add_comment.html'
    form_class = CommentForm
    success_url = '/Index'

    # Fixing a object error

    def post(self, request, *args, **kwargs):
        # self.object = self.get_object()
        # return super(UpdateOwnComment, self).post(request, *args, **kwargs)
        instance = get_object_or_404(Comments, pk=self.kwargs['pk'])
        form = self.form_class(request.POST, instance=instance)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_sinvalid(form)

    def get(self, *args, **kwargs):
        self.object = self.get_object()
        return super(UpdateOwnComment, self).get(self.request, *args, **kwargs)

    # edfine a function for F.valid
    def form_valid(self, form):
        post_comment = form.save(commit=False)
        post_comment.user = self.request.user
        post_comment.save()
        print('Your comment has been updated')
        return redirect('/Index')

    def form_invalid(self, form):
        print('You have an invalid form data')
        return render(self.request, self.template_name, {'form': self.form})

    # Delete users each comment view


class DeleteOwnComment(DeleteView):
    model = Comments
    template_name = 'delete_your_comment.html'
    success_url = ('/Index')

    def get_context_data(self, *args, **kwargs):
        context = super(DeleteOwnComment, self).get_context_data(**kwargs)
        context['instance'] = get_object_or_404(Comments, pk=self.kwargs['pk'])
        #context['post'] = get_object_or_404(MyPosts, pk=self.kwargs['pk'])
        return context

    # Category View


class CategoryHomeView(ListView):
    model = MyPosts
    template_name = 'category_view.html'

    # def get_queryset(self):
    #     category = get_object_or_404(MyPosts, pk=self.kwargs['pk'])
    #     return MyPosts.objects.active().filter(category=self.category)

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryHomeView, self).get_context_data(**kwargs)
        category = get_object_or_404(Category, pk=self.kwargs['pk'])
        context['allcategories'] = MyPosts.objects.filter(category=category)
        return context
