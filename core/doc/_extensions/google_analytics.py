# -*- coding: utf-8 -*-

from sphinx.errors import ExtensionError

GOOGLE_ANALYTICS_META_TAG = """
<script type="text/javascript">
  var _gaq = _gaq || [];
  _gaq.push(['_setAccount', '%s']);
  _gaq.push(['_trackPageview']);
  (function() {
    var ga = document.createElement('script');
    ga.type = 'text/javascript';
    ga.async = true;
    if ('https:' == document.location.protocol) {
      ga.src = 'https://ssl.google-analytics.com/ga.js'
    } else {
      ga.src = 'http://www.google-analytics.com/ga.js'
    }
    var s = document.getElementsByTagName('script')[0];
    s.parentNode.insertBefore(ga, s);
  })();
</script>
"""


def setup(app):
    app.add_config_value("google_analytics_id", "", "html")
    app.add_config_value("google_analytics_enabled", True, "html")
    app.connect("html-page-context", add_ga_javascript)
    app.connect("builder-inited", check_config)
    return {"version": "0.1"}


def check_config(app):
    if not app.config.google_analytics_id:
        raise ExtensionError("`google_analytics_id` config value must be set for ga statistics to function properly.")  # noqa


def add_ga_javascript(app, page_name, template_name, context, doc_tree):
    if not app.config.google_analytics_enabled:
        return

    meta_tags = context.get("metatags", "")
    meta_tags += GOOGLE_ANALYTICS_META_TAG % app.config.google_analytics_id
    context["metatags"] = meta_tags
