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


        object = partner_obj.browse([int(x) for x in docids.split(',')])
        #object = [x for x in object if x.sponsored_child]
        if len(object)>0:
            response = ReportController().report_download(data, token)
            try:
                filename = object[0].report_filename
            except:
                filename = 'report'

            response.headers.set('Content-Disposition', 'attachment; filename=%s.pdf;' % filename)
            return response
        else:
            # TODO issue a 302 to somewhere
            raise Warning('Illegal selection', 'One or more sponsored children must be selected.')