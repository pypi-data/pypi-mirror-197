import lxml
from lxml import etree
from PIL import Image, ImageTk
from . import Widget

class WT_ICON_LIST(Widget):
    """
        Icon list for displaying pictures of levels
    """
    def __init__(this, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
