from agents.quality.spams import Spams, Spam
from models.models import *

# obj = Spams(spams=[Spam(explanation='The changes involve renaming functions and variables without any functional enhancement or bug fix. Such changes can confuse maintainers and do not contribute to any real improvement in code quality or functionality.', severity='Medium', snippets=['-def post_list(request):', '+def post_article_list(request):', "-    posts =Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')", "+    postings =Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')", '-def post_detail(request, pk):', '+def post_article_detail(request, pk):', '-    post = get_object_or_404(Post, pk=pk)', '+    post_on_click = get_object_or_404(Post, pk=pk)', '-def post_new(request):', '+def post_new_article(request):', '-def post_edit(request, pk):', '+def update_article(request, article_id):']), Spam(explanation='The renaming of URL pattern names and function references in the urlpatterns also constitutes unnecessary changes. These alterations do not improve the functionality but potentially disrupt existing references and documentation.', severity='Medium', snippets=["-    path('', views.post_list, name='post_list'),", "+    path('', views.post_article_list, name='post_article_list'),", "-    path('post/<int:pk>/', views.post_detail, name='post_detail'),", "+    path('post/<int:pk>/', views.post_article_detail, name='post_article_detail'),", "-    path('post/new/', views.post_new , name='post_new'),", "+    path('post/new/', views.post_new_article , name='post_new_article'),", "-    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),", "+    path('post/<int:pk>/edit/', views.post_edit, name='update_article')"])])

# print(obj.model_dump_json())

pr_data = PRModel(
    url="https://github.com/DoubtifyOrg/Doubtify/pull/2",
    title="chore: adds comments in frontend",
    contributor="tanishadixit0206",
    discussions=[],
    changes=[
        Patch(
            filename="frontend/react-demo/src/Pages/HomePage.jsx",
            raw_url="https://github.com/DoubtifyOrg/Doubtify/raw/5af0ec5206e8606b2758a22b9ba30f2be27e8ab5/frontend%2Freact-demo%2Fsrc%2FPages%2FHomePage.jsx",
            patch="@@ -58,7 +58,7 @@\n const [isClicked2,setIsClicked2] = useState(false)\n \n \n-\n+//fetching doubts from backend\n const getDoubts = async ()=>{\n const response  =  await axios.get(\"http://localhost:5000/home\",{headers:{\n 'Authorization':`Bearer ${user}`"
        ),
        Patch(
            filename="frontend/react-demo/src/components/AddSolutionDiv.jsx",
            raw_url="https://github.com/DoubtifyOrg/Doubtify/raw/5af0ec5206e8606b2758a22b9ba30f2be27e8ab5/frontend%2Freact-demo%2Fsrc%2Fcomponents%2FAddSolutionDiv.jsx",
            patch="@@ -18,6 +18,7 @@ function AddSolutionDiv(props) {\n \n const { user } = useAuthContext()\n \n+//Converting file to base64\n function convertToBase64(file) {\n return new Promise((resolve, reject) => {\n const fileReader = new FileReader()\n@@ -31,25 +32,26 @@ function AddSolutionDiv(props) {\n })\n \n }\n-\n+//handling image file 1\n async function handlePicInsert1(e) {\n const file = e.target.files[0]\n const base64 = await convertToBase64(file)\n seTb64(base64)\n setPostImage1({ ...postImage1, myFile1: base64 })\n setPic1(true)\n }\n-\n+//handling image file 2\n async function handlePicInsert2(e) {\n const file = e.target.files[0]\n const base64 = await convertToBase64(file)\n seTb642(base64)\n setPostImage2({ ...postImage2, myFile2: base64 })\n setPic2(true)\n }\n-\n+//Uploading doubt to backend\n async function handleSubmit() {\n var dup = false;\n+ //Checking if duplicate doubt exists\n try {\n const response1 = await axios.get(\"http://localhost:5000/home\", {\n headers: {"
        ),
        Patch(
            filename="frontend/react-demo/src/components/LoginForm.jsx",
            raw_url="https://github.com/DoubtifyOrg/Doubtify/raw/5af0ec5206e8606b2758a22b9ba30f2be27e8ab5/frontend%2Freact-demo%2Fsrc%2Fcomponents%2FLoginForm.jsx",
            patch="@@ -18,6 +18,7 @@ function LoginForm() {\n \n const [error,setError] = useState(\"\")\n \n+//Sending login details to backend\n async function handleSubmit(event) {\n event.preventDefault(); "
        ),
        Patch(
            filename="frontend/react-demo/src/components/RegisterForm.jsx",
            raw_url="https://github.com/DoubtifyOrg/Doubtify/raw/5af0ec5206e8606b2758a22b9ba30f2be27e8ab5/frontend%2Freact-demo%2Fsrc%2Fcomponents%2FRegisterForm.jsx",
            patch="@@ -16,6 +16,7 @@ function RegisterForm() {\n \n const [error, setError] = useState(null); // To store error messages\n \n+//Sending registration details to backend\n async function handleSubmit(event) {\n event.preventDefault();\n console.log(user) // Prevent default form submission"
        ),
    ]
)

from agents.quality.quality_eval import quality_eval

# score = quality_eval(pr_data)
# print(score)

from llm import call_llm

response = call_llm(f"""
From the following text find out final score, only output a single integer:

To evaluate the PR, we start with a perfect score of 1000 and deduct points based on the severity of the code smells and spam indicators identified in the description. Here's the calculation:

1. **Duplicated Code**:
   - Severity: Medium
   - Deduction: Medium severity issues might reasonably deduct around 100 points each.

2. **Comments**:
   - Severity: Low
   - Deduction: Low severity issues might deduct around 25 points each.

3. **Bad Words**:
   - Severity: Medium
   - Deduction: Similar to other medium severity, deduct around 100 points.

4. **Spam Comments**:
   - Severity: Low (though numerous spam comments)
   - Deduction: Given their number and low severity, consider a deduction of about 50 points for the aggregate spam impact.

Calculating the total deduction:
- Duplicated Code: 100 points
- Comments: 25 points
- Bad Words: 100 points
- Spam Comments: 50 points

Total deduction = 100 + 25 + 100 + 50 = 275 points

Final Score = 1000 - 275 = 725
""")

print(response)