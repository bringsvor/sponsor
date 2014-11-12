from openerp.addons.web.http import Controller, route, request
from openerp.addons.web.controllers.main import _serialize_exception
from openerp.osv import osv
from openerp.addons.report.controllers.main import ReportController
from openerp import http
import simplejson

class SponsorReportController(ReportController):

    @route(['/report/download'], type='http', auth="user")
    def report_download(self, data, token):
        partner_obj = http.request.env['res.partner']
        requestcontent = simplejson.loads(data)
        url, type = requestcontent[0], requestcontent[1]
        assert type == 'qweb-pdf'
        reportname = url.split('/report/pdf/')[1].split('?')[0]

        reportname, docids = reportname.split('/')
        assert docids
        object = partner_obj.browse(int(docids))
        response = ReportController().report_download(data, token)
        filename = object.report_filename

        response.headers.set('Content-Disposition', 'attachment; filename=%s.pdf;' % filename)
        return response
