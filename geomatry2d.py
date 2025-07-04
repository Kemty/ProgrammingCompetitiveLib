from functools import cmp_to_key
from math import atan2, cos, sin, acos, asin, sqrt, degrees, pi
inf = float('inf')

EPS = 1e-10
def sgn(a):
    return -1 if a < -EPS else (1 if a > EPS else 0)

class Point:
    def __init__(self, *point) -> None:
        if len(point) == 0:
            self.x = 0
            self.y = 0
        elif len(point) == 1:
            self.x = point[0][0]
            self.y = point[0][1]
        else:
            self.x = point[0]
            self.y = point[1]
    def __getitem__(self, i):
        if i == 0: return self.x
        elif i == 1: return self.y
        raise IndexError
    def __setitem__(self, i, value):
        if i == 0: self.x = value
        elif i == 1: self.y = value
        raise IndexError
    def __neg__(self):
        return Point(-self.x, -self.y)
    def __add__(self, other):
        return Point(self.x+other.x, self.y+other.y)
    def __sub__(self, other):
        return Point(self.x-other.x, self.y-other.y)
    def __mul__(self, other):
        if type(other) is Point: # 複素数としての積
            return Point(self.x*other.x - self.y*other.y, self.x*other.y + self.y*other.x)
        return Point(self.x*other, self.y*other) # スカラー倍
    def __rmul__(self, other):
        if type(other) is Point: # 複素数としての積
            return Point(other.x*self.x - other.y*self.y, other.x*self.y + other.y*self.x)
        return Point(self.x*other, self.y*other) # スカラー倍
    def __truediv__(self, other):
        if type(other) is Point: # 複素数としての除算
            return self*other.conjugation()/other.length_sq()
        return Point(self.x/other, self.y/other) # スカラー除算
    def __floordiv__(self, other):
        if type(other) is Point: # 複素数としての除算、otherのノルムで割らない
            return self*other.conjugation()
        return Point(self.x//other, self.y//other) # スカラー除算
    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self
    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self
    def __imul__(self, other):
        if type(other) is Point: # 複素数としての積
            a, b, c, d = self.x, self.y, other.x, other.y
            self.x = a*c - b*d
            self.y = a*d + b*c
        else: # スカラー倍
            self.x *= other
            self.y *= other
        return self
    def __itruediv__(self, other):
        if type(other) is Point: # 複素数としての除算
            self *= other.conjugation()/other.length_sq()
        else: # スカラー除算
            self.x /= other
            self.y /= other
        return self
    def __ifloordiv__(self, other):
        if type(other) is Point: # 複素数としての除算、otherのノルム^2で割らない
            self *= other.conjugation()
        else: # スカラー除算
            self.x //= other
            self.y //= other
        return self
    def __eq__(self, other) -> bool:
        return sgn(self.x-other.x) == sgn(self.y-other.y) == 0
    def __lt__(self, other) -> bool:
        if sgn(self.x-other.x) != 0:
            return sgn(self.x-other.x) < 0
        return sgn(self.y-other.y) < 0
    def __repr__(self) -> str:
        return (self.x, self.y).__repr__()
    def __abs__(self):
        return self.length()
    
    def length_sq(self):
        return self.x*self.x + self.y*self.y
    def length(self):
        return sqrt(self.length_sq())
    def dot(self, other):
        return self.x*other.x + self.y*other.y
    def cross(self, other):
        return self.x*other.y - self.y*other.x
    def is_zero(self):
        return sgn(self.x) == sgn(self.y) == 0
    def normalized(self):
        return self/self.length()
    def normal_vector(self):
        return Point(-self.y, self.x)
    def normal_unit_vector(self):
        tmp = self.normalized()
        return Point(-tmp.y, tmp.x)
    def rotate(self, arg):
        cs = cos(arg); sn = sin(arg)
        return Point(self.x*cs - self.y*sn, self.x*sn + self.y*cs)
    def angle(self):
        return atan2(self.y, self.x)
    def is_same_angle(self, other): # selfとotherの偏角は等しいか
        return Point.ccw(Point(), self, other) in (0, 2)
    def is_same_slope(self, other): # selfとotherの((0, 0)と結んだ直線での)傾きは等しいか
        return sgn(self.cross(other)) == 0
    def conjugation(self): # 共役な複素数
        return Point(self.x, -self.y)
    def print(self):
        print(f"{self.x: .9f} {self.y: .9f}")

    def distance_from_Point_sq(self, other):
        if type(other) is not Point:
            raise ValueError
        return (self.x-other.x)*(self.x-other.x) + (self.y-other.y)*(self.y-other.y)
    def distance_from_Point(self, other):
        if type(other) is not Point:
            raise ValueError
        return sqrt(self.distance_from_Point_sq(other))
    def distance_from_Line(self, other):
        if type(other) is not Line:
            raise ValueError
        return abs(other.vec().cross(self-other.begin))/other.vec().length()
    def distance_from_Ray(self, other):
        if type(other) is not Ray:
            raise ValueError
        if Point.angle_type(self, other.begin, other.end) == 2:
            return self.distance_from_Point(other.begin)
        return abs(other.vec().cross(self-other.begin))/other.vec().length()
    def distance_from_Segment(self, other):
        if type(other) is not Segment:
            raise ValueError
        if Point.angle_type(self, other.begin, other.end) == 2:
            return self.distance_from_Point(other.begin)
        if Point.angle_type(self, other.end, other.begin) == 2:
            return self.distance_from_Point(other.end)
        return abs(other.vec().cross(self-other.begin))/other.vec().length()
    def projection(self, line):
        return line.begin+line.vec().normalized()*(self-line.begin).dot(line.vec())/line.vec().length()
    def reflection(self, line):
        return self+2*(self.projection(line)-self)

	# 3点A, B, Cの位置関係を返す関数 A, Bがすべて異なった点であるのが前提
	# ABから見てBCは左に曲がるのなら +1
	# ABから見てBCは右に曲がるのなら -1
	# ABC(CBA)の順番で一直線上に並ぶなら +2
	# ACB(BCA)の順番で一直線上に並ぶなら 0
	# BAC(CAB)の順番で一直線上に並ぶなら -2
    # a ≠ b を仮定(a = b ならValueError)
    def ccw(a, b, c):
        if a == b:
            return ValueError
        flg = sgn((b-a).cross(c-a))
        if flg == 1:
            return 1
        elif flg == -1:
            return -1
        # ABC(CBA)
        if sgn((b-a).dot(c-b)) > 0:
            return 2
        # BAC(CAB)
        elif (sgn((a-b).dot(c-a)) > 0):
            return -2
        # ACB(BCA) または cがa, bいずれかと一致
        return 0
    
    # 角ABCが鋭角なら0、直角なら1、鈍角なら2を返す。
    # cc: ABから反時計回りに見るBCの偏角(0 ≤ Θ ≤ 2π)で考え、π < Θ < 2πなら3を返す。
    def angle_type(a, b, c, cc=True):
        if cc and sgn((a-b).cross(c-b)) < 0:
            return 3
        v = (a-b).dot(c-b)
        if sgn(v) > 0:
            return 0
        elif sgn(v) == 0:
            return 1
        return 2

# Line, Ray, Segment は相互にキャスト可能
# ただし、Rayにキャストする際は向きに注意
class Line:
    begin = None
    end = None
    def __init__(self, *args) -> None:
        # args: begin, end
        # begin = end なら ValueError
        if len(args) == 2:
            self.begin = Point(args[0])
            self.end = Point(args[1])
        # args: a, b, c (ax+by+c = 0)
        # a = b = 0 なら ValueError
        elif len(args) == 3:
            a, b, c = args
            if sgn(a) == sgn(b) == 0:
                raise ValueError
            if sgn(b) == 0:
                self.begin = Point(-c/a, 0)
                self.end = Point(-c/a, 1)
            else:
                self.begin = Point(0, -c/b)
                self.end = Point(1, -(a+c)/b)
        elif len(args) == 1 and isinstance(args[0], Line):
            self.begin = Point(args[0].begin)
            self.end = Point(args[0].end)
        if self.begin == self.end:
            raise ValueError
    def __eq__(self, other): # 同一の直線か
        if type(other) is not Line:
            return False
        return self.is_parallel(other) and self.is_intersect_with_Point(other.begin)
    def __repr__(self) -> str:
        return f"{type(self)}({self.begin}, {self.end})"
    def vec(self):
        return self.end-self.begin
    def rvec(self):
        return self.begin-self.end
    def is_orthogonal(self, other):
        if not isinstance(other, Line):
            raise ValueError
        return sgn(self.vec().dot(other.vec())) == 0
    def is_parallel(self, other):
        if not isinstance(other, Line):
            raise ValueError
        return self.vec().is_same_slope(other.vec())
    
    def is_intersect_with_Point(self, other) -> bool:
        if type(other) is not Point:
            raise ValueError
        return Point.ccw(self.begin, self.end, other) in (-2, 0, 2)
    def is_intersect_with_Line(self, other) -> bool:
        if type(other) is not Line:
            raise ValueError
        return not (self.is_parallel(other) and not self.is_intersect_with_Point(other.begin))
    def is_intersect_with_Ray(self, other) -> bool:
        if type(other) is not Ray:
            return ValueError
        c = Point.ccw(self.begin, self.end, other.begin)
        if c in (-2, 0, 2): return True
        elif c == 1:
            return Point.ccw(other.begin, other.begin+self.vec(), other.end) == -1
        else:
            return Point.ccw(other.begin, other.begin+self.vec(), other.end) == 1
    def is_intersect_with_Segment(self, other) -> bool:
        if type(other) is not Segment:
            return ValueError
        return sgn(self.vec().cross(other.begin-self.begin))*sgn(self.vec().cross(other.end-self.begin)) <= 0
    
    def intersection_with_Line(self, other):
        if type(other) is not Line:
            raise ValueError
        if not self.is_intersect_with_Line(other):
            return None
        if self == other:
            return Line(self)
        return Point(self.begin+self.vec()*(other.end-self.begin).cross(other.vec())/self.vec().cross(other.vec()))
    def intersection_with_Ray(self, other):
        if type(other) is not Ray:
            raise ValueError
        if not self.is_intersect_with_Ray(other):
            return None
        if self == Line(other):
            return Ray(other)
        return self.intersection_with_Line(Line(other))
    def intersection_with_Segment(self, other):
        if type(other) is not Segment:
            raise ValueError
        if not self.is_intersect_with_Segment(other):
            return None
        if self == Line(other):
            return Segment(other)
        return self.intersection_with_Line(Line(other))
    
    def distance_from_Point(self, other):
        if type(other) is not Point:
            raise ValueError
        return other.distance_from_Line(self)
    def distance_from_Line(self, other):
        if type(other) is not Line:
            raise ValueError
        if self.is_intersect_with_Line(other):
            return 0
        return self.begin.distance_from_Line(other)
    def distance_from_Ray(self, other):
        if type(other) is not Ray:
            raise ValueError
        if self.is_intersect_with_Ray(other):
            return 0
        return other.begin.distance_from_Line(self)
    def distance_from_segment(self, other):
        if type(other) is not Segment:
            raise ValueError
        if self.is_intersect_with_Line:
            return 0
        return min(other.begin.distance_from_Line(self), other.end.distance_from_Line(self))

class Ray(Line):
    def __init__(self, *args) -> None:
        super().__init__(*args)
    def __eq__(self, other) -> bool:
        if type(other) is not Ray:
            return False
        return sgn(self.begin-other.begin) == 0 and self.vec().is_same_angle(other.vec())
    def reverse(self):
        self.begin, self.end = self.end, self.begin
    def reversed(ray):
        return Ray(ray.end, ray.begin)
    
    def is_intersect_with_Point(self, other) -> bool:
        if type(other) is not Point:
            raise ValueError
        return Point.ccw(self.begin, self.end, other) in (0, 2)
    def is_intersect_with_Line(self, other) -> bool:
        if type(other) is not Line:
            raise ValueError
        return other.is_intersect_with_Ray(self)
    def is_intersect_with_Ray(self, other) -> bool:
        if type(other) is not Ray:
            raise ValueError
        if not Line(self).is_intersect_with_Ray(other):
            return False
        if Point.ccw(self.begin, self.end, other.begin) in (0, 2) or Point.ccw(self.begin, self.end, other.end) in (0, 2):
            return True
        if sgn(self.vec().cross(other.begin-self.begin)) > 0:
            return sgn(other.vec().cross(self.begin-other.begin)) <= 0
        if sgn(self.vec().cross(other.begin-self.begin)) < 0:
            return sgn(other.vec().cross(self.begin-other.begin)) >= 0
        return False
    def is_intersect_with_Segment(self, other) -> bool:
        if type(other) is not Segment:
            raise ValueError
        return self.is_intersect_with_Ray(Ray(other.begin, other.end)) and self.is_intersect_with_Ray(Ray(other.end, other.begin))

    def intersection_with_Line(self, other):
        return other.intersection_with_Ray(self)
    def intersection_with_Ray(self, other):
        if type(other) is not Ray:
            raise ValueError
        if not self.is_intersect_with_Ray(other):
            return None
        c = Point.ccw(self.begin, self.end, other.begin)
        if c in (0, 2):
            if self.vec().is_same_angle(other.vec()):
                return Ray(other)
            if self.vec().is_same_slope(other.vec()):
                if self.begin == other.end:
                    return Point(self.begin)
                return Segment(self.begin, other.end)
            return Point(other.begin)
        if c == -2 and self.is_parallel(other):
            return Ray(self)
        return super().intersection_with_Ray(other)
    def intersection_with_Segment(self, other):
        if type(other) is not Segment:
            raise ValueError
        if not self.is_intersect_with_Segment(other):
            return None
        if self.is_parallel(other):
            if Point.ccw(self.begin, self.end, other.begin) == -2:
                return Segment(self.begin, other.end)
            if Point.ccw(self.begin, self.end, other.end) == -2:
                return Segment(self.begin, other.begin)
        return super().intersection_with_Segment(other)
    
    def distance_from_Point(self, other):
        if type(other) is not Point:
            raise ValueError
        return other.distance_from_Ray(self)
    def distance_from_Line(self, other):
        if type(other) is not Line:
            raise ValueError
        return other.distance_from_Ray(self)
    def distance_from_Ray(self, other):
        if type(other) is not Ray:
            raise ValueError
        if self.is_intersect_with_Ray(other):
            return 0
        return min(self.begin.distance_from_Ray(other), other.begin.distance_from_Ray(self))
    def distance_from_segment(self, other):
        if type(other) is not Segment:
            raise ValueError
        if self.is_intersect_with_Segment(other):
            return 0
        return min(self.begin.distance_from_Segment(other), other.begin.distance_from_Ray(self), other.end.distance_from_Ray(self))

class Segment(Line):
    def __init__(self, *args) -> None:
        super().__init__(*args)
    def __eq__(self, other) -> bool:
        if type(other) is not Segment:
            return False
        return (self.begin == other.begin and self.end == other.end) or (self.begin == other.end and self.end == other.begin)
    def length_sq(self):
        return self.vec().length_sq()
    def length(self):
        return self.vec().length()
    
    def is_intersect_with_Point(self, other) -> bool:
        if type(other) is not Point:
            return ValueError
        return Point.ccw(self.begin, self.end, other) == 0
    def is_intersect_with_Line(self, other) -> bool:
        if type(other) is not Line:
            return ValueError
        return other.is_intersect_with_Segment(self)
    def is_intersect_with_Ray(self, other) -> bool:
        if type(other) is not Ray:
            return ValueError
        return other.is_intersect_with_Segment(self)
    def is_intersect_with_Segment(self, other) -> bool:
        if type(other) is not Segment:
            return ValueError
        ray = Ray(self)
        return ray.is_intersect_with_Segment(other) and Ray.reversed(ray).is_intersect_with_Segment(other)
    
    def intersection_with_Line(self, other):
        if type(other) is not Line:
            raise ValueError
        return other.intersection_with_Segment(self)
    def intersection_with_Ray(self, other):
        if type(other) is not Ray:
            raise ValueError
        return other.intersection_with_Ray(self)
    def intersection_with_Segment(self, other):
        if type(other) is not Segment:
            raise ValueError
        if not self.is_intersect_with_Segment(other):
            return None
        if not self.is_parallel(other):
            return super().intersection_with_Segment(other)
        cb = Point.ccw(self.begin, self.end, other.begin)
        ce = Point.ccw(self.begin, self.end, other.end)
        if cb == 0:
            if ce == 0:
                return Segment(other)
            if ce == -2:
                if other.begin == self.begin:
                    return Point(other.begin)
                return Segment(self.begin, other.begin)
            if ce == 2:
                if other.begin == self.end:
                    return Point(other.begin)
                return Segment(self.end, other.begin)
        if ce == 0:
            if cb == -2:
                if other.end == self.begin:
                    return Point(other.end)
                return Segment(self.begin, other.end)
            if cb == 2:
                if other.end == self.end:
                    return Point(other.end)
                return Segment(self.end, other.end)
        return Segment(self)
    
    def distance_from_Point(self, other):
        if type(other) is not Point:
            raise ValueError
        return other.distance_from_Segment(self)
    def distance_from_Line(self, other):
        if type(other) is not Line:
            raise ValueError
        return other.distance_from_Segment(self)
    def distance_from_Ray(self, other):
        if type(other) is not Ray:
            raise ValueError
        return other.distance_from_Segment(self)
    def distance_from_Segment(self, other):
        if type(other) is not Segment:
            raise ValueError
        if self.is_intersect_with_Segment(other):
            return 0
        return min(self.distance_from_Point(other.begin), self.distance_from_Point(other.end),
                   other.distance_from_Point(self.begin), other.distance_from_Point(self.end))

class Polygon:
    def __init__(self, points) -> None:
        self.points = [Point(p) for p in points]
        if len(points) < 3:
            return ValueError
    def __getitem__(self, i):
        return self.points[i]
    def __setitem__(self, i, x):
        self.points[i] = Point(x)
    def __iter__(self):
        i = 0
        for i in range(len(self.points)):
            yield self.points[i]
    def __len__(self):
        return len(self.points)
    def __repr__(self) -> str:
        return f"{type(self)}({self.points})"
    def area(self):
        ret = 0
        for i in range(len(self.points)-1):
            ret += self.points[i].cross(self.points[i+1])
        ret += self.points[-1].cross(self.points[0])
        return ret/2
    def is_convex(self):
        size = len(self.points)
        for i in range(size):
            if Point.ccw(self.points[i-1], self.points[i], self.points[(i+1)%size]) == -1:
                return False
        return True
    
    # 内部なら2, 境界上なら1, 外部なら0
    def is_contain_Point(self, other):
        if type(other) is not Point:
            raise ValueError
        ray = Ray(Point(), Point((1, 0)))
        ret = 0
        for i in range(len(self.points)):
            a, b = self.points[i]-other, self.points[(i+1)%len(self.points)]-other
            if Point.ccw(a, b, Point()) == 0:
                return 1
            if not ray.is_intersect_with_Segment(Segment(a, b)):
                continue
            if sgn(a.y-b.y) < 0:
                ret ^= (sgn(b.y) != 0)
            if sgn(a.y-b.y) > 0:
                ret ^= (sgn(a.y) != 0)
        return 2 if ret else 0

class Convex(Polygon):
    def __init__(self, points) -> None:
        super().__init__(points)
        # if not self.is_convex(): # 安全性を考慮するならやるべき
        #     raise ValueError
    def convex_full(points, on_line=True):
        if type(points[0]) is not Point:
            Points.cast_to_Point(points)
        sp = sorted(points)
        ret = [sp[0], sp[1]]
        if on_line:
            for i in range(2, len(sp)):
                while len(ret) >= 2 and Point.ccw(ret[-2], ret[-1], sp[i]) < 0:
                    ret.pop()
                ret.append(sp[i])
            t = len(ret)+1
            for i in range(len(sp)-2, -1, -1):
                while len(ret) >= t and Point.ccw(ret[-2], ret[-1], sp[i]) < 0:
                    ret.pop()
                ret.append(sp[i])
        else:
            for i in range(2, len(sp)):
                while len(ret) >= 2 and Point.ccw(ret[-2], ret[-1], sp[i]) <= 0:
                    ret.pop()
                ret.append(sp[i])
            t = len(ret)+1
            for i in range(len(sp)-2, -1, -1):
                while len(ret) >= t and Point.ccw(ret[-2], ret[-1], sp[i]) <= 0:
                    ret.pop()
                ret.append(sp[i])
        ret.pop()
        return Convex(ret)
    def cut(self, line):
        if not isinstance(line, Line):
            raise ValueError
        points = self.points
        l = None
        r = None
        for i in range(len(points)):
            c = Point.ccw(line.begin, line.end, points[i])
            if c == 1:
                l = i
            elif c == -1:
                r = i
        if r is None:
            return Convex(self), None
        if l is None:
            return None, Convex(self)
        left = [points[l]]
        right = []
        i = (l+1)%len(points)
        t = 0
        for _ in range(len(points)-1):
            p = line.intersection_with_Segment(Segment(points[i], points[(i-1)%len(points)]))
            if p is None or p == points[(i-1)%len(points)]:
                if t == 0:
                    left.append(points[i])
                else:
                    right.append(points[i])
            else:
                if t == 0:
                    left.append(p)
                    right.append(p)
                    if p != points[i]:
                        right.append(points[i])
                    t ^= 1
                else:
                    right.append(p)
                    left.append(p)
                    if p != points[i]:
                        left.append(points[i])
                    t ^= 1
            i = (i+1)%len(points)
        if t:
            p = line.intersection_with_Segment(Segment(points[i], points[(i-1)%len(points)]))
            right.append(p)
            left.append(p)
        return Convex(left), Convex(right)
    def common_with_Convex(self, other):
        if type(other) is not Convex:
            raise ValueError
        ret = Convex(other)
        for i in range(len(self.points)):
            line = Line(self.points[i], self.points[(i+1)%len(self.points)])
            ret = ret.cut(line)[0]
            if ret is None:
                return None
        return ret
    def common_area_with_Convex(self, other):
        if type(other) is not Convex:
            raise ValueError
        c = self.common_with_Convex(other)
        if c is None:
            return 0
        return c.area()

    # 内部なら2, 境界上なら1, 外部なら0
    def is_contain_Point(self, other):
        if type(other) is not Point:
            raise ValueError
        if len(self.points) == 3:
            for i in range(len(self.points)):
                a, b = self.points[i], self.points[(i+1)%len(self.points)]
                c = Point.ccw(a, b, other)
                if c == 0:
                    return 1
                if c < 0:
                    return 0
            return 2
        ok, ng = 0, len(self.points)-1
        while(abs(ok-ng)>1):
            mid = (ok+ng)//2
            a = self.points[mid]-self.points[0]
            b = other-self.points[0]
            if sgn(a.cross(b)) >= 0:
                ok = mid
            else:
                ng = mid
        if ok == 0:
            return 0
        x = Convex([self.points[0], self.points[ok], self.points[ng]]).is_contain_Point(other)
        if x != 1:
            return x
        if sgn(Point.ccw(self.points[ok], self.points[ng], other)) == 0:
            return 1
        if ok == 1 and sgn(Point.ccw(self.points[0], self.points[1], other)) == 0:
            return 1
        if ng == len(self.points)-1 and sgn(Point.ccw(self.points[0], self.points[-1], other)) == 0:
            return 1
        return 2

class Points:
    def cast_to_Point(points):
        for i in range(len(points)):
            points[i] = Point(points[i])
    # 最近点対
    def closest_pair(points):
        if type(points[0]) is not Point:
            Points.cast_to_Point(points)
        n = len(points)
        return Points._cp_rec(sorted(points), 0, n)[:2]
    def _cp_rec(points, i, n):
        if n <= 1:
            return inf, None, [points[i]]
        m = n//2
        x = points[i+m][0]
        dl, pairl, pointsl = Points._cp_rec(points, i, m)
        dr, pairr, pointsr = Points._cp_rec(points, i+m, n-m)
        if dl <= dr:
            d = dl
            pair = pairl
        else:
            d = dr
            pair = pairr
        sorted_points = [None]*n
        l = r = idx = 0
        while l < m and r < n-m:
            if pointsl[l].y < pointsr[r].y:
                sorted_points[idx] = pointsl[l]
                l += 1
            else:
                sorted_points[idx] = pointsr[r]
                r += 1
            idx += 1
        while l < m:
            sorted_points[idx] = pointsl[l]
            l += 1
            idx += 1
        while r < n-m:
            sorted_points[idx] = pointsr[r]
            r += 1
            idx += 1
        b = []
        for i in range(n):
            p = sorted_points[i]
            if abs(p.x-x) >= d:
                continue
            for j in range(len(b)-1, -1, -1):
                if p.y-b[j].y >= d: break
                nd = p.distance_from_Point(b[j])
                if nd < d:
                    d = nd
                    pair = (p, b[j])
            b.append(p)
        return d, pair, sorted_points
    # 最遠点対
    def farthest_pair(points):
        if type(points[0]) is not Point:
            Points.cast_to_Point(points)
        if len(points) == 2:
            return points[0].distance_from_Point(points[1]), (points[0], points[1])
        convex = Convex.convex_full(points, False)
        if len(convex) > len(points):
            p, q = min(points), max(points)
            return p.distance_from_Point(q), (p, q)
        j = 1
        n = len(convex)
        d_sq = 0
        pair = None
        for i in range(n):
            while j == i or sgn((convex[(i+1)%n]-convex[i]).dot(convex[(j+1)%n]-convex[i])) > 0:
                j += 1
                j %= n
            nd_sq = convex[i].distance_from_Point_sq(convex[j])
            if d_sq < nd_sq:
                d_sq = nd_sq
                pair = (convex[i], convex[j])
            nd_sq = convex[i].distance_from_Point_sq(convex[(j+1)%n])
            if d_sq < nd_sq:
                d_sq = nd_sq
                pair = (convex[i], convex[(j+1)%n])
        return sqrt(d_sq), pair
    
    def argsort(points, base=Point(), by_cross=True):
        if by_cross:
            U, D = [], []
            for p in points:
                p = p-base
                if p.is_zero(): continue
                if sgn(p.y) == 0:
                    if sgn(p.x) > 0:
                        U.append(p)
                    else:
                        D.append(p)
                else:
                    if sgn(p.y) > 0:
                        U.append(p)
                    else:
                        D.append(p)
            U.sort(key=cmp_to_key(lambda p, q: sgn(q.cross(p))))
            D.sort(key=cmp_to_key(lambda p, q: sgn(q.cross(p))))
            return list(map(lambda p: p+base, U))+list(map(lambda p: p+base, D))
        else:
            args = [(degrees((p-base).angle())%360, p) for p in points if p != base]
            args.sort(key=lambda x: x[0])
            return args
        
class Circle:
    def __init__(self, centre, radius) -> None:
        if type(centre) is not Point:
            raise ValueError
        self.centre = centre
        self.radius = radius
    def __eq__(self, other):
        if type(other) is not Circle:
            return False
        return self.centre == other.centre and sgn(self.radius-other.radius) == 0
    def __repr__(self) -> str:
        return f"{type(self)}({self.centre}, {self.radius})"
    def area(self):
        return pi*self.radius**2
    def common_area_with_Circle(self, other):
        if type(other) is not Circle:
            raise ValueError
        if self == other:
            return self.area()
        tn = self.tangent_num_with_Circle(other)
        if tn == 0 or tn == 1:
            return min(self.area(), other.area())
        elif tn == 2:
            a, b = self.intersection_with_Circle(other)
            arg1 = ((a-self.centre).angle()-(other.centre-self.centre).angle())%(2*pi)
            t1 = Convex([self.centre, b, a]).area()
            s1 = self.area()/pi*arg1
            arg2 = ((b-other.centre).angle()-(self.centre-other.centre).angle())%(2*pi)
            t2 = Convex([other.centre, a, b]).area()
            s2 = other.area()/pi*arg2
            return s1+s2-t1-t2
        return 0
    
    def inscribed_circle(triangle): # 内接円
        if not isinstance(triangle, Polygon):
            raise ValueError
        if len(triangle) != 3:
            raise ValueError
        if not triangle.is_convex():
            triangle[0], triangle[2] = triangle[2], triangle[0]
        a, b, c = triangle
        B = b-a
        C = c-a
        arg = (C.angle()-B.angle())/2
        la = Line(a, B.rotate(arg)+a)
        A = a-b
        C = c-b
        arg = (A.angle()-C.angle())/2
        lb = Line(b, C.rotate(arg)+b)
        c = la.intersection_with_Line(lb)
        return Circle(c, c.distance_from_Line(Line(a, b)))
    def circumscribed_circle(triangle): # 外接円
        if not isinstance(triangle, Polygon):
            raise ValueError
        if len(triangle) != 3:
            raise ValueError
        A, B, C = triangle
        AB = B-A
        AC = C-A
        a = AB.dot(AC)
        b = A.distance_from_Point_sq(B)
        c = A.distance_from_Point_sq(C)
        t = b*(a-c)/(2*a**2-2*b*c)
        s = 0.5-a*t/b
        AO = Point((s*AB.x+t*AC.x, s*AB.y+t*AC.y))
        O = A+AO
        return Circle(O, O.distance_from_Point(A))

    def tangent_num_with_Circle(self, other) -> int:
        if type(other) is not Circle:
            raise ValueError
        d = self.centre.distance_from_Point_sq(other.centre)
        r1 = self.radius
        r2 = other.radius
        if sgn(d-(r1+r2)**2) > 0: # 外部
            return 4
        elif sgn(d-(r1+r2)**2) == 0: # 外接
            return 3
        elif sgn((r1-r2)**2-d) == 0: # 内接
            return 1
        elif sgn((r1-r2)**2-d) > 0: # 内部
            return 0
        else: # 交差
            return 2
    def tangent_Point_from_Point(self, other):
        if type(other) is not Point:
            raise ValueError
        icp = self.is_contain_Point(other)
        if icp == 2:
            return None, None
        elif icp == 1:
            return Point(other), None
        d = self.centre-other
        arg = asin(self.radius/d.length())
        x = d.normalized()*sqrt(d.length_sq()-self.radius**2)
        a = x.rotate(arg)+other
        b = x.rotate(-arg)+other
        return a, b
    def tangent_Line_from_Point(self, other):
        if type(other) is not Point:
            raise ValueError
        a, b = self.tangent_point_from_Point(other)
        if a is None:
            return None, None
        elif b is None:
            d = other-self.centre
            return Line(other, other+d.normal_vector()), None
        return Line(other, a), Line(other, b)
    def tangent_Line_with_Circle(self, other):
        if type(other) is not Circle:
            raise ValueError
        if self.centre == other.centre:
            return []
        tn = self.tangent_num_with_Circle(other)
        if tn == 0:
            return []
        elif tn == 1:
            p, _ = self.intersection_with_Circle(other)
            n = (p-self.centre).normal_vector()
            return [Line(p, p+n)]
        elif tn == 2:
            if self.radius < other.radius:
                c1, c2 = self, other
            elif self.radius > other.radius:
                c2, c1 = self, other
            else:
                d = other.centre-self.centre
                n = d.normal_unit_vector()*self.radius
                a1, b1 = self.centre+n, self.centre-n
                a2, b2 = other.centre+n, other.centre-n
                return [Line(a1, a2), Line(b1, b2)]
            q = c2.centre+(c1.centre-c2.centre)/(c2.radius-c1.radius)*c2.radius
            a1, b1 = self.tangent_Point_from_Point(q)
            a2, b2 = other.tangent_Point_from_Point(q)
            return [Line(a1, a2), Line(b1, b2)]
        elif tn == 3:
            p, _ = self.intersection_with_Circle(other)
            n = (p-self.centre).normal_vector()
            if self.radius < other.radius:
                c1, c2 = self, other
            elif self.radius > other.radius:
                c2, c1 = self, other
            else:
                d = other.centre-self.centre
                n = d.normal_unit_vector()*self.radius
                a1, b1 = self.centre+n, self.centre-n
                a2, b2 = other.centre+n, other.centre-n
                return [Line(p, p+n), Line(a1, a2), Line(b1, b2)]
            q = c2.centre+(c1.centre-c2.centre)/(c2.radius-c1.radius)*c2.radius
            a1, b1 = self.tangent_Point_from_Point(q)
            a2, b2 = other.tangent_Point_from_Point(q)
            return [Line(p, p+n), Line(a1, a2), Line(b1, b2)]
        else:
            p = self.centre+(other.centre-self.centre)/(self.radius+other.radius)*self.radius
            a1, b1 = self.tangent_Point_from_Point(p)
            a2, b2 = other.tangent_Point_from_Point(p)
            la, lb = Line(a1, a2), Line(b1, b2)
            if self.radius < other.radius:
                c1, c2 = self, other
            elif self.radius > other.radius:
                c2, c1 = self, other
            else:
                d = other.centre-self.centre
                n = d.normal_unit_vector()*self.radius
                a1, b1 = self.centre+n, self.centre-n
                a2, b2 = other.centre+n, other.centre-n
                return [la, lb, Line(a1, a2), Line(b1, b2)]
            q = c2.centre+(c1.centre-c2.centre)/(c2.radius-c1.radius)*c2.radius
            a1, b1 = self.tangent_Point_from_Point(q)
            a2, b2 = other.tangent_Point_from_Point(q)
            return [la, lb, Line(a1, a2), Line(b1, b2)]
    
    # 内部なら2, 境界上なら1, 外部なら0
    def is_contain_Point(self, other):
        if type(other) is not Point:
            raise ValueError
        s = sgn(other.distance_from_Point_sq(self.centre)-self.radius**2)
        if s < 0:
            return 2
        elif s == 0:
            return 1
        return 0
    
    def is_intersect_with_Point(self, other) -> bool:
        if type(other) is not Point:
            raise ValueError
        return self.is_contain_Point(other) == 1
    def is_intersect_with_Line(self, other) -> bool:
        if type(other) is not Line:
            raise ValueError
        p = self.centre.projection(other)
        d = p.distance_from_Point(self.centre)
        return sgn(self.radius-d) >= 0
    def is_intersect_with_Circle(self, other) -> bool:
        if type(other) is not Circle:
            raise ValueError
        return 1 <= self.tangent_num_with_Circle(other) <= 3
    
    def intersection_with_Point(self, other) -> bool:
        if type(other) is not Point:
            raise ValueError
        if sgn(other.distance_from_Point_sq(self.centre)-self.radius**2) == 0:
            return other
        return None
    def intersection_with_Line(self, other):
        if type(other) is not Line:
            raise ValueError
        p = self.centre.projection(other)
        d = p.distance_from_Point(self.centre)
        if sgn(self.radius-d) == 0:
            return p, None
        elif sgn(self.radius-d) > 0:
            e = sqrt(self.radius**2-d**2)
            return other.vec().normalized()*e+p, other.vec().normalized()*-e+p
        return None, None
    def intersection_with_Circle(self, other):
        if type(other) is not Circle:
            raise ValueError
        tn = self.tangent_num_with_Circle(other)
        if tn == 1:
            if self.radius < other.radius:
                c2, c1 = self, other
            else:
                c1, c2 = self, other
            a = c1.centre+(c2.centre-c1.centre).normalized()*c1.radius
            return a, None
        elif tn == 3:
            a = self.centre+(other.centre-self.centre).normalized()*self.radius
            return a, None
        elif tn == 2:
            d = self.centre.distance_from_Point_sq(other.centre)
            r1, r2 = self.radius, other.radius
            arg = acos((r1**2+d-r2**2)/(2*r1*sqrt(d)))
            a = self.centre+((other.centre-self.centre).normalized()*r1).rotate(arg)
            b = self.centre+((other.centre-self.centre).normalized()*r1).rotate(-arg)
            return a, b
        return None, None
    
if __name__ == "__main__":
    N = int(input())
    A = [tuple(map(int, input().split())) for _ in range(N)]
    B = [tuple(map(int, input().split())) for _ in range(N)]
    fda = Points.farthest_pair(A)[0]
    fdb = Points.farthest_pair(B)[0]
    print(fdb/fda)