from flask.views import MethodView
from flask import render_template, redirect, session
from auth import *
import cx_Oracle
from db import *
from .forms import *
from common import *
__all__ =('OptionAddView', 'OptionUpdateView', 'OptionDeleteView')


class OptionDeleteView(MethodView):
    @login_required
    def get(self, pk):
        try:
            connection = cx_Oracle.connect(conection_str, mode=cx_Oracle.SYSDBA)
            cursor = connection.cursor()
            cursor.execute(f"update options set deleted=1 where pk={pk} and deleted=0")
            connection.commit()
            cursor.close()
            connection.close()
            return redirect(f'/question_sets/')
        except:
            return redirect('/')


class OptionAddView(MethodView):
    @login_required
    def post(self, pk):
        form = OptionForm()
        if form.validate_on_submit():
            try:
                connection = cx_Oracle.connect(conection_str, mode=cx_Oracle.SYSDBA)
                cursor = connection.cursor()
                cursor.callproc('question_pack.add_option',
                                [form.text.data,
                                 form.question_pk.data
                                 ])
                connection.commit()
                cursor.close()
                connection.close()
            except:
                return redirect('/')
        return redirect(f'/question_set/{pk}/')


class OptionUpdateView(MethodView):
    @login_required
    def get(self, pk):
        try:
            form = OptionForm()
            connection = cx_Oracle.connect(conection_str, mode=cx_Oracle.SYSDBA)
            cursor = connection.cursor()
            cursor.execute(f'select pk, text from options where pk={pk} and deleted=0')
            opt = cursor.fetchone()
            cursor.close()
            connection.close()
            return render_template('option_update.html', opt=opt, form=form)
        except:
            return redirect('/')

    @login_required
    def post(self, pk):
        form = OptionForm()
        if form.validate_on_submit():
            try:
                connection = cx_Oracle.connect(conection_str, mode=cx_Oracle.SYSDBA)
                cursor = connection.cursor()
                cursor.execute(f"update options set text='{form.text.data}' where pk={pk} and deleted=0")
                connection.commit()
                cursor.close()
                connection.close()
                return redirect(f'/question_sets/')
            except:
                return redirect('/')
        connection = cx_Oracle.connect(conection_str, mode=cx_Oracle.SYSDBA)
        cursor = connection.cursor()
        cursor.execute(f'select pk, text from options where pk={pk} and deleted=0')
        opt = cursor.fetchone()
        cursor.close()
        connection.close()
        return render_template('option_update.html', opt=opt, form=form)
