# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

import pytermor as pt


class Styles(pt.Styles):
    TEXT_DISABLED = pt.Style(fg=pt.cv.GRAY_23)
    TEXT_LABEL = pt.Style(fg=pt.cv.GRAY_35)
    TEXT_DEFAULT = pt.Style(fg=pt.cv.GRAY_62)

    STATUSBAR_BG = pt.NOOP_COLOR

    VALUE_LBL_5 = TEXT_LABEL
    VALUE_UNIT_4 = TEXT_LABEL
    VALUE_FRAC_3 = pt.Style(fg=pt.cv.GRAY_50)
    VALUE_PRIM_2 = TEXT_DEFAULT
    VALUE_PRIM_1 = pt.Style(fg=pt.cv.GRAY_70, bold=True)

    TEXT_ACCENT = pt.Style(fg=pt.cv.GRAY_85)
    TEXT_SUBTITLE = pt.Style(fg=pt.cv.GRAY_93, bold=True)
    TEXT_TITLE = pt.Style(fg=pt.cv.HI_WHITE, bold=True, underlined=True)
    TEXT_UPDATED = pt.Style(fg=pt.cv.HI_GREEN, bold=True)

    BORDER_DEFAULT = pt.Style(fg=pt.cv.GRAY_30)
    FILL_DEFAULT = pt.Style(fg=pt.cv.GRAY_46)

    STDERR_DEBUG = pt.Style(fg=pt.resolve_color('medium purple 7'))
    STDERR_TRACE = pt.Style(fg=pt.resolve_color('pale turquoise 4'))

    #PBAR_BG = pt.Style(bg=pt.cv.GRAY_3)
    PBAR_DEFAULT = pt.Style(TEXT_DEFAULT, bg=pt.cv.GRAY_19)
    PBAR_ALERT_1 = pt.Style(fg=pt.cv.GRAY_7, bg=pt.resolve_color('orange 3'))
    PBAR_ALERT_2 = pt.Style(PBAR_ALERT_1, bg=pt.resolve_color('dark goldenrod'))
    PBAR_ALERT_3 = pt.Style(PBAR_ALERT_1, bg=pt.resolve_color('orange 2'))
    PBAR_ALERT_4 = pt.Style(PBAR_ALERT_1, bg=pt.resolve_color('dark orange'))
    PBAR_ALERT_5 = pt.Style(PBAR_ALERT_1, bg=pt.resolve_color('orange-red 1'))
    PBAR_ALERT_6 = pt.Style(PBAR_ALERT_1, bg=pt.resolve_color('red 3'))
    PBAR_ALERT_7 = pt.Styles.CRITICAL_ACCENT

    DEBUG = pt.Style(fg=0x8163a2, bg=0x444, underlined=True, overlined=True, blink=False)
    DEBUG_SEP_INT = pt.Style(fg=0x7280e2)
    DEBUG_SEP_EXT = pt.Style(fg=0x7e59a9)
