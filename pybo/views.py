from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import HttpResponseNotAllowed
from django.core.paginator import Paginator
from .models import Question
from .forms import QuestionForm, AnswerForm

#from django.http import HttpResponse
# Create your views here.
def index(request):
    page = request.GET.get('page','1') #페이지
    question_list = Question.objects.order_by('-create_date')
    paginator = Paginator(question_list,10) # 한 페이지에 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj}
    return render(request, 'pybo/question_list.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question':question}
    return render(request,'pybo/question_detail.html',context)

def answer_create(request, question_id):
    '''
    pybo 답변 등록
    '''
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail',question_id=question.id)
    else:
        return HttpResponseNotAllowed('Only POST is possible.')
    context = {'question':question, 'form':form}
    return render(request,'pybo/question_detail.html',context)

def question_create(request):
    if(request.method == 'POST'): # POST방식으로 전달
        form = QuestionForm(request.POST) # 유효하지 않은 데이터가 들어오면 오류 메세지가 저장됨
        if(form.is_valid()):    # 입력된 Form이 유효한 경우
            question = form.save(commit=False) #question 객체에 임시저장
            question.create_date = timezone.now() # 시간을 설정하고
            question.save() # 저장
            return redirect('pybo:index')
    else:   #GET방식으로 전달
        form = QuestionForm()
    context = {'form':form}
    return render(request, 'pybo/question_form.html', context)
