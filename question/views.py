from flask.views import MethodView
from flask import render_template, redirect, session
from auth import *
import cx_Oracle
from db import *
from .forms import *
from common import *

__all__ =('QuestionUpdateView', 'QuestionDeleteView')


class QuestionAddView(MethodView):
    def get(self):
        pass
    def post(self):
        pass


class QuestionDeleteView(MethodView):

    @login_required
    def get(self, pk):
        try:
            connection = cx_Oracle.connect(conection_str, mode=cx_Oracle.SYSDBA)
            cursor = connection.cursor()
            cursor.execute(f"update question set deleted=1 where pk={pk} and deleted=0")
            connection.commit()
            cursor.close()
            connection.close()
            return redirect(f'/question_sets/')
        except:
            return redirect('/')

class QuestionUpdateView(MethodView):

    @login_required
    def get(self, pk):
        try:
            form = QuestionForm()
            connection = cx_Oracle.connect(conection_str, mode=cx_Oracle.SYSDBA)
            cursor = connection.cursor()
            cursor.execute(f'select pk, text from question where pk={pk} and deleted=0')
            opt = cursor.fetchone()
            cursor.close()
            connection.close()
            return render_template('question_update.html', opt=opt, form=form)
        except:
            return redirect('/')

    @login_required
    def post(self, pk):
        form = QuestionForm()
        if form.validate_on_submit():
            try:
                connection = cx_Oracle.connect(conection_str, mode=cx_Oracle.SYSDBA)
                cursor = connection.cursor()
                cursor.execute(f"update question set text='{form.text.data}' where pk={pk} and deleted=0")
                connection.commit()
                cursor.close()
                connection.close()
                return redirect(f'/question_sets/')
            except:
                return redirect('/')
        try:
            connection = cx_Oracle.connect(conection_str, mode=cx_Oracle.SYSDBA)
            cursor = connection.cursor()
            cursor.execute(f'select pk, text from question where pk={pk} and deleted=0')
            opt = cursor.fetchone()
            cursor.close()
            connection.close()
            return render_template('question_update.html', opt=opt, form=form)
        except:
            return redirect('/')

