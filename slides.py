from manim import *  # or: from manimlib import *

from manim_slides import Slide

def Item(*str,dot = True,font_size = 35,math=False,pw="8cm",color=WHITE):
    if math:
        tex = MathTex(*str,font_size=font_size,color=color)
    else:
        tex = Tex(*str,font_size=font_size,color=color,tex_environment=f"{{minipage}}{{{pw}}}")
    if dot:
        dot = MathTex("\\cdot").scale(2)
        dot.next_to(tex[0][0], LEFT, SMALL_BUFF)
        tex[0].add_to_back(dot)
    else:
        dot = MathTex("\\cdot",color=BLACK).scale(2)
        dot.next_to(tex[0], LEFT, SMALL_BUFF)
        tex[0].add_to_back(dot)
    g2 = VGroup()
    for item in tex:
        g2.add(item)

    return(g2)


def ItemList(*item,buff=MED_SMALL_BUFF):
    list = VGroup(*item).arrange(DOWN, aligned_edge=LEFT,buff=buff)
    return(list)

def Ray(start,end,ext:float=0,eext:float = 0,pos:float=0.5,color=BLUE):
    dir_lin = Line(start=start,end=end)
    dir = dir_lin.get_length()*ext*dir_lin.get_unit_vector()
    edir = dir_lin.get_length()*eext*dir_lin.get_unit_vector()
    lin = Line(start=start-edir,end=end+dir,color=color)
    arrow_start = lin.get_start()+pos*lin.get_length()*lin.get_unit_vector()
    arrow = Arrow(start=arrow_start-0.1*lin.get_unit_vector(),end=arrow_start+0.1*lin.get_unit_vector(),tip_shape=StealthTip,max_tip_length_to_length_ratio=0.75,color=color)
    ray = VGroup(lin,arrow)
    return ray

def CurvedRay(start,end,ext:float=0,radius=2,color=RED,rev = False):
    arc = ArcBetweenPoints(start=start,end=end,radius=radius,color=color)
    n = int(len(arc.get_all_points())/2)
    pt = arc.get_all_points()[n]
    pt2 = arc.get_all_points()[n+1]
    if rev:
        arrow = Arrow(start=pt2,end=pt,tip_shape=StealthTip,max_tip_length_to_length_ratio=0.75,color=color)
    else:
        arrow = Arrow(start=pt,end=pt2,tip_shape=StealthTip,max_tip_length_to_length_ratio=0.75,color=color)
    ray = VGroup(arc,arrow)
    return ray

def MyLabeledDot(label_in:Tex| None = None,label_out:Tex| None = None,pos:Vector = DOWN,shift=[0,0,0], point=ORIGIN,radius: float = DEFAULT_DOT_RADIUS,color = WHITE):
        if isinstance(label_in, Tex):
            radius = 0.02 + max(label_in.width, label_in.height) / 2
        
        dot = Dot(point=point,radius=radius,color=color)
        g1 = VGroup(dot)
        if isinstance(label_in, Tex):
            label_in.move_to(dot.get_center())
            g1.add(label_in)
        if isinstance(label_out, Tex):
            label_out.next_to(dot,pos)
            label_out.shift(shift)
            g1.add(label_out)

        return g1


class MyDashLabeledLine(DashedLine):
    def __init__(self,label: Tex|MathTex, pos = None, rel_pos: float = 0.5,bg = BLACK, opacity:float= 0.7,rot: bool =True  , *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # calculating the vector for the label position
        line_start, line_end = self.get_start_and_end()
        new_vec = (line_end - line_start) * rel_pos
        label_coords = line_start + new_vec
        label.move_to(label_coords)
        
        if rot:
            ang=angle_of_vector(self.get_unit_vector())
            if ang < -PI/2:
                ang =  ang+PI
            elif ang > PI/2:
                ang=ang-PI

            label.rotate(ang)

        if pos is None:
            mask  = Line(label.get_center()-0.6*label.width*self.get_unit_vector(),label.get_center()+0.6*label.width*self.get_unit_vector(),color=bg,stroke_width=self.get_stroke_width()+1,stroke_opacity=opacity)
            self.add(mask)
        else:
            label.shift(pos)
        self.add(label)

class MyLabeledLine(Line):
    def __init__(self,label: Tex|MathTex, pos = None, rel_pos: float = 0.5,bg = BLACK, opacity:float= 0.7,rot: bool =True , *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # calculating the vector for the label position
        line_start, line_end = self.get_start_and_end()
        new_vec = (line_end - line_start) * rel_pos
        label_coords = line_start + new_vec
        label.move_to(label_coords)
        if pos is None:
            if rot:
                mask  = Line(label.get_center()-0.65*label.width*self.get_unit_vector(),label.get_center()+0.65*label.width*self.get_unit_vector(),color=bg,stroke_width=self.get_stroke_width()+1,stroke_opacity=opacity)
            else:
                mask  = Line(label.get_center()-0.65*label.height*self.get_unit_vector(),label.get_center()+0.65*label.height*self.get_unit_vector(),color=bg,stroke_width=self.get_stroke_width()+1,stroke_opacity=opacity)
            self.add(mask)
        else:
            label.shift(pos)
        
        if rot:
            ang=angle_of_vector(self.get_unit_vector())
            if ang < -PI/2:
                ang =  ang+PI
            elif ang > PI/2:
                ang=ang-PI

            label.rotate(ang)
        self.add(label)


class MyLabeledArrow(MyLabeledLine, Arrow):

    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(buff=0,*args, **kwargs)

class MyDoubLabArrow(MyLabeledLine, DoubleArrow):

    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(buff=0,*args, **kwargs)





def ir(a,b): # inclusive range, useful for TransformByGlyphMap
    return list(range(a,b+1))


class LatexItems(Tex):
    def __init__(self, *args, page_width="15em", itemize="itemize",font_size=35, **kwargs):
        template = TexTemplate()
        template.body = (r"\documentclass[preview]{standalone}\usepackage[english]{babel}"
                         r"\usepackage{amsmath}\usepackage{amssymb}\begin{document}"
                         rf"\begin{{minipage}}{{{page_width}}}"
                         rf"\begin{{{itemize}}}YourTextHere\end{{{itemize}}}"
                         r"\end{minipage}\end{document}"
        )
        super().__init__(*args, tex_template=template, tex_environment=None,font_size=font_size, **kwargs)


class AlignTex(Tex):
    def __init__(self, *args, page_width="15em",align="align*",font_size=35, **kwargs):
        template = TexTemplate()
        template.body = (r"\documentclass[preview]{standalone}\usepackage[english]{babel}"
                         r"\usepackage{amsmath}\usepackage{amssymb}\usepackage{cancel}\begin{document}"
                         rf"\begin{{minipage}}{{{page_width}}}"
                         rf"\begin{{{align}}}YourTextHere\end{{{align}}}"
                         r"\end{minipage}\end{document}"
        )
        super().__init__(*args,font_size=font_size, tex_template=template, tex_environment=None, **kwargs)


class TransformByGlyphMap(AnimationGroup):
    def __init__(self, mobA, mobB, *glyph_map, replace=True, from_copy=True, show_indices=False, **kwargs):
		# replace=False does not work properly
        if from_copy:
            self.mobA = mobA.copy()
            self.replace = True
        else:
            self.mobA = mobA
            self.replace = replace
        self.mobB = mobB
        self.glyph_map = glyph_map
        self.show_indices = show_indices

        animations = []
        mentioned_from_indices = []
        mentioned_to_indices = []
        for from_indices, to_indices in self.glyph_map:
            print(from_indices, to_indices)
            if len(from_indices) == 0 and len(to_indices) == 0:
                self.show_indices = True
                continue
            elif len(to_indices) == 0:
                animations.append(FadeOut(
                    VGroup(*[self.mobA[0][i] for i in from_indices]),
                    shift = self.mobB.get_center()-self.mobA.get_center()
                ))
            elif len(from_indices) == 0:
                animations.append(FadeIn(
                    VGroup(*[self.mobB[0][j] for j in to_indices]),
                    shift = self.mobB.get_center() - self.mobA.get_center()
                ))
            else:
                animations.append(Transform(
                    VGroup(*[self.mobA[0][i].copy() if i in mentioned_from_indices else self.mobA[0][i] for i in from_indices]),
                    VGroup(*[self.mobB[0][j] for j in to_indices]),
                    replace_mobject_with_target_in_scene=self.replace
                ))
            mentioned_from_indices.extend(from_indices)
            mentioned_to_indices.extend(to_indices)

        print(mentioned_from_indices, mentioned_to_indices)
        remaining_from_indices = list(set(range(len(self.mobA[0]))) - set(mentioned_from_indices))
        remaining_from_indices.sort()
        remaining_to_indices = list(set(range(len(self.mobB[0]))) - set(mentioned_to_indices))
        remaining_to_indices.sort()
        print(remaining_from_indices, remaining_to_indices)
        if len(remaining_from_indices) == len(remaining_to_indices) and not self.show_indices:
            for from_index, to_index in zip(remaining_from_indices, remaining_to_indices):
                animations.append(Transform(
                    self.mobA[0][from_index],
                    self.mobB[0][to_index],
                    replace_mobject_with_target_in_scene=self.replace
                ))
            super().__init__(*animations, **kwargs)
        else:
            print(f"From indices: {len(remaining_from_indices)}    To indices: {len(remaining_to_indices)}")
            print("Showing indices...")
            super().__init__(
                Create(index_labels(self.mobA[0], color=PINK)),
                FadeIn(self.mobB.next_to(self.mobA, DOWN), shift=DOWN),
                Create(index_labels(self.mobB[0], color=PINK)),
                Wait(5),
                lag_ratio=0.5
                )


class Obj(Slide):
    def construct(self):
        title = Title('CHAPTER 2 : ELECTROSTATIC POTENTIAL AND CAPACITANCE',font_size=40,color=GREEN,match_underline_width_to_text=True)
        self.play(Write(title))
        #self.play(Rotate(title,2*PI))
        self.next_slide()
        Outline = Tex('Learning Objectives :',color=BLUE)
        self.play(Write(Outline))
        self.next_slide()
        self.play(Outline.animate.next_to(title,DOWN,buff=0.5).to_corner(LEFT).scale(0.8))
        self.next_slide()
        list = BulletedList('INTRODUCTION','ELECTROSTATIC POTENTIAL',r'POTENTIAL DUE TO\\ A POINT CHARGE',r'POTENTIAL DUE TO AN\\ ELECTRIC DIPOLE',r'POTENTIAL DUE TO\\ A SYSTEM OF CHARGES',' EQUIPOTENTIAL SURFACES',
                            r' RELATION BETWEEN FIELD\\ AND POTENTIAL',r'POTENTIAL ENERGY OF A SYSTEM\\ OF CHARGES').scale(0.7).next_to(Outline,DOWN).to_corner(LEFT).shift(0.1*RIGHT)
        
        for i in range(len(list)):
            list.fade_all_but(i)
            self.play(Write(list[i]))
            self.next_slide()
    
        list2 = BulletedList(r'POTENTIAL ENERGY IN\\ AN EXTERNAL FIELD',r'POTENTIAL ENERGY OF A DIPOLE\\ IN AN EXTERNAL FIELD','ELECTROSTATICS OF CONDUCTORS','DIELECTRICS AND POLARISATION',
                             'CAPACITORS AND CAPACITANCE','COMBINATION OF CAPACITORS',r"ENERGY STORED IN\\ A CAPACITOR").scale(0.7).next_to(Outline,DOWN).to_corner(RIGHT)
        
        for i in range(len(list2)):
            list2.fade_all_but(i)
            self.play(Write(list2[i]))
            self.next_slide()
        list2.fade()
        list.fade_all_but(0)
        self.next_slide(loop=True)
        self.play(FocusOn(list[0]))
        self.play(Circumscribe(list[0]))
        self.next_slide()
        self.play(RemoveTextLetterByLetter(list2))
        self.play(RemoveTextLetterByLetter(list))
        self.play(RemoveTextLetterByLetter(Outline))
        Intro_title = Title('INTRODUCTION', color=BLUE)
        self.play(ReplacementTransform(title,Intro_title))
        self.wait()

class Intro(Slide):
    def construct(self):
        Intro_title = Title('Introduction', color=BLUE)
        self.add(Intro_title)
        Cur_title = Tex('Potential energy and Conservative forces :',color=PINK,font_size=40).next_to(Intro_title,DOWN,buff=0.5).to_corner(LEFT)
        self.play(Write(Cur_title))
        self.next_slide()

        list1 = ItemList(Item(r" When an external force does work in taking a body from a point to another against a force like spring force or gravitational force, that work gets stored as potential energy of the body.",pw="13 cm"),
                          Item(r"When the external force is removed, the body moves, gaining kinetic energy and losing an equal amount of potential energy.",pw="13 cm"),
                          Item(r"The sum of kinetic and potential energies is thus conserved. Forces of this kind are called conservative forces. ",pw="13 cm"),
                          Item(r" Spring force and gravitational force are examples of conservative forces. ",pw="13 cm"),
                          Item(r" Since, Coulomb force  and Gravitational force both have inverse square dependence on distance. So, we can say that Coulomb force is also a conservative force.",pw="13 cm"),
                          buff=0.4).next_to(Cur_title,DOWN,buff=0.4).to_corner(LEFT)
        
        for item in list1:
            self.play(Write(item))
            self.next_slide()
        
        self.play(FadeOut(list1,Intro_title))

        PED_title = Tex(r'Electrostatic Potential Energy Difference $(\Delta U_{BA})$:',color=PINK,font_size=40).to_edge(UL)
        self.play(ReplacementTransform(Cur_title,PED_title))
        Q = MyLabeledDot(Tex("+",font_size=30,color=BLACK),Tex(r"Q",font_size=35),color=RED)
        q = MyLabeledDot(Tex("+",font_size=25,color=BLACK),Tex(r"q",font_size=35),color=GREEN,point=3*RIGHT+UP).set_z_index(2)
        A = MyLabeledDot(label_out=Tex(r"A",font_size=35),color=BLUE,radius=0.07,point=4.5*RIGHT+1.5*UP).set_z_index(2)
        B = MyLabeledDot(label_out=Tex(r"B",font_size=35),color=BLUE,radius=0.07,point=1.8*RIGHT+0.6*UP).set_z_index(2)
        line = Line(4.5*RIGHT+1.5*UP,1.8*RIGHT+0.6*UP,color=BLUE_E).set_z_index(1)
        dr = MyLabeledArrow(label=Tex(r"$d\vec{r}$",font_size=35),start=3*RIGHT+UP,end=3*RIGHT+UP-0.7*line.get_unit_vector(),color=ORANGE,pos=0.2*DOWN).set_z_index(1)
        r = MyDoubLabArrow(label=Tex(r"$r$",font_size=35),start=ORIGIN,end=3*RIGHT+UP,color=GREY,opacity=1,tip_length=0.1).shift(0.15*UP).set_z_index(1)
        FE = MyLabeledArrow(label=Tex(r"$\vec{F}_E$",font_size=35),start=q.get_center(),end=q.get_center()-1.1*line.get_unit_vector(),color=RED,tip_length=0.1,pos=0.3*UP).shift(0.5*UP)
        FExt = MyLabeledArrow(label=Tex(r"$\vec{F}_{ext}$",font_size=35),start=q.get_center(),end=q.get_center()+1.1*line.get_unit_vector(),tip_length=0.1,color=YELLOW,pos=0.3*UP).shift(0.5*UP)
        img = VGroup(Q,A,B,line,q,FE,FExt,dr,r).to_corner(RIGHT).shift(1.5*UP)

        list2 = ItemList(Item(r" Consider a charge $Q$ fixed at the origin.",pw="7 cm"),
                          Item(r"We are bringing a charge $q$ by applying  an external force $\vec{F}_{ext}$ just enough to counter the repulsive electric force $\vec{F}_E$ (i.e, $\vec{F}_{ext}= -\vec{F}_E$ ).",pw="7 cm"),
                          Item(r"This means there is no net force on or acceleration of  the charge q when it is brought from A to B, i.e., it is brought with infinitesimally slow constant speed. ",pw="13 cm"),
                          Item(r" In this situation, work done by the external force is the negative of the work done by the electric force, and gets fully stored in the form of potential energy of the charge q.  ",pw="13 cm"),
                          Item(r" If the external force is removed on reaching B,  the stored energy (potential energy) at B is used to provide kinetic energy to the charge $q$ in such away that the sum of the kinetic and potential energies is conserved. ",pw="13 cm"),
                          buff=0.4).next_to(Cur_title,DOWN,buff=0.4).to_corner(LEFT)
        
        anm = [VGroup(list2[0],Q),VGroup(list2[1],q,FE,FExt),VGroup(list2[2],A,B,line),list2[3],list2[4]]
        
        for item in anm:
            self.play(Write(item))
            self.next_slide()

        self.play(FadeOut(list2))
        self.wait(2)
        self.play(Write(dr),Write(r))


        list2 = ItemList(Item(r" Thus, work done by external forces in moving a charge $q$ from A to B is.",pw="7 cm"),
                          Item(r"$W_{AB}=\int_{A}^{B}\vec{F}_{ext}\cdot d\vec{r}$", r"$=-\int_{r_A}^{r_B}\vec{F}_{E}\cdot d\vec{r}$",pw="7 cm"),
                          Item(r"This work done increases its potential energy by an amount equal to potential energy difference between points B and A. ",pw="13 cm"),
                          Item(r" $\Delta U_{BA}=U_B-U_A=W_{AB}$ ", r"$=-\int_{r_A}^{r_B}\vec{F}_{E}\cdot d\vec{r}$",pw="13 cm"),
                          Item(r"We can define electric potential energy difference between two points as the work required to be done by an external force in moving (without accelerating ) charge q from one point to another against the electrostatic field.",color=YELLOW_D,pw="13 cm"),
                          buff=0.4).next_to(Cur_title,DOWN,buff=0.4).to_corner(LEFT)
        
        for item in list2:
            for subitem in item:
                self.play(Write(subitem))
                self.next_slide()

        self.play(FadeOut(list2))
        self.wait(2)

        
        list3 = ItemList(Item(r" Thus, Potential energy difference (Change in P.E.) is",pw="8 cm"),
                          Item(r"$\Delta U_{BA}=W_{AB}$", r"$=-\int_{r_A}^{r_B}\vec{F}_{E}\cdot d\vec{r}$",pw="7 cm",dot=False),
                          Item(r"$F_E = \dfrac{1}{4\pi\epsilon_0}\dfrac{Qq}{r^2}$ ",pw="13 cm"),
                          Item(r" $\Delta U_{BA}=-\int_{r_A}^{r_B} \dfrac{1}{4\pi\epsilon_0}\dfrac{Qq}{r^2} dr$",pw="13 cm",dot=False),
                          Item(r" $\Delta U_{BA}=\dfrac{-Qq}{4\pi\epsilon_0}\int_{r_A}^{r_B} r^{-2} dr$",pw="13 cm",dot=False),
                          Item(r" $\Delta U_{BA}=\dfrac{-Qq}{4\pi\epsilon_0}\left[ \dfrac{r^{(-2+1)}}{-2+1} \right]_{r_A}^{r_B}$",r"$=\dfrac{-Qq}{4\pi\epsilon_0}\left[ \dfrac{-1}{r} \right]_{r_A}^{r_B}$",pw="13 cm",dot=False),
                          buff=0.4).next_to(Cur_title,DOWN,buff=0.4).to_corner(LEFT)
        
        list4 = ItemList(Item(r" $\Delta U_{BA}=U_B-U_A=\dfrac{Qq}{4\pi\epsilon_0}\left[ \dfrac{1}{r_B} -\dfrac{1}{r_A} \right]$",pw="13 cm",dot=False),
                         Item(r" Here, $U_A \rightarrow $ P.E. at A",pw="6 cm"),
                         Item(r" And, $U_B \rightarrow $ P.E. at B",pw="6 cm"),
                          buff=0.4).next_to(img,DOWN,buff=0.2).to_corner(RIGHT)
        
        sr =SurroundingRectangle(list4[0])
        
        for item in list3:
            for subitem in item:
                self.play(Write(subitem))
                self.next_slide()
        
        self.play(Write(sr))

        for item in list4:
            for subitem in item:
                self.play(Write(subitem))
                self.next_slide()

        self.play(FadeOut(list3,list4,img))
        self.wait(1)
        self.play(FadeIn(list4[0]),VGroup(list4[0],sr).animate.next_to(Cur_title,DOWN))

        list5 = ItemList(Item(r"The work done by an electrostatic field in moving a charge from one point to another depends only on the initial and the final points and is independent of the path taken to go from one point to the other. ", r"This is the fundamental characteristic of a conservative force.",pw="13 cm",color=GREEN),
                          Item(r" The concept of the potential energy would not be meaningful if the work depended on the path(or if force is not conservative).",pw="13 cm",color=GOLD),
                          Item(r"The actual value of potential energy is not physically significant; it is only the difference of potential energy that is significant. \\", r"$\Delta U_{BA}=U_B-U_A=(U_B+\alpha)-(U_A+\alpha)=W_{AB}$",pw="13 cm",color=GREEN),
                          Item(r"There is a freedom in choosing the point where potential energy is zero. A convenient choice is to have electrostatic potential energy zero at infinity. (i.e., $U_{\infty}=0$)",pw="13 cm",color=GOLD),
                          buff=0.4).next_to(sr,DOWN,buff=0.2).to_corner(LEFT)
        
        for item in list5:
            for subitem in item:
                self.play(Write(subitem))
                self.next_slide()

        list6 = ItemList(Item(r"With this choice, if we take the point A at infinity ",pw="13 cm",color=GREEN),
                          Item(r" $U_B-U_{\infty}=W_{\infty B}=$", r"$\dfrac{Qq}{4\pi\epsilon_0}\left[ \dfrac{1}{r_B} -\dfrac{1}{\infty} \right]$",pw="13 cm",color=GOLD),
                          Item(r" $U_B=W_{\infty B}=$", r"$\dfrac{Qq}{4\pi\epsilon_0} \dfrac{1}{r_B} \quad (\because U_{\infty=0})$",pw="13 cm",color=RED_D),
                          Item(r"Potential Energy ($U$) : ", r"Potential energy of charge $q$ at a point is the work done by the external force (equal and opposite to the electric force) in bringing the charge $q$ from infinity to that point.",pw="13 cm",color=YELLOW),
                          buff=0.4).next_to(sr,DOWN,buff=0.2).to_corner(LEFT)
        
        sr2 = SurroundingRectangle(list6[2])
        arrow = MyLabeledArrow(label=Tex("Potential Energy",font_size=35),start=sr2.get_right(),end=sr2.get_right()+1.5*RIGHT,tip_length=0.2,rel_pos=3,opacity=0)
        arrow2 = MyLabeledArrow(label=Tex("Potential Energy Difference",font_size=35),start=sr.get_right(),end=sr.get_right()+1.5*RIGHT,tip_length=0.2,rel_pos=2.5,opacity=0)

        self.play(FadeOut(list5))
        for item in list6:
            for subitem in item:
                self.play(Write(subitem))
                self.next_slide()

        self.play(Write(sr2),Write(arrow),Write(arrow2))


class Potential(Slide):
    def construct(self):
        title = Title('CHAPTER 2 : ELECTROSTATIC POTENTIAL AND CAPACITANCE',font_size=40,color=GREEN,match_underline_width_to_text=True)
        self.play(Write(title))
        #self.play(Rotate(title,2*PI))
        self.next_slide()
        Outline = Tex('Learning Objectives :',color=BLUE)
        self.play(Write(Outline))
        self.next_slide()
        self.play(Outline.animate.next_to(title,DOWN,buff=0.5).to_corner(LEFT).scale(0.8))
        self.next_slide()
        list = BulletedList('INTRODUCTION','ELECTROSTATIC POTENTIAL',r'POTENTIAL DUE TO\\ A POINT CHARGE',r'POTENTIAL DUE TO AN\\ ELECTRIC DIPOLE',r'POTENTIAL DUE TO\\ A SYSTEM OF CHARGES',' EQUIPOTENTIAL SURFACES',
                            r' RELATION BETWEEN FIELD\\ AND POTENTIAL',r'POTENTIAL ENERGY OF A SYSTEM\\ OF CHARGES').scale(0.7).next_to(Outline,DOWN).to_corner(LEFT).shift(0.1*RIGHT)

    
        list2 = BulletedList(r'POTENTIAL ENERGY IN\\ AN EXTERNAL FIELD',r'POTENTIAL ENERGY OF A DIPOLE\\ IN AN EXTERNAL FIELD','ELECTROSTATICS OF CONDUCTORS','DIELECTRICS AND POLARISATION',
                             'CAPACITORS AND CAPACITANCE','COMBINATION OF CAPACITORS',r"ENERGY STORED IN\\ A CAPACITOR").scale(0.7).next_to(Outline,DOWN).to_corner(RIGHT)
        
        self.add(list,list2)
        self.next_slide(loop=True)
        self.play(FocusOn(list[1]))
        self.play(Circumscribe(list[1]))
        self.next_slide()
        self.play(RemoveTextLetterByLetter(list2))
        self.play(RemoveTextLetterByLetter(list))
        self.play(RemoveTextLetterByLetter(Outline))
        Intro_title = Title('ELECTROSTATIC POTENTIAL  DIFFERENCE $(\Delta V)$ \& POTENTIAL $(V)$', font_size=40,color=BLUE,underline_buff=SMALL_BUFF,match_underline_width_to_text=True)
        self.play(ReplacementTransform(title,Intro_title))
        self.wait()
        self.next_slide()

        list = ItemList(Item(r" The potential energy (or work) we just defined is proportional to the test charge $q$ .",pw="13 cm",color=GREEN),
                          Item(r"It is, therefore, convenient to divide the work by the amount of charge $q$, so that the resulting quantity is independent of $q$ ",pw="13 cm",color=GREEN),
                          Item(r"Electrostatic Potential Difference ($\Delta V_{BA}$) : ", r"It is defined as the work done by external force in bringing a unit positive charge from point one point (A) to another (B) ",pw="13 cm",color=GOLD),
                          Item(r"$\Delta V_{BA}=V_B-V_A=\dfrac{W_{AB}}{q}$",r"$=\dfrac{U_{BA}}{q}$",color=PINK,pw="13 cm",dot=False),
                          Item(r"Electrostatic Potential  ($ V_{B}$) : ", r"It is defined as the work done by external force in bringing a unit positive charge (without acceleration) from infinity to that point (B). ",pw="13 cm",color=GOLD),
                          Item(r"$ V_{B}=\dfrac{W_{\infty B}}{q}$",r"$=\dfrac{U_{B}}{q}$",color=PINK,pw="13 cm",dot=False),
                          buff=0.4).next_to(Intro_title,DOWN,buff=0.25).to_corner(LEFT)
        sr1 = SurroundingRectangle(list[3])
        sr2 = SurroundingRectangle(list[5])
        arrow = MyLabeledArrow(label=Tex("Potential Difference",font_size=35),start=sr1.get_right(),end=sr1.get_right()+1.5*RIGHT,tip_length=0.2,rel_pos=3,opacity=0)
        arrow2 = MyLabeledArrow(label=Tex("Potential",font_size=35),start=sr2.get_right(),end=sr2.get_right()+1.5*RIGHT,tip_length=0.2,rel_pos=2.5,opacity=0)

        
        for item in list:
            for subitem in item:
                self.play(Write(subitem))
                self.next_slide()

        self.play(Write(VGroup(sr1,sr2,arrow,arrow2)))
        self.wait(1)

class PointCharge(Slide):
    def construct(self):
        title = Title('CHAPTER 2 : ELECTROSTATIC POTENTIAL AND CAPACITANCE',font_size=40,color=GREEN,match_underline_width_to_text=True)
        Outline = Tex('Learning Objectives :',color=BLUE).next_to(title,DOWN,buff=0.5).to_corner(LEFT).scale(0.8)
        list = BulletedList('INTRODUCTION','ELECTROSTATIC POTENTIAL',r'POTENTIAL DUE TO\\ A POINT CHARGE',r'POTENTIAL DUE TO AN\\ ELECTRIC DIPOLE',r'POTENTIAL DUE TO\\ A SYSTEM OF CHARGES',' EQUIPOTENTIAL SURFACES',
                            r' RELATION BETWEEN FIELD\\ AND POTENTIAL',r'POTENTIAL ENERGY OF A SYSTEM\\ OF CHARGES').scale(0.7).next_to(Outline,DOWN).to_corner(LEFT).shift(0.1*RIGHT)

    
        list2 = BulletedList(r'POTENTIAL ENERGY IN\\ AN EXTERNAL FIELD',r'POTENTIAL ENERGY OF A DIPOLE\\ IN AN EXTERNAL FIELD','ELECTROSTATICS OF CONDUCTORS','DIELECTRICS AND POLARISATION',
                             'CAPACITORS AND CAPACITANCE','COMBINATION OF CAPACITORS',r"ENERGY STORED IN\\ A CAPACITOR").scale(0.7).next_to(Outline,DOWN).to_corner(RIGHT)
        
        self.add(title,Outline,list,list2)
        self.next_slide(loop=True)
        self.play(FocusOn(list[2]))
        self.play(Circumscribe(list[2]))
        self.next_slide()
        self.play(RemoveTextLetterByLetter(list2))
        self.play(RemoveTextLetterByLetter(list))
        self.play(RemoveTextLetterByLetter(Outline))
        Intro_title = Title('POTENTIAL DUE TO A POINT CHARGE', font_size=40,color=BLUE,underline_buff=SMALL_BUFF,match_underline_width_to_text=True)
        self.play(ReplacementTransform(title,Intro_title))
        self.wait()
