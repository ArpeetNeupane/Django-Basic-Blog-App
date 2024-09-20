from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Comment
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .forms import CommentForm

'''
post = [
    {
        'author': 'John Doe',
        'title': 'Blog Post 1',
        'content': 'First Post Content',
        'date_posted': 'September 2, 2024'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second Post Content',
        'date_posted': 'September 2, 2024'
    },
    {
        'author': 'John Raam Doe',
        'title': 'Blog Post 3',
        'content': 'Third Post Content',
        'date_posted': 'September 27, 2024'
    }
]
'''

'''
def home(request):
    return HttpResponse('<h1>Blog Home</h1>') ->before using templates
'''

#these are function based views
#our url patterns are directed to a certain view which as these functions and the views handle the logic for the routes
#and then render our templates  
'''
@login_required(login_url='login')  # redirect to login if not authenticated
def home(request):
    context = { #context is a dict
        #'posts': post  ---- which is dictionary we created above, for dummy data which is passed as render's 3rd argument, allowing us to access it(the key of dict which is posts) within the template
        'posts': Post.objects.all() #don't have to change anything as fieldnames in databases are same
    }
    return render(request, 'blog/home.html', context) #render is also just returning a HTTP response in the bg, views alsways need to return a http response or an exception
'''
    
class PostListView(LoginRequiredMixin, ListView):
    #LoginRequiredMixin is a django built-in mixin which is used to add functionality to views, forms, and models, 
    #allowing developers to reuse code and improve the efficiency of their applications.
    #Mixins are typically defined as classes, and can be added to other classes by using inheritance.
    model = Post #this will tell our listview what model to query to create the list, in this case, its post
    #model = Post will use a default queryset (select *), if filtering is needed we should use def get_queryset(self)
    template_name = 'blog/home.html' #looks for directory -- <app>/<model>_<viewtype>.html
    #by default it looks for a template which follows a certain naming convention for template so we're changing where it looks for the template
    ##but just doing this is not enough as we're using variable called post in home.html, but class based view uses variable called objetct_list by default##
    #2 ways to solve that, change variable name to object_list or let the class know that we want the variable to be
    #called post, we're doin the latter
    context_object_name = 'posts'
    ordering = ['-last_updated'] #writing just date_posted orders from oldest to newest, so we added '-' for newest to oldest, ast_updated is used here

    #we dont need to import paginate at all, just use it as an attribute as we're using a CBV
    paginate_by = 13

#view for all of a user's post
class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 13

    def get_queryset(self):
        user = get_object_or_404(User, username = self.kwargs.get('username'))
        #if user exists, username variable captures the username, if doesn't exists, instead of returning blank page which is bad ui, we're returning 404
        return Post.objects.filter(author=user).order_by('-last_updated')
        #since we are overriding the query the list view will be making, the ordering is reset, so removed it above and added here

#detailed view for individual post
class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    #method is used to add additional context to the template
    #get_context_data is detailview's method
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) #calls parent class to see if any prior comments are there (; initializes the context with the post object and any other context data.)
        #creating 2 keys for context and returning
        context['form'] = CommentForm() #Adds an empty CommentForm instance to the context, which will be used in the template to allow users to submit new comments.
        #adds a new CommentForm instance to the context, used in the template to allow users to submit new comments

        context['comments'] = self.object.post_comment.all()
        #This line adds the list of comments related to the current post to the context. self.object refers to the post object being viewed(self.object refers to the post instance), 
        #and self.object.post_comment.all() retrieves all comments associated with this post. post_comment is related name for accessing the comments from the post model
        return context
    
    #handles the submission of the comment form
    #The post() method is a lower-level method in Django views that directly handles HTTP POST requests. It allows you to define custom 
    #behavior for processing POST data, including handling form submissions.
    def post(self, request, *args, **kwargs):
        post = self.get_object() #self.get_object() is a method provided by DetailView that returns the object(Post) being viewed.
        form = CommentForm(request.POST) #Creates a new CommentForm instance populated with the data from the POST request. This data includes the user’s comment input.
        if form.is_valid():
            comment = form.save(commit=False) #Creates a new Comment instance with the form data but not committing it to the database yet
            comment.post = post #Associates the comment with the current post
            comment.user = request.user #Sets the comment user to the one who made the request(commented)
            comment.save() #saving to datbase
        return redirect('post-detail', pk=post.pk) #This prevents the form from being resubmitted if the user refreshes the page, pk is used in identifying which post to display as there could be a lot of posts.

#create post using CBV
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    #create view automatically create forms but doesn't provide fields by itself for security reasons
    fields = ['title', 'content']
    #if you don’t specify fields or form_class, you’ll get an error since Django won’t know how to generate the form for you

    #The form_valid method is executed after Django confirms that the form has passed all the validation rules.
    #handles what happens after a form has been successfully validated and submitted
    def form_valid(self, form):
        form.instance.author = self.request.user
        #form.instance refers to the object that is being created through the form. For example, if you are creating a new Post object, form.instance is that Post object in memory before it’s saved.
        #self.request.user refers to the currently logged-in user. Django tracks the user making the request, and the user object is available as self.request.user.
        #By setting form.instance.author = self.request.user, we are effectively saying: "Before saving the form to the database, set the author field of the post to the currently logged-in user."
        return super().form_valid(form) #super().... performs the default behavior of saving the form.
        #using super(), parent class is called. This ensures that Django continues with its normal form-handling logic

    #get_success_url in the view for redirecting to the home page after form submission is successful
    def get_success_url(self):
        #reverse('blog-home'): This function takes the name of a URL ('home' in this case) and returns the actual URL path, used when FBV
        #reverse_lazy('blog-home') is used when you want to delay the return for a bit, used in CBV
        #reverse_lazy is used because it waits to resolve the URL until it's actually needed (when the view is executed)
        return reverse_lazy('blog-home')
        #return '' -- hardcoding isn't recommended, because if you want to change the home page, every hard coded link have to be changed

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):#mixins need to be left of the UpdateView
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.pk})
    
    def test_func(self):
        #getting the exact post that we're currently updating using get
        post = self.get_object()

        #checking if current user is the author of this post, self.request.user-current logged in user
        if self.request.user == post.author:
                return True
        return False

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['content']

    def form_valid(self, form):
        form.instance.user = self.request.user  # Associate the current user with the comment
        return super().form_valid(form)

    # Redirect to the post detail view after successful update
    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})
        #no need for post pk, the CommentUpdateView will use the comment's pk

    # Ensure only the comment author can update their comment
    def test_func(self):
        comment = self.get_object()  # Retrieve the comment being updated
        return self.request.user == comment.user

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False #after returning true it will exit the function so return False is not executeed
    
    def get_success_url(self):
        return reverse_lazy('blog-home')
    
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.user
    
    def get_success_url(self):
        return reverse_lazy('post-detail' , kwargs={'pk': self.object.post.pk})

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'}) #if it's small enough, you don't need to create a dictionary, and straight-up pass it as argument

#class based views have a lot more built-in functionality that'll handle a lot of backend logic for us
#there are a lot of class based views = list views, detail views, create views, update views, delete views.
#in class-based view, we are basically setting variables, but in function-based view, we have to render that function and pass in that information

