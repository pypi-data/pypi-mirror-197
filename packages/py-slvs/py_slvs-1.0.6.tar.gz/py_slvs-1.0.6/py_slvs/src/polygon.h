//-----------------------------------------------------------------------------
// Anything relating to plane polygons and triangles, and (generally, non-
// planar) meshes thereof.
//
// Copyright 2008-2013 Jonathan Westhues.
//-----------------------------------------------------------------------------

#ifndef __POLYGON_H
#define __POLYGON_H

class SPointList;
class SPolygon;
class SContour;
class SMesh;
class SBsp3;
class SOutlineList;

class SEdge {
public:
    int    tag;
    int    auxA, auxB;
    Vector a, b;

    static SEdge From(Vector a, Vector b);
    bool EdgeCrosses(Vector a, Vector b, Vector *pi=NULL, SPointList *spl=NULL);
};

class SEdgeList {
public:
    List<SEdge>     l;

    void Clear(void);
    void AddEdge(Vector a, Vector b, int auxA=0, int auxB=0);
    bool AssemblePolygon(SPolygon *dest, SEdge *errorAt, bool keepDir=false);
    bool AssembleContour(Vector first, Vector last, SContour *dest,
                            SEdge *errorAt, bool keepDir);
    int AnyEdgeCrossings(Vector a, Vector b,
        Vector *pi=NULL, SPointList *spl=NULL);
    bool ContainsEdgeFrom(SEdgeList *sel);
    bool ContainsEdge(SEdge *se);
    void CullExtraneousEdges(void);
    void MergeCollinearSegments(Vector a, Vector b);
};

// A kd-tree element needs to go on a side of a node if it's when KDTREE_EPS
// of the boundary. So increasing this number never breaks anything, but may
// result in more duplicated elements. So it's conservative to be sloppy here.
#define KDTREE_EPS (20*LENGTH_EPS)

class SEdgeLl {
public:
    SEdge       *se;
    SEdgeLl     *next;

    static SEdgeLl *Alloc(void);
};

class SKdNodeEdges {
public:
    int which; // whether c is x, y, or z
    double c;
    SKdNodeEdges    *gt;
    SKdNodeEdges    *lt;

    SEdgeLl         *edges;

    static SKdNodeEdges *From(SEdgeList *sel);
    static SKdNodeEdges *From(SEdgeLl *sell);
    static SKdNodeEdges *Alloc(void);
    int AnyEdgeCrossings(Vector a, Vector b, int cnt,
        Vector *pi=NULL, SPointList *spl=NULL);
};

class SPoint {
public:
    int     tag;

    enum {
        UNKNOWN = 0,
        NOT_EAR = 1,
        EAR     = 2
    };
    int     ear;

    Vector  p;
    Vector  auxv;
};

class SPointList {
public:
    List<SPoint>    l;

    void Clear(void);
    bool ContainsPoint(Vector pt);
    int IndexForPoint(Vector pt);
    void IncrementTagFor(Vector pt);
    void Add(Vector pt);
};

class SContour {
public:
    int             tag;
    int             timesEnclosed;
    Vector          xminPt;
    List<SPoint>    l;

    void AddPoint(Vector p);
    void MakeEdgesInto(SEdgeList *el);
    void Reverse(void);
    Vector ComputeNormal(void);
    double SignedAreaProjdToNormal(Vector n);
    bool IsClockwiseProjdToNormal(Vector n);
    bool ContainsPointProjdToNormal(Vector n, Vector p);
    void OffsetInto(SContour *dest, double r);
    void CopyInto(SContour *dest);
    void FindPointWithMinX(void);
    Vector AnyEdgeMidpoint(void);

    bool IsEar(int bp, double scaledEps);
    bool BridgeToContour(SContour *sc, SEdgeList *el, List<Vector> *vl);
    void ClipEarInto(SMesh *m, int bp, double scaledEps);
    void UvTriangulateInto(SMesh *m, SSurface *srf);
};

typedef struct {
    uint32_t face;
    RgbaColor color;
} STriMeta;

class SPolygon {
public:
    List<SContour>  l;
    Vector          normal;

    Vector ComputeNormal(void);
    void AddEmptyContour(void);
    int WindingNumberForPoint(Vector p);
    double SignedArea(void);
    bool ContainsPoint(Vector p);
    void MakeEdgesInto(SEdgeList *el);
    void FixContourDirections(void);
    void Clear(void);
    bool SelfIntersecting(Vector *intersectsAt);
    bool IsEmpty(void);
    Vector AnyPoint(void);
    void OffsetInto(SPolygon *dest, double r);
    void UvTriangulateInto(SMesh *m, SSurface *srf);
    void UvGridTriangulateInto(SMesh *m, SSurface *srf);
};

class STriangle {
public:
    int         tag;
    STriMeta    meta;
    Vector      a, b, c;
    Vector      an, bn, cn;

    static STriangle From(STriMeta meta, Vector a, Vector b, Vector c);
    Vector Normal(void);
    void FlipNormal(void);
    double MinAltitude(void);
    int WindingNumberForPoint(Vector p);
    bool ContainsPoint(Vector p);
    bool ContainsPointProjd(Vector n, Vector p);
};

class SBsp2 {
public:
    Vector      np;     // normal to the plane

    Vector      no;     // outer normal to the edge
    double      d;
    SEdge       edge;

    SBsp2       *pos;
    SBsp2       *neg;

    SBsp2       *more;

    enum { POS = 100, NEG = 101, COPLANAR = 200 };
    void InsertTriangleHow(int how, STriangle *tr, SMesh *m, SBsp3 *bsp3);
    void InsertTriangle(STriangle *tr, SMesh *m, SBsp3 *bsp3);
    Vector IntersectionWith(Vector a, Vector b);
    void InsertEdge(SEdge *nedge, Vector nnp, Vector out);
    static SBsp2 *InsertOrCreateEdge(SBsp2 *where, SEdge *nedge, Vector nnp, Vector out);
    static SBsp2 *Alloc(void);

    void DebugDraw(Vector n, double d);
};

class SBsp3 {
public:
    Vector      n;
    double      d;

    STriangle   tri;
    SBsp3       *pos;
    SBsp3       *neg;

    SBsp3       *more;

    SBsp2       *edges;

    static SBsp3 *Alloc(void);
    static SBsp3 *FromMesh(SMesh *m);

    Vector IntersectionWith(Vector a, Vector b);

    enum { POS = 100, NEG = 101, COPLANAR = 200 };
    void InsertHow(int how, STriangle *str, SMesh *instead);
    void Insert(STriangle *str, SMesh *instead);
    static SBsp3 *InsertOrCreate(SBsp3 *where, STriangle *str, SMesh *instead);

    void InsertConvexHow(int how, STriMeta meta, Vector *vertex, int n,
                                SMesh *instead);
    SBsp3 *InsertConvex(STriMeta meta, Vector *vertex, int n, SMesh *instead);

    void InsertInPlane(bool pos2, STriangle *tr, SMesh *m);

    void GenerateInPaintOrder(SMesh *m);

    void DebugDraw(void);
};

class SMesh {
public:
    List<STriangle>     l;

    bool    flipNormal;
    bool    keepCoplanar;
    bool    atLeastOneDiscarded;
    bool    isTransparent;

    void Clear(void);
    void AddTriangle(STriangle *st);
    void AddTriangle(STriMeta meta, Vector a, Vector b, Vector c);
    void AddTriangle(STriMeta meta, Vector n, Vector a, Vector b, Vector c);
    void DoBounding(Vector v, Vector *vmax, Vector *vmin);
    void GetBounding(Vector *vmax, Vector *vmin);

    void Simplify(int start);

    void AddAgainstBsp(SMesh *srcm, SBsp3 *bsp3);
    void MakeFromUnionOf(SMesh *a, SMesh *b);
    void MakeFromDifferenceOf(SMesh *a, SMesh *b);

    void MakeFromCopyOf(SMesh *a);
    void MakeFromTransformationOf(SMesh *a,
                                    Vector trans, Quaternion q, double scale);
    void MakeFromAssemblyOf(SMesh *a, SMesh *b);

    void MakeEdgesInPlaneInto(SEdgeList *sel, Vector n, double d);
    void MakeCertainEdgesAndOutlinesInto(SEdgeList *sel, SOutlineList *sol, int type);

    bool IsEmpty(void);
    void RemapFaces(Group *g, int remap);

    uint32_t FirstIntersectionWith(Point2d mp);
};

// A linked list of triangles
class STriangleLl {
public:
    STriangle       *tri;

    STriangleLl     *next;

    static STriangleLl *Alloc(void);
};

class SOutline {
public:
    int    tag;
    Vector a, b, nl, nr;
};

class SOutlineList {
public:
    List<SOutline> l;

    void Clear();
    void AddEdge(Vector a, Vector b, Vector nl, Vector nr);

    void MakeFromCopyOf(SOutlineList *ol);

    void FillOutlineTags(Vector projDir);
};

class SKdNode {
public:
    struct EdgeOnInfo {
        int        count;
        bool       frontFacing;
        bool       intersectsMesh;
        STriangle *tr;
        int        ai;
        int        bi;
    };

    int which;  // whether c is x, y, or z
    double c;

    SKdNode      *gt;
    SKdNode      *lt;

    STriangleLl  *tris;

    static SKdNode *Alloc(void);
    static SKdNode *From(SMesh *m);
    static SKdNode *From(STriangleLl *tll);

    void AddTriangle(STriangle *tr);
    void MakeMeshInto(SMesh *m);
    void ListTrianglesInto(std::vector<STriangle *> *tl);
    void ClearTags(void);

    void FindEdgeOn(Vector a, Vector b, int cnt, bool coplanarIsInter, EdgeOnInfo *info);
    enum {
        NAKED_OR_SELF_INTER_EDGES  = 100,
        SELF_INTER_EDGES           = 200,
        TURNING_EDGES              = 300,
        EMPHASIZED_EDGES           = 400,
        SHARP_EDGES                = 500,
    };
    void MakeCertainEdgesInto(SEdgeList *sel, int how, bool coplanarIsInter,
                              bool *inter, bool *leaky, int auxA=0);
    void MakeOutlinesInto(SOutlineList *sel);

    void OcclusionTestLine(SEdge orig, SEdgeList *sel, int cnt, bool removeHidden);
    void SplitLinesAgainstTriangle(SEdgeList *sel, STriangle *tr, bool removeHidden);

    void SnapToMesh(SMesh *m);
    void SnapToVertex(Vector v, SMesh *extras);
};

#endif

