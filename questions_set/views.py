from flask import render_template, session, redirect
from flask.views import MethodView
import cx_Oracle
from db import *
from options import *
from question import *
from .forms import *
from common import *
__all__ = ('QuestionSetView', 'QuestionSetInstanceView', 'QuestionSetUpdateView', 'QuestionSetDeleteView')


class QuestionSetView(MethodView):

    @login_required
    def get(self):
        try:
            connection = cx_Oracle.connect(conection_str, mode=cx_Oracle.SYSDBA)
            cursor = connection.cursor()
            print(session['user_pk'])
            # cursor.execute(f'select qs.pk, qs.text from customer cu join question_set '
            #                f'qs on cu.pk=qs.customer_pk where cu.deleted=0 and qs.deleted=0 and cu.pk={session["user_pk"]}')
            cursor.execute(f'select * from table(question_pack.get_question_set_list({session["user_pk"]}))')
            question_set_list = cursor.fetchall()
            cursor.close()
            connection.close()
            context = {
                'form': QuestionSetForm(),
                'question_set_list': question_set_list,
                       }
            return render_template('questions_set_list.html', **context)
        except:
            return redirect('/')

    @login_required
    def post(self):
        try:
            form = QuestionSetForm()
            connection = cx_Oracle.connect(conection_str, mode=cx_Oracle.SYSDBA)
            cursor = connection.cursor()
            cursor.callproc('question_pack.add_question_set',
                            [form.text.data,
                             session['user_pk']
                             ]
                            )
            connection.commit()
            cursor.close()
            connection.close()
            return redirect('/question_sets/')
        except:
            return redirect('/')

class QuestionSetInstanceView(MethodView):
    @login_required
    def get(self, pk):
        try:
            connection = cx_Oracle.connect(conection_str, mode=cx_Oracle.SYSDBA)
            cursor = connection.cursor()
            # cursor.execute(f'select qs.pk, qs.text from customer cu join question_set '
            #                f'qs on cu.pk=qs.customer_pk where cu.deleted=0 and qs.deleted=0 and cu.pk={session["user_pk"]}')
            cursor.execute(f'select * from table(question_pack.get_question_set({session["user_pk"]}, {pk}))')
            questions = []
            for i in  cursor.fetchall():
                i2 = i[2].split('|||') if i[2] else i[2]
                i3 = i[3].split('|||') if i[3] else i[3]
                if i2 and i3:
                    questions.append((i[0], i[1], zip(i2, i3)))
                else:
                    questions.append((i[0], i[1], None))
            cursor.close()
            connection.close()
            op_form = OptionForm()
            qu_form = QuestionForm()
            context = {'question_set': questions, 'op_form': op_form, 'qu_form': qu_form, 'pk': pk}
            return render_template('question_set.html', **context)
        except:
            return redirect('/')

    @login_required
    def post(self, pk):
        form = QuestionForm()
        try:
            if form.validate_on_submit():
                connection = cx_Oracle.connect(conection_str, mode=cx_Oracle.SYSDBA)
                cursor = connection.cursor()
                cursor.callproc('question_pack.add_question',
                                [form.text.data,
                                 pk
                                 ])
                connection.commit()
                cursor.close()
                connection.close()
            return redirect(f'/question_set/{pk}')
        except:
            return redirect('/')


class QuestionSetUpdateView(MethodView):
    @login_required
    def get(self, pk):
        form = QuestionSetForm()
        try:
            connection = cx_Oracle.connect(conection_str, mode=cx_Oracle.SYSDBA)
            cursor = connection.cursor()
            cursor.execute(f'select pk, text from question_set where pk={pk} and deleted=0')
            qs = cursor.fetchone()
            cursor.close()
            connection.close()
            return render_template('question_set_update.html', qs=qs, form=form)
        except:
            return redirect('/')

    @login_required
    def post(self, pk):
        try:
            form = QuestionSetForm()
            if form.validate_on_submit():
                connection = cx_Oracle.connect(conection_str, mode=cx_Oracle.SYSDBA)
                cursor = connection.cursor()
                cursor.execute(f"update question_set set text='{form.text.data}' where pk={pk} and deleted=0")
                connection.commit()
                cursor.close()
                connection.close()
                return redirect(f'/question_sets/')
            connection = cx_Oracle.connect(conection_str, mode=cx_Oracle.SYSDBA)
            cursor = connection.cursor()
            cursor.execute(f'select pk, text from question_set where pk={pk} and deleted=0')
            qs = cursor.fetchone()
            cursor.close()
            connection.close()
            return render_template('question_set_update.html', qs=qs, form=form)
        except:
            return redirect('/')

class QuestionSetDeleteView(MethodView):
    @login_required
    def get(self, pk):
        try:
            connection = cx_Oracle.connect(conection_str, mode=cx_Oracle.SYSDBA)
            cursor = connection.cursor()
            cursor.execute(f"update question_set set deleted=1 where pk={pk} and deleted=0")
            connection.commit()
            cursor.close()
            connection.close()
            return redirect(f'/question_sets/')
        except:
            return redirect('/')