from tempfile import NamedTemporaryFile
from flask.views import MethodView
from flask import render_template, redirect, session, send_file
from auth import *
import cx_Oracle
import pdfkit
from db import *
from common import *

__all__ = ('PdfView', )


class PdfView(MethodView):
    @login_required
    def get(self, pk):
        try:
            connection = cx_Oracle.connect(conection_str, mode=cx_Oracle.SYSDBA)
            cursor = connection.cursor()
            # cursor.execute(f'select qs.pk, qs.text from customer cu join question_set '
            #                f'qs on cu.pk=qs.customer_pk where cu.deleted=0 and qs.deleted=0 and cu.pk={session["user_pk"]}')
            cursor.execute(f'select * from table(question_pack.get_question_set({session["user_pk"]}, {pk}))')
            questions = []
            for i in cursor.fetchall():
                i2 = i[2].split('|||') if i[2] else i[2]
                i3 = i[3].split('|||') if i[3] else i[3]
                if i2 and i3:
                    questions.append((i[0], i[1], zip(i2, i3)))
                else:
                    questions.append((i[0], i[1], None))
            cursor.execute(f'select text from question_set where pk={pk}')
            set_title = cursor.fetchone()
            cursor.close()
            connection.close()

            context = {'question_set': questions, 'set_title': set_title}
            html = render_template('pdf.html', **context)
            tmp = NamedTemporaryFile()
            pdfkit.from_string(html, tmp.name)
            # pdfkit.from_string(html, 'ggeew.pdf')
            tmp.seek(0)
            resp = send_file(tmp, as_attachment=True, mimetype='application/pdf', attachment_filename='test_task.pdf', add_etags=False)

            return resp
        except:
            return redirect('/')