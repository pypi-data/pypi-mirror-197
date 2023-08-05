from cms.models import CMSPlugin
from django.db import models
from django.utils.translation import ugettext_lazy as _


class HtmlSitemapPluginConf(CMSPlugin):
    min_depth = models.PositiveIntegerField(verbose_name=_("Minimum depth"), default=0)
    max_depth = models.PositiveIntegerField(
        verbose_name=_("Maximum depth"), blank=True, null=True
    )
    in_navigation = models.NullBooleanField(
        verbose_name=_("In navigation"), default=None
    )

    class Meta:
        verbose_name = _("HTML Sitemap plugin configuration")
        verbose_name_plural = _("HTML Sitemap plugin configurations")

    def __str__(self):
        return "Django-CMS HTML Sitemap #{}".format(self.pk)
