from django.shortcuts import render, get_object_or_404, redirect
from .models import TravelPost,TravelImage,Comment,UserProfile
from .models import Contact as ContactModel
from .forms import CommentForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
  
# Create your views here.

def Index(request):
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    return render(request, "blog/shop_page.html",{
        "user":user,
        "user_profile":user_profile})

@login_required()
def Home(request):
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    return render(request, "blog/home.html",{"user_profile":user_profile})


@login_required()
def Blogs(request):
    posts = TravelPost.objects.all().order_by('-id')

    context = {
        'posts': posts
    }
    return render(request, "blog/blog_page.html", context)

@login_required()
def public_blog(request):
    posts = TravelPost.objects.select_related('user') \
        .prefetch_related('images', 'likes', 'comments') \
        .order_by('-id')

    return render(request, "blog/public_blog.html", {'posts': posts})



@login_required()
def Like_post(request, pk):
    post = TravelPost.objects.get(pk=pk)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect('blog')   # ✅ FIXED

@login_required()   
def add_comment(request, pk):
    if request.method == "POST":
        post = TravelPost.objects.get(pk=pk)
        content = request.POST.get("content")

        Comment.objects.create(
            user=request.user,
            post=post,
            content=content
        )

    return redirect('blog')

@login_required()
def Post_detail(request, pk):
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    post_d = get_object_or_404(TravelPost, pk=pk)
    comments = post_d.comments.all().order_by('-date')        # it is used for realated_name="comments"
    form = CommentForm()

    if request.method == "POST":
        form = CommentForm(request.POST)
        comment = form.save(commit=False)
        comment.post = post_d
        comment.user = request.user
        comment.save()
        messages.success(request,"Comment added successfully...!")
        return redirect("post_detail",pk=post_d.pk)

    return render(request, "blog/post_detail.html", {
        'post_d': post_d,
        'comments': comments,
        'form': form,
        "user_profile":user_profile
    })

@login_required
def Delete_comment(request, comment_id):

    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.user or request.user.is_superuser:

        comment.delete()
        messages.success(request, "Comment deleted.")
    else:
        messages.warning(request, "You don't have permission to delete this comment.")
    return redirect('post_detail', pk=comment.post.pk)


# @login_required
# def Like_post(request, pk):
#     post = TravelPost.objects.get(pk=pk)
#     if request.user in post.likes.all():
#         post.likes.remove(request.user)
#     else:
#         post.likes.add(request.user)
#     return redirect('post_detail', pk=pk)


@login_required()
def Post_form(request):
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    return render(request, "blog/post_form.html",{"user_profile":user_profile})

@login_required()
def Post_blog(request):    #Post all data from form fields to database
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    if request.method == "POST":
        title = request.POST.get("title")  # get value from post_form
        destination = request.POST.get("destination")
        date = request.POST.get("date")
        description = request.POST.get("description")
        images = request.FILES.getlist("images")
        video = request.FILES.get("video")

        try:
            post = TravelPost.objects.create(
                user=request.user,
                title= title,
                destination = destination,
                date = date,
                description = description,
                video = video
            )

            for img in images:   # here i use loop because i am taking multiple images.
                TravelImage.objects.create(post=post, images=img)

            return redirect("blog")
        except:
            return render(request,"blog/post_form.html")
    return render(request,"blog/post_form.html",{"user_profile":user_profile})

# from this view get all the data from post_form and put database and by using html show the data
    # in blog page and  post_detail.

        # travelpost = TravelPost(
        #     title = title,
        #     destination = destination,
        #     date = date,
        #     description = description,
        #     images = images
        # )
#
#         try:
#             travelpost.save()
#             return redirect("blog")
#
#         except:
#              return render(request,"blog/post_form.html")
#     return render(request,"blog/post_form.html")


@login_required()
def Gallery(request):
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    images = TravelImage.objects.select_related('post').order_by('-id')
    return render(request,"blog/gallery.html",{
        'images':images,
        'user_profile':user_profile,
    })

@login_required()
def Video(request):
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    video = TravelPost.objects.only('video').order_by('-id')
    return render(request,"blog/video.html",{
        'video':video,
        'user_profile':user_profile
    })

def Signin(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        username = request.POST.get("username")  # get all data from signin form
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if User.objects.filter(username=username).exists():    # check here or filters
            messages.warning(request,"Username already exists..!")
            return redirect('signin')

        if User.objects.filter(email=email).exists():
            messages.warning(request,"Email already exists..!")
            return redirect('signin')

        if password != password2:
            messages.warning(request,"Password doesn't match..!")
            return redirect('signin')

        user = User(
            username=username,
            email=email,
        )  # use inbuilt User model

        user.set_password(password)
        user.save()

        send_mail(
            subject='Welcome to Travel Blog!',
            message=f'Hello {username},\n\n Thank you for registering on Travel Blog. \n '
                    f'Your account has been successfully created \n\n Thanks and regards..!',

            from_email='shubhampati712@gmail.com',
            recipient_list=[email],
            fail_silently=False,
        )

        return redirect('login')

    return render(request,"blog/signin.html")

def Login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            messages.warning(request,"Invalid username and password ")
            return redirect('login')

    return render(request,"blog/login.html")


def Logout(request):
    logout(request)
    messages.success(request,"You are logout Successfully...!")
    return redirect('login')

@login_required()
def Profile(request):
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    my_posts = TravelPost.objects.filter(user=user).order_by('-id')

    return render(request,"blog/profile.html",{
        'user':user,
        'user_profile':user_profile,
        'my_posts':my_posts,
    })


@login_required()
def Delete_post(request, pk):
    post = get_object_or_404(TravelPost, pk=pk)

    if post.user == request.user:
        post.delete()
        messages.success(request, "Post deleted successfully!")

    return redirect('profile')


@login_required
def Edit_profile(request):
    user = request.user
    # user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    # Ensure the user has a profile
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        profile_pic = request.FILES.get('profile_pic')
        if profile_pic:
            profile.profile_pic = profile_pic
            profile.save()
            messages.success(request, "Profile picture updated!")
        return redirect('profile')

    return render(request, 'blog/edit_profile.html',{'user_profile':user_profile})


@login_required()
def About(request):
    user=request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    return render(request,"blog/about.html",{"user_profile":user_profile})

@login_required()
def Contact(request):
    user=request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == "POST":
        fullname = request.POST.get("fullname")
        email = request.POST.get("email")
        mobile = request.POST.get("mob")
        message = request.POST.get("msg")

        contact = ContactModel(
            fullname = fullname,
            email = email,
            mobile = mobile,
            message =message
        )

        try:
            contact.save()
            send_mail(
                subject='Your message submitted to Travel Blog',
                message=f'Hello {fullname},\n\n Thank you for contact Us. \n '
                        f'Your message is successfully submitted. \n\n Thanks and regards..!',

                from_email='shubhampati712@gmail.com',
                recipient_list=[email],
                fail_silently=False,
            )

            messages.success(request, "Your message is submitted.")
            return render(request,"blog/contact.html",{"user_profile":user_profile})
        except:
            messages.error(request, "Something went wrong.")
            return render(request,"blog/contact.html",{"user_profile": user_profile})

    return render(request,"blog/contact.html",{"user_profile": user_profile})