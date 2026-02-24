from django.core.mail import send_mail
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from blog.models import Blog


class BlogCreateView(CreateView):
    model = Blog
    fields = ("title", "content", "preview_image")
    success_url = reverse_lazy("blog:blog_list")


class BlogListView(ListView):
    model = Blog

    def get_queryset(self):
        return Blog.objects.filter(is_published=True)


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()

        if self.object.views_count == 100:
            try:
                subject = f"Поздравляем: Ваша статья '{object.title}' достигла 100 просмотров!"
                message = "Ваше творчество оценили читатели! Продолжайте в том же духе"
                from_email = "admin@examplr.com"
                recipient_list = ["recipient@example.com"]

                send_mail(subject, message, from_email, recipient_list)
            except Exception as e:
                print(f"Ошибка отправки email: {e}")
        return self.object


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ("title", "content", "preview_image")
    success_url = reverse_lazy("blog:blog_list")

    def get_success_url(self):
        return reverse("blog:blog_detail", args=[self.kwargs.get("pk")])


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy("blog:blog_list")
