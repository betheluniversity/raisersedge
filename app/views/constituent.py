from flask import jsonify
from flask.ext.classy import FlaskView, route

from app.controller import RaisersEdgeSyncController


class ConstituentView(FlaskView):

    def __init__(self):
        self.controller = RaisersEdgeSyncController(route_prefix='constituent/v1/constituents')

    def before_request(self, name, **args):
        self.controller.refresh_token()

    def constituent(self, constituent_id):
        data = self.controller.call_api('/%s' % constituent_id)
        return jsonify(data)

    @route('/search/<query>')
    def constituent_search(self, query):
        data = self.controller.call_api('/search?search_text=%s' % query)
        return jsonify(data)

    @route('/get/bethelid/<bethelid>')
    def get_constituent_by_bethel_id(self, bethelid):
        data = self.controller.call_api('/search?search_text=%s&limit=1' % bethelid)
        data = data[0]  # bethel IDs are unique
        if int(data.get('count')) != 1:
            return "search for %s did not return exactly one record" % bethelid
        re_id = int(data.get('value')[0].get('id'))
        return self.constituent(re_id)

    @route('/list/')
    @route('/list/<int:days>')
    def constituent_list(self, days=0):
        import datetime
        date = datetime.datetime.now() + datetime.timedelta(-days)
        if days is 0:
            data = self.controller.call_api('/')
        else:
            data = self.controller.call_api('?last_modified=%s' % date.isoformat())

        return jsonify(data)