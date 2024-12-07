from llm import call_llm
from typing import List
from pydantic import BaseModel
import json

class Spam(BaseModel):
    explanation: str
    severity: str
    snippets: List[str]

class Spams(BaseModel):
    spams: List[Spam]

def spams_agent(code_changes):
    prompt = f"""
Analyze the provided code changes to a github repository in form of git diffs with some context for unnecessary and spammy changes.
Your job is to recognise useless changes added just to boost line changes or commits and to confuse maintainers.

Certain examples include:
- only changing minor sections of README.md
- fixing spelling mistakes
- unnecessary code refactoring
- creating a artificial bug and then fixing it

For each detected spam, include:
- Explanation of why it is a unnecessary change or a spam change.
- Severity Level (Low, Medium, High) based on the impact on maintainability and extensibility.
- Code Snippets to back your answwers

The code snippets are as follows:
{code_changes}

Give the output in form of json dump following the provided pydantic models
class Spam(BaseModel):
    explanation: str
    severity: str | "High", "Medium", "Low"
    snippets: List[str]

class Spams(BaseModel):
    spams: List[Spam]

Do not provide any output other than json dump.
"""
    response = call_llm(prompt)
    try:
        fin = Spams(**json.loads(response[7:-3]))
        return fin
    except:
        print(f"Failed in Code Smells Agent")
        return Spams(spams=[])

if __name__ == "__main__":
    change = "@@ -2,8 +2,8 @@\n from . import views\n \n urlpatterns = [\n-    path('', views.post_list, name='post_list'),\n-    path('post/<int:pk>/', views.post_detail, name='post_detail'),\n-    path('post/new/', views.post_new , name='post_new'),\n-    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),\n+    path('', views.post_list, name='post_article_list'),\n+    path('post/<int:pk>/', views.post_detail, name='post_article_detail'),\n+    path('post/new/', views.post_new , name='post_new_article'),\n+    path('post/<int:pk>/edit/', views.post_edit, name='update_article'),\n ]\n\\ No newline at end of file"
    change2 = "@@ -5,15 +5,18 @@\n from .forms import PostForm\n from django.shortcuts import redirect\n \n-def post_list(request):\n-    posts =Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')\n-    return render(request, 'blog/post_list.html', {'posts':posts})\n+def post_article_list(request):\n+    '''Provides a list of articles published.'''\n+    postings =Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')\n+    return render(request, 'blog/post_list.html', {'posts':postings})\n \n-def post_detail(request, pk):\n-    post = get_object_or_404(Post, pk=pk)\n-    return render(request, 'blog/post_detail.html', {'post': post})\n+def post_article_detail(request, pk):\n+    '''Displays article details.'''\n+    post_on_click = get_object_or_404(Post, pk=pk)\n+    return render(request, 'blog/post_detail.html', {'post': post_on_click})\n \n-def post_new(request):\n+def post_new_article(request):\n+    '''Posts new article.'''\n     if request.method == \"POST\":\n         form=PostForm(request.POST)\n         if form.is_valid():\n@@ -26,16 +29,17 @@ def post_new(request):\n         form=PostForm()\n     return render(request, 'blog/post_edit.html', {'form': form})\n \n-def post_edit(request, pk):\n-    post = get_object_or_404(Post, pk=pk)\n-    if request.method == \"POST\":\n-        form = PostForm(request.POST, instance=post)\n-        if form.is_valid():\n-            post = form.save(commit=False)\n-            post.author = request.user\n-            post.published_date = timezone.now()\n-            post.save()\n-            return redirect('post_detail', pk=post.pk)\n-    else:\n-        form = PostForm(instance=post)\n-    return render(request, 'blog/post_edit.html', {'form': form})\n+def update_article(request, article_id):\n+  \"\"\"Edits an existing article.\"\"\"\n+  article = get_object_or_404(Post, pk=article_id)\n+  if request.method == \"POST\":\n+    edit_form = PostForm(request.POST, instance=article)\n+    if edit_form.is_valid():\n+      edited_article = edit_form.save(commit=False)\n+      edited_article.author = request.user\n+      edited_article.published_date = timezone.now()\n+      edited_article.save()\n+      return redirect('post_detail', pk=edited_article.pk)\n+  else:\n+    edit_form = PostForm(instance=article)\n+  return render(request, 'blog/post_edit.html', {'edit_form': edit_form})"

    response = spams_agent([change2, change])
    print(response)