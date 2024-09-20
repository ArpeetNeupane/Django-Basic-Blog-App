from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length = 100)
    content = models.TextField()
    date_posted = models.DateTimeField(default = timezone.now) #timezone is a function but here we're passing the actual function as default value, we dont want to trigger/activate the function hence not writing the paranthesis
    #Another way of saying that is : Instead of calling timezone.now() (which would store the current time immediately when Post is called), the function timezone.now is passed as a reference to be called when a new Post instance is created. This ensures the date_posted is set to the exact time when the post is created.
    #parameter auto_now = True -- every time the post is updaed, date_posted is updated to update date AND auto_now_add = True doesn't change and only keeps date of when object was created
    #Django's DateTimeField expects the default parameter to be a callable, not an immediate value, so this doesn't work: date_posted = models.DateTimeField(timezone.now)
    
    last_updated = models.DateTimeField(auto_now=True) #saves every time new update is made

    #as django provides a way to create user and there is a one-to-many relation between user and post
    #we use a foreign key to establish a relationship

    author = models.ForeignKey(User, on_delete = models.CASCADE)#post is deleted if user is deleted
    #we need to tell what to do with the post in case a user is deleted, on_delete is helpful in that scenario
    #If you want to keep the content (posts) even after the associated user is deleted, use on_delete = models.SET_NULL null = True (needed) (author will be null) or on_delete=models.SET_DEFAULT (author name will be default, you need to set default)
    #on_delete = models.PROTECT: When you try to delete a User instance that has related Post instances, Django will raise a ProtectedError. This prevents the deletion of the User and keeps the related posts intact.


    #need to migrate(in cmd) after changes which is a great way to easily update your database with heavy SQL commands

    def __str__(self): #double underscore is called dunder, these methods are called special/magic methods
        return self.title #for now returning title when instance is called
    
    #about __repr__ and __str__, repr is for developers, debuggers, goal of repr is to be unambiguous(gives output which is passable to eval(), which means it returns output which itself looksd like py command)
    #str is more user-friendly version of repr , goal of str's is to be readable(str not all able to eval())
    #if we have repr defined but not str, when str is called, it will fallback to repr.

    #helper method to easily count number of likes and comments on a post, can be done through related_name
    def total_likes(self):
        return self.post_likes.count()
    
    def total_comments(self):
        return self.post_comment.count()

class Like(models.Model):
    #defining relationship between likes and post, user
    post = models.ForeignKey(Post, related_name='post_likes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('post', 'user')
        #this is a meta constraint which makes it so that one user can like a post only once uless they unlike first

    def __str__(self):
        return f"Liked by {self.user} on {self.post}"

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='post_comment', on_delete=models.CASCADE) #sets a null value to pointing user
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    commented_at = models.DateTimeField(auto_now=True)
    content = models.TextField()

    def __str__(self):
        return f"Commented by {self.user} on {self.post}"





