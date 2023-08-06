#include "solvespace.h"
#include "libdxfrw.h"
#include "libdwgr.h"

#ifdef WIN32
// Conflicts with DRW::TEXT.
#   undef TEXT
#endif

namespace SolveSpace {

static std::string ToUpper(std::string str) {
    std::transform(str.begin(), str.end(), str.begin(), ::toupper);
    return str;
}

class DxfReadInterface : public DRW_Interface {
public:
    Vector blockX;
    Vector blockY;
    Vector blockT;

    void invertXTransform() {
        blockX.x = -blockX.x;
        blockY.x = -blockY.x;
        blockT.x = -blockT.x;
    }

    void multBlockTransform(double x, double y, double sx, double sy, double angle) {
        Vector oldX = blockX;
        Vector oldY = blockY;
        Vector oldT = blockT;

        Vector newX = Vector::From(sx, 0.0, 0.0).RotatedAbout(Vector::From(0.0, 0.0, 1.0), angle);
        Vector newY = Vector::From(0.0, sy, 0.0).RotatedAbout(Vector::From(0.0, 0.0, 1.0), angle);
        Vector newT = Vector::From(x, y, 0.0);

        blockX = oldX.ScaledBy(newX.x).Plus(
                 oldY.ScaledBy(newX.y));

        blockY = oldX.ScaledBy(newY.x).Plus(
                 oldY.ScaledBy(newY.y));

        blockT = oldX.ScaledBy(newT.x).Plus(
                 oldY.ScaledBy(newT.y)).Plus(oldT);
    }

    void clearBlockTransform() {
        blockX = Vector::From(1.0, 0.0, 0.0);
        blockY = Vector::From(0.0, 1.0, 0.0);
        blockT = Vector::From(0.0, 0.0, 0.0);
    }

    Vector blockTransform(Vector v) {
        Vector r = blockT;
        r = r.Plus(blockX.ScaledBy(v.x));
        r = r.Plus(blockY.ScaledBy(v.y));
        return r;
    }

    void blockTransformArc(Vector *c, Vector *p0, Vector *p1) {
        bool oldSign = p0->Minus(*c).Cross(p1->Minus(*c)).z > 0.0;

        *c = blockTransform(*c);
        *p0 = blockTransform(*p0);
        *p1 = blockTransform(*p1);

        bool newSign = p0->Minus(*c).Cross(p1->Minus(*c)).z > 0.0;
        if(oldSign != newSign) std::swap(*p0, *p1);
    }

    Vector toVector(const DRW_Coord &c, bool transform = true) {
        Vector result = Vector::From(c.x, c.y, 0.0);
        if(transform) return blockTransform(result);
        return result;
    }

    Vector toVector(const DRW_Vertex2D &c) {
        Vector result = Vector::From(c.x, c.y, 0.0);
        return blockTransform(result);
    }

    Vector toVector(const DRW_Vertex &c) {
        Vector result = Vector::From(c.basePoint.x, c.basePoint.y, 0.0);
        return blockTransform(result);
    }

    double angleTo(Vector v0, Vector v1) {
        Vector d = v1.Minus(v0);
        double a = atan2(d.y, d.x);
        return M_PI + remainder(a - M_PI, 2 * M_PI);
    }

    Vector polar(double radius, double angle) {
        return Vector::From(radius * cos(angle), radius * sin(angle), 0.0);
    }

    hRequest createBulge(Vector p0, Vector p1, double bulge) {
        bool reversed = bulge < 0.0;
        double alpha = atan(bulge) * 4.0;

        Vector middle = p1.Plus(p0).ScaledBy(0.5);
        double dist = p1.Minus(p0).Magnitude() / 2.0;
        double angle = angleTo(p0, p1);

        // alpha can't be 0.0 at this point
        double radius = fabs(dist / sin(alpha / 2.0));
        double wu = fabs(radius * radius - dist * dist);
        double h = sqrt(wu);

        if(bulge > 0.0) {
            angle += M_PI_2;
        } else {
            angle -= M_PI_2;
        }

        if (fabs(alpha) > M_PI) {
            h *= -1.0;
        }

        Vector center = polar(h, angle);
        center = center.Plus(middle);

        if(reversed) std::swap(p0, p1);
        blockTransformArc(&center, &p0, &p1);

        hRequest hr = SS.GW.AddRequest(Request::ARC_OF_CIRCLE, false);
        SK.GetEntity(hr.entity(1))->PointForceTo(center);
        SK.GetEntity(hr.entity(2))->PointForceTo(p0);
        SK.GetEntity(hr.entity(3))->PointForceTo(p1);
        processPoint(hr.entity(1));
        processPoint(hr.entity(2));
        processPoint(hr.entity(3));
        return hr;
    }

    struct Block {
        std::vector<std::unique_ptr<DRW_Entity>> entities;
        DRW_Block data;
    };

    unsigned unknownEntities = 0;
    std::map<std::string, hStyle> styles;
    std::map<std::string, Block> blocks;
    std::map<std::string, DRW_Layer> layers;
    Block *readBlock = NULL;
    const DRW_Insert *insertInsert = NULL;

    template<class T>
    bool addPendingBlockEntity(const T &e) {
        if(readBlock == NULL) return false;
        readBlock->entities.emplace_back(new T(e));
        return true;
    }

    void addEntity(DRW_Entity *e) {
        switch(e->eType) {
            case DRW::POINT:
                addPoint(*static_cast<DRW_Point *>(e));
                break;
            case DRW::LINE:
                addLine(*static_cast<DRW_Line *>(e));
                break;
            case DRW::ARC:
                addArc(*static_cast<DRW_Arc *>(e));
                break;
            case DRW::CIRCLE:
                addCircle(*static_cast<DRW_Circle *>(e));
                break;
            case DRW::POLYLINE:
                addPolyline(*static_cast<DRW_Polyline *>(e));
                break;
            case DRW::LWPOLYLINE:
                addLWPolyline(*static_cast<DRW_LWPolyline *>(e));
                break;
            case DRW::SPLINE:
                addSpline(static_cast<DRW_Spline *>(e));
                break;
            case DRW::INSERT:
                addInsert(*static_cast<DRW_Insert *>(e));
                break;
            case DRW::TEXT:
                addText(*static_cast<DRW_Text *>(e));
                break;
            case DRW::MTEXT:
                addMText(*static_cast<DRW_MText *>(e));
                break;
            case DRW::DIMALIGNED:
                addDimAlign(static_cast<DRW_DimAligned *>(e));
                break;
            case DRW::DIMLINEAR:
                addDimLinear(static_cast<DRW_DimLinear *>(e));
                break;
            case DRW::DIMRADIAL:
                addDimRadial(static_cast<DRW_DimRadial *>(e));
                break;
            case DRW::DIMDIAMETRIC:
                addDimDiametric(static_cast<DRW_DimDiametric *>(e));
                break;
            case DRW::DIMANGULAR:
                addDimAngular(static_cast<DRW_DimAngular *>(e));
                break;
            default:
                unknownEntities++;
        }
    }

    int dxfAlignToOrigin(DRW_Text::HAlign alignH, DRW_Text::VAlign alignV) {
        int origin = 0;
        switch(alignH) {
            case DRW_Text::HLeft:
                origin |= Style::ORIGIN_LEFT;
                break;

            case DRW_Text::HMiddle:
            case DRW_Text::HCenter:
                break;

            case DRW_Text::HRight:
                origin |= Style::ORIGIN_RIGHT;
                break;

            case DRW_Text::HAligned:
            case DRW_Text::HFit:
            default:
                origin |= Style::ORIGIN_LEFT;
                break;
        }

        switch(alignV) {
            case DRW_Text::VBaseLine:
            case DRW_Text::VBottom:
                origin |= Style::ORIGIN_BOT;
                break;

            case DRW_Text::VMiddle:
                break;

            case DRW_Text::VTop:
                origin |= Style::ORIGIN_TOP;
                break;

            default:
                origin |= Style::ORIGIN_BOT;
                break;
        }

        return origin;
    }

    DRW_Layer *getSourceLayer(const DRW_Entity *e) {
        DRW_Layer *layer = NULL;
        if(insertInsert != NULL) {
            std::string l = insertInsert->layer;
            auto bi = layers.find(l);
            if(bi != layers.end()) layer = &bi->second;
        } else {
            std::string l = e->layer;
            auto bi = layers.find(l);
            if(bi != layers.end()) layer = &bi->second;
        }
        return layer;
    }

    int getColor(const DRW_Entity *e) {
        int col = e->color;
        if(col == DRW::ColorByBlock) {
            if(insertInsert != NULL) {
                col = insertInsert->color;
            } else {
                col = 7;
            }
        }
        if(col == DRW::ColorByLayer) {
            DRW_Layer *layer = getSourceLayer(e);
            if(layer != NULL) {
                col = layer->color;
            } else {
                col = 7;
            }
        }
        return col;
    }

    DRW_LW_Conv::lineWidth getLineWidth(const DRW_Entity *e) {
        DRW_LW_Conv::lineWidth result = e->lWeight;
        if(result == DRW_LW_Conv::widthByBlock) {
            if(insertInsert != NULL) {
                result = insertInsert->lWeight;
            } else {
                result = DRW_LW_Conv::widthDefault;
            }
        }
        if(result == DRW_LW_Conv::widthByLayer) {
            DRW_Layer *layer = getSourceLayer(e);
            if(layer != NULL) {
                result = layer->lWeight;
            } else {
                result = DRW_LW_Conv::widthDefault;
            }
        }
        return result;
    }

    std::string getLineType(const DRW_Entity *e) {
        std::string  result = e->lineType;
        if(result == "BYBLOCK") {
            if(insertInsert != NULL) {
                result = ToUpper(insertInsert->lineType);
            } else {
                result = "CONTINUOUS";
            }
        }
        if(result == "BYLAYER") {
            DRW_Layer *layer = getSourceLayer(e);
            if(layer != NULL) {
                result = ToUpper(layer->lineType);
            } else {
                result = "CONTINUOUS";
            }
        }
        return result;
    }

    hStyle invisibleStyle() {
        std::string id = "@dxf-invisible";

        auto si = styles.find(id);
        if(si != styles.end()) {
            return si->second;
        }

        hStyle hs = { Style::CreateCustomStyle(/*rememberForUndo=*/false) };
        Style *s = Style::Get(hs);
        s->name = id;
        s->visible = false;

        styles.emplace(id, hs);
        return hs;
    }

    hStyle styleFor(const DRW_Entity *e) {
        // Color.
        // TODO: which color to choose: index or RGB one?
        int col = getColor(e);
        RgbaColor c = RgbaColor::From(DRW::dxfColors[col][0],
                                      DRW::dxfColors[col][1],
                                      DRW::dxfColors[col][2]);

        // Line width.
        DRW_LW_Conv::lineWidth lw = getLineWidth(e);
        double width = DRW_LW_Conv::lineWidth2dxfInt(e->lWeight) / 100.0;
        if(width < 0.0) width = 1.0;

        // Line stipple.
        // TODO: Probably, we can load default autocad patterns and match it with ours.
        std::string lineType = getLineType(e);
        int stipple = Style::STIPPLE_CONTINUOUS;
        for(int i = 0; i <= Style::LAST_STIPPLE; i++) {
            if(lineType == DxfFileWriter::lineTypeName(i)) {
                stipple = i;
                break;
            }
        }

        // Text properties.
        DRW_Text::HAlign alignH = DRW_Text::HLeft;
        DRW_Text::VAlign alignV = DRW_Text::VBaseLine;
        double textAngle = 0.0;
        double textHeight = Style::DefaultTextHeight();

        if(e->eType == DRW::TEXT || e->eType == DRW::MTEXT) {
            const DRW_Text *text = static_cast<const DRW_Text *>(e);
            alignH = text->alignH;
            alignV = text->alignV;
            textHeight = text->height;
            textAngle = text->angle;
            // I have no idea why, but works
            if(alignH == DRW_Text::HMiddle) {
                alignV = DRW_Text::VMiddle;
            }
        }

        // Unique identifier based on style properties.
        std::string id = "@dxf";
        if(lw != DRW_LW_Conv::widthDefault)
            id += ssprintf("-w%.4g", width);
        if(lineType != "CONTINUOUS")
            id += ssprintf("-%s", lineType.c_str());
        if(c.red != 0 || c.green != 0 || c.blue != 0)
            id += ssprintf("-#%02x%02x%02x", c.red, c.green, c.blue);
        if(textHeight != Style::DefaultTextHeight())
            id += ssprintf("-h%.4g", textHeight);
        if(textAngle != 0.0)
            id += ssprintf("-a%.5g", textAngle);
        if(alignH != DRW_Text::HLeft)
            id += ssprintf("-oh%d", alignH);
        if(alignV != DRW_Text::VBaseLine)
            id += ssprintf("-ov%d", alignV);

        auto si = styles.find(id);
        if(si != styles.end()) {
            return si->second;
        }

        hStyle hs = { Style::CreateCustomStyle(/*rememberForUndo=*/false) };
        Style *s = Style::Get(hs);
        if(lw != DRW_LW_Conv::widthDefault) {
            s->widthAs = Style::UNITS_AS_MM;
            s->width = width;
            s->stippleScale = 1.0 + width * 2.0;
        }
        s->name = id;
        s->stippleType = stipple;
        if(c.red != 0 || c.green != 0 || c.blue != 0) s->color = c;
        s->textHeightAs = Style::UNITS_AS_MM;
        s->textHeight = textHeight;
        s->textAngle = textAngle;
        s->textOrigin = dxfAlignToOrigin(alignH, alignV);

        styles.emplace(id, hs);
        return hs;
    }

    void setStyle(hRequest hr, hStyle hs) {
        Request *r = SK.GetRequest(hr);
        r->style = hs;
    }

    struct VectorHash {
        size_t operator()(const Vector &v) const {
            static const size_t size = std::numeric_limits<size_t>::max() / 2 - 1;
            static const double eps = (4.0 * LENGTH_EPS);

            double x = fabs(v.x) / eps;
            double y = fabs(v.y) / eps;

            size_t xs = size_t(fmod(x, double(size)));
            size_t ys = size_t(fmod(y, double(size)));

            return ys * size + xs;
        }
    };

    struct VectorPred {
        bool operator()(Vector a, Vector b) const {
            return a.Equals(b, LENGTH_EPS);
        }
    };

    std::unordered_map<Vector, hEntity, VectorHash, VectorPred> points;

    void processPoint(hEntity he, bool constrain = true) {
        Entity *e = SK.GetEntity(he);
        Vector pos = e->PointGetNum();
        hEntity p = findPoint(pos);
        if(p.v == he.v) return;
        if(p.v != Entity::NO_ENTITY.v) {
            if(constrain) {
                Constraint::ConstrainCoincident(he, p);
            }
            // We don't add point because we already
            // have point in this position
            return;
        }
        points.emplace(pos, he);
    }

    hEntity findPoint(const Vector &p) {
        auto it = points.find(p);
        if(it == points.end()) return Entity::NO_ENTITY;
        return it->second;
    }

    hEntity createOrGetPoint(const Vector &p) {
        hEntity he = findPoint(p);
        if(he.v != Entity::NO_ENTITY.v) return he;

        hRequest hr = SS.GW.AddRequest(Request::DATUM_POINT, false);
        he = hr.entity(0);
        SK.GetEntity(he)->PointForceTo(p);
        points.emplace(p, he);
        return he;
    }

    hEntity createLine(Vector p0, Vector p1, uint32_t style, bool constrainHV = false) {
        if(p0.Equals(p1)) return Entity::NO_ENTITY;
        hRequest hr = SS.GW.AddRequest(Request::LINE_SEGMENT, false);
        SK.GetEntity(hr.entity(1))->PointForceTo(p0);
        SK.GetEntity(hr.entity(2))->PointForceTo(p1);
        processPoint(hr.entity(1));
        processPoint(hr.entity(2));

        if(constrainHV) {
            int cType = -1;
            if(fabs(p0.x - p1.x) < LENGTH_EPS) {
                cType = Constraint::VERTICAL;
            }
            else if(fabs(p0.y - p1.y) < LENGTH_EPS) {
                cType = Constraint::HORIZONTAL;
            }
            if(cType != -1) {
                Constraint::Constrain(
                    cType,
                    Entity::NO_ENTITY,
                    Entity::NO_ENTITY,
                    hr.entity(0)
                );
            }
        }

        if(style != 0) {
            Request *r = SK.GetRequest(hr);
            r->style = hStyle{ style };
        }
        return hr.entity(0);
    }

    hEntity createCircle(const Vector &c, double r, uint32_t style) {
        hRequest hr = SS.GW.AddRequest(Request::CIRCLE, false);
        SK.GetEntity(hr.entity(1))->PointForceTo(c);
        processPoint(hr.entity(1));
        SK.GetEntity(hr.entity(64))->DistanceForceTo(r);
        if(style != 0) {
            Request *r = SK.GetRequest(hr);
            r->style = hStyle{ style };
        }
        return hr.entity(0);
    }

    virtual void addLayer(const DRW_Layer &data) {
        layers.emplace(data.name, data);
    }

    virtual void addBlock(const DRW_Block &data) {
        readBlock = &blocks[data.name];
        readBlock->data = data;
    }

    virtual void endBlock() {
        readBlock = NULL;
    }

    virtual void addPoint(const DRW_Point &data) {
        if(data.space != DRW::ModelSpace) return;
        if(addPendingBlockEntity<DRW_Point>(data)) return;

        hRequest hr = SS.GW.AddRequest(Request::DATUM_POINT, false);
        SK.GetEntity(hr.entity(0))->PointForceTo(toVector(data.basePoint));
        processPoint(hr.entity(0));
    }

    virtual void addLine(const DRW_Line &data) {
        if(data.space != DRW::ModelSpace) return;
        if(addPendingBlockEntity<DRW_Line>(data)) return;

        createLine(toVector(data.basePoint), toVector(data.secPoint), styleFor(&data).v, true);
    }

    virtual void addArc(const DRW_Arc &data) {
        if(data.space != DRW::ModelSpace) return;
        if(addPendingBlockEntity<DRW_Arc>(data)) return;

        hRequest hr = SS.GW.AddRequest(Request::ARC_OF_CIRCLE, false);
        double r = data.radious;
        double sa = data.staangle;
        double ea = data.endangle;
        Vector c = Vector::From(data.basePoint.x, data.basePoint.y, 0.0);
        Vector rvs = Vector::From(r * cos(sa), r * sin(sa), data.basePoint.z).Plus(c);
        Vector rve = Vector::From(r * cos(ea), r * sin(ea), data.basePoint.z).Plus(c);

        if(data.extPoint.z == -1.0) {
            c.x = -c.x;
            rvs.x = - rvs.x;
            rve.x = - rve.x;
            std::swap(rvs, rve);
        }

        blockTransformArc(&c, &rvs, &rve);

        SK.GetEntity(hr.entity(1))->PointForceTo(c);
        SK.GetEntity(hr.entity(2))->PointForceTo(rvs);
        SK.GetEntity(hr.entity(3))->PointForceTo(rve);
        processPoint(hr.entity(1));
        processPoint(hr.entity(2));
        processPoint(hr.entity(3));
        setStyle(hr, styleFor(&data));
    }

    virtual void addCircle(const DRW_Circle &data) {
        if(data.space != DRW::ModelSpace) return;
        if(addPendingBlockEntity<DRW_Circle>(data)) return;

        createCircle(toVector(data.basePoint), data.radious, styleFor(&data).v);
    }

    virtual void addLWPolyline(const DRW_LWPolyline &data)  {
        if(data.space != DRW::ModelSpace) return;
        if(addPendingBlockEntity<DRW_LWPolyline>(data)) return;

        size_t vNum = data.vertlist.size();

        // Check for closed polyline.
        if((data.flags & 1) != 1) vNum--;

        // Correct coordinate system for the case where z=-1, as described in
        // http://paulbourke.net/dataformats/dxf/dxf10.html.
        bool needSwapX = data.extPoint.z == -1.0;

        for(size_t i = 0; i < vNum; i++) {
            DRW_Vertex2D c0 = *data.vertlist[i];
            DRW_Vertex2D c1 = *data.vertlist[(i + 1) % data.vertlist.size()];

            if(needSwapX) {
                c0.x = -c0.x;
                c1.x = -c1.x;
                c0.bulge = -c0.bulge;
            }

            Vector p0 = Vector::From(c0.x, c0.y, 0.0);
            Vector p1 = Vector::From(c1.x, c1.y, 0.0);
            hStyle hs = styleFor(&data);

            if(EXACT(data.vertlist[i]->bulge == 0.0)) {
                createLine(blockTransform(p0), blockTransform(p1), hs.v, true);
            } else {
                hRequest hr = createBulge(p0, p1, c0.bulge);
                setStyle(hr, hs);
            }
        }
    }

    virtual void addPolyline(const DRW_Polyline &data) {
        if(data.space != DRW::ModelSpace) return;
        if(addPendingBlockEntity<DRW_Polyline>(data)) return;

        int vNum = data.vertlist.size();

        // Check for closed polyline.
        if((data.flags & 1) != 1) vNum--;

        // Correct coordinate system for the case where z=-1, as described in
        // http://paulbourke.net/dataformats/dxf/dxf10.html.
        bool needSwapX = data.extPoint.z == -1.0;

        for(int i = 0; i < vNum; i++) {
            DRW_Coord c0 = data.vertlist[i]->basePoint;
            DRW_Coord c1 = data.vertlist[(i + 1) % data.vertlist.size()]->basePoint;

            double bulge = data.vertlist[i]->bulge;
            if(needSwapX) {
                c0.x = -c0.x;
                c1.x = -c1.x;
                bulge = -bulge;
            }

            Vector p0 = Vector::From(c0.x, c0.y, 0.0);
            Vector p1 = Vector::From(c1.x, c1.y, 0.0);
            hStyle hs = styleFor(&data);

            if(EXACT(bulge == 0.0)) {
                createLine(blockTransform(p0), blockTransform(p1), hs.v, true);
            } else {
                hRequest hr = createBulge(p0, p1, bulge);
                setStyle(hr, hs);
            }
        }
    }

    virtual void addSpline(const DRW_Spline *data) {
        if(data->space != DRW::ModelSpace) return;
        if(data->degree != 3) return;
        if(addPendingBlockEntity<DRW_Spline>(*data)) return;

        hRequest hr = SS.GW.AddRequest(Request::CUBIC, false);
        for(int i = 0; i < 4; i++) {
            SK.GetEntity(hr.entity(i + 1))->PointForceTo(toVector(*data->controllist[i]));
            processPoint(hr.entity(i + 1));
        }
        setStyle(hr, styleFor(data));
    }

    virtual void addInsert(const DRW_Insert &data) {
        if(data.space != DRW::ModelSpace) return;
        if(addPendingBlockEntity<DRW_Insert>(data)) return;

        auto bi = blocks.find(data.name);
        if(bi == blocks.end()) oops();
        Block *block = &bi->second;

        // Push transform.
        Vector x = blockX;
        Vector y = blockY;
        Vector t = blockT;

        const DRW_Insert *oldInsert = insertInsert;
        insertInsert = &data;

        if(data.extPoint.z == -1.0) invertXTransform();
        multBlockTransform(data.basePoint.x, data.basePoint.y, data.xscale, data.yscale, data.angle);
        for(auto &e : block->entities) {
            addEntity(&*e);
        }

        insertInsert = oldInsert;

        // Pop transform.
        blockX = x;
        blockY = y;
        blockT = t;
    }

    virtual void addMText(const DRW_MText &data) {
        if(data.space != DRW::ModelSpace) return;
        if(addPendingBlockEntity<DRW_MText>(data)) return;

        DRW_MText text = data;
        text.secPoint = text.basePoint;
        addText(text);
    }

    virtual void addText(const DRW_Text &data) {
        if(data.space != DRW::ModelSpace) return;
        if(addPendingBlockEntity<DRW_Text>(data)) return;

        Constraint c = {};
        c.group         = SS.GW.activeGroup;
        c.workplane     = SS.GW.ActiveWorkplane();
        c.type          = Constraint::COMMENT;
        if(data.alignH == DRW_Text::HLeft && data.alignV == DRW_Text::VBaseLine) {
            c.disp.offset   = toVector(data.basePoint);
        } else {
            c.disp.offset   = toVector(data.secPoint);
        }
        c.comment       = data.text;
        c.disp.style    = styleFor(&data);
        Constraint::AddConstraint(&c, false);
    }

    virtual void addDimAlign(const DRW_DimAligned *data) {
        if(data->space != DRW::ModelSpace) return;
        if(addPendingBlockEntity<DRW_DimAligned>(*data)) return;

        Vector p0 = toVector(data->getDef1Point());
        Vector p1 = toVector(data->getDef2Point());
        Vector p2 = toVector(data->getTextPoint());
        hConstraint hc = Constraint::Constrain(
            Constraint::PT_PT_DISTANCE,
            createOrGetPoint(p0),
            createOrGetPoint(p1),
            Entity::NO_ENTITY
        );

        Constraint *c = SK.GetConstraint(hc);
        if(data->hasActualMeasurement()) {
            c->valA = data->getActualMeasurement();
        } else {
            c->ModifyToSatisfy();
        }
        c->disp.offset = p2.Minus(p0.Plus(p1).ScaledBy(0.5));
    }

    virtual void addDimLinear(const DRW_DimLinear *data) {
        if(data->space != DRW::ModelSpace) return;
        if(addPendingBlockEntity<DRW_DimLinear>(*data)) return;

        Vector p0 = toVector(data->getDef1Point(), false);
        Vector p1 = toVector(data->getDef2Point(), false);
        Vector p2 = toVector(data->getTextPoint(), false);

        double angle = data->getAngle() * PI / 180.0;
        Vector dir = Vector::From(cos(angle), sin(angle), 0.0);
        Vector p3 = p1.Minus(p1.ClosestPointOnLine(p2, dir)).Plus(p1);
        if(p1.Minus(p3).Magnitude() < LENGTH_EPS) {
            p3 = p0.Minus(p0.ClosestPointOnLine(p2, dir)).Plus(p1);
        }

        Vector p4 = p0.ClosestPointOnLine(p1, p3.Minus(p1)).Plus(p0).ScaledBy(0.5);

        p0 = blockTransform(p0);
        p1 = blockTransform(p1);
        p2 = blockTransform(p2);
        p3 = blockTransform(p3);
        p4 = blockTransform(p4);

        hConstraint hc = Constraint::Constrain(
            Constraint::PT_LINE_DISTANCE,
            createOrGetPoint(p0),
            Entity::NO_ENTITY,
            createLine(p1, p3, invisibleStyle().v)
        );

        Constraint *c = SK.GetConstraint(hc);
        if(data->hasActualMeasurement()) {
            c->valA = data->getActualMeasurement();
        } else {
            c->ModifyToSatisfy();
        }
        c->disp.offset = p2.Minus(p4);
    }

    virtual void addDimAngular(const DRW_DimAngular *data) {
        if(data->space != DRW::ModelSpace) return;
        if(addPendingBlockEntity<DRW_DimAngular>(*data)) return;

        Vector l0p0 = toVector(data->getFirstLine1());
        Vector l0p1 = toVector(data->getFirstLine2());
        Vector l1p0 = toVector(data->getSecondLine1());
        Vector l1p1 = toVector(data->getSecondLine2());

        hConstraint hc = Constraint::Constrain(
            Constraint::ANGLE,
            Entity::NO_ENTITY,
            Entity::NO_ENTITY,
            createLine(l0p0, l0p1, invisibleStyle().v),
            createLine(l1p1, l1p0, invisibleStyle().v),
            /*other=*/false,
            /*other2=*/false
        );

        Constraint *c = SK.GetConstraint(hc);
        c->ModifyToSatisfy();
        if(data->hasActualMeasurement()) {
            double actual = data->getActualMeasurement() / PI * 180.0;
            if(fabs(180.0 - actual - c->valA) < fabs(actual - c->valA)) {
                c->other = true;
            }
            c->valA = actual;
        }

        bool skew = false;
        Vector pi = Vector::AtIntersectionOfLines(l0p0, l0p1, l1p0, l1p1, &skew);
        if(!skew) {
            c->disp.offset = toVector(data->getTextPoint()).Minus(pi);
        }
    }

    hConstraint createDiametric(Vector cp, double r, Vector tp, double actual, bool asRadius = false) {
        hEntity he = createCircle(cp, r, invisibleStyle().v);

        hConstraint hc = Constraint::Constrain(
            Constraint::DIAMETER,
            Entity::NO_ENTITY,
            Entity::NO_ENTITY,
            he
        );

        Constraint *c = SK.GetConstraint(hc);
        if(actual > 0.0) {
            c->valA = asRadius ? actual * 2.0 : actual;
        } else {
            c->ModifyToSatisfy();
        }
        c->disp.offset = tp.Minus(cp);
        if(asRadius) c->other = true;
        return hc;
    }

    virtual void addDimRadial(const DRW_DimRadial *data) {
        if(data->space != DRW::ModelSpace) return;
        if(addPendingBlockEntity<DRW_DimRadial>(*data)) return;

        Vector cp = toVector(data->getCenterPoint());
        Vector dp = toVector(data->getDiameterPoint());
        Vector tp = toVector(data->getTextPoint());
        double actual = -1.0;
        if(data->hasActualMeasurement()) {
            actual = data->getActualMeasurement();
        }

        createDiametric(cp, cp.Minus(dp).Magnitude(), tp, actual, /*asRadius=*/true);
    }

    virtual void addDimDiametric(const DRW_DimDiametric *data) {
        if(data->space != DRW::ModelSpace) return;
        if(addPendingBlockEntity<DRW_DimRadial>(*data)) return;

        Vector dp1 = toVector(data->getDiameter1Point());
        Vector dp2 = toVector(data->getDiameter2Point());

        Vector cp = dp1.Plus(dp2).ScaledBy(0.5);
        Vector tp = toVector(data->getTextPoint());
        double actual = -1.0;
        if(data->hasActualMeasurement()) {
            actual = data->getActualMeasurement();
        }

        createDiametric(cp, cp.Minus(dp1).Magnitude(), tp, actual, /*asRadius=*/false);
    }

    virtual void addDimAngular3P(const DRW_DimAngular3p *data) {
        if(data->space != DRW::ModelSpace) return;
        if(addPendingBlockEntity<DRW_DimAngular3p>(*data)) return;

        DRW_DimAngular dim = *static_cast<const DRW_Dimension *>(data);
        dim.setFirstLine1(data->getVertexPoint());
        dim.setFirstLine2(data->getFirstLine());
        dim.setSecondLine1(data->getVertexPoint());
        dim.setSecondLine2(data->getSecondLine());
        addDimAngular(&dim);
    }
};

void ImportDxf(const std::string &filename) {
    DxfReadInterface interface;
    interface.clearBlockTransform();

    std::string data;
    if(!ReadFile(filename, &data)) {
        Error("Couldn't read from '%s'", filename.c_str());
        return;
    }

    SS.UndoRemember();
    std::stringstream stream(data);
    if(!dxfRW().read(stream, &interface, /*ext=*/false)) {
        Error("Corrupted DXF file.");
    }

    if(interface.unknownEntities > 0) {
        Message(ssprintf("%u DXF entities of unknown type were ignored.",
                         interface.unknownEntities).c_str());
    }
}

void ImportDwg(const std::string &filename) {
    DxfReadInterface interface;
    interface.clearBlockTransform();

    std::string data;
    if(!ReadFile(filename, &data)) {
        Error("Couldn't read from '%s'", filename.c_str());
        return;
    }

    SS.UndoRemember();
    std::stringstream stream(data);
    if(!dwgR().read(stream, &interface, /*ext=*/false)) {
        Error("Corrupted DWG file.");
    }

    if(interface.unknownEntities > 0) {
        Message(ssprintf("%u DWG entities of unknown type were ignored.",
                         interface.unknownEntities).c_str());
    }
}

}
