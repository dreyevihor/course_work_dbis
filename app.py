from flask import Flask, session, render_template
from config import Config

from auth.views import *
from questions_set import *
from options import *
from question import *
from pdf import *

app = Flask(__name__)
app.config.from_object(Config)
app.add_url_rule('/registration/', view_func=RegistrationView.as_view('registration'))
app.add_url_rule('/login/', view_func=LoginView.as_view('login'))
app.add_url_rule('/logout/', view_func=LogoutView.as_view('logout'))

app.add_url_rule('/question_sets/', view_func=QuestionSetView.as_view('question_sets'))
app.add_url_rule('/question_set/<int:pk>/', view_func=QuestionSetInstanceView.as_view('question_set_instance'))
app.add_url_rule('/question_set/update/<int:pk>/', view_func=QuestionSetUpdateView.as_view('question_set_update'))
app.add_url_rule('/question_set/delete/<int:pk>/', view_func=QuestionSetDeleteView.as_view('question_set_delete'))

app.add_url_rule('/question_set/pdf/<int:pk>/', view_func=PdfView.as_view('pdf'))

app.add_url_rule('/option/add/<int:pk>/', view_func=OptionAddView.as_view('option_add'))
app.add_url_rule('/option/update/<int:pk>/', view_func=OptionUpdateView.as_view('option_update'))
app.add_url_rule('/option/delete/<int:pk>/', view_func=OptionDeleteView.as_view('option_delete'))

app.add_url_rule('/question/delete/<int:pk>/', view_func=QuestionDeleteView.as_view('question_delete'))
app.add_url_rule('/question/update/<int:pk>/', view_func=QuestionUpdateView.as_view('question_update'))




@app.route('/')
def hello_world():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
