from django.db import models
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight
from django.contrib.auth.models import User

LANGUAGE_CHOICES = [
    ("py", "python"),
    ("js", "javascript"),
    ("C", "cprogramming"),
    ("C++", "c++"),
]
STYLE_CHOICES = [("friendly", "friendly"), ("native", "native")]


class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name="Created time")
    title = models.CharField(max_length=100, blank=True, default="")
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(
        choices=LANGUAGE_CHOICES, default="python", max_length=100
    )
    style = models.CharField(choices=STYLE_CHOICES, default="friendly", max_length=100)
    owner = models.ForeignKey(
        "auth.User", related_name="snippets", on_delete=models.CASCADE
    )
    highlighted = models.TextField()

    class Meta:
        ordering = ["-created"]
        verbose_name = "Snippet"

    def save(self, *args, **kwargs):
        """
        Use the `pygments` library to create a highlighted HTML
        representation of the code snippet.
        """
        lexer = get_lexer_by_name(self.language)
        linenos = "table" if self.linenos else False
        options = {"title": self.title} if self.title else {}
        formatter = HtmlFormatter(
            style=self.style, linenos=linenos, full=True, **options
        )
        self.highlighted = highlight(self.code, lexer, formatter)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Project(models.Model):
    title = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True, upload_to="works/")
    snippets = models.ManyToManyField(Snippet, blank=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title
