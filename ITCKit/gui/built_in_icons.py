__author__ = 'Kristo Koert'

try:
    from gi.repository import AppIndicator3 as AppIndicator
except ImportError:
    from gi.repository import AppIndicator


icon_indicator = AppIndicator.Indicator.new("for-retrieving-icons", "user-available",
                                            AppIndicator.IndicatorCategory.APPLICATION_STATUS)

pro_icon = icon_indicator.get_icon()
icon_indicator.set_icon("user-offline")
neu_icon = icon_indicator.get_icon()
icon_indicator.set_icon("user-busy")
cou_icon = icon_indicator.get_icon()