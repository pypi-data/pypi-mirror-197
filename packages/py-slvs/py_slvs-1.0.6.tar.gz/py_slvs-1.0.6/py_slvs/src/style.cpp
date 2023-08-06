//-----------------------------------------------------------------------------
// Implementation of a cosmetic line style, which determines the color and
// other appearance of a line or curve on-screen and in exported files. Some
// styles are predefined, and others can be created by the user.
//
// Copyright 2008-2013 Jonathan Westhues.
//-----------------------------------------------------------------------------
#include "solvespace.h"
#include <png.h>

#define DEFAULT_TEXT_HEIGHT 11.5

const Style::Default Style::Defaults[] = {
    { { ACTIVE_GRP },   "ActiveGrp",    RGBf(1.0, 1.0, 1.0), 1.5, 4 },
    { { CONSTRUCTION }, "Construction", RGBf(0.1, 0.7, 0.1), 1.5, 0 },
    { { INACTIVE_GRP }, "InactiveGrp",  RGBf(0.5, 0.3, 0.0), 1.5, 3 },
    { { DATUM },        "Datum",        RGBf(0.0, 0.8, 0.0), 1.5, 0 },
    { { SOLID_EDGE },   "SolidEdge",    RGBf(0.8, 0.8, 0.8), 1.0, 2 },
    { { CONSTRAINT },   "Constraint",   RGBf(1.0, 0.1, 1.0), 1.0, 0 },
    { { SELECTED },     "Selected",     RGBf(1.0, 0.0, 0.0), 1.5, 0 },
    { { HOVERED },      "Hovered",      RGBf(1.0, 1.0, 0.0), 1.5, 0 },
    { { CONTOUR_FILL }, "ContourFill",  RGBf(0.0, 0.1, 0.1), 1.0, 0 },
    { { NORMALS },      "Normals",      RGBf(0.0, 0.4, 0.4), 1.0, 0 },
    { { ANALYZE },      "Analyze",      RGBf(0.0, 1.0, 1.0), 1.0, 0 },
    { { DRAW_ERROR },   "DrawError",    RGBf(1.0, 0.0, 0.0), 8.0, 0 },
    { { DIM_SOLID },    "DimSolid",     RGBf(0.1, 0.1, 0.1), 1.0, 0 },
    { { HIDDEN_EDGE },  "HiddenEdge",   RGBf(0.8, 0.8, 0.8), 2.0, 1 },
    { { OUTLINE },      "Outline",      RGBf(0.8, 0.8, 0.8), 3.0, 5 },
    { { 0 },            NULL,           RGBf(0.0, 0.0, 0.0), 0.0, 0 }
};

std::string Style::CnfColor(const std::string &prefix) {
    return "Style_" + prefix + "_Color";
}
std::string Style::CnfWidth(const std::string &prefix) {
    return "Style_" + prefix + "_Width";
}
std::string Style::CnfTextHeight(const std::string &prefix) {
    return "Style_" + prefix + "_TextHeight";
}

std::string Style::CnfPrefixToName(const std::string &prefix) {
    std::string name = "#def-";

    for(size_t i = 0; i < prefix.length(); i++) {
        if(isupper(prefix[i]) && i != 0)
            name += '-';
        name += tolower(prefix[i]);
    }

    return name;
}

void Style::CreateAllDefaultStyles(void) {
    const Default *d;
    for(d = &(Defaults[0]); d->h.v; d++) {
        (void)Get(d->h);
    }
}

void Style::CreateDefaultStyle(hStyle h) {
    bool isDefaultStyle = true;
    const Default *d;
    for(d = &(Defaults[0]); d->h.v; d++) {
        if(d->h.v == h.v) break;
    }
    if(!d->h.v) {
        // Not a default style; so just create it the same as our default
        // active group entity style.
        d = &(Defaults[0]);
        isDefaultStyle = false;
    }

    Style ns = {};
    FillDefaultStyle(&ns, d);
    ns.h = h;
    if(isDefaultStyle) {
        ns.name = CnfPrefixToName(d->cnfPrefix);
    } else {
        ns.name = "new-custom-style";
    }

    SK.style.Add(&ns);
}

void Style::FillDefaultStyle(Style *s, const Default *d, bool factory) {
    if(d == NULL) d = &Defaults[0];
    s->color         = (factory) ? d->color : CnfThawColor(d->color, CnfColor(d->cnfPrefix));
    s->width         = (factory) ? d->width : CnfThawFloat((float)(d->width), CnfWidth(d->cnfPrefix));
    s->widthAs       = UNITS_AS_PIXELS;
    s->textHeight    = (factory) ? DEFAULT_TEXT_HEIGHT
                                 : CnfThawFloat(DEFAULT_TEXT_HEIGHT, CnfTextHeight(d->cnfPrefix));
    s->textHeightAs  = UNITS_AS_PIXELS;
    s->textOrigin    = 0;
    s->textAngle     = 0;
    s->visible       = true;
    s->exportable    = true;
    s->filled        = false;
    s->fillColor     = RGBf(0.3, 0.3, 0.3);
    s->stippleType   = (d->h.v == Style::HIDDEN_EDGE) ? Style::STIPPLE_DASH
                                                      : Style::STIPPLE_CONTINUOUS;
    s->stippleScale  = 15.0;
    s->zIndex        = d->zIndex;
}

void Style::LoadFactoryDefaults(void) {
    const Default *d;
    for(d = &(Defaults[0]); d->h.v; d++) {
        Style *s = Get(d->h);
        FillDefaultStyle(s, d, /*factory=*/true);
    }
    SS.backgroundColor = RGBi(0, 0, 0);
    if(SS.bgImage.fromFile) MemFree(SS.bgImage.fromFile);
    SS.bgImage.fromFile = NULL;
}

void Style::FreezeDefaultStyles(void) {
    const Default *d;
    for(d = &(Defaults[0]); d->h.v; d++) {
        CnfFreezeColor(Color(d->h), CnfColor(d->cnfPrefix));
        CnfFreezeFloat((float)Width(d->h), CnfWidth(d->cnfPrefix));
        CnfFreezeFloat((float)TextHeight(d->h), CnfTextHeight(d->cnfPrefix));
    }
}

uint32_t Style::CreateCustomStyle(bool rememberForUndo) {
    if(rememberForUndo) SS.UndoRemember();
    uint32_t vs = max((uint32_t)Style::FIRST_CUSTOM, SK.style.MaximumId() + 1);
    hStyle hs = { vs };
    (void)Style::Get(hs);
    return hs.v;
}

void Style::AssignSelectionToStyle(uint32_t v) {
    bool showError = false;
    SS.GW.GroupSelection();

    SS.UndoRemember();
    int i;
    for(i = 0; i < SS.GW.gs.entities; i++) {
        hEntity he = SS.GW.gs.entity[i];
        Entity *e = SK.GetEntity(he);
        if(!e->IsStylable()) continue;

        if(!he.isFromRequest()) {
            showError = true;
            continue;
        }

        hRequest hr = he.request();
        Request *r = SK.GetRequest(hr);
        r->style.v = v;
        SS.MarkGroupDirty(r->group);
    }
    for(i = 0; i < SS.GW.gs.constraints; i++) {
        hConstraint hc = SS.GW.gs.constraint[i];
        Constraint *c = SK.GetConstraint(hc);
        if(!c->IsStylable()) continue;

        c->disp.style.v = v;
    }

    if(showError) {
        Error("Can't assign style to an entity that's derived from another "
              "entity; try assigning a style to this entity's parent.");
    }

    SS.GW.ClearSelection();
    InvalidateGraphics();
    SS.ScheduleGenerateAll();

    // And show that style's info screen in the text window.
    SS.TW.GoToScreen(TextWindow::SCREEN_STYLE_INFO);
    SS.TW.shown.style.v = v;
    SS.ScheduleShowTW();
}

//-----------------------------------------------------------------------------
// Look up a style by its handle. If that style does not exist, then create
// the style, according to our table of default styles.
//-----------------------------------------------------------------------------
Style *Style::Get(hStyle h) {
    if(h.v == 0) h.v = ACTIVE_GRP;

    Style *s = SK.style.FindByIdNoOops(h);
    if(s) {
        // It exists, good.
        return s;
    } else {
        // It doesn't exist; so we should create it and then return that.
        CreateDefaultStyle(h);
        return SK.style.FindById(h);
    }
}

//-----------------------------------------------------------------------------
// A couple of wrappers, so that I can call these functions with either an
// hStyle or with the integer corresponding to that hStyle.v.
//-----------------------------------------------------------------------------
RgbaColor Style::Color(int s, bool forExport) {
    hStyle hs = { (uint32_t)s };
    return Color(hs, forExport);
}
float Style::Width(int s) {
    hStyle hs = { (uint32_t)s };
    return Width(hs);
}

//-----------------------------------------------------------------------------
// If a color is almost white, then we can rewrite it to black, just so that
// it won't disappear on file formats with a light background.
//-----------------------------------------------------------------------------
RgbaColor Style::RewriteColor(RgbaColor rgbin) {
    Vector rgb = Vector::From(rgbin.redF(), rgbin.greenF(), rgbin.blueF());
    rgb = rgb.Minus(Vector::From(1, 1, 1));
    if(rgb.Magnitude() < 0.4 && SS.fixExportColors) {
        // This is an almost-white color in a default style, which is
        // good for the default on-screen view (black bg) but probably
        // not desired in the exported files, which typically are shown
        // against white backgrounds.
        return RGBi(0, 0, 0);
    } else {
        return rgbin;
    }
}

//-----------------------------------------------------------------------------
// Return the stroke color associated with our style as 8-bit RGB.
//-----------------------------------------------------------------------------
RgbaColor Style::Color(hStyle h, bool forExport) {
    Style *s = Get(h);
    if(forExport) {
        return RewriteColor(s->color);
    } else {
        return s->color;
    }
}

//-----------------------------------------------------------------------------
// Return the fill color associated with our style as 8-bit RGB.
//-----------------------------------------------------------------------------
RgbaColor Style::FillColor(hStyle h, bool forExport) {
    Style *s = Get(h);
    if(forExport) {
        return RewriteColor(s->fillColor);
    } else {
        return s->fillColor;
    }
}

//-----------------------------------------------------------------------------
// Return the width associated with our style in pixels..
//-----------------------------------------------------------------------------
float Style::Width(hStyle h) {
    double r = 1.0;
    Style *s = Get(h);
    if(s->widthAs == UNITS_AS_MM) {
        r = s->width * SS.GW.scale;
    } else if(s->widthAs == UNITS_AS_PIXELS) {
        r = s->width;
    }
    // This returns a float because ssglLineWidth expects a float, avoid casts.
    return (float)r;
}

//-----------------------------------------------------------------------------
// Return the width associated with our style in millimeters..
//-----------------------------------------------------------------------------
double Style::WidthMm(int hs) {
    double widthpx = Width(hs);
    return widthpx / SS.GW.scale;
}

//-----------------------------------------------------------------------------
// Return the associated text height, in pixels.
//-----------------------------------------------------------------------------
double Style::TextHeight(hStyle hs) {
    Style *s = Get(hs);
    if(s->textHeightAs == UNITS_AS_MM) {
        return s->textHeight * SS.GW.scale;
    } else /* s->textHeightAs == UNITS_AS_PIXELS */ {
        return s->textHeight;
    }
}

double Style::DefaultTextHeight() {
    hStyle hs { Style::CONSTRAINT };
    return TextHeight(hs);
}

//-----------------------------------------------------------------------------
// Should lines and curves from this style appear in the output file? Only
// if it's both shown and exportable.
//-----------------------------------------------------------------------------
bool Style::Exportable(int si) {
    hStyle hs = { (uint32_t)si };
    Style *s = Get(hs);
    return (s->exportable) && (s->visible);
}

//-----------------------------------------------------------------------------
// Return the appropriate style for our entity. If the entity has a style
// explicitly assigned, then it's that style. Otherwise it's the appropriate
// default style.
//-----------------------------------------------------------------------------
hStyle Style::ForEntity(hEntity he) {
    Entity *e = SK.GetEntity(he);
    // If the entity has a special style, use that. If that style doesn't
    // exist yet, then it will get created automatically later.
    if(e->style.v != 0) {
        return e->style;
    }

    // Otherwise, we use the default rules.
    hStyle hs;
    if(e->group.v != SS.GW.activeGroup.v) {
        hs.v = INACTIVE_GRP;
    } else if(e->construction) {
        hs.v = CONSTRUCTION;
    } else {
        hs.v = ACTIVE_GRP;
    }
    return hs;
}

int Style::PatternType(hStyle hs) {
    Style *s = Get(hs);
    return s->stippleType;
}

double Style::StippleScaleMm(hStyle hs) {
    Style *s = Get(hs);
    if(s->widthAs == UNITS_AS_MM) {
        return s->stippleScale;
    } else if(s->widthAs == UNITS_AS_PIXELS) {
        return s->stippleScale / SS.GW.scale;
    }
    return 1.0;
}

std::string Style::DescriptionString(void) {
    if(name.empty()) {
        return ssprintf("s%03x-(unnamed)", h.v);
    } else {
        return ssprintf("s%03x-%s", h.v, name.c_str());
    }
}


void TextWindow::ScreenShowListOfStyles(int link, uint32_t v) {
    SS.TW.GoToScreen(SCREEN_LIST_OF_STYLES);
}
void TextWindow::ScreenShowStyleInfo(int link, uint32_t v) {
    SS.TW.GoToScreen(SCREEN_STYLE_INFO);
    SS.TW.shown.style.v = v;
}

void TextWindow::ScreenLoadFactoryDefaultStyles(int link, uint32_t v) {
    Style::LoadFactoryDefaults();
    SS.TW.GoToScreen(SCREEN_LIST_OF_STYLES);
}

void TextWindow::ScreenCreateCustomStyle(int link, uint32_t v) {
    Style::CreateCustomStyle();
}

void TextWindow::ScreenChangeBackgroundColor(int link, uint32_t v) {
    RgbaColor rgb = SS.backgroundColor;
    SS.TW.ShowEditControlWithColorPicker(3, rgb);
    SS.TW.edit.meaning = EDIT_BACKGROUND_COLOR;
}

static int RoundUpToPowerOfTwo(int v)
{
    int i;
    for(i = 0; i < 31; i++) {
        int vt = (1 << i);
        if(vt >= v) {
            return vt;
        }
    }
    return 0;
}

void TextWindow::ScreenBackgroundImage(int link, uint32_t v) {
    if(SS.bgImage.fromFile) MemFree(SS.bgImage.fromFile);
    SS.bgImage.fromFile = NULL;

    if(link == 'l') {
        FILE *f = NULL;
        png_struct *png_ptr = NULL;
        png_info *info_ptr = NULL;

        std::string importFile;
        if(!GetOpenFile(&importFile, "", PngFileFilter)) goto err;
        f = ssfopen(importFile, "rb");
        if(!f) goto err;

        uint8_t header[8];
        if (fread(header, 1, 8, f) != 8)
            goto err;
        if(png_sig_cmp(header, 0, 8)) goto err;

        png_ptr = png_create_read_struct(PNG_LIBPNG_VER_STRING,
            NULL, NULL, NULL);
        if(!png_ptr) goto err;

        info_ptr = png_create_info_struct(png_ptr);
        if(!info_ptr) goto err;

        if(setjmp(png_jmpbuf(png_ptr))) goto err;

        png_init_io(png_ptr, f);
        png_set_sig_bytes(png_ptr, 8);

        png_read_png(png_ptr, info_ptr,
            PNG_TRANSFORM_EXPAND | PNG_TRANSFORM_STRIP_ALPHA, NULL);

        int w; w = (int)png_get_image_width(png_ptr, info_ptr);
        int h; h = (int)png_get_image_height(png_ptr, info_ptr);
        uint8_t **rows; rows = png_get_rows(png_ptr, info_ptr);

        // Round to next-highest powers of two, since the textures require
        // that. And round up to 4, to guarantee 32-bit alignment.
        int rw; rw = max(4, RoundUpToPowerOfTwo(w));
        int rh; rh = max(4, RoundUpToPowerOfTwo(h));

        SS.bgImage.fromFile = (uint8_t *)MemAlloc(rw*rh*3);
        {for(int i = 0; i < h; i++) {
            memcpy(SS.bgImage.fromFile + ((h - 1) - i)*(rw*3), rows[i], w*3);
        }}
        SS.bgImage.w      = w;
        SS.bgImage.h      = h;
        SS.bgImage.rw     = rw;
        SS.bgImage.rh     = rh;
        SS.bgImage.scale  = SS.GW.scale;
        SS.bgImage.origin = SS.GW.offset.ScaledBy(-1);

err:
        if(png_ptr) png_destroy_read_struct(&png_ptr, &info_ptr, NULL);
        if(f) fclose(f);
    }
    SS.ScheduleShowTW();
}

void TextWindow::ScreenChangeBackgroundImageScale(int link, uint32_t v) {
    SS.TW.edit.meaning = EDIT_BACKGROUND_IMG_SCALE;
    SS.TW.ShowEditControl(10, ssprintf("%.3f", SS.bgImage.scale * SS.MmPerUnit()));
}

void TextWindow::ShowListOfStyles(void) {
    Printf(true, "%Ft color  style-name");

    bool darkbg = false;
    Style *s;
    for(s = SK.style.First(); s; s = SK.style.NextAfter(s)) {
        Printf(false, "%Bp  %Bz   %Bp   %Fl%Ll%f%D%s%E",
            darkbg ? 'd' : 'a',
            &s->color,
            darkbg ? 'd' : 'a',
            ScreenShowStyleInfo, s->h.v,
            s->DescriptionString().c_str());

        darkbg = !darkbg;
    }

    Printf(true, "  %Fl%Ll%fcreate a new custom style%E",
        &ScreenCreateCustomStyle);

    Printf(false, "");

    RgbaColor rgb = SS.backgroundColor;
    Printf(false, "%Ft background color (r, g, b)%E");
    Printf(false, "%Ba   %@, %@, %@ %Fl%D%f%Ll[change]%E",
        rgb.redF(), rgb.greenF(), rgb.blueF(),
        top[rows-1] + 2, &ScreenChangeBackgroundColor);

    Printf(false, "");
    Printf(false, "%Ft background bitmap image%E");
    if(SS.bgImage.fromFile) {
        Printf(false, "%Ba   %Ftwidth:%E %dpx   %Ftheight:%E %dpx",
            SS.bgImage.w, SS.bgImage.h);

        Printf(false, "   %Ftscale:%E %# px/%s %Fl%Ll%f%D[change]%E",
            SS.bgImage.scale*SS.MmPerUnit(),
            SS.UnitName(),
            &ScreenChangeBackgroundImageScale, top[rows-1] + 2);

        Printf(false, "%Ba   %Fl%Lc%fclear background image%E",
            &ScreenBackgroundImage);
    } else {
        Printf(false, "%Ba   none - %Fl%Ll%fload background image%E",
            &ScreenBackgroundImage);
        Printf(false, "   (bottom left will be center of view)");
    }

    Printf(false, "");
    Printf(false, "  %Fl%Ll%fload factory defaults%E",
        &ScreenLoadFactoryDefaultStyles);
}


void TextWindow::ScreenChangeStyleName(int link, uint32_t v) {
    hStyle hs = { v };
    Style *s = Style::Get(hs);
    SS.TW.ShowEditControl(12, s->name);
    SS.TW.edit.style = hs;
    SS.TW.edit.meaning = EDIT_STYLE_NAME;
}

void TextWindow::ScreenDeleteStyle(int link, uint32_t v) {
    SS.UndoRemember();
    hStyle hs = { v };
    Style *s = SK.style.FindByIdNoOops(hs);
    if(s) {
        SK.style.RemoveById(hs);
        // And it will get recreated automatically if something is still using
        // the style, so no need to do anything else.
    }
    SS.TW.GoToScreen(SCREEN_LIST_OF_STYLES);
    InvalidateGraphics();
}

void TextWindow::ScreenChangeStylePatternType(int link, uint32_t v) {
    hStyle hs = { v };
    Style *s = Style::Get(hs);
    s->stippleType = link - 1;
}

void TextWindow::ScreenChangeStyleMetric(int link, uint32_t v) {
    hStyle hs = { v };
    Style *s = Style::Get(hs);
    double val;
    int units, meaning, col;
    switch(link) {
        case 't':
            val = s->textHeight;
            units = s->textHeightAs;
            col = 10;
            meaning = EDIT_STYLE_TEXT_HEIGHT;
            break;

        case 's':
            val = s->stippleScale;
            units = s->widthAs;
            col = 17;
            meaning = EDIT_STYLE_STIPPLE_PERIOD;
            break;

        case 'w':
        case 'W':
            val = s->width;
            units = s->widthAs;
            col = 9;
            meaning = EDIT_STYLE_WIDTH;
            break;

        default: oops();
    }

    std::string edit_value;
    if(units == Style::UNITS_AS_PIXELS) {
        edit_value = ssprintf("%.2f", val);
    } else {
        edit_value = SS.MmToString(val);
    }
    SS.TW.ShowEditControl(col, edit_value);
    SS.TW.edit.style = hs;
    SS.TW.edit.meaning = meaning;
}

void TextWindow::ScreenChangeStyleTextAngle(int link, uint32_t v) {
    hStyle hs = { v };
    Style *s = Style::Get(hs);
    SS.TW.ShowEditControl(9, ssprintf("%.2f", s->textAngle));
    SS.TW.edit.style = hs;
    SS.TW.edit.meaning = EDIT_STYLE_TEXT_ANGLE;
}

void TextWindow::ScreenChangeStyleColor(int link, uint32_t v) {
    hStyle hs = { v };
    Style *s = Style::Get(hs);
    // Same function used for stroke and fill colors
    int em;
    RgbaColor rgb;
    if(link == 's') {
        em = EDIT_STYLE_COLOR;
        rgb = s->color;
    } else if(link == 'f') {
        em = EDIT_STYLE_FILL_COLOR;
        rgb = s->fillColor;
    } else {
        oops();
    }
    SS.TW.ShowEditControlWithColorPicker(13, rgb);
    SS.TW.edit.style = hs;
    SS.TW.edit.meaning = em;
}

void TextWindow::ScreenChangeStyleYesNo(int link, uint32_t v) {
    SS.UndoRemember();
    hStyle hs = { v };
    Style *s = Style::Get(hs);
    switch(link) {
        // Units for the width
        case 'w':
            if(s->widthAs != Style::UNITS_AS_MM) {
                s->widthAs = Style::UNITS_AS_MM;
                s->width /= SS.GW.scale;
                s->stippleScale /= SS.GW.scale;
            }
            break;
        case 'W':
            if(s->widthAs != Style::UNITS_AS_PIXELS) {
                s->widthAs = Style::UNITS_AS_PIXELS;
                s->width *= SS.GW.scale;
                s->stippleScale *= SS.GW.scale;
            }
            break;

        // Units for the height
        case 'g':
            if(s->textHeightAs != Style::UNITS_AS_MM) {
                s->textHeightAs = Style::UNITS_AS_MM;
                s->textHeight /= SS.GW.scale;
            }
            break;

        case 'G':
            if(s->textHeightAs != Style::UNITS_AS_PIXELS) {
                s->textHeightAs = Style::UNITS_AS_PIXELS;
                s->textHeight *= SS.GW.scale;
            }
            break;

        case 'e':
            s->exportable = !(s->exportable);
            break;

        case 'v':
            s->visible = !(s->visible);
            break;

        case 'f':
            s->filled = !(s->filled);
            break;

        // Horizontal text alignment
        case 'L':
            s->textOrigin |=  Style::ORIGIN_LEFT;
            s->textOrigin &= ~Style::ORIGIN_RIGHT;
            break;
        case 'H':
            s->textOrigin &= ~Style::ORIGIN_LEFT;
            s->textOrigin &= ~Style::ORIGIN_RIGHT;
            break;
        case 'R':
            s->textOrigin &= ~Style::ORIGIN_LEFT;
            s->textOrigin |=  Style::ORIGIN_RIGHT;
            break;

        // Vertical text alignment
        case 'B':
            s->textOrigin |=  Style::ORIGIN_BOT;
            s->textOrigin &= ~Style::ORIGIN_TOP;
            break;
        case 'V':
            s->textOrigin &= ~Style::ORIGIN_BOT;
            s->textOrigin &= ~Style::ORIGIN_TOP;
            break;
        case 'T':
            s->textOrigin &= ~Style::ORIGIN_BOT;
            s->textOrigin |=  Style::ORIGIN_TOP;
            break;
    }
    InvalidateGraphics();
}

bool TextWindow::EditControlDoneForStyles(const char *str) {
    Style *s;
    switch(edit.meaning) {
        case EDIT_STYLE_STIPPLE_PERIOD:
        case EDIT_STYLE_TEXT_HEIGHT:
        case EDIT_STYLE_WIDTH: {
            SS.UndoRemember();
            s = Style::Get(edit.style);

            double v;
            int units = (edit.meaning == EDIT_STYLE_TEXT_HEIGHT) ?
                            s->textHeightAs : s->widthAs;
            if(units == Style::UNITS_AS_MM) {
                v = SS.StringToMm(str);
            } else {
                v = atof(str);
            }
            v = max(0.0, v);
            if(edit.meaning == EDIT_STYLE_TEXT_HEIGHT) {
                s->textHeight = v;
            } else if(edit.meaning == EDIT_STYLE_STIPPLE_PERIOD) {
                s->stippleScale = v;
            } else {
                s->width = v;
            }
            break;
        }
        case EDIT_STYLE_TEXT_ANGLE:
            SS.UndoRemember();
            s = Style::Get(edit.style);
            s->textAngle = WRAP_SYMMETRIC(atof(str), 360);
            break;

        case EDIT_BACKGROUND_COLOR:
        case EDIT_STYLE_FILL_COLOR:
        case EDIT_STYLE_COLOR: {
            Vector rgb;
            if(sscanf(str, "%lf, %lf, %lf", &rgb.x, &rgb.y, &rgb.z)==3) {
                rgb = rgb.ClampWithin(0, 1);
                if(edit.meaning == EDIT_STYLE_COLOR) {
                    SS.UndoRemember();
                    s = Style::Get(edit.style);
                    s->color = RGBf(rgb.x, rgb.y, rgb.z);
                } else if(edit.meaning == EDIT_STYLE_FILL_COLOR) {
                    SS.UndoRemember();
                    s = Style::Get(edit.style);
                    s->fillColor = RGBf(rgb.x, rgb.y, rgb.z);
                } else {
                    SS.backgroundColor = RGBf(rgb.x, rgb.y, rgb.z);
                }
            } else {
                Error("Bad format: specify color as r, g, b");
            }
            break;
        }
        case EDIT_STYLE_NAME:
            if(!*str) {
                Error("Style name cannot be empty");
            } else {
                SS.UndoRemember();
                s = Style::Get(edit.style);
                s->name = str;
            }
            break;

        case EDIT_BACKGROUND_IMG_SCALE: {
            Expr *e = Expr::From(str, true);
            if(e) {
                double ev = e->Eval();
                if(ev < 0.001 || isnan(ev)) {
                    Error("Scale must not be zero or negative!");
                } else {
                    SS.bgImage.scale = ev / SS.MmPerUnit();
                }
            }
            break;
        }
        default: return false;
    }
    return true;
}

void TextWindow::ShowStyleInfo(void) {
    Printf(true, "%Fl%f%Ll(back to list of styles)%E", &ScreenShowListOfStyles);

    Style *s = Style::Get(shown.style);

    if(s->h.v < Style::FIRST_CUSTOM) {
        Printf(true, "%FtSTYLE  %E%s ", s->DescriptionString().c_str());
    } else {
        Printf(true, "%FtSTYLE  %E%s "
                     "[%Fl%Ll%D%frename%E/%Fl%Ll%D%fdel%E]",
            s->DescriptionString().c_str(),
            s->h.v, &ScreenChangeStyleName,
            s->h.v, &ScreenDeleteStyle);
    }
    Printf(true, "%Ft line stroke style%E");
    Printf(false, "%Ba   %Ftcolor %E%Bz  %Ba (%@, %@, %@) %D%f%Ls%Fl[change]%E",
        &s->color,
        s->color.redF(), s->color.greenF(), s->color.blueF(),
        s->h.v, ScreenChangeStyleColor);

    // The line width, and its units
    if(s->widthAs == Style::UNITS_AS_PIXELS) {
        Printf(false, "   %Ftwidth%E %@ %D%f%Lp%Fl[change]%E",
            s->width,
            s->h.v, &ScreenChangeStyleMetric,
            (s->h.v < Style::FIRST_CUSTOM) ? 'w' : 'W');
    } else {
        Printf(false, "   %Ftwidth%E %s %D%f%Lp%Fl[change]%E",
            SS.MmToString(s->width).c_str(),
            s->h.v, &ScreenChangeStyleMetric,
            (s->h.v < Style::FIRST_CUSTOM) ? 'w' : 'W');
    }

    if(s->h.v >= Style::FIRST_CUSTOM) {
        if(s->widthAs == Style::UNITS_AS_PIXELS) {
            Printf(false, "%Ba   %Ftstipple width%E %@ %D%f%Lp%Fl[change]%E",
                s->stippleScale,
                s->h.v, &ScreenChangeStyleMetric, 's');
        } else {
            Printf(false, "%Ba   %Ftstipple width%E %s %D%f%Lp%Fl[change]%E",
                SS.MmToString(s->stippleScale).c_str(),
                s->h.v, &ScreenChangeStyleMetric, 's');
        }
    }

    bool widthpx = (s->widthAs == Style::UNITS_AS_PIXELS);
    if(s->h.v < Style::FIRST_CUSTOM) {
        Printf(false,"   %Ftin units of %Fdpixels%E");
    } else {
        Printf(false,"%Ba   %Ftin units of  %Fd"
                            "%D%f%LW%s pixels%E  "
                            "%D%f%Lw%s %s",
            s->h.v, &ScreenChangeStyleYesNo,
            widthpx ? RADIO_TRUE : RADIO_FALSE,
            s->h.v, &ScreenChangeStyleYesNo,
            !widthpx ? RADIO_TRUE : RADIO_FALSE,
            SS.UnitName());
    }

    Printf(false,"%Ba   %Ftstipple type:%E");

    const size_t patternCount = Style::LAST_STIPPLE + 1;
    const char *patternsSource[patternCount] = {
        "___________",
        "- - - - - -",
        "__ __ __ __",
        "-.-.-.-.-.-",
        "..-..-..-..",
        "...........",
        "~~~~~~~~~~~",
        "__~__~__~__"
    };
    std::string patterns[patternCount];

    for(int i = 0; i <= Style::LAST_STIPPLE; i++) {
        const char *str = patternsSource[i];
        do {
            switch(*str) {
                case ' ': patterns[i] += " "; break;
                case '.': patterns[i] += "\xEE\x80\x84"; break;
                case '_': patterns[i] += "\xEE\x80\x85"; break;
                case '-': patterns[i] += "\xEE\x80\x86"; break;
                case '~': patterns[i] += "\xEE\x80\x87"; break;
                default: oops();
            }
        } while(*(++str));
    }

    for(int i = 0; i <= Style::LAST_STIPPLE; i++) {
        const char *radio = s->stippleType == i ? RADIO_TRUE : RADIO_FALSE;
        Printf(false, "%Bp     %D%f%Lp%s %s%E",
            (i % 2 == 0) ? 'd' : 'a',
            s->h.v, &ScreenChangeStylePatternType,
            i + 1, radio, patterns[i].c_str());
    }

    if(s->h.v >= Style::FIRST_CUSTOM) {
        // The fill color, and whether contours are filled

        Printf(false, "");
        Printf(false, "%Ft contour fill style%E");
        Printf(false,
            "%Ba   %Ftcolor %E%Bz  %Ba (%@, %@, %@) %D%f%Lf%Fl[change]%E",
            &s->fillColor,
            s->fillColor.redF(), s->fillColor.greenF(), s->fillColor.blueF(),
            s->h.v, ScreenChangeStyleColor);

        Printf(false, "%Bd   %D%f%Lf%s  contours are filled%E",
            s->h.v, &ScreenChangeStyleYesNo,
            s->filled ? CHECK_TRUE : CHECK_FALSE);
    }

    // The text height, and its units
    Printf(false, "");
    Printf(false, "%Ft text style%E");

    if(s->textHeightAs == Style::UNITS_AS_PIXELS) {
        Printf(false, "%Ba   %Ftheight %E%@ %D%f%Lt%Fl%s%E",
            s->textHeight,
            s->h.v, &ScreenChangeStyleMetric,
            "[change]");
    } else {
        Printf(false, "%Ba   %Ftheight %E%s %D%f%Lt%Fl%s%E",
            SS.MmToString(s->textHeight).c_str(),
            s->h.v, &ScreenChangeStyleMetric,
            "[change]");
    }

    bool textHeightpx = (s->textHeightAs == Style::UNITS_AS_PIXELS);
    if(s->h.v < Style::FIRST_CUSTOM) {
        Printf(false,"%Bd   %Ftin units of %Fdpixels");
    } else {
        Printf(false,"%Bd   %Ftin units of  %Fd"
                            "%D%f%LG%s pixels%E  "
                            "%D%f%Lg%s %s",
            s->h.v, &ScreenChangeStyleYesNo,
            textHeightpx ? RADIO_TRUE : RADIO_FALSE,
            s->h.v, &ScreenChangeStyleYesNo,
            !textHeightpx ? RADIO_TRUE : RADIO_FALSE,
            SS.UnitName());
    }

    if(s->h.v >= Style::FIRST_CUSTOM) {
        Printf(false, "%Ba   %Ftangle %E%@ %D%f%Ll%Fl[change]%E",
            s->textAngle,
            s->h.v, &ScreenChangeStyleTextAngle);

        Printf(false, "");
        Printf(false, "%Ft text comment alignment%E");
        bool neither;
        neither = !(s->textOrigin & (Style::ORIGIN_LEFT | Style::ORIGIN_RIGHT));
        Printf(false, "%Ba   "
                      "%D%f%LL%s left%E    "
                      "%D%f%LH%s center%E  "
                      "%D%f%LR%s right%E  ",
            s->h.v, &ScreenChangeStyleYesNo,
            (s->textOrigin & Style::ORIGIN_LEFT) ? RADIO_TRUE : RADIO_FALSE,
            s->h.v, &ScreenChangeStyleYesNo,
            neither ? RADIO_TRUE : RADIO_FALSE,
            s->h.v, &ScreenChangeStyleYesNo,
            (s->textOrigin & Style::ORIGIN_RIGHT) ? RADIO_TRUE : RADIO_FALSE);

        neither = !(s->textOrigin & (Style::ORIGIN_BOT | Style::ORIGIN_TOP));
        Printf(false, "%Bd   "
                      "%D%f%LB%s bottom%E  "
                      "%D%f%LV%s center%E  "
                      "%D%f%LT%s top%E  ",
            s->h.v, &ScreenChangeStyleYesNo,
            (s->textOrigin & Style::ORIGIN_BOT) ? RADIO_TRUE : RADIO_FALSE,
            s->h.v, &ScreenChangeStyleYesNo,
            neither ? RADIO_TRUE : RADIO_FALSE,
            s->h.v, &ScreenChangeStyleYesNo,
            (s->textOrigin & Style::ORIGIN_TOP) ? RADIO_TRUE : RADIO_FALSE);
    }

    if(s->h.v >= Style::FIRST_CUSTOM) {
        Printf(false, "");

        Printf(false, "  %Fd%D%f%Lv%s  show these objects on screen%E",
                s->h.v, &ScreenChangeStyleYesNo,
                s->visible ? CHECK_TRUE : CHECK_FALSE);

        Printf(false, "  %Fd%D%f%Le%s  export these objects%E",
                s->h.v, &ScreenChangeStyleYesNo,
                s->exportable ? CHECK_TRUE : CHECK_FALSE);

        Printf(false, "");
        Printf(false, "To assign lines or curves to this style,");
        Printf(false, "right-click them on the drawing.");
    }
}

void TextWindow::ScreenAssignSelectionToStyle(int link, uint32_t v) {
    Style::AssignSelectionToStyle(v);
}

