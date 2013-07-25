from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import redirect_to
from django.conf import settings

from . import views, feeds

products = r'/products/(?P<product>\w+)'
versions = r'/versions/(?P<versions>[;\w\.()]+)'
crash_type = r'/crash_type/(?P<crash_type>\w+)'
date_range_type = r'/date_range_type/(?P<date_range_type>\w+)'
# putting a * on the following regex so we allow URLs to be things like
# `.../os_name/` without any default value which the view function will
# take care of anyway
os_name = r'/os_name/(?P<os_name>[\w\s]*)'
perm_legacy_redirect = settings.PERMANENT_LEGACY_REDIRECTS


urlpatterns = patterns(
    '',  # prefix
    url('^favicon\.ico$',
        views.favicon_ico,
        name='crashstats.favicon_ico'),
    url('^robots\.txt$',
        views.robots_txt,
        name='crashstats.robots_txt'),
    url('^home' + products + '$',
        views.home,
        name='crashstats.home'),
    url('^home' + products + versions + '$',
        views.home,
        name='crashstats.home'),
    url(r'^home/frontpage_json$',
        views.frontpage_json,
        name='crashstats.frontpage_json'),
    url(r'^status/$',
        views.status,
        name='crashstats.status'),
    url(r'^status/json/$',
        views.status_json,
        name='crashstats.status_json'),
    url(r'^crontabber-state/$',
        views.crontabber_state,
        name='crashstats.crontabber_state'),
    url(r'^crontabber-state/data.json$',
        views.crontabber_state_json,
        name='crashstats.crontabber_state_json'),
    url(r'^products/$',
        views.products_list,
        name="crashstats.products_list"),
    url('^topcrasher' + products + '$',
        views.topcrasher,
        name='crashstats.topcrasher'),
    url('^topcrasher' + products + versions + '$',
        views.topcrasher,
        name='crashstats.topcrasher'),
    url('^topcrasher' + products + versions + '$',
        views.topcrasher,
        name='crashstats.topcrasher'),
    url('^topcrasher' + products + versions + date_range_type + '$',
        views.topcrasher,
        name='crashstats.topcrasher'),
    url('^topcrasher' + products + versions + date_range_type +
        crash_type + '$',
        views.topcrasher,
        name='crashstats.topcrasher'),
    url('^topcrasher' + products + versions + date_range_type +
        crash_type + os_name + '$',
        views.topcrasher,
        name='crashstats.topcrasher'),
    url('^topcrasher' + products + versions + crash_type + os_name + '$',
        views.topcrasher,
        name='crashstats.topcrasher'),
    url('^topcrasher' + products + versions + crash_type + '$',
        views.topcrasher,
        name='crashstats.topcrasher'),
    url('^topcrasher' + products + versions + os_name + '$',
        views.topcrasher,
        name='crashstats.topcrasher'),
    url('^daily$',
        views.daily,
        name='crashstats.daily'),
    url('^builds' + products + '$',
        views.builds,
        name='crashstats.builds'),
    # note the deliberate omission of the ';' despite calling the regex
    # variable 'versionS'
    url('^builds' + products + '/versions/(?P<versions>[\w\.()]+)' + '$',
        views.builds,
        name='crashstats.builds'),
    url('^builds' + products + '/rss$',
        feeds.BuildsRss(),
        name='crashstats.buildsrss'),
    url('^builds' + products + versions + '/rss$',
        feeds.BuildsRss(),
        name='crashstats.buildsrss'),
    # handle old-style urls
    url('^topchangers' + products + '$',
        views.topchangers,
        name='crashstats.topchangers'),
    url('^topchangers' + products + versions + '$',
        views.topchangers,
        name='crashstats.topchangers'),
    url('^topchangers' + products + versions + '$',
        views.topchangers,
        name='crashstats.topchangers'),
    url(r'^report/list$',
        views.report_list,
        name='crashstats.report_list'),
    url(r'^report/exploitability/$',
        views.exploitable_crashes,
        name='crashstats.exploitable_crashes'),
    url(r'^report/index/(?P<crash_id>.*)$',
        views.report_index,
        name='crashstats.report_index'),
    # make the suffix `_ajax` optional there.
    # we prefer report/pending/XXX but because of legacy we need to
    # support report/pending_ajax/XXX too
    url(r'^report/pending(_ajax)?/(?P<crash_id>.*)$',
        views.report_pending,
        name='crashstats.report_pending'),
    url(r'^query/$',
        views.query,
        name='crashstats.query'),
    url(r'^query/query$',
        redirect_to, {'url': '/query/',
                      'permanent': perm_legacy_redirect,
                      'query_string': True}),
    url(r'^buginfo/bug', views.buginfo,
        name='crashstats.buginfo'),
    url(r'^topcrasher/plot_signature/(?P<product>\w+)/(?P<versions>[;\w\.()]+)'
        r'/(?P<start_date>[0-9]{4}-[0-9]{2}-[0-9]{2})/'
        r'(?P<end_date>[0-9]{4}-[0-9]{2}-[0-9]{2})/(?P<signature>.*)',
        views.plot_signature,
        name='crashstats.plot_signature'),
    url(r'^signature_summary/json_data$',
        views.signature_summary,
        name='crashstats.signature_summary'),
    url(r'^rawdumps/(?P<crash_id>[\w-]{36}).(?P<extension>json|dmp)$',
        views.raw_data,
        name='crashstats.raw_data'),
    url(r'^crash_trends' + products + '$',
        views.crash_trends,
        name='crashstats.crash_trends'),
    url(r'^crash_trends' + products + versions + '$',
        views.crash_trends,
        name='crashstats.crash_trends'),
    url(r'^crash_trends/json_data$',
        views.crashtrends_json,
        name='crashstats.crashtrends_json'),
    url(r'^crash_trends/product_versions$',
        views.crashtrends_versions_json,
        name='crashstats.crashtrends_versions_json'),
    url(r'^correlation/signatures$',
        views.correlations_signatures_json,
        name='crashstats.correlations_signatures_json'),
    url(r'^correlation$',
        views.correlations_json,
        name='crashstats.correlations_json'),
    # if we do a permanent redirect, the browser will "cache" the redirect and
    # it will make it very hard to ever change the DEFAULT_PRODUCT
    url(r'^$',
        redirect_to,
        {'url': '/home/products/%s' % settings.DEFAULT_PRODUCT,
         'permanent': False}),  # this is not a legacy URL

    # handle old-style URLs
    url(r'^products/(?P<product>\w+)/$',
        redirect_to, {'url': '/home/products/%(product)s',
                      'permanent': perm_legacy_redirect}),
    url(r'^products/(?P<product>\w+)/versions/(?P<versions>[;\w\.()]+)/$',
        redirect_to,
        {'url': '/home/products/%(product)s/versions/%(versions)s',
         'permanent': perm_legacy_redirect}),
    url(r'^products/(?P<product>\w+)/versions/(?P<versions>[;\w\.()]+)/'
        r'builds$',
        redirect_to,
        {'url': '/builds/products/%(product)s',
         'permanent': perm_legacy_redirect}),
    url(r'^products/(?P<product>\w+)/versions/(?P<versions>[;\w\.()]+)/'
        r'topchangers$',
        redirect_to,
        {'url': '/topchangers/products/%(product)s',
         'permanent': perm_legacy_redirect}),
    url(r'^topcrasher/byversion/(?P<product>\w+)/(?P<versions>[;\w\.()]+)$',
        redirect_to,
        {'url': '/topcrasher/products/%(product)s/versions/%(versions)s',
         'permanent': perm_legacy_redirect}),
    url(r'^topcrasher' + products + '/versions/$',
        redirect_to,
        {'url': '/topcrasher/products/%(product)s',
         'permanent': perm_legacy_redirect}),

)
