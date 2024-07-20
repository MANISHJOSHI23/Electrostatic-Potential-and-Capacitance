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

class Ex1(Slide):
    def construct(self):

        ex_title = Tex(r"Example 1 :", r"(a) Calculate the potential at a point P due to a charge of $4 \times 10^{-7}$ C located 9 cm away.\\", r"(b) Hence obtain the work done in bringing a charge of $2 \times 10^{-9}$ C from infinity to the point P. Does the answer depend on the path along which the charge is brought?",tex_environment="{minipage}{13 cm}",font_size=35, color=BLUE_C).to_corner(UP,buff=0.2).to_corner(LEFT,buff=0.2)
        ex_title[0].set_color(GREEN)
        self.play(Write(ex_title))
        self.wait(2)

class Ex2(Slide):
    def construct(self):

        ex_title = Tex(r"Example 2 :", r" Figures 2.8 (a) and (b) show the field lines of a positive and negative point charge respectively.",tex_environment="{minipage}{13 cm}",font_size=35, color=BLUE_C).to_corner(UP,buff=0.2).to_corner(LEFT,buff=0.2)
        ex_title[0].set_color(GREEN)
        self.play(Write(ex_title))
        self.next_slide()
        img = ImageMobject("Ex2.png").scale(0.8).next_to(ex_title,DOWN).to_edge(RIGHT)
        self.play(FadeIn(img))
        ex_title2 = ItemList(Item(r"(a) Give the signs of the potential difference $V_P- V_Q$; $V_B - V_A$.",pw="7 cm",color=GREEN,dot=False),
                          Item(r"(b) Give the sign of the potential energy difference of a small negative charge between the points Q and P; A and B.",pw="7 cm",color=GOLD,dot=False),
                          Item(r" (c) Give the sign of the work done by the field in moving a small positive charge from Q to P.",pw="7 cm",color=RED_D,dot=False),
                          Item(r"(d) Give the sign of the work done by the external agency in moving a small negative charge from B to A.",pw="13 cm",color=YELLOW,dot=False),
                          Item(r"(e) Does the kinetic energy of a small negative charge increase or decrease in going from B to A?",pw="13 cm",color=RED_D,dot=False),
                          buff=0.4).next_to(ex_title,DOWN).to_edge(LEFT)
        for item in ex_title2:
            self.play(Write(item))
            self.next_slide()

class SystemCharge(Slide):
    def construct(self):
        title = Title('CHAPTER 2 : ELECTROSTATIC POTENTIAL AND CAPACITANCE',font_size=40,color=GREEN,match_underline_width_to_text=True)
        Outline = Tex('Learning Objectives :',color=BLUE).next_to(title,DOWN,buff=0.5).to_corner(LEFT).scale(0.8)
        list = BulletedList('INTRODUCTION','ELECTROSTATIC POTENTIAL',r'POTENTIAL DUE TO\\ A POINT CHARGE',r'POTENTIAL DUE TO\\ A SYSTEM OF CHARGES',r'POTENTIAL DUE TO AN\\ ELECTRIC DIPOLE',' EQUIPOTENTIAL SURFACES',
                            r' RELATION BETWEEN FIELD\\ AND POTENTIAL',r'POTENTIAL ENERGY OF A SYSTEM\\ OF CHARGES').scale(0.7).next_to(Outline,DOWN).to_corner(LEFT).shift(0.1*RIGHT)

    
        list2 = BulletedList(r'POTENTIAL ENERGY IN\\ AN EXTERNAL FIELD',r'POTENTIAL ENERGY OF A DIPOLE\\ IN AN EXTERNAL FIELD','ELECTROSTATICS OF CONDUCTORS','DIELECTRICS AND POLARISATION',
                             'CAPACITORS AND CAPACITANCE','COMBINATION OF CAPACITORS',r"ENERGY STORED IN\\ A CAPACITOR").scale(0.7).next_to(Outline,DOWN).to_corner(RIGHT)
        
        self.add(title,Outline,list,list2)
        self.next_slide(loop=True)
        self.play(FocusOn(list[3]))
        self.play(Circumscribe(list[3]))
        self.next_slide()
        self.play(RemoveTextLetterByLetter(list2))
        self.play(RemoveTextLetterByLetter(list))
        self.play(RemoveTextLetterByLetter(Outline))
        Intro_title = Title('POTENTIAL DUE TO A SYSTEM OF CHARGES', font_size=40,color=BLUE,underline_buff=SMALL_BUFF,match_underline_width_to_text=True)
        self.play(ReplacementTransform(title,Intro_title))
        self.wait()


class Ex3(Slide):
    def construct(self):

        ex_title = Tex(r"Example 3 :", r"Two charges $3 \times 10^{-8}$ C and $-2 \times 10^{-8}$ C are located 15 cm apart. At what point on the line joining the two charges is the electric potential zero? Take the potential at infinity to be zero.",tex_environment="{minipage}{13 cm}",font_size=35, color=BLUE_C).to_corner(UP,buff=0.2).to_corner(LEFT,buff=0.2)
        ex_title[0].set_color(GREEN)
        self.play(Write(ex_title))
        self.wait(2)

class DipolePotential(Slide):
    def construct(self):
        title = Title('CHAPTER 2 : ELECTROSTATIC POTENTIAL AND CAPACITANCE',font_size=40,color=GREEN,match_underline_width_to_text=True)
        Outline = Tex('Learning Objectives :',color=BLUE).next_to(title,DOWN,buff=0.5).to_corner(LEFT).scale(0.8)
        list = BulletedList('INTRODUCTION','ELECTROSTATIC POTENTIAL',r'POTENTIAL DUE TO\\ A POINT CHARGE',r'POTENTIAL DUE TO\\ A SYSTEM OF CHARGES',r'POTENTIAL DUE TO AN\\ ELECTRIC DIPOLE',' EQUIPOTENTIAL SURFACES',
                            r' RELATION BETWEEN FIELD\\ AND POTENTIAL',r'POTENTIAL ENERGY OF A SYSTEM\\ OF CHARGES').scale(0.7).next_to(Outline,DOWN).to_corner(LEFT).shift(0.1*RIGHT)

    
        list2 = BulletedList(r'POTENTIAL ENERGY IN\\ AN EXTERNAL FIELD',r'POTENTIAL ENERGY OF A DIPOLE\\ IN AN EXTERNAL FIELD','ELECTROSTATICS OF CONDUCTORS','DIELECTRICS AND POLARISATION',
                             'CAPACITORS AND CAPACITANCE','COMBINATION OF CAPACITORS',r"ENERGY STORED IN\\ A CAPACITOR").scale(0.7).next_to(Outline,DOWN).to_corner(RIGHT)
        
        self.add(title,Outline,list,list2)
        self.next_slide(loop=True)
        self.play(FocusOn(list[4]))
        self.play(Circumscribe(list[4]))
        self.next_slide()
        self.play(RemoveTextLetterByLetter(list2))
        self.play(RemoveTextLetterByLetter(list))
        self.play(RemoveTextLetterByLetter(Outline))
        Intro_title = Title('POTENTIAL DUE TO AN ELECTRIC DIPOLE', font_size=40,color=BLUE,underline_buff=SMALL_BUFF,match_underline_width_to_text=True)
        self.play(ReplacementTransform(title,Intro_title))
        self.wait()
        q1 = MyLabeledDot(label_in=Tex("$-$",font_size=35,color=BLACK),label_out=Tex("$-q$",font_size=30,color=BLUE),color=BLUE).shift(2*LEFT).set_z_index(2)
        q2 = MyLabeledDot(label_in=Tex("$+$",font_size=35,color=BLACK),label_out=Tex("$+q$",font_size=30,color=GREEN),color=GREEN).shift(2*RIGHT).set_z_index(2)
        lin = Line(q1[0].get_right(),q2[0].get_left(),color=ORANGE)
        pt = MyLabeledDot(label_out=Tex("P",font_size=30),point=5*UP+3*RIGHT,radius=0.06,pos=UP).set_z_index(2)
        o = MyLabeledDot(label_out=Tex("O",font_size=30),radius=0.06,pos=0.2*DOWN+0.02*RIGHT).set_z_index(2)
        lin = VGroup(MyLabeledLine(label=Tex("$a$",font_size=30),start=q1[0].get_right(),end=o[0].get_left(),color=ORANGE,pos=0.2*DOWN),MyLabeledLine(label=Tex("$a$",font_size=30),start=o[0].get_right(),end=q2[0].get_left(),color=ORANGE,pos=0.2*DOWN))
        r1 = MyLabeledLine(label=Tex("$r_1$",font_size=30),pos=0.2*RIGHT,start=q2[0].get_center(),end=pt[0].get_center(),color=PINK,rot=False).set_z_index(1)
        r2 = MyLabeledLine(label=Tex("$r_2$",font_size=30),pos=0.2*LEFT,start=q1[0].get_center(),end=pt[0].get_center(),color=PINK).set_z_index(1)
        r = MyLabeledLine(label=Tex("$r$",font_size=30),pos=0.2*LEFT,start=o[0].get_center(),end=pt[0].get_center(),color=RED).set_z_index(1)
        theta = Angle(lin[1],r[0],radius=0.4,color=YELLOW)
        ang = theta.get_value()
        c = np.cos(ang)*np.cos(ang)*RIGHT+np.cos(ang)*np.sin(ang)*UP
        N = MyLabeledDot(label_out=Tex("N",font_size=30),point=2*c,radius=0.06,pos=0.3*UP).set_z_index(2)
        M = MyLabeledDot(label_out=Tex("M",font_size=30),point=-2*c,radius=0.06,pos=0.3*DL).set_z_index(2)
        line1 = DashedLine(start=q2[0].get_center(),end=N[0].get_center(),color=GOLD)
        line2 = DashedLine(start=q1[0].get_center(),end=M[0].get_center(),color=GOLD)
        line3 = DashedLine(start=o[0].get_center(),end=M[0].get_center(),color=RED)
        theta_lbl = Tex(r"$\theta$",font_size=30).next_to(theta,RIGHT,buff=0.01).shift(0.15*UP)
        theta2 = Angle(lin[0],line3,radius=0.4,color=YELLOW,quadrant=(-1,1))
        theta2_lbl= Tex(r"$\theta$",font_size=30).next_to(theta2,LEFT,buff=0.01).shift(0.15*DOWN)
        ra1= RightAngle(line2, line3, length=0.18, quadrant=(-1,-1), color=YELLOW_A)
        ra2= RightAngle(r[0], line1, length=0.18, quadrant=(-1,-1), color=YELLOW_A)
        ca1 = CurvedArrow(start_point=c,end_point=c+0.5*LEFT+0.5*UP,tip_length=0.1)
        ca1_lbl = Tex(r"$a\cos\theta$",font_size=30).rotate(ang).move_to(ca1.get_end()).shift(0.25*LEFT)
        ca2 = CurvedArrow(start_point=-c,end_point=-c+0.5*RIGHT+0.5*DOWN,tip_length=0.1)
        ca2_lbl = Tex(r"$a\cos\theta$",font_size=30).rotate(ang).move_to(ca2.get_end()).shift(0.25*RIGHT)
        img = VGroup(q1,q2,lin,o,pt,r,r1,r2,theta,theta_lbl,N,line1,M,line3,line2,theta2,theta2_lbl,ra1,ra2,ca1,ca1_lbl,ca2,ca2_lbl).to_corner(UR)

        steps1 = ItemList(Item(r"Consider a dipole of dipole moment $p=q\times 2a$",pw="10 cm"),
                          Item(r"We have to find the electric potential at point P located at a distance $r$ from the centre of the dipole (O)",pw="8.5 cm"),
                          Item(r"$\theta \rightarrow$ Angle between $r$ and dipole axis.",pw="9 cm"),
                          Item(r"Potential at point P due to $+q$ charge :",pw="9 cm"),
                          Item(r"$V_{+q}=\dfrac{1}{4\pi\epsilon_0}\dfrac{q}{r_1}$",pw="9 cm",dot=False),
                          Item(r"Potential at point P due to $-q$ charge :",pw="9 cm"),
                          Item(r"$V_{-q}=\dfrac{1}{4\pi\epsilon_0}\dfrac{-q}{r_2}$",pw="9 cm",dot=False),
                          buff=0.5).next_to(title,DOWN).to_edge(LEFT)
        
        anm1 = [VGroup(steps1[0],q1,q2,lin,o),VGroup(steps1[1],pt,r,theta,theta_lbl),steps1[2],VGroup(steps1[3],r1),steps1[4],VGroup(steps1[5],r2),steps1[6]]
        
        steps2 = ItemList(Item(r"Net potential at (P) due to the dipole:",pw="9 cm"),
                          Item(r"$V=V_{+q}+V_{-q}$",r"$=\dfrac{1}{4\pi\epsilon_0}\dfrac{q}{r_1}-\dfrac{1}{4\pi\epsilon_0}\dfrac{q}{r_2}$",pw="9 cm",dot=False),
                          Item(r"$V=\dfrac{q}{4\pi\epsilon_0}\left[\dfrac{1}{r_1}-\dfrac{1}{r_2}\right]......(1)$",color=RED,pw="9 cm",dot=False),
                          Item(r"By Geometry :",pw="9 cm"),
                          Item(r"$ON=a\cos\theta$",r"\quad and \quad $OM=a\cos\theta$",pw="9 cm",dot=False),
                          Item(r"For small/point dipole $(a<<<r)$ :",pw="9 cm"),
                          Item(r"$r_1=r-a\cos\theta$",r"\quad and \quad $r_2=r+a\cos\theta$",color=RED,pw="9 cm",dot=False),
                          Item(r"Substituting values of $r_1$ and $r_2$ in eq(1)",pw="9 cm"),
                          buff=0.4).next_to(title,DOWN).to_edge(LEFT)
        
        anm2 = [steps2[0],steps2[1],steps2[2],VGroup(steps2[3],line1,line2,line3,M,N,ra1,ra2,theta2,theta2_lbl),VGroup(steps2[4],ca1,ca1_lbl,ca2,ca2_lbl),steps2[5],steps2[6],steps2[7]]
        
        steps3 = ItemList(Item(r"$V=\dfrac{q}{4\pi\epsilon_0}\left[\dfrac{1}{(r-a\cos\theta)}-\dfrac{1}{(r+a\cos\theta)}\right]$",pw="9 cm",dot=False),
                          Item(r"$V=\dfrac{q}{4\pi\epsilon_0}\left[\dfrac{r+a\cos\theta-(r-a\cos\theta)}{r^2-a^2\cos^2\theta}\right]$",pw="9 cm",dot=False),
                          Item(r"$V=\dfrac{q}{4\pi\epsilon_0}\left[\dfrac{r+a\cos\theta-r+a\cos\theta}{r^2-a^2\cos^2\theta}\right]$",pw="9 cm",dot=False),
                          Item(r"$V=\dfrac{q}{4\pi\epsilon_0}\left[\dfrac{2a\cos\theta}{r^2-a^2\cos^2\theta}\right]$",pw="9 cm",dot=False),
                          Item(r"$V=\dfrac{1}{4\pi\epsilon_0}\left[\dfrac{p\cos\theta}{r^2-a^2\cos^2\theta}\right]\quad (\because p=q\times 2a)$",pw="9 cm",dot=False),
                          buff=0.5).next_to(title,DOWN).to_edge(LEFT)
        
        steps4 = ItemList(Item(r"Since, $r>>>a$",pw="9 cm"),
                          Item(r"$\therefore r^2-a^2\cos^2\theta\approx r^2$",pw="9 cm",dot=False),
                          Item(r"$V=\dfrac{1}{4\pi\epsilon_0}\left[\dfrac{p\cos\theta}{r^2}\right]$",color=PINK,pw="9 cm",dot=False),
                          Item(r"Special Cases -",pw="9 cm",color=PURE_GREEN),
                          Item(r"(i) When P lies on axial line of dipole $(\theta=0^\circ $ Or $180^\circ$)",pw="9 cm",dot=False),
                          Item(r"$V_{ax}=\dfrac{1}{4\pi\epsilon_0}\left[\dfrac{p\cos(0^\circ\ or\ 180^\circ)}{r^2}\right]$",pw="9 cm",dot=False),
                          Item(r"$V_{ax}=\pm \dfrac{1}{4\pi\epsilon_0}\left[\dfrac{p}{r^2}\right]$",color=PINK,pw="9 cm",dot=False),
                          buff=0.45).next_to(title,DOWN).to_edge(LEFT)
        sr = SurroundingRectangle(steps4[2])
        sr2 = SurroundingRectangle(steps4[6])
        p = Tex(r"$+$ if $\theta=0^\circ$",font_size=30).next_to(sr2,UR,buff=0).shift(2*RIGHT+0.2*DOWN)
        n = Tex(r"$-$ if $\theta=180^\circ$",font_size=30).next_to(sr2,DR,buff=0).shift(2*RIGHT+0.5*UP)
        pa = CurvedArrow(start_point=sr2.get_edge_center(RIGHT),end_point=p.get_left(),tip_length=0.1)
        na = CurvedArrow(start_point=sr2.get_edge_center(RIGHT),end_point=n.get_left(),tip_length=0.1)

        anm3 =[steps4[0],steps4[1],VGroup(steps4[2],sr),steps4[3],steps4[4],steps4[5],VGroup(steps4[6],sr2),VGroup(pa,p),VGroup(na,n)]

        steps5 = ItemList(Item(r"(ii) When P lies on equitorial line of dipole $(\theta=90^\circ)$",pw="9 cm",dot=False),
                          Item(r"$V_{eq}=\dfrac{1}{4\pi\epsilon_0}\left[\dfrac{p\cos(90^\circ)}{r^2}\right]$",pw="9 cm",dot=False),
                          Item(r"$V_{eq}=0$",color=PINK,pw="9 cm",dot=False),
                          Item(r"Potential due to electric dipole not just depend on $r$ but also on the angle $(\theta)$ between $r$ and dipole axis.",color=GOLD,pw="8 cm"),
                          Item(r"$V_{dipole}\propto \dfrac{1}{r^2}$", r" But, $V_{\text{point charge}}\propto \dfrac{1}{r}$",color=GOLD,pw="9 cm"),
                          buff=0.45).next_to(title,DOWN).to_edge(LEFT)
        sr3 = SurroundingRectangle(steps5[2])
        anm4=[steps5[0],steps5[1],VGroup(steps5[2],sr3),steps5[3],steps5[4][0],steps5[4][1]]
        self.next_slide()
        for item in anm1:
            self.play(Write(item))
            self.next_slide()
        self.play(FadeOut(steps1))
        self.wait()
        for item in anm2:
            self.play(Write(item))
            self.next_slide()
        self.next_slide()
        self.play(FadeOut(steps2))
        self.wait()
        for item in steps3:
            self.play(Write(item))
            self.next_slide()
        self.play(FadeOut(steps3))
        self.wait()
        for item in anm3:
            self.play(Write(item))
            self.next_slide()
        self.play(FadeOut(steps4,sr2,sr,p,n,pa,na))
        self.wait()
        for item in anm4:
            self.play(Write(item))
            self.next_slide()

class Ex4(Slide):
    def construct(self):

        ex_title = Tex(r"Example 4 :", r"The electric potential at a distance 3 m on the axis of a short dipole of dipole moment $4\times 10^{-2}$ coulomb-metre is",tex_environment="{minipage}{13 cm}",font_size=35, color=BLUE_C).to_corner(UP,buff=0.2).to_corner(LEFT,buff=0.2)
        ex_title[0].set_color(GREEN)
        self.play(Write(ex_title))
        self.next_slide()

        op = VGroup(Tex(r'(a) 1.33 mV ',font_size=35),Tex(r'(b) 4 mV ',font_size=35),Tex(r'(c) 12 mV',font_size=35),Tex(r'(d) 27 mV',font_size=35) ).arrange_in_grid(2,2,buff=(4,0.3),col_alignments='ll').next_to(ex_title,DOWN)

        sol_label =Tex('Solution: ',font_size=35, color=ORANGE).next_to(op,DOWN).align_to(ex_title,LEFT)
        self.play(Write(op))
        self.next_slide()
        self.play(Write(sol_label)) 
        self.next_slide(loop=True)
        self.play(Circumscribe(op[1]))

class Ex5(Slide):
    def construct(self):

        ex_title = Tex(r"Example 5 :", r"The electric potential in volts due to an electric dipole of dipole moment $2\times 10^{-8}$ coulomb-metre at a distance of 3 m on a line making an angle of $60^\circ$ with the axis of the dipole is",tex_environment="{minipage}{13 cm}",font_size=35, color=BLUE_C).to_corner(UP,buff=0.2).to_corner(LEFT,buff=0.2)
        ex_title[0].set_color(GREEN)
        self.play(Write(ex_title))
        self.next_slide()

        op = VGroup(Tex(r'(a) Zero ',font_size=35),Tex(r'(b) 10 ',font_size=35),Tex(r'(c) 20',font_size=35),Tex(r'(d) 40',font_size=35) ).arrange_in_grid(2,2,buff=(4,0.3),col_alignments='ll').next_to(ex_title,DOWN)

        sol_label =Tex('Solution: ',font_size=35, color=ORANGE).next_to(op,DOWN).align_to(ex_title,LEFT)
        self.play(Write(op))
        self.next_slide()
        self.play(Write(sol_label)) 
        self.next_slide(loop=True)
        self.play(Circumscribe(op[1]))

class Shell(Slide):
    def construct(self):
        Intro_title = Title('POTENTIAL DUE TO A UNIFORMLY CHARGED SPHERICAL SHELL', font_size=40,color=BLUE,underline_buff=SMALL_BUFF,match_underline_width_to_text=True)
        self.play(Write(Intro_title))
        self.wait()
        self.next_slide()
        shell = Circle(1.75,color=RED,stroke_width=2)
        Q =Tex(r"$Q$",font_size=30).next_to(shell,DR,buff=0).shift(0.5*UP+0.5*LEFT)
        R = MyLabeledLine(label=Tex(r"$R$",font_size=30),start=shell.get_center(),end=shell.get_boundary_point(UL),opacity=1)
        o = MyLabeledDot(label_out=Tex(r"O",font_size=30),point=shell.get_center(),radius=0.06,color=RED,pos=0.2*DOWN)
        P = MyLabeledDot(label_out=Tex(r"P",font_size=30),point=3*UP+1.5*RIGHT,radius=0.04,color=GOLD,pos=0.2*LEFT)
        r = MyLabeledLine(label=Tex(r"$r$",font_size=30),start=shell.get_center(),end=P[0].get_center(),opacity=1,color=PURPLE,rel_pos=0.75)
        line = MyDashLabeledLine(label=Tex(r"$\infty$",font_size=30),start=P[0].get_center(),end=P[0].get_center()+2*r[0].get_unit_vector(),color=PURPLE,rel_pos=1.02,opacity=1)
        q = MyLabeledDot(label_out=Tex(r"q",font_size=30),point=line.get_center(),radius=0.04,color=YELLOW,pos=0.2*DOWN)
        Ein = Tex(r"$E_{in}=0$",font_size=25).next_to(shell.get_center(),DOWN,buff=0.8)
        Eout = Tex(r"$E_{out}=\dfrac{1}{4\pi\epsilon_0}\dfrac{Q}{r^2}$",font_size=25).next_to(shell.get_top(),UP,buff=0.8)
        P2 = MyLabeledDot(label_out=Tex(r"P",font_size=30),point=1*UP+0.5*RIGHT,radius=0.04,color=GOLD,pos=0.2*LEFT)
        r2 = MyLabeledLine(label=Tex(r"$r$",font_size=30),start=shell.get_center(),end=P2[0].get_center(),opacity=1,color=PURPLE,rel_pos=0.5)
        line2 = MyDashLabeledLine(label=Tex(r"$\infty$",font_size=30),start=P2[0].get_center(),end=P2[0].get_center()+4*r2[0].get_unit_vector(),color=PURPLE,rel_pos=1.02,opacity=1)
        q2 = MyLabeledDot(label_out=Tex(r"q",font_size=30),point=line2.get_center(),radius=0.04,color=YELLOW,pos=0.2*DOWN)
        cgroup = VGroup()
        for pt in shell.get_all_points():
            cgroup.add(Tex("$\mathbf{+}$",font_size=25,color=YELLOW).move_to(pt))
        
        img = VGroup(shell,Ein,Eout,cgroup,Q,r,R,o,P,line,q,P2,r2,line2,q2).next_to(Intro_title,DOWN).to_edge(RIGHT)

        steps1 = ItemList(Item(r"Consider a uniformly charged spherical shell of Radius (R) and having charge (Q).",pw="10 cm"),
                          Item(r"We have to find the electric potential at a point P", r" which is $r$ distance from the centre of the shell.",pw="10 cm"),
                          Item(r"Case (1) : For point(P) outside the shell $(r>R)$ ",pw="9 cm",color=GREEN),
                          Item(r"$\displaystyle V_{out}=\dfrac{W_{\infty P}}{q}$",r"$\displaystyle =-\int_{\infty}^{r} \dfrac{F_E}{q}\ dr$",pw="9 cm",dot=False),
                          Item(r"$\displaystyle V_{out}=-\int_{\infty}^{P} E\ dr$", r"$\displaystyle =-\int_{\infty}^{r}\dfrac{1}{4\pi\epsilon_0}\dfrac{Q}{r^2} dr$",pw="9 cm",dot=False),
                          Item(r"$ \displaystyle V_{out}=\dfrac{1}{4\pi\epsilon_0}\dfrac{Q}{r} \quad (r>R)\quad$",r"(Same as point charge.)",pw="9 cm",dot=False,color=PINK),
                          buff=0.45).next_to(Intro_title,DOWN).to_edge(LEFT)
        
        sr = SurroundingRectangle(steps1[5][0])
        anm1 = [VGroup(steps1[0],shell,cgroup,o,Q,R,Ein,Eout),VGroup(steps1[1][0],P),VGroup(steps1[1][1],r),steps1[2],VGroup(steps1[3],line,q),steps1[4],VGroup(steps1[5][0],sr),steps1[5][1]]

        steps2 = ItemList(Item(r"Case (2) : For point(P) at the surface of the shell $(r=R)$ ",pw="9 cm",color=GREEN),
                          Item(r"$ \displaystyle V_{\text{surf}}=\dfrac{1}{4\pi\epsilon_0}\dfrac{Q}{R} \quad (r=R)$",pw="9 cm",dot=False,color=PINK),
                          buff=0.45).next_to(Intro_title,DOWN).to_edge(LEFT)
        
        steps3 = ItemList(Item(r"Case (3) : For point(P) inside the shell $(r<R)$ ",pw="9 cm",color=GREEN),
                          Item(r"$\displaystyle V_{in}=\dfrac{W_{\infty P}}{q}$",r"$\displaystyle =-\int_{\infty}^{r} \dfrac{F_E}{q}\ dr$",pw="9 cm",dot=False),
                          Item(r"$\displaystyle V_{in}=-\int_{\infty}^{P} E\ dr$", r"$\displaystyle =-\int_{\infty}^{R} E_{out}\ dr-\int_{R}^{r} E_{in}\ dr$",pw="9 cm",dot=False),
                          Item(r"$\displaystyle V_{in}=-\int_{\infty}^{R} \dfrac{1}{4\pi\epsilon_0}\dfrac{Q}{r^2}\ dr-\int_{R}^{r} 0 \ dr \quad (\because E_{in}=0)$",pw="9 cm",dot=False),
                          Item(r"$ \displaystyle V_{in}=\dfrac{1}{4\pi\epsilon_0}\dfrac{Q}{R} $", r"$=V_{\text{surf}}$ (Constant)",pw="9 cm",dot=False,color=PINK),
                          Item(r"Hence, potential remains constant inside the spherical shell, and is equal to the value at the surface. ",pw="8.3 cm",color=YELLOW_B),
                          buff=0.44).next_to(Intro_title,DOWN).to_edge(LEFT)
        
        sr2 = SurroundingRectangle(steps2[1])
        sr3 = SurroundingRectangle(steps3[4])
        anm2 = [steps2[0],VGroup(steps2[1],sr2)]

        axes_2 = (Axes(
        x_range=[0, 10, 2],
        y_range=[0, 50, 5],
        y_length=5,
        x_length=8,
        axis_config={'tip_shape': StealthTip,"tip_width":0.08,"tip_height":0.15},
        y_axis_config={"include_ticks": False}
      ).set_color(GREEN_C))
        axes_labels = axes_2.get_axis_labels(x_label=Tex(r"$r$",font_size=30), y_label=Tex(r"$V(r)$",font_size=30))

        func1 = axes_2.plot(lambda x: 35, x_range=[0, 2], color=BLUE)
        func2 = axes_2.plot(lambda x: 70/x, x_range=[2, 9.5], color=BLUE)
        lines = VGroup(axes_2.get_lines_to_point(axes_2.c2p(2,70/2),color=RED),
                       axes_2.get_lines_to_point(axes_2.c2p(4,70/4),color=RED),
                       axes_2.get_lines_to_point(axes_2.c2p(6,70/6),color=RED),
                       axes_2.get_lines_to_point(axes_2.c2p(8,70/8),color=RED),
                       Dot(axes_2.c2p(2,70/2), color=PINK),
                       Dot(axes_2.c2p(4,70/4), color=GOLD),
                       Dot(axes_2.c2p(6,70/6), color=ORANGE),
                       Dot(axes_2.c2p(8,70/8), color=WHITE),)
        axes_2.get_x_axis().add_labels({0:"O",2:"R",4:"2R",6:"3R",8:"4R"},font_size=25)
        axes_2.get_y_axis().add_labels({70/2:"V",70/4:"V/2",70/6:"V/3",70/8:"V/4"},font_size=25)
        c1 = CurvedArrow(start_point=func1.get_center(),end_point=func1.get_center()+0.8*UP+0.4*RIGHT,tip_length=0.1)
        V1 = Tex(r"$V=\dfrac{1}{4\pi\epsilon_0}\dfrac{Q}{R}\ (r<R)$",font_size=25).next_to(c1.get_end(),UP,buff=0.05)
        c2 = CurvedArrow(start_point=axes_2.c2p(5,70/5),end_point=axes_2.c2p(5,70/5)+0.8*UP+0.4*RIGHT,tip_length=0.1)
        V2 = Tex(r"$V=\dfrac{1}{4\pi\epsilon_0}\dfrac{Q}{r}\ (r>R)$",font_size=25).next_to(c2.get_end(),UP,buff=0.05)
        label = Tex("Graph of potential $(V)$ versus $r$ for spherical shell. ",font_size=30,color=GOLD).next_to(axes_2,DOWN)

        for item in anm1:
            self.play(Write(item))
            self.next_slide()
        
        self.play(FadeOut(steps1,sr))
        for item in anm2:
            self.play(Write(item))
            self.next_slide()
        self.wait()

        self.play(FadeOut(steps2,sr2,P,r,line,q),FadeIn(P2,r2,line2,q2))
        for item in steps3:
            for subitem in item:
                self.play(Write(subitem))
                self.next_slide()
        self.play(Write(sr3))
        self.next_slide()
        self.play(FadeOut(steps3,sr3,img))
        self.play(Create(axes_2),Create(axes_labels))
        self.next_slide()
        self.play(Create(VGroup(func1,c1,V1)))
        self.next_slide()
        self.play(Create(VGroup(func2,c2,V2)))
        self.next_slide()
        self.play(Create(lines),Create(label))
        self.wait(2)

class Equipotential(Slide):
    def construct(self):
        title = Title('CHAPTER 2 : ELECTROSTATIC POTENTIAL AND CAPACITANCE',font_size=40,color=GREEN,match_underline_width_to_text=True)
        Outline = Tex('Learning Objectives :',color=BLUE).next_to(title,DOWN,buff=0.5).to_corner(LEFT).scale(0.8)
        list = BulletedList('INTRODUCTION','ELECTROSTATIC POTENTIAL',r'POTENTIAL DUE TO\\ A POINT CHARGE',r'POTENTIAL DUE TO\\ A SYSTEM OF CHARGES',r'POTENTIAL DUE TO AN\\ ELECTRIC DIPOLE',' EQUIPOTENTIAL SURFACES',
                            r' RELATION BETWEEN FIELD\\ AND POTENTIAL',r'POTENTIAL ENERGY OF A SYSTEM\\ OF CHARGES').scale(0.7).next_to(Outline,DOWN).to_corner(LEFT).shift(0.1*RIGHT)

    
        list2 = BulletedList(r'POTENTIAL ENERGY IN\\ AN EXTERNAL FIELD',r'POTENTIAL ENERGY OF A DIPOLE\\ IN AN EXTERNAL FIELD','ELECTROSTATICS OF CONDUCTORS','DIELECTRICS AND POLARISATION',
                             'CAPACITORS AND CAPACITANCE','COMBINATION OF CAPACITORS',r"ENERGY STORED IN\\ A CAPACITOR").scale(0.7).next_to(Outline,DOWN).to_corner(RIGHT)
        
        self.add(title,Outline,list,list2)
        self.next_slide(loop=True)
        self.play(FocusOn(list[5]))
        self.play(Circumscribe(list[5]))
        self.next_slide()
        self.play(RemoveTextLetterByLetter(list2))
        self.play(RemoveTextLetterByLetter(list))
        self.play(RemoveTextLetterByLetter(Outline))
        Intro_title = Title('EQUIPOTENTIAL SURFACES', font_size=40,color=BLUE,underline_buff=SMALL_BUFF,match_underline_width_to_text=True)
        self.play(ReplacementTransform(title,Intro_title))
        self.next_slide()
        steps1 = ItemList(Item(r"A surface, which has same electrostatic potential at every point is called equipotential surface.",pw="8 cm"),
                          Item(r"For a single point charge $(Q)$",pw="6 cm",color=GREEN),
                          Item(r"$V=\dfrac{1}{4\pi\epsilon_0}\dfrac{Q}{r}$",pw="6 cm"),
                          Item(r"if $r$ is same (constant) the $V$ is also same (constant)",pw="6 cm",color=PINK),
                          Item(r"Thus equipotential surfaces of a single point charge are ", r"concentric spherical surfaces ", r" centred at the charge.",pw="6 cm"),
                          buff=0.45).next_to(Intro_title,DOWN).to_edge(LEFT).set_z_index(2)
        
        img1 = ImageMobject("equip1.png").scale(1.2).next_to(steps1[3],RIGHT).align_to(steps1[0],UP).set_z_index(1)
        img2 = ImageMobject("equip2.png").scale(1.2).next_to(Intro_title,DOWN)
        img2_lbl = Tex(r"Equipotential surfaces for a dipole",font_size=35).next_to(img2,DOWN)
        img3 = ImageMobject("equip3.png").scale(1.3).next_to(Intro_title,DOWN)
        img3_lbl = Tex(r"Equipotential surfaces for two identical positive charges.",font_size=35).next_to(img3,DOWN)
        img4 = ImageMobject("equip4.png").scale(1).next_to(Intro_title,DOWN)
        img4_lbl = Tex(r"Equipotential surfaces for a uniform electric field.",font_size=35).next_to(img4,DOWN)
        steps1[4][1].set_color(YELLOW)
        anm1 = [Write(steps1[0]),Write(steps1[1]),Write(steps1[2]),Write(steps1[3]),FadeIn(img1),Write(steps1[4])]

        prop_title = Tex(r"Properties of equipotential surfaces",font_size=40,color=PURE_GREEN).next_to(Intro_title,DOWN).to_edge(LEFT)
        steps2 = ItemList(Item(r"The work done in moving any charge(q) over an equipotential surface is always zero.",pw="13 cm"),
                          Item(r"We know that $ \Delta V_{AB}=(V_A-V_B)=\dfrac{W_{BA}}{q}$",pw="7 cm",dot=False),
                          Item(r"$\because V_A = V_B$ (Points on equipotential surface)",pw="7 cm",color=GREEN,dot=False),
                          Item(r"$\therefore W_{BA} = q(V_A-V_B)=0$",pw="7 cm",color=YELLOW,dot=False),
                          buff=0.5).next_to(prop_title,DOWN,buff=0.6).to_edge(LEFT).set_z_index(2)
        img5 = ImageMobject("equip5.png").scale(0.8).next_to(steps2[1],RIGHT).align_to(steps2[1],UP)

        steps3 = ItemList(Item(r"The electric field at every point is normal to the equipotential surface passing through that point.",pw="13 cm"),
                          Item(r"We know that $dW = Fdr\cos\theta$",r"$=qEdr\cos\theta$",pw="7 cm",dot=False),
                          Item(r"$\because dW = 0$ (Work done over equipotential surface = 0)",pw="9 cm",color=GREEN,dot=False),
                          Item(r"$\therefore dW = qEdr\cos\theta = 0$",pw="7 cm",dot=False),
                          Item(r"Neither $q$ nor $E$ is zero; $dr$ is also not zero.",pw="7 cm",dot=False),
                          Item(r"So, $\cos\theta=0\quad$ ", r"Or\quad $\theta=90^\circ$",pw="7 cm",color=YELLOW,dot=False),
                          buff=0.5).next_to(prop_title,DOWN,buff=0.6).to_edge(LEFT).set_z_index(2)
        img6 = ImageMobject("equip6.png").scale(0.9).next_to(steps3[4],RIGHT).align_to(steps3[2],UP)

        steps4 = ItemList(Item(r"In a region, where electric field $(\vec{E})$ is strong equipotential surfaces are close together, and where $(\vec{E})$ is weaker, the equipotential surfaces are farther apart.",pw="7 cm"),
                          Item(r"Two equipotential surfaces never intersect each other.",pw="7 cm"),
                          Item(r"As electric field is perpendicular to the equipotential surface their intersection means that there are two directions of electric field at the intersection point which is not possible.",pw="7 cm",color=GREEN,dot=False),
                          buff=0.5).next_to(prop_title,DOWN,buff=0.6).to_edge(LEFT).set_z_index(2)
        img7 = ImageMobject("equip7.png").scale(1.1).next_to(steps4,RIGHT)
        
        for item in anm1:
            self.play(item)
            self.next_slide()

        self.play(Succession(FadeOut(steps1,img1),FadeIn(img2),Write(img2_lbl)))
        self.next_slide()
        self.play(Succession(FadeOut(img2_lbl,img2),FadeIn(img3),Write(img3_lbl)))
        self.next_slide()
        self.play(Succession(FadeOut(img3_lbl,img3),FadeIn(img4),Write(img4_lbl))) 
        self.next_slide()
        self.play(Succession(FadeOut(img4_lbl,img4),Write(prop_title))) 
        self.next_slide()
        self.play(FadeIn(img5))
        for item in steps2:
            self.play(Write(item))
            self.next_slide()

        self.play(Succession(FadeOut(img5,steps2),FadeIn(img6)))
        for item in steps3:
            self.play(Write(item))
            self.next_slide()
        
        self.play(Succession(FadeOut(img6,steps3),FadeIn(img7)))
        for item in steps4:
            self.play(Write(item))
            self.next_slide()



class Relation(Slide):
    def construct(self):
        title = Title('CHAPTER 2 : ELECTROSTATIC POTENTIAL AND CAPACITANCE',font_size=40,color=GREEN,match_underline_width_to_text=True)
        Outline = Tex('Learning Objectives :',color=BLUE).next_to(title,DOWN,buff=0.5).to_corner(LEFT).scale(0.8)
        list = BulletedList('INTRODUCTION','ELECTROSTATIC POTENTIAL',r'POTENTIAL DUE TO\\ A POINT CHARGE',r'POTENTIAL DUE TO\\ A SYSTEM OF CHARGES',r'POTENTIAL DUE TO AN\\ ELECTRIC DIPOLE',' EQUIPOTENTIAL SURFACES',
                            r' RELATION BETWEEN FIELD\\ AND POTENTIAL',r'POTENTIAL ENERGY OF A SYSTEM\\ OF CHARGES').scale(0.7).next_to(Outline,DOWN).to_corner(LEFT).shift(0.1*RIGHT)

    
        list2 = BulletedList(r'POTENTIAL ENERGY IN\\ AN EXTERNAL FIELD',r'POTENTIAL ENERGY OF A DIPOLE\\ IN AN EXTERNAL FIELD','ELECTROSTATICS OF CONDUCTORS','DIELECTRICS AND POLARISATION',
                             'CAPACITORS AND CAPACITANCE','COMBINATION OF CAPACITORS',r"ENERGY STORED IN\\ A CAPACITOR").scale(0.7).next_to(Outline,DOWN).to_corner(RIGHT)
        
        self.add(title,Outline,list,list2)
        self.next_slide(loop=True)
        self.play(FocusOn(list[6]))
        self.play(Circumscribe(list[6]))
        self.next_slide()
        self.play(RemoveTextLetterByLetter(list2))
        self.play(RemoveTextLetterByLetter(list))
        self.play(RemoveTextLetterByLetter(Outline))
        Intro_title = Title('RELATION BETWEEN FIELD AND POTENTIAL', font_size=40,color=BLUE,underline_buff=SMALL_BUFF,match_underline_width_to_text=True)
        self.play(ReplacementTransform(title,Intro_title))
        self.next_slide()
        steps1 = ItemList(Item(r"Consider two closely spaced equipotential surfaces with potential values $V$ and $V + dV$.",pw="13 cm",color=GREEN),
                          Item(r"$dr$  is the perpendicular distance between the two equipotential surfaces.",pw="13 cm",color=GREEN),
                          Item(r" Imagine that a unit positive charge $(q)$ is moved from point A to point B",pw="13 cm",color=GREEN),
                          Item(r"$d\vec{s}$ is the displacement vector from A to B",pw="8 cm",color=GREEN),
                          Item(r"Work done by the electric field $\vec{E}$ is",pw="8 cm",color=ORANGE),
                          Item(r"$dW_{\text{field}} = \vec{F_E}\cdot d\vec{s}$ ",r"$=q\vec{E}\cdot d\vec{s}$",pw="8 cm",dot=False,color=ORANGE),
                          Item(r"$dW_{\text{field}} = qE ds\cos\theta$ ",r"$=qE dr\ (\because dr=ds\cos\theta)$",pw="8 cm",dot=False,color=ORANGE),
                          Item(r"Change in Potential energy $= -$ Work done by field:",pw="8 cm",color=YELLOW_C),
                          Item(r"$dU= - dW_{\text{field}} $",r"$=-qE dr$",color=YELLOW_C,pw="8 cm",dot=False),
                          buff=0.45).next_to(Intro_title,DOWN).to_edge(LEFT).set_z_index(2)
        
        img1 = ImageMobject("rel1.png").scale(1).next_to(steps1[4],RIGHT).align_to(steps1[3],UP).to_edge(RIGHT)
        img2 = ImageMobject("rel2.png").scale(1).next_to(steps1[4],RIGHT).align_to(steps1[3],UP).to_edge(RIGHT)
        anm1 = [Succession(FadeIn(img1),Write(steps1[0])),Write(steps1[1]),Succession(FadeIn(img2),Write(steps1[2])),Write(steps1[3]),Write(steps1[4]),Write(steps1[5][0]),Write(steps1[5][1]),Write(steps1[6][0]),Write(steps1[6][1]),Write(steps1[7]),Write(steps1[8][0]),Write(steps1[8][1]),Succession(FadeOut(steps1[0:7]),VGroup(steps1[7],steps1[8]).animate.next_to(Intro_title,DOWN).to_corner(LEFT),Group(img1,img2).animate.next_to(Intro_title,DOWN).to_corner(RIGHT))]
        
        for item in anm1:
            self.play(item)
            self.next_slide()

        steps2 = ItemList(Item(r"Change in Potential $dV=\dfrac{dU}{q}$",pw="8 cm",color=RED),
                          Item(r"$dV =- E dr$",color=PURE_RED,pw="8 cm",dot=False),
                          Item(r"$E=-\dfrac{dV}{dr}$",color=PURE_RED,pw="8 cm",dot=False),
                          Item(r"Electric field is in the direction in which the potential decreases steepest.",color=GOLD,pw="13 cm"),
                          Item(r"Magnitude of Electric field is given by the change in the magnitude of potential (dV) per unit displacement (dr) normal to the equipotential surface at the point.",color=GOLD,pw="13 cm"),
                          buff=0.45).next_to(steps1[8],DOWN).to_edge(LEFT).set_z_index(2)
        
        sr1 = SurroundingRectangle(steps2[1])
        sr2 = SurroundingRectangle(steps2[2])
        anm2 = [Write(steps2[0]),Succession(Write(steps2[1]),Write(sr1)),Succession(Write(steps2[2]),Write(sr2)),Write(steps2[3]),Write(steps2[4])]
        for item in anm2:
            self.play(item)
            self.next_slide()

class Ex6(Slide):
    def construct(self):

        ex_title = Tex(r"Example 6 :", r"The electric potential $V$ at a point  $P(x,y,z)$ in space is given by $V=4x^2$ volt. Electric field at point (1m, 0, 2m) in V/m is",tex_environment="{minipage}{13 cm}",font_size=35, color=BLUE_C).to_corner(UP,buff=0.2).to_corner(LEFT,buff=0.2)
        ex_title[0].set_color(GREEN)
        self.play(Write(ex_title))
        self.next_slide()

        op = VGroup(Tex(r'(a) 8 along -ve x-axis ',font_size=35),Tex(r'(b) 8 along +ve x-axis ',font_size=35),Tex(r'(c) 16 along -ve x-axis',font_size=35),Tex(r'(d) 16 along +ve x-axis ',font_size=35) ).arrange_in_grid(2,2,buff=(4,0.3),col_alignments='ll').next_to(ex_title,DOWN)

        sol_label =Tex('Solution: ',font_size=35, color=ORANGE).next_to(op,DOWN).align_to(ex_title,LEFT)
        self.play(Write(op))
        self.next_slide()
        self.play(Write(sol_label)) 
        self.next_slide(loop=True)
        self.play(Circumscribe(op[0]))

class Ex7(Slide):
    def construct(self):

        ex_title = Tex(r"Example 7 :", r"Figure shows the variation of electric field intensity $E$ versus distance $x$. What is the potential difference between the points at $x=2$ m and $x=6$ m from O?",tex_environment="{minipage}{13 cm}",font_size=35, color=BLUE_C).to_corner(UP,buff=0.2).to_corner(LEFT,buff=0.2)
        ex_title[0].set_color(GREEN)
        self.play(Write(ex_title))
        self.next_slide()

        op = VGroup(Tex(r'(a) 30 V',font_size=35),Tex(r'(b) 60 V',font_size=35),Tex(r'(c) 40 V',font_size=35),Tex(r'(d) 80 V ',font_size=35) ).arrange_in_grid(2,2,buff=(4,0.3),col_alignments='ll').next_to(ex_title,DOWN)

        sol_label =Tex('Solution: ',font_size=35, color=ORANGE).next_to(op,DOWN).align_to(ex_title,LEFT)
        axes_2 = (Axes(
        x_range=[0, 8, 2],
        y_range=[0, 15, 5],
        y_length=3,
        x_length=5,
        axis_config={'tip_shape': StealthTip,"tip_width":0.08,"tip_height":0.15,"include_numbers": True},
        y_axis_config={"include_ticks": True,"exclude_origin_tick":False}
      ).set_color(GREEN_C)).next_to(sol_label,DOWN).to_edge(RIGHT)
        axes_labels = axes_2.get_axis_labels(x_label=Tex(r"$x(m)$",font_size=30), y_label=Tex(r"$E\ (N/C)$",font_size=30))
        axes_2.get_x_axis().add_labels({0:Tex("O",color=GREEN)})
        

        func1 = axes_2.plot(lambda x: 5*x, x_range=[0, 2], color=BLUE)
        func2 = axes_2.plot(lambda x: 10, x_range=[2, 4], color=BLUE)
        func3 = axes_2.plot(lambda x: -5*x+30, x_range=[4, 6], color=BLUE)
        lines = VGroup(axes_2.get_lines_to_point(axes_2.c2p(2,10),color=RED),
                       axes_2.get_lines_to_point(axes_2.c2p(4,10),color=RED),)
        
        self.next_slide()
        self.play(Create(axes_2),Create(axes_labels))
        self.wait(1)
        self.play(Succession(Create(func1),Create(func2),Create(func3),Create(lines)))
        self.next_slide()
        self.play(Write(op))
        self.next_slide()
        self.play(Write(sol_label)) 
        self.next_slide(loop=True)
        self.play(Circumscribe(op[0]))


class Ex8(Slide):
    def construct(self):

        ex_title = Tex(r"Example 8 :", r"An infinite plane sheet of charge density $10^{-8}\ Cm^{-2}$ is held in air. In this situation how far apart are two equipotential surfaces, whose potential difference is 5 V?",tex_environment="{minipage}{13 cm}",font_size=35, color=BLUE_C).to_corner(UP,buff=0.2).to_corner(LEFT,buff=0.2)
        ex_title[0].set_color(GREEN)
        self.play(Write(ex_title))
        self.next_slide()

        op = VGroup(Tex(r'(a) 2.25 mm ',font_size=35),Tex(r'(b) 3.52 mm ',font_size=35),Tex(r'(c) 6 mm',font_size=35),Tex(r'(d) 8.85 mm ',font_size=35) ).arrange_in_grid(2,2,buff=(4,0.3),col_alignments='ll').next_to(ex_title,DOWN)

        sol_label =Tex('Solution: ',font_size=35, color=ORANGE).next_to(op,DOWN).align_to(ex_title,LEFT)
        self.play(Write(op))
        self.next_slide()
        self.play(Write(sol_label)) 
        self.next_slide(loop=True)
        self.play(Circumscribe(op[3]))

class Ex9(Slide):
    def construct(self):

        ex_title = Tex(r"Example 9 :", r"A uniform electric field $E$ of 500 N/C is directed along +x-axis. O, B and A are three points in the field having x- and y-coordinates (in cm) (0, 0), (4, 0) and  (0, 3) respectively. Calculate the potential difference between the points (i) O and A, and (ii) O and B. \quad [CBSE 23C]",tex_environment="{minipage}{13 cm}",font_size=35, color=BLUE_C).to_corner(UP,buff=0.2).to_corner(LEFT,buff=0.2)
        ex_title[0].set_color(GREEN)
        fig = VGroup()
        for i in [3.5,2.5,1.5,0.5,-0.5]:
            fig.add(Arrow(start=1*LEFT+i*UP,end=5*RIGHT+i*UP,color=RED,tip_length=0.2))
        
        fig.add(MyLabeledDot(label_out=Tex(r"O\\ (0,0)",font_size=30),pos=0.2*DOWN,radius=0.04),MyLabeledDot(label_out=Tex(r"B\\ (4,0)",font_size=30),point=4*RIGHT,pos=0.2*DOWN,radius=0.04),MyLabeledDot(label_out=Tex(r"A\\ (0,3)",font_size=30),point=3*UP,pos=0.2*LEFT,radius=0.04),Tex(r"E",font_size=30,color=RED).shift(5.2*RIGHT+1.5*UP))
        fig.add(DashedLine(start=0*LEFT+0*UP,end=4*RIGHT,color=GREEN_B),
                DashedLine(start=0*LEFT+0*UP,end=3*UP,color=GREEN_B))
        ex_title[0].set_color(GREEN)
        self.play(Write(ex_title))
        self.next_slide()
        sol_label =Tex('Solution: ',font_size=35, color=ORANGE).next_to(ex_title,DOWN).align_to(ex_title,LEFT)
        self.play(Write(sol_label)) 
        self.play(Write(fig.next_to(ex_title,DOWN).to_edge(RIGHT)))
        
class Ex10(Slide):
    def construct(self):

        ex_title = Tex(r"Example 10 :", r"Three points A, B and C lie in a uniform electric field $(E)$ of $5\times 10^3\ NC^{-1}$ as shown in the figure. Find the potential difference between A and C. [CBSE F 09]",tex_environment="{minipage}{13 cm}",font_size=35, color=BLUE_C).to_corner(UP,buff=0.2).to_corner(LEFT,buff=0.2)
        fig = VGroup()
        for i in [2,1,0,-1]:
            fig.add(Arrow(start=3*LEFT+i*UP,end=3*RIGHT+i*UP,color=RED,tip_length=0.2))
        
        fig.add(MyLabeledDot(label_out=Tex(r"A",font_size=30),point=LEFT+1.5*UP,pos=0.2*LEFT,radius=0.02),MyLabeledDot(label_out=Tex(r"B",font_size=30),point=RIGHT+1.5*UP,pos=0.2*RIGHT,radius=0.02),MyLabeledDot(label_out=Tex(r"C",font_size=30),point=RIGHT-0.5*UP,pos=0.2*RIGHT,radius=0.02),Tex(r"E",font_size=30,color=RED).shift(3.2*RIGHT))
        ex_title[0].set_color(GREEN)
        fig.add(MyDashLabeledLine(label=Tex("5 cm",font_size=30),pos=0.3*DOWN,start=LEFT+1.5*UP,end=RIGHT-0.5*UP,color=GREEN_B),
                MyDashLabeledLine(label=Tex("3 cm",font_size=30),pos=0.3*RIGHT,start=RIGHT+1.5*UP,end=RIGHT-0.5*UP,color=GREEN_B),
                DashedLine(start=LEFT+1.5*UP,end=RIGHT+1.5*UP,color=GREEN_B))
        self.play(Write(ex_title),Write(fig.next_to(ex_title,DOWN).to_edge(RIGHT)))
        sol_label =Tex('Solution: ',font_size=35, color=ORANGE).next_to(ex_title,DOWN).align_to(ex_title,LEFT)
        self.next_slide()
        self.play(Write(sol_label)) 


class Ex11(Slide):
    def construct(self):

        ex_title = Tex(r"Example 11 :", r"If the potential in the region of space around the point (-1 m, 2 m, 3 m) is given by $V=(10x^2+5y^2-3z^2)$ volt, calculate the three components of electric field at this point.",tex_environment="{minipage}{13 cm}",font_size=35, color=BLUE_C).to_corner(UP,buff=0.2).to_corner(LEFT,buff=0.2)
        ex_title[0].set_color(GREEN)
        self.play(Write(ex_title))
        self.next_slide()
        sol_label =Tex('Solution: ',font_size=35, color=ORANGE).next_to(ex_title,DOWN).align_to(ex_title,LEFT)
        self.play(Write(sol_label)) 

class SystemEnergy(Slide):
    def construct(self):
        title = Title('CHAPTER 2 : ELECTROSTATIC POTENTIAL AND CAPACITANCE',font_size=40,color=GREEN,match_underline_width_to_text=True)
        Outline = Tex('Learning Objectives :',color=BLUE).next_to(title,DOWN,buff=0.1).to_corner(LEFT).scale(0.8)
        list = BulletedList('INTRODUCTION','ELECTROSTATIC POTENTIAL',r'POTENTIAL DUE TO\\ A POINT CHARGE',r'POTENTIAL DUE TO\\ A SYSTEM OF CHARGES',r'POTENTIAL DUE TO AN\\ ELECTRIC DIPOLE',' EQUIPOTENTIAL SURFACES',
                            r' RELATION BETWEEN FIELD\\ AND POTENTIAL').scale(0.7).next_to(Outline,DOWN,buff=0.2).to_corner(LEFT).shift(0.1*RIGHT)

    
        list2 = BulletedList(r'POTENTIAL ENERGY OF A SYSTEM\\ OF CHARGES',r'POTENTIAL ENERGY IN\\ AN EXTERNAL FIELD',r'POTENTIAL ENERGY OF A DIPOLE\\ IN AN EXTERNAL FIELD','ELECTROSTATICS OF CONDUCTORS','DIELECTRICS AND POLARISATION',
                             'CAPACITORS AND CAPACITANCE','COMBINATION OF CAPACITORS',r"ENERGY STORED IN A CAPACITOR").scale(0.7).next_to(Outline,DOWN,buff=0.2).to_corner(RIGHT)
        
        self.add(title,Outline,list,list2)
        self.next_slide(loop=True)
        self.play(FocusOn(list2[0]))
        self.play(Circumscribe(list2[0]))
        self.next_slide()
        self.play(RemoveTextLetterByLetter(list2))
        self.play(RemoveTextLetterByLetter(list))
        self.play(RemoveTextLetterByLetter(Outline))
        Intro_title = Title('POTENTIAL ENERGY OF A SYSTEM OF CHARGES', font_size=40,color=BLUE,underline_buff=SMALL_BUFF,match_underline_width_to_text=True)
        self.play(ReplacementTransform(title,Intro_title))
        self.next_slide(loop=True)

        steps1 = ItemList(Item(r"The electric potential energy of a system of fixed point charges is equal to the work that must be done by an external agent to assemble the system, bring the charges in from  an infinite distance.",pw="10 cm",color=YELLOW_D),
                          Item(r"Work done in moving charge $q_1$ first from $\infty$ to A:",pw="7.6 cm"),
                          Item(r"$W_{q_1}=0\ ...(1)\ (\because$ no electrostatic force acting on it) ",pw="8 cm",dot=False),
                          Item(r"Work done in moving charge $q_2$ from $\infty$ to B:",pw="7.3 cm"),
                          Item(r"$W_{q_2}=q_2\times V_{q_1B}\ ( V_{q_1B}\rightarrow$ Potential due to $q_2$ at B.)",pw="8 cm",dot=False),
                          Item(r"$W_{q_2}=q_2\times \dfrac{1}{4\pi\epsilon_0}\dfrac{q_1}{r_{12}}$",pw="8 cm",dot=False),
                          Item(r"$W_{q_2}= \dfrac{1}{4\pi\epsilon_0}\dfrac{q_1q_2}{r_{12}}\ ...(2)$",pw="8 cm",dot=False),
                          buff=0.42).next_to(Intro_title,DOWN).to_edge(LEFT,buff=0.2)
        
        steps2 = ItemList(Item(r"Work done in moving charge $q_3$ from $\infty$ to C:",pw="11 cm"),
                          Item(r"$W_{q_3}=q_3\times V_{q_1q_2C}\ ( V_{q_1q_2C}\rightarrow$ Potential due to $q_1$ and $q_2$ at C.)",pw="11 cm",dot=False),
                          Item(r"$W_{q_3}=q_3\times \left[\dfrac{1}{4\pi\epsilon_0}\dfrac{q_1}{r_{13}}+\dfrac{1}{4\pi\epsilon_0}\dfrac{q_3}{r_{23}}\right]$",pw="8 cm",dot=False),
                          Item(r"$W_{q_3}= \dfrac{1}{4\pi\epsilon_0}\left[\dfrac{q_1q_3}{r_{13}}+\dfrac{q_2q_3}{r_{23}}\right]\ ...(3)$",pw="8 cm",dot=False),
                          Item(r"Total work done in assembling the system of charges:",color=ORANGE,pw="8 cm"),
                          Item(r"$W=W_{q_1}+W_{q_2}+W_{q_3}$",color=ORANGE,pw="8 cm",dot=False),
                          Item(r"$W=0+\dfrac{1}{4\pi\epsilon_0}\dfrac{q_1q_2}{r_{12}}+\dfrac{1}{4\pi\epsilon_0}\left[\dfrac{q_1q_3}{r_{13}}+\dfrac{q_2q_3}{r_{23}}\right]$",color=ORANGE,pw="8 cm",dot=False),
                          buff=0.42).next_to(Intro_title,DOWN).to_edge(LEFT,buff=0.2)

        axes = (Axes(
        x_range=[0, 10, 2],
        y_range=[0, 10, 2],
        y_length=4.5,
        x_length=5,
        axis_config={'tip_shape': StealthTip,"tip_width":0.08,"tip_height":0.15,"include_ticks":False},
      ).set_color(GREEN_C))
        axes.get_x_axis().add_labels({0:Tex("O",color=GREEN_C)})
        A = MyLabeledDot(label_out=Tex(r"A",font_size=30,color=RED),point=axes.c2p(2,8.5),radius=0.04,pos=0.4*LEFT,color=RED)
        B = MyLabeledDot(label_out=Tex(r"B",font_size=30,color=YELLOW),point=axes.c2p(5,2),radius=0.04,pos=0.4*DOWN,color=YELLOW)
        C = MyLabeledDot(label_out=Tex(r"C",font_size=30,color=GREEN),point=axes.c2p(8,7.5),radius=0.04,pos=0.4*RIGHT,color=GREEN)
        inf = MyLabeledDot(label_out=Tex(r"$\infty$",font_size=30,color=GOLD),point=axes.c2p(10.5,13.5),radius=0.01,pos=0.2*UP,
        color=GREEN)
        r12 = MyLabeledLine(label=Tex(r"$r_{12}$",font_size=30),pos=0.2*LEFT,start=A[0].get_center(),end=B[0].get_center(),color=DARK_BROWN)
        r23 = MyLabeledLine(label=Tex(r"$r_{23}$",font_size=30),pos=0.2*RIGHT,start=B[0].get_center(),end=C[0].get_center(),color=DARK_BROWN)
        r13 = MyLabeledLine(label=Tex(r"$r_{13}$",font_size=30),pos=0.2*UP,start=A[0].get_center(),end=C[0].get_center(),color=DARK_BROWN)
        q1 = MyLabeledDot(label_in=Tex(r"$q_1$",font_size=25,color=BLACK),point=axes.c2p(9.5,12.75),color=RED)
        q2 = MyLabeledDot(label_in=Tex(r"$q_2$",font_size=25,color=BLACK),point=axes.c2p(10,12.75),color=YELLOW)
        q3 = MyLabeledDot(label_in=Tex(r"$q_3$",font_size=25,color=BLACK),point=axes.c2p(10.5,12.75),color=GREEN)
        fig = VGroup(axes,A,B,C,inf,r12,r13,r23,q1,q2,q3).next_to(Intro_title,DOWN).to_edge(RIGHT,buff=0.1)
        self.play(Write(fig))
        self.play(MoveAlongPath(q1,Line(start=q1[0].get_center(),end=A[0].get_center())))
        self.wait()
        self.play(MoveAlongPath(q2,Line(start=q2[0].get_center(),end=B[0].get_center())))
        self.wait()
        self.play(MoveAlongPath(q3,Line(start=q3[0].get_center(),end=C[0].get_center())))
        self.wait()
        self.next_slide()
        self.play(Write(steps1[0]))
        self.next_slide()
        self.play(q1.animate.move_to(axes.c2p(9.5,12.75)),q2.animate.move_to(axes.c2p(10,12.75)),q3.animate.move_to(axes.c2p(10.5,12.75)))
        self.play(Write(steps1[1]),MoveAlongPath(q1,Line(start=q1[0].get_center(),end=A[0].get_center())))
        self.next_slide()
        self.play(Write(steps1[2]))
        self.next_slide()
        self.play(Write(steps1[3]),MoveAlongPath(q2,Line(start=q2[0].get_center(),end=B[0].get_center())))
        self.next_slide()
        self.play(Write(steps1[4]))
        self.next_slide()
        self.play(Write(steps1[5]))
        self.next_slide()
        self.play(Write(steps1[6]))
        self.next_slide()
        self.play(FadeOut(steps1))
        self.play(Write(steps2[0]),MoveAlongPath(q3,Line(start=q3[0].get_center(),end=C[0].get_center())))
        self.next_slide()
        self.play(Write(steps2[1]))
        self.next_slide()
        self.play(Write(steps2[2]))
        self.next_slide()
        self.play(Write(steps2[3]))
        self.next_slide()
        self.play(Write(steps2[4]))
        self.next_slide()
        self.play(Write(steps2[5]))
        self.next_slide()
        self.play(Write(steps2[6]))
        self.next_slide()
        self.play(FadeOut(steps2[0:4]),VGroup(steps2[4:7]).animate.next_to(Intro_title,DOWN).to_edge(LEFT,buff=0.2))
        steps3 = ItemList(Item(r"This work don by external agent gets stored in the form of potential energy (U) of the system of charges",color=YELLOW,pw="7 cm"),
                          Item(r"$U=\dfrac{1}{4\pi\epsilon_0}\left[\dfrac{q_1q_2}{r_{12}}+\dfrac{q_1q_3}{r_{13}}+\dfrac{q_2q_3}{r_{23}}\right]$",pw="8 cm",color=YELLOW,dot=False),
                          Item(r"The potential energy (U) of a system of charges is independent of the manner in which the configuration of charges is assembled.",color=GOLD,pw="7 cm"),
                          buff=0.42).next_to(steps2[6],DOWN).to_edge(LEFT)
        for item in steps3:
            self.play(Write(item))
            self.next_slide()
        self.play(Write(SurroundingRectangle(steps3[1],color=PINK)))
        self.wait(3)

class Ex12(Slide):
    def construct(self):

        ex_title = Tex(r"Example 12 :", r"Four charges are arranged at the corners of a square ABCD of side d, as shown in Fig.\\(a) Find the work required to put together this arrangement.\\", r"(b) A charge $q_0$ is brought to the centre E of the square, the four charges being held fixed at its corners. How much extra work is needed to do this? [NCERT]",tex_environment="{minipage}{13 cm}",font_size=35, color=BLUE_C).to_corner(UP,buff=0.2).to_corner(LEFT,buff=0.2)
        sq = Square(4)
        q1 = MyLabeledDot(label_in=Tex(r"$+q$",font_size=25,color=BLACK),label_out=Tex(r"$A$",font_size=25),pos=0.2*LEFT,point=2*UP+2*LEFT,color=RED)
        q2 = MyLabeledDot(label_in=Tex(r"$-q$",font_size=25,color=BLACK),label_out=Tex(r"$B$",font_size=25),pos=0.2*RIGHT,point=2*UP+2*RIGHT,color=RED)
        q3 = MyLabeledDot(label_in=Tex(r"$+q$",font_size=25,color=BLACK),label_out=Tex(r"$C$",font_size=25),pos=0.2*RIGHT,point=2*DOWN+2*RIGHT,color=RED)
        q4 = MyLabeledDot(label_in=Tex(r"$-q$",font_size=25,color=BLACK),label_out=Tex(r"$D$",font_size=25),pos=0.2*LEFT,point=2*DOWN+2*LEFT,color=RED)
        q0 = MyLabeledDot(label_in=Tex(r"$q_0$",font_size=25,color=BLACK),label_out=Tex(r"$E$",font_size=25),pos=0.2*DOWN,point=sq.get_center(),color=YELLOW)
        d = Tex(r"$d$",font_size=25).next_to(sq,RIGHT,buff=0.1)
        fig = VGroup(sq,q1,q2,q3,q4,d,q0).next_to(ex_title,DOWN).to_edge(RIGHT)
        ex_title[0].set_color(GREEN)
        self.play(Write(ex_title[0:2]),Write(fig[0:-1]))
        self.next_slide()
        self.play(Write(ex_title[2]),Write(q0))
        self.next_slide()
        sol_label =Tex('Solution: ',font_size=35, color=ORANGE).next_to(ex_title,DOWN).align_to(ex_title,LEFT)
        self.play(Write(sol_label)) 


class Ex13(Slide):
    def construct(self):

        ex_title = Tex(r"Example 13 :", r"(a) Determine the electrostatic potential energy of a system consisting of two charges 7 $\mu$C and $-2\ \mu C$ (and with no external field) placed at $(-9$ cm, 0, 0) and (9 cm, 0, 0) respectively.\\ \\",r"(b) How much work is required to separate the two charges infinitely away from each other?\\ \\",r"(c) Suppose that the same system of charges is now placed in an external electric field $E = A \left(\dfrac{1}{r^2}\right)$; $A = 9 \times 10^5\ NC^{-1} m^2$. What would the electrostatic energy of the configuration be? [NCERT]",tex_environment="{minipage}{13 cm}",font_size=35, color=BLUE_C).to_corner(UP,buff=0.2).to_corner(LEFT,buff=0.2)
        ex_title[0].set_color(GREEN)
        for item in ex_title:
            self.play(Write(item))
            self.next_slide()
        sol_label =Tex('Solution: ',font_size=35, color=ORANGE).next_to(ex_title,DOWN).align_to(ex_title,LEFT)
        self.play(Write(sol_label)) 

class Ex14(Slide):
    def construct(self):

        ex_title = Tex(r"Example 14 : ", r"Two protons are separated by a distance $R$. What will be the speed of each proton when they reach infinity under their mutual repulsion?",tex_environment="{minipage}{13 cm}",font_size=35, color=BLUE_C).to_corner(UP,buff=0.2).to_corner(LEFT,buff=0.2)
        ex_title[0].set_color(GREEN)
        for item in ex_title:
            self.play(Write(item))
            self.next_slide()
        sol_label =Tex('Solution: ',font_size=35, color=ORANGE).next_to(ex_title,DOWN).align_to(ex_title,LEFT)
        self.play(Write(sol_label)) 

class Ex15(Slide):
    def construct(self):

        ex_title = Tex(r"Example 15 : ", r"Two particles have equal masses of 5 g each and opposite charges of $4\times 10^{-5}$ C and $-4\times 10^{-5}$ C. They are released from rest with a separation of 1 m between them. Find the speed of particles when the separation is reduced to 50 cm.",tex_environment="{minipage}{13 cm}",font_size=35, color=BLUE_C).to_corner(UP,buff=0.2).to_corner(LEFT,buff=0.2)
        ex_title[0].set_color(GREEN)
        for item in ex_title:
            self.play(Write(item))
            self.next_slide()
        sol_label =Tex('Solution: ',font_size=35, color=ORANGE).next_to(ex_title,DOWN).align_to(ex_title,LEFT)
        self.play(Write(sol_label)) 

class DipolePE(Slide):
    def construct(self):
        title = Title('CHAPTER 2 : ELECTROSTATIC POTENTIAL AND CAPACITANCE',font_size=40,color=GREEN,match_underline_width_to_text=True)
        Outline = Tex('Learning Objectives :',color=BLUE).next_to(title,DOWN,buff=0.1).to_corner(LEFT).scale(0.8)
        list = BulletedList('INTRODUCTION','ELECTROSTATIC POTENTIAL',r'POTENTIAL DUE TO\\ A POINT CHARGE',r'POTENTIAL DUE TO\\ A SYSTEM OF CHARGES',r'POTENTIAL DUE TO AN\\ ELECTRIC DIPOLE',' EQUIPOTENTIAL SURFACES',
                            r' RELATION BETWEEN FIELD\\ AND POTENTIAL').scale(0.7).next_to(Outline,DOWN,buff=0.2).to_corner(LEFT).shift(0.1*RIGHT)

    
        list2 = BulletedList(r'POTENTIAL ENERGY OF A SYSTEM\\ OF CHARGES',r'POTENTIAL ENERGY IN\\ AN EXTERNAL FIELD',r'POTENTIAL ENERGY OF A DIPOLE\\ IN AN EXTERNAL FIELD','ELECTROSTATICS OF CONDUCTORS','DIELECTRICS AND POLARISATION',
                             'CAPACITORS AND CAPACITANCE','COMBINATION OF CAPACITORS',r"ENERGY STORED IN A CAPACITOR").scale(0.7).next_to(Outline,DOWN,buff=0.2).to_corner(RIGHT)
        
        self.add(title,Outline,list,list2)
        self.next_slide(loop=True)
        self.play(FocusOn(list2[2]))
        self.play(Circumscribe(list2[2]))
        self.next_slide()
        self.play(RemoveTextLetterByLetter(list2))
        self.play(RemoveTextLetterByLetter(list))
        self.play(RemoveTextLetterByLetter(Outline))
        Intro_title = Title('POTENTIAL ENERGY OF A DIPOLE IN AN EXTERNAL FIELD', font_size=40,color=BLUE,underline_buff=SMALL_BUFF,match_underline_width_to_text=True)
        self.play(ReplacementTransform(title,Intro_title))
        self.next_slide()

        steps1 = ItemList(Item(r"Consider a dipole of dipole moment $p=q\times 2a$,", r" placed in a uniform external field $\vec{E}$.",pw="13 cm",color=YELLOW_D),
                          Item(r"Torque experienced by dipole $\tau=pE\sin\theta$",pw="7.6 cm"),
                          Item(r"Work done$(dW)$ by external torque ($\vec{\tau}_{ext}=\vec{\tau}$) in rotating the dipole from angle $\theta_{i}$ to $(\theta_{i}+d\theta)$ ",pw="7.8 cm"),
                          Item(r"$dW = \tau_{ext}\ d\theta$",r"$ =pE\sin\theta\ d\theta$",pw="7.3 cm",dot=False),
                          Item(r"Now, total work done by external torque in rotating the dipole from $\theta_{i}$ to $\theta_{f}$",pw="6.5 cm",dot=False),
                          Item(r"$W= \displaystyle \int_{\theta_i}^{\theta_f} pE\sin\theta \ d\theta$",r"$ = -pE\left[ \cos\theta \right]_{\theta_i}^{\theta_f}$",pw="8 cm",dot=False),
                          Item(r"$W= -pE\left[\cos\theta_f-\cos\theta_i\right]$",pw="8 cm",dot=False),
                          buff=0.42).next_to(Intro_title,DOWN).to_edge(LEFT,buff=0.2)
        
        
        arrowgroup = VGroup()

        for i in range(5):
            arrowgroup.add(Arrow(start=ORIGIN,end=4.5*RIGHT,tip_length=0.2,color=GREY,buff=0).set_z_index(0).shift(i*0.8*DOWN))

        arrowgroup.add(Tex(r"$\vec{E}$",font_size=35).next_to(arrowgroup,DR,buff=0).shift(0.7*UP)).set_z_index(1)
        lin =  Line(end=[3.5,-0.6,0],start= [1,-2.8,0],color=PINK).set_z_index(2)
        q1 = always_redraw(lambda:MyLabeledDot(label_in=Tex("$+$",font_size=25,color=BLACK),label_out=Tex("$+q$",font_size=30,color=BLUE),pos=0.2*UP,point=lin.get_end(),color=BLUE)).set_z_index(2)
        q2 = always_redraw(lambda:MyLabeledDot(label_in=Tex("$-$",font_size=25,color=BLACK),label_out=Tex("$-q$",font_size=30,color=GREEN),color=GREEN,pos=0.2*DOWN,point=lin.get_start())).set_z_index(2)
        p  = always_redraw(lambda: Arrow(start=lin[0].get_center()-1.205*lin[0].get_unit_vector(),end= lin[0].get_center()+1.205*lin[0].get_unit_vector(),color=RED,tip_length=0.2)).set_z_index(2)
        bline = DashedLine(start=lin[0].get_center(),end=lin[0].get_center()+1.5*RIGHT,stroke_width=2,color=BLUE).set_z_index(2)
        ang = Angle(bline,lin[0],radius=0.4,quadrant=(1,1),color=YELLOW).set_z_index(2)
        anglbl = Tex(r"$\theta_i$",font_size=30,color=YELLOW).next_to(ang,RIGHT,buff=0.1).set_z_index(2)
        d2 = VGroup(DashedLine(end=[3.5,-0.6,0],start= [1,-2.8,0],color=PINK),q1.copy(),q2.copy(), MyLabeledArrow(label=Tex(r"$\vec{p}$",font_size=30,color=RED),start=lin[0].get_center()-1*lin[0].get_unit_vector(),end= lin[0].get_center()+1*lin[0].get_unit_vector(),color=RED,rel_pos=0.2,opacity=1,tip_length=0.2)).set_z_index(2)
        dang = always_redraw(lambda:Angle(lin[0],d2[0][0],radius=0.5,quadrant=(1,1),color=WHITE,other_angle=True)).set_z_index(2)
        dang_lbl = always_redraw(lambda:Tex(r"$d\theta$",font_size=30,color=WHITE).next_to(dang,UR,buff=0.01)).set_z_index(2)
        ca1 = CurvedArrow(start_point=q1[0].get_left(),end_point=q1[0].get_left()+0.5*LEFT+0.5*UP,tip_length=0.1,color=BLUE_C)
        ca1_lbl = Tex(r"$\tau_{\text{ext}}$",font_size=30,color=BLUE_C).move_to(ca1.get_end()).shift(0.25*LEFT)
        ca2 = CurvedArrow(start_point=q2[0].get_right(),end_point=q2[0].get_right()+0.5*RIGHT+0.5*DOWN,tip_length=0.1,color=BLUE_C)
        ca2_lbl = Tex(r"$\tau_{\text{ext}}$",font_size=30,color=BLUE_C).move_to(ca2.get_end()).shift(0.25*RIGHT)
        fig = VGroup(arrowgroup,lin,q1,q2,p,bline,ang,anglbl,d2,dang,ca1,ca1_lbl,ca2,ca2_lbl,dang_lbl).next_to(Intro_title,DOWN).to_corner(DR,buff=0.8)

        ca3 = ArcBetweenPoints(start=q1[0].get_right()-0.5*LEFT-0.5*UP,end=q1[0].get_right(),color=GREEN_B).add_tip(at_start=True,tip_shape=ArrowTriangleFilledTip,tip_width=0.1,tip_length=0.1)
        ca3_lbl = Tex(r"$\tau$",font_size=30,color=GREEN_B).move_to(ca3.get_start()).shift(0.25*RIGHT)
        ca4 = ArcBetweenPoints(start=q2[0].get_left()-0.5*RIGHT-0.5*DOWN,end=q2[0].get_left(),color=GREEN_B).add_tip(at_start=True,tip_shape=ArrowTriangleFilledTip,tip_width=0.1,tip_length=0.1)
        ca4_lbl = Tex(r"$\tau$",font_size=30,color=GREEN_B).move_to(ca4.get_start()).shift(0.25*LEFT)
        VGroup(ca1,ca1_lbl,ca3,ca3_lbl).next_to(q1[0].get_center(),UR,buff=0.1)
        VGroup(ca2,ca2_lbl,ca4,ca4_lbl).next_to(q2[0].get_center(),DL,buff=0)
        fig = VGroup(arrowgroup,lin,q1,q2,p,bline,ang,anglbl,d2,dang,ca3,ca3_lbl,ca4,ca4_lbl,ca1,ca1_lbl,ca2,ca2_lbl,dang_lbl).next_to(Intro_title,DOWN).to_corner(DR,buff=0.3)

        anm1 = [Write(VGroup(steps1[0][0],q1,q2,lin,p,d2)),Write(VGroup(steps1[0][1],arrowgroup,bline,ang,anglbl)),Write(VGroup(steps1[1],ca3,ca3_lbl,ca4,ca4_lbl)), Succession(Write(VGroup(steps1[2],ca1,ca1_lbl,ca2,ca2_lbl)),lin.set_z_index(1).animate.rotate(angle=30*DEGREES),Succession(Write(dang),Write(dang_lbl))), Write(steps1[3][0]), Write(steps1[3][1]), Write(steps1[4]), Write(steps1[5][0]), Write(steps1[5][1]), Write(steps1[6]),Succession(FadeOut(steps1[0:-1]),steps1[6].animate.next_to(Intro_title,DOWN).to_edge(LEFT,buff=0.2))]
        
        for item in anm1:
            self.play(item)
            self.next_slide()
        steps2 = ItemList(Item(r"This work done (W) is equal to the change in potential energy $(\Delta U)$ of the dipole",pw="13 cm",color=YELLOW_D),
                          Item(r"$\Delta U = U_{\theta_f}-U_{\theta_i}= -pE\left[\cos\theta_f-\cos\theta_i\right]$",color=PINK,pw="8 cm",dot=False),
                          Item(r" There is a freedom in choosing the angle where the potential energy $U$ is taken to be zero.", r" A natural choice is to take $\theta_i=\dfrac{\pi}{2}\ Or\ 90^\circ$. Or $(U_{90^\circ}=0)$ ",pw="8cm"),
                          Item(r"$ U_{\theta}-U_{90^\circ}= -pE\left[\cos\theta-\cos (90^\circ)\right]$",pw="8 cm",dot=False),
                          Item(r"$ U_{\theta}= -pEcos\theta$",color=PINK,pw="8 cm",dot=False),
                          Item(r"Case 1: if $\theta = 0^\circ \rightarrow \ U_{min} = -PE $(Stable Equilibrium)",color=GOLD,pw="11 cm"),
                          Item(r"Case 2: if $\theta = 180^\circ \rightarrow \ U_{max} = PE $(Unstable Equilibrium)",color=GOLD,pw="11 cm"),
                          buff=0.42).next_to(steps1[6],DOWN).to_edge(LEFT,buff=0.2)
        sr = SurroundingRectangle(steps2[1])
        sr2 = SurroundingRectangle(steps2[4])
        arrow = MyLabeledArrow(label=Tex("Potential Energy",font_size=35),start=sr2.get_right(),end=sr2.get_right()+1*RIGHT,tip_length=0.2,rel_pos=2.5,opacity=0)
        arrow2 = MyLabeledArrow(label=Tex("Change in Potential Energy",font_size=35),start=sr.get_right(),end=sr.get_right()+1*RIGHT,tip_length=0.2,rel_pos=3.2,opacity=0)
        
        anm2 = [Write(steps2[0]),Succession(Write(steps2[1]),Write(sr),Write(arrow2)),Write(steps2[2][0]),Write(steps2[2][1]),Write(steps2[3]),Succession(Write(steps2[4]),Write(sr2),Write(arrow)),Write(steps2[5]),Write(steps2[6])]
        for item in anm2:
            self.play(item)
            self.next_slide()


class Ex16(Slide):
    def construct(self):

        ex_title = Tex(r"Example 16 :", r"An electric dipole of length 2 cm is placed with its axis making an angle of $30^\circ$ to a uniform electric field $10^5$ N/C. If it experiences a torque of $10\sqrt{3}$ Nm, then potential energy of the dipole ",tex_environment="{minipage}{13 cm}",font_size=35, color=BLUE_C).to_corner(UP,buff=0.2).to_corner(LEFT,buff=0.2)
        ex_title[0].set_color(GREEN)
        self.play(Write(ex_title))
        self.next_slide()

        op = VGroup(Tex(r'(a) -10 J ',font_size=35),Tex(r'(b) -20 J ',font_size=35),Tex(r'(c) -30 J',font_size=35),Tex(r'(d) -40 J ',font_size=35) ).arrange_in_grid(2,2,buff=(4,0.3),col_alignments='ll').next_to(ex_title,DOWN)

        sol_label =Tex('Solution: ',font_size=35, color=ORANGE).next_to(op,DOWN).align_to(ex_title,LEFT)
        self.play(Write(op))
        self.next_slide()
        self.play(Write(sol_label)) 
        self.next_slide(loop=True)
        self.play(Circumscribe(op[3]))



class Ex17(Slide):
    def construct(self):

        ex_title = Tex(r"Example 17 : ", r"An electric dipole in a uniform electric field E is turned from $\theta =0^\circ$ position to $\theta=60^\circ$ position. Find work done by the field.",tex_environment="{minipage}{13 cm}",font_size=35, color=BLUE_C).to_corner(UP,buff=0.2).to_corner(LEFT,buff=0.2)
        ex_title[0].set_color(GREEN)
        for item in ex_title:
            self.play(Write(item))
            self.next_slide()
        sol_label =Tex('Solution: ',font_size=35, color=ORANGE).next_to(ex_title,DOWN).align_to(ex_title,LEFT)
        self.play(Write(sol_label)) 


class Ex18(Slide):
    def construct(self):

        ex_title = Tex(r"Example 17 : ", r"A molecule of a substance has a permanent electric dipole moment of magnitude $10^{-29}$ C m. A mole of this substance is polarized (at low temperature) by applying a strong electrostatic field of magnitude $10^6\ V m^{-1}$. The direction of the field is suddenly changed by an angle of $60^\circ$. Estimate the heat released by the substance in aligning its dipoles along the new direction of the field. For simplicity, assume 100\% polarisation of the sample.",tex_environment="{minipage}{13 cm}",font_size=35, color=BLUE_C).to_corner(UP,buff=0.2).to_corner(LEFT,buff=0.2)
        ex_title[0].set_color(GREEN)
        for item in ex_title:
            self.play(Write(item))
            self.next_slide()
        sol_label =Tex('Solution: ',font_size=35, color=ORANGE).next_to(ex_title,DOWN).align_to(ex_title,LEFT)
        self.play(Write(sol_label)) 



class Conductor(Slide):
    def construct(self):
        title = Title('CHAPTER 2 : ELECTROSTATIC POTENTIAL AND CAPACITANCE',font_size=40,color=GREEN,match_underline_width_to_text=True)
        Outline = Tex('Learning Objectives :',color=BLUE).next_to(title,DOWN,buff=0.1).to_corner(LEFT).scale(0.8)
        list = BulletedList('INTRODUCTION','ELECTROSTATIC POTENTIAL',r'POTENTIAL DUE TO\\ A POINT CHARGE',r'POTENTIAL DUE TO\\ A SYSTEM OF CHARGES',r'POTENTIAL DUE TO AN\\ ELECTRIC DIPOLE',' EQUIPOTENTIAL SURFACES',
                            r' RELATION BETWEEN FIELD\\ AND POTENTIAL').scale(0.7).next_to(Outline,DOWN,buff=0.2).to_corner(LEFT).shift(0.1*RIGHT)

    
        list2 = BulletedList(r'POTENTIAL ENERGY OF A SYSTEM\\ OF CHARGES',r'POTENTIAL ENERGY IN\\ AN EXTERNAL FIELD',r'POTENTIAL ENERGY OF A DIPOLE\\ IN AN EXTERNAL FIELD','ELECTROSTATICS OF CONDUCTORS','DIELECTRICS AND POLARISATION',
                             'CAPACITORS AND CAPACITANCE','COMBINATION OF CAPACITORS',r"ENERGY STORED IN A CAPACITOR").scale(0.7).next_to(Outline,DOWN,buff=0.2).to_corner(RIGHT)
        
        self.add(title,Outline,list,list2)
        self.next_slide(loop=True)
        self.play(FocusOn(list2[3]))
        self.play(Circumscribe(list2[3]))
        self.next_slide()
        self.play(RemoveTextLetterByLetter(list2))
        self.play(RemoveTextLetterByLetter(list))
        self.play(RemoveTextLetterByLetter(Outline))
        Intro_title = Title('ELECTROSTATICS OF CONDUCTORS', font_size=40,color=BLUE,underline_buff=SMALL_BUFF,match_underline_width_to_text=True)
        self.play(ReplacementTransform(title,Intro_title))
        self.next_slide()
        title = Tex(r"Conductors :",font_size=40,color=ORANGE).next_to(Intro_title,DOWN).to_edge(LEFT,buff=0.1)
        self.play(Write(title))
        steps1 = ItemList(Item(r"Conductors contains mobile/free charge carriers.",pw="13 cm"),
                          Item(r"In metals charge carriers are outer (valance) electrons,", r" They are free to move within the metal but not free to leave the metal. ",pw="13 cm",color=YELLOW_D),
                          Item(r"In an external field the free electrons drifts in opposite direction of field.", r" But the nuclei and bound electron remain held in their fixed position.",pw="13 cm"),
                          Item(r"In electrolytic conductors the charge carriers are both positive and negative ions.",pw="13 cm"),
                          Item(r"Electrostatic Condition $\rightarrow$ Assuming charges at rest.",color=PINK,pw="13 cm"),
                          buff=0.5).next_to(title,DOWN).to_edge(LEFT,buff=0.3)
        
        for item in steps1:
            for subitem in item:
                self.play(Write(subitem))
                self.next_slide()

        self.play(FadeOut(steps1,title))

        steps2 = ItemList(Item(r"Under electrostatic condition, the conductors have following properties-",color=RED_D,pw="13 cm"),
                          Item(r"(1) Inside a conductor, electrostatic  field is zero.",pw="8 cm",color=YELLOW_D),
                          Item(r"Consider a charged/neutral conductor. There may also be an external field.",pw="8 cm",dot=False),
                          Item(r"If there is a net electric field inside a conductor the free electrons will experience force and starts moving which results in the flow of current and violates the static condition.",dot=False,color=PINK,pw="9 cm"),
                          Item(r"Therefore, In static situation there is no current inside or at the surface, the free charges have so distribute themselves that electric field is zero everywhere inside the conductor.",pw="9 cm",dot=False),
                          buff=0.5).next_to(title,DOWN).to_edge(LEFT,buff=0.3)
        cond_img = SVGMobject("conductor.svg",fill_color=GREY_D,stroke_color=TEAL,stroke_width=5)
        cond_lbl = Tex("Conductor",font_size=35).next_to(cond_img,DOWN,buff=-0.35)
        Ein = Tex(r"$E_{\text{in}}=0$",font_size=35,color=YELLOW).move_to(cond_img.get_center())
        img1 = VGroup(cond_img,cond_lbl,Ein).next_to(steps2[1],RIGHT).align_to(steps2[1],UP).to_edge(RIGHT,buff=0.1)
        cond_img = SVGMobject("conductor.svg",fill_color=GREY_D,stroke_color=TEAL,stroke_width=5)
        cond_lbl = Tex("Conductor",font_size=35).next_to(cond_img,DOWN,buff=-0.35)
        Ein = Tex(r"If $E_{\text{in}}\neq 0$",font_size=35,color=YELLOW).move_to(cond_img.get_center()+0.25*DOWN)
        E = MyLabeledArrow(label=Tex(r"$\vec{E}_{in}$",font_size=30),pos=0.25*UP,start=cond_img.get_center()+0.5*UP+0.5*RIGHT,end=cond_img.get_center()+0.5*UP-0.5*RIGHT,tip_length=0.2,color=GREEN_D)
        e = MyLabeledDot(label_in=Tex("$-$",font_size=30),point=cond_img.get_center()+0.25*UP+1.5*LEFT,color=PINK)
        img2 = VGroup(cond_img,cond_lbl,Ein,e,E).next_to(img1,DOWN,buff=0.5).to_edge(RIGHT,buff=0.1)
        
        steps3 = ItemList(Item(r"(2) At the surface of a charged conductor, electrostatic field must be normal to the surface at every point",color=YELLOW_D,pw="8 cm"),
                          Item(r"If E were not normal to the surface, it would have some non-zero component along the surface.", r" Free charges on the surface of the conductor would then experience force and move.",pw="8 cm",dot=False),
                          Item(r"In the static situation, therefore, E should have no tangential component.",pw="8 cm",dot=False),
                          Item(r"$E\cos\theta=0\quad $",r"Or $\cos\theta=0$",dot=False,pw="13 cm"),
                          Item(r"$\theta=90^\circ $",dot=False,pw="13 cm"),
                          buff=0.5).next_to(title,DOWN).to_edge(LEFT,buff=0.3)
        
        cond_img = SVGMobject("conductor.svg",fill_color=GREY_D,stroke_color=TEAL,stroke_width=5)
        cond_lbl = Tex("Conductor",font_size=35).next_to(cond_img,DOWN,buff=-0.35)
        E = MyLabeledArrow(label=Tex(r"$\vec{E}$",font_size=30),pos=0.25*LEFT,start=cond_img.get_top(),end=cond_img.get_top()+1*UP,tip_length=0.2,color=GREEN_D)
        line = DashedLine(start=cond_img.get_top(),end=cond_img.get_top()+0.5*RIGHT)
        rang = RightAngle(line,E,length=0.2)
        img3 = VGroup(cond_img,cond_lbl,E,rang).next_to(steps2[0],RIGHT).align_to(steps2[0],UP).to_edge(RIGHT,buff=0.1)

        cond_img = SVGMobject("conductor.svg",fill_color=GREY_D,stroke_color=TEAL,stroke_width=5)
        cond_lbl = Tex("Conductor",font_size=35).next_to(cond_img,DOWN,buff=-0.35)
        E = MyLabeledArrow(label=Tex(r"$\vec{E}$",font_size=30),pos=0.25*LEFT,start=cond_img.get_top()-0.5*LEFT,end=cond_img.get_top()-0.5*LEFT+0.8*UP+0.6*RIGHT,tip_length=0.2,color=GREEN_D)
        line = DashedLine(start=cond_img.get_top(),end=cond_img.get_top()+0.5*RIGHT)
        ang = Angle(line,E,radius=0.2)
        e2 = MyLabeledDot(label_in=Tex("$-$",font_size=30),point=cond_img.get_top()-0.5*LEFT,color=PINK)
        ang_lbl = Tex(r"$\theta$",font_size=35).next_to(ang,RIGHT,buff=0.05)
        img4 = VGroup(cond_img,cond_lbl,E,ang,e2,ang_lbl).next_to(img3,DOWN,buff=0.5).to_edge(RIGHT,buff=0.1)
        

        steps4 = ItemList(Item(r"(3)  The interior of a conductor can have no excess charge in the static situation, any excess charge must reside at the surface.",color=YELLOW_D,pw="13 cm"),
                          buff=0.5).next_to(title,DOWN).to_edge(LEFT,buff=0.3)
        
        cond_img = SVGMobject("conductor.svg",fill_color=GREY_D,stroke_color=TEAL,stroke_width=5)
        cond_lbl = Tex("Conductor",font_size=35).next_to(cond_img,DOWN,buff=-0.35)
        qin = Tex(r"$q_{\text{in}}=0$ or $\rho=0$",font_size=35,color=YELLOW).move_to(cond_img.get_center()+0.3*UP)
        Ein = Tex(r"$E_{\text{in}}=0$",font_size=35,color=YELLOW).move_to(cond_img.get_center()+0.25*DOWN)
        q = VGroup()
        for pt in cond_img.get_all_points():
            q.add(Tex(r"-",font_size=40,color=ORANGE).move_to(pt))
            
        img5 = VGroup(cond_img,cond_lbl,Ein,qin,q).next_to(steps4[0],DOWN).to_edge(RIGHT,buff=0.1)
        
        steps5 = ItemList(Item(r"(4)  Electrostatic potential is constant throughout the volume of the conductor and has the same value (as inside) on its surface",color=YELLOW_D,pw="13 cm"),
                          Item(r" At each point on the surface of a conductor electric potential is same Or the surface of conductor is an equipotential surface.",color=YELLOW_D,pw="13 cm"),
                          Item(r"Using $dV = -E\ dr$",color=RED,pw="8 cm",dot=False),
                          Item(r" $\displaystyle \int_{V_{\text{surf}}}^{V_{in}}dV = \int_{R}^{r}-E\ dr$",color=RED,pw="8 cm",dot=False),
                          Item(r" $V_{\text{in}}-V_{\text{surf}} = 0\quad (\because E_{\text{in}}=0)$",color=RED,pw="8 cm",dot=False),
                          Item(r"$V_{\text{in}} = V_{\text{surf}} = $ Constant",color=PINK,pw="8 cm",dot=False),
                          buff=0.5).next_to(title,DOWN).to_edge(LEFT,buff=0.3)
        
        cond_img = SVGMobject("conductor.svg",fill_color=GREY_D,stroke_color=TEAL,stroke_width=5)
        cond_lbl = Tex("Conductor",font_size=35).next_to(cond_img,DOWN,buff=-0.35)
        qin = Tex(r"$V_{\text{in}}=V_{\text{surf}} = $ Constant",font_size=35,color=YELLOW).move_to(cond_img.get_center()+0.3*UP)
        Ein = Tex(r"$E_{\text{in}}=0$",font_size=35,color=YELLOW).move_to(cond_img.get_center()+0.25*DOWN)
        E = MyLabeledArrow(label=Tex(r"$\vec{E}$",font_size=30),pos=0.25*LEFT,start=cond_img.get_top(),end=cond_img.get_top()+1*UP,tip_length=0.2,color=GREEN_D)
        line = DashedLine(start=cond_img.get_top(),end=cond_img.get_top()+0.5*RIGHT)
        rang = RightAngle(line,E,length=0.2)
        q = VGroup()
        for pt in cond_img.get_all_points():
            q.add(Tex(r"-",font_size=40,color=ORANGE).move_to(pt))
            
        img6 = VGroup(cond_img,cond_lbl,Ein,qin,q,E,rang).next_to(steps5[1],DOWN).to_edge(RIGHT,buff=0.1)
        
        steps6 = ItemList(Item(r"(5)  Electric field at the surface of a charged conductor: $\vec{E}=\dfrac{\sigma}{\epsilon_0}\hat{n}$",color=YELLOW_D,pw="13 cm"),
                          Item(r"Using Gauss's law : $\oint E\ dS = \dfrac{q}{\epsilon_0}$",dot=False,pw="13 cm"),
                          Item(r"$E\oint dS = \dfrac{\sigma A}{\epsilon_0}$",dot=False,pw="13 cm"),
                          Item(r"$EA = \dfrac{\sigma A}{\epsilon_0}$",dot=False,pw="13 cm"),
                          Item(r"$E = \dfrac{\sigma }{\epsilon_0}$",color=PINK,dot=False,pw="13 cm"),
                          buff=0.5).next_to(title,DOWN).to_edge(LEFT,buff=0.3)
        
        steps7 = ItemList(Item(r"(6) Electrostatic shielding",color=YELLOW_D,pw="13 cm"),
                          Item(r"Whatever be the charge and field configuration outside, any cavity (having no charges) in a conductor remains shielded from outside electric influence: the field inside the cavity is always zero. This is known as electrostatic shielding.",color=ORANGE,pw="8 cm"),
                          Item(r" Shielding effect can be made use of in protecting sensitive instruments from outside electrical influence.",color=BLUE,pw="13 cm"),
                          buff=0.5).next_to(title,DOWN).to_edge(LEFT,buff=0.3)
        
        cond_img = SVGMobject("cavity.svg",stroke_color=TEAL,stroke_width=5)
        cond_lbl = Tex("Conductor",font_size=35).next_to(cond_img,DOWN,buff=-0.35)
        qin = Tex(r"if $q=0$ ",font_size=32,color=YELLOW).move_to(cond_img.get_center()+0.35*UP)
        Ein = Tex(r"$E_{\text{in}}=0$",font_size=32,color=YELLOW).move_to(cond_img.get_center())
        cav = Tex(r"Cavity",font_size=32).move_to(cond_img.get_center()+0.35*DOWN)
            
        img7 = VGroup(cond_img,cond_lbl,Ein,qin,cav).next_to(steps7[0],DOWN).to_edge(RIGHT,buff=0.1)

        cond_img = SVGMobject("surface.svg").scale(1.5)
        cond_lbl = Tex("Conductor",font_size=35).next_to(cond_img,DOWN,buff=-0.35)
        E= Tex(r"$\vec{E}$",font_size=32,color=YELLOW).move_to(cond_img.get_center()).move_to(cond_img.get_top()+0.2*LEFT)
        Ein = Tex(r"$E_{\text{in}}=0$",font_size=32,color=RED).move_to(cond_img.get_top()+2.6*DOWN)
        ds = Tex(r"$d\vec{S}$",font_size=32,color=GREEN).move_to(cond_img.get_top()+0.55*RIGHT)
        sigma = Tex(r"$\sigma$",font_size=32,color=PINK).move_to(cond_img.get_center()+0.1*UP)
        img8 = VGroup(cond_img,Ein,E,ds,sigma).next_to(steps7[0],DOWN).to_edge(RIGHT,buff=0.1)


        for i in range(0,len(steps2)):
            self.play(Write(steps2[i]))
            if i == 1:
                self.play(Write(img1))
            if i == 3:
                self.play(Write(img2))
                self.wait(5)
                self.play(MoveAlongPath(e,Line(start=e.get_center(),end=e.get_center()+2.7*RIGHT),run_time=4))
            self.next_slide()

        self.play(FadeOut(steps2,img1,img2))

        for i in range(0,len(steps3)):
            self.play(Write(steps3[i]))
            if i == 0:
                self.play(Write(img3))
            if i == 1:
                self.play(Write(img4))
                self.wait(5)
                self.play(MoveAlongPath(e2,Line(start=e2.get_center(),end=e2.get_center()-1.7*RIGHT),run_time=4))
            self.next_slide()
        
        self.play(FadeOut(steps3,img3,img4))

        for i in range(0,len(steps4)):
            self.play(Write(steps4[i]))
            if i == 0:
                self.play(Write(img5))
            self.next_slide()

        self.play(FadeOut(steps4,img5))

        for i in range(0,len(steps5)):
            self.play(Write(steps5[i]))
            if i == 0:
                self.play(Write(img6))
            self.next_slide()

        self.play(FadeOut(steps5,img6))

        for i in range(0,len(steps6)):
            self.play(Write(steps6[i]))
            if i == 0:
                self.play(Write(img8))
                self.wait(2)
            self.next_slide()

        self.play(FadeOut(steps6,img8))

        for i in range(0,len(steps7)):
            self.play(Write(steps7[i]))
            if i == 0:
                self.play(Write(img7))
            self.next_slide()

        self.play(FadeOut(steps7))

class Dielectric(Slide):
    def construct(self):
        title = Title('CHAPTER 2 : ELECTROSTATIC POTENTIAL AND CAPACITANCE',font_size=40,color=GREEN,match_underline_width_to_text=True)
        Outline = Tex('Learning Objectives :',color=BLUE).next_to(title,DOWN,buff=0.1).to_corner(LEFT).scale(0.8)
        list = BulletedList('INTRODUCTION','ELECTROSTATIC POTENTIAL',r'POTENTIAL DUE TO\\ A POINT CHARGE',r'POTENTIAL DUE TO\\ A SYSTEM OF CHARGES',r'POTENTIAL DUE TO AN\\ ELECTRIC DIPOLE',' EQUIPOTENTIAL SURFACES',
                            r' RELATION BETWEEN FIELD\\ AND POTENTIAL').scale(0.7).next_to(Outline,DOWN,buff=0.2).to_corner(LEFT).shift(0.1*RIGHT)

    
        list2 = BulletedList(r'POTENTIAL ENERGY OF A SYSTEM\\ OF CHARGES',r'POTENTIAL ENERGY IN\\ AN EXTERNAL FIELD',r'POTENTIAL ENERGY OF A DIPOLE\\ IN AN EXTERNAL FIELD','ELECTROSTATICS OF CONDUCTORS','DIELECTRICS AND POLARISATION',
                             'CAPACITORS AND CAPACITANCE','COMBINATION OF CAPACITORS',r"ENERGY STORED IN A CAPACITOR").scale(0.7).next_to(Outline,DOWN,buff=0.2).to_corner(RIGHT)
        
        self.add(title,Outline,list,list2)
        self.next_slide(loop=True)
        self.play(FocusOn(list2[4]))
        self.play(Circumscribe(list2[4]))
        self.next_slide()
        self.play(RemoveTextLetterByLetter(list2))
        self.play(RemoveTextLetterByLetter(list))
        self.play(RemoveTextLetterByLetter(Outline))
        Intro_title = Title('DIELECTRICS AND POLARISATION', font_size=40,color=BLUE,underline_buff=SMALL_BUFF,match_underline_width_to_text=True)
        self.play(ReplacementTransform(title,Intro_title))
        self.next_slide()

        steps1 = ItemList(Item(r"Dielectrics are non-conducting substances. ",r"They have no (or negligible number of) charge carriers.",pw="13 cm"),
                          Item(r"Examples: Glass, wax, water, air, wood, rubber, plastic, etc. ",pw="13 cm",color=YELLOW_D),
                          buff=0.5).next_to(title,DOWN).to_edge(LEFT,buff=0.3)
        
        title = Tex(r"Behaviour of a conductor and dielectric in the presence of an external field :",font_size=35,color=ORANGE).next_to(Intro_title,DOWN).to_edge(LEFT,buff=0.1)
        steps2 = ItemList(Item(r"When a conductor is placed in an external field $(\vec{E}_0)$. ",r" The free charge carriers moves and charge distribution adjust itself itself in such a way that the electric field due to induced charge $\vec{E}_{\text{ind}}$ cancels the external field $(\vec{E}_0)$ which results in net zero electrostatic field inside.",pw="7.2 cm"),
                          Item(r"In dielectric charges are not free to move because they are tightly bounded to the atom. ",pw="7.2 cm",color=YELLOW_D),
                          Item(r"When dielectric is placed in an external field $(\vec{E}_0)$. ",r"This field induces dipole moment by stretching or reorienting molecules of the dielectric. ", r"Due to the induced dipoles charges builds on the surface which produces an electric field $(\vec{E}_{\text{ind}})$ that opposes the external field but does not exactly cancel the external field. It only reduces it.",pw="13 cm",color=GOLD),
                          buff=0.55).next_to(title,DOWN).to_edge(LEFT,buff=0.3)
        cond = RoundedRectangle(corner_radius=0.8,height=1.854,width=3,fill_opacity=0.3,fill_color=RED_E)
        cond_lbl = Tex("Conductor",font_size=35).next_to(cond,DOWN,buff=-0.35)
        qin = Tex(r"$E_{\text{net}}=0$",font_size=35,color=YELLOW).move_to(cond.get_center()+0.35*DOWN)
        Eo = MyLabeledArrow(label=Tex(r"$\vec{E}_{0}$",font_size=30),pos=0.25*UP,start=cond.get_top()+0.5*DOWN+0.5*LEFT,end=cond.get_top()+0.5*DOWN+0.5*RIGHT,tip_length=0.2,color=GREEN_D)
        Eo1 = MyLabeledArrow(label=Tex(r"$\vec{E}_{0}$",font_size=30),pos=0.5*DOWN,start=cond.get_top()+0.5*DOWN+2.8*LEFT,end=cond.get_top()+0.5*DOWN+1.8*LEFT,tip_length=0.2,color=GREEN_D)
        Eo2 = Arrow(start=cond.get_top()+1.6*DOWN+2.8*LEFT,end=cond.get_top()+1.6*DOWN+1.8*LEFT,tip_length=0.2,color=GREEN_D,buff=0)
        Eo3 = MyLabeledArrow(label=Tex(r"$\vec{E}_{0}$",font_size=30),pos=0.5*DOWN,start=cond.get_top()+0.5*DOWN+1.8*RIGHT,end=cond.get_top()+0.5*DOWN+2.8*RIGHT,tip_length=0.2,color=GREEN_D)
        Eo4 = Arrow(start=cond.get_top()+1.6*DOWN+1.8*RIGHT,end=cond.get_top()+1.6*DOWN+2.8*RIGHT,tip_length=0.2,color=GREEN_D,buff=0)
        Ein = MyLabeledArrow(label=Tex(r"$\vec{E}_{\text{ind}}$",font_size=30),pos=0.25*UP,start=cond.get_top()+0.95*DOWN+0.5*RIGHT,end=cond.get_top()+0.95*DOWN+0.5*LEFT,tip_length=0.2,color=BLUE_D)
        img1= VGroup(cond,Eo,Eo1,Eo2,Eo3,Eo4)
        for i in [-0.87,-0.6,-0.3,0,0.3,0.6,0.87]:
            img1.add(Tex(r"-",font_size=40).move_to(cond.get_left()+i*UP+(np.absolute(i/2)+0.1)*RIGHT))
        
        for i in [-0.87,-0.6,-0.3,0,0.3,0.6,0.87]:
            img1.add(Tex(r"+",font_size=25).move_to(cond.get_right()+i*UP+(np.absolute(i/2)+0.1)*LEFT))
        
        img1.add(Ein,cond_lbl,qin).next_to(steps2[0],RIGHT).align_to(steps2[0],UP).to_edge(RIGHT)
        Ein2 = MyLabeledArrow(label=Tex(r"$\vec{E}_{\text{ind}}$",font_size=30),pos=0.25*UP,start=cond.get_top()+0.95*DOWN+0.5*RIGHT,end=cond.get_top()+0.95*DOWN+0.2*LEFT,tip_length=0.2,color=BLUE_D)
        
        dielectric_lbl = Tex("Dielectric",font_size=35).next_to(cond,DOWN,buff=-0.35)
        E_net = Tex(r"$E_{\text{net}}\neq 0$",font_size=35,color=YELLOW).move_to(cond.get_center()+0.35*DOWN)
        img2 = VGroup(img1[0:-3].copy(),Ein2,dielectric_lbl,E_net).next_to(img1,DOWN,buff=0.5).to_edge(RIGHT)
        anm1 = [Write(steps1[0][0]),Write(steps1[0][1]),Write(steps1[1]),FadeOut(steps1),Write(title),Succession(Write(steps2[0][0]),Write(img1)),Write(steps2[0][1]), Write(steps2[1]),Succession(Write(steps2[2][0]),Write(img2)),Write(steps2[2][1]),Write(steps2[2][2]),FadeOut(img1,img2,steps2,title)]

        for item in anm1:
            self.play(item)
            self.next_slide()
        
        title = Tex(r"Polar and Non-Polar Dielectrics :",font_size=35,color=ORANGE).next_to(Intro_title,DOWN).to_edge(LEFT,buff=0.1)
        steps3 = ItemList(Item(r"Non-Polar Dielectric :",r" In a non-polar molecule, the centres of positive and negative charges coincide. ", r"These molecules do not have any permanent dipole moment.",pw="8 cm"),
                          Item(r"Examples: H$_2$, O$_2$, N$_2$, CO$_2$, CH$_4$ etc. ",pw="8 cm",color=YELLOW_D),
                          Item(r"Polar Dielectric :",r" In a polar molecule, the centres of positive and negative charges are separated. ", r"These molecules have permanent dipole moment.",pw="8 cm"),
                          Item(r"Examples: H$_2$O, NH$_3$, HCl etc. ",pw="8 cm",color=YELLOW_D),
                          buff=0.55).next_to(title,DOWN).to_edge(LEFT,buff=0.3)
        img3 = ImageMobject("npolar.png").scale(0.8).next_to(steps3,RIGHT).shift(1.2*LEFT)
        img4 = ImageMobject("polar.png").scale(0.8).next_to(img3,DOWN)
        
        anm2 = [Write(title),Write(steps3[0][0].set_color(GOLD)),Succession(Write(steps3[0][1]),FadeIn(img3)),Write(steps3[0][2]),Write(steps3[1]),Write(steps3[2][0].set_color(GOLD)),Write(steps3[2][1]),Write(steps3[2][2]),Succession(Write(steps3[3]),FadeIn(img4)),FadeOut(steps3,img3,img4,title)]

        for item in anm2:
            self.play(item)
            self.next_slide()
        
        title = Tex(r"Non-Polar Dielectrics in external field :",font_size=35,color=ORANGE).next_to(Intro_title,DOWN).to_edge(LEFT,buff=0.1)
        steps4 = ItemList(Item(r"In an external electric field, the positive and negative charges of a non- polar molecule are displaced in opposite directions ",pw="6 cm"),
                          Item(r"The non-polar molecule thus develops an induced dipole moment. The dielectric is said to be polarised by the external field.",pw="6 cm",color=YELLOW_D),
                          Item(r"Linear  isotropic dielectrics :",r" Dielectrics for which the induced dipole moment is in the direction of the field and is proportional to the field strength",pw="13 cm"),
                          buff=0.55).next_to(title,DOWN).to_edge(LEFT,buff=0.3)
        
        d_img = Rectangle(height=3,width=2.4,fill_opacity=0.3).set_color_by_gradient(BLUE,BLUE_E)
        Ein = Tex(r"$\vec{E}_{\text{net}}=0$ \\ $\vec{p}_{\text{net}}=0$",font_size=35,color=YELLOW).next_to(d_img,DOWN)
        d_lbl = Tex("In absence of external field",font_size=35).next_to(d_img,DOWN,buff=-0.35).next_to(Ein,DOWN)
        img1 = VGroup(d_img,Ein)
        for i in [1.2, 0.6, 0, -0.6, -1.2]:
            for j in [0.4, 1.2, 2]:
                c = Circle(0.2,color=RED).move_to(d_img.get_left()+i*UP+j*RIGHT)
                pm = Tex(r"$\pm$",font_size=22).move_to(c.get_center())
                img1.add(VGroup(c,pm))
        
        d_img = Rectangle(height=3,width=2.4,fill_opacity=0.3).set_color_by_gradient(BLUE,BLUE_E)
        E_net = Tex(r"$\vec{E}_{\text{net}}\neq0$ \\ $\vec{p}_{\text{net}}\neq0$",font_size=35,color=YELLOW).next_to(d_img,DOWN)
        d_lbl = Tex("In the presence of external field",font_size=35).next_to(d_img,DOWN,buff=-0.35).next_to(Ein,DOWN)
        Eo = MyLabeledArrow(label=Tex(r"$\vec{E}_{0}$",font_size=30),pos=0.25*UP,start=d_img.get_top()+0.25*UP+0.5*LEFT,end=d_img.get_top()+0.25*UP+0.5*RIGHT,tip_length=0.2,color=GREEN_D)
        Ein = MyLabeledArrow(label=Tex(r"$\vec{E}_{\text{ind}}$",font_size=30),pos=0.55*RIGHT,start=d_img.get_top()+1.2*DOWN+0.5*RIGHT,end=d_img.get_top()+1.2*DOWN+0.15*LEFT,tip_length=0.2,color=PINK)
        img2 = VGroup(d_img,Ein,Eo,E_net)
        for i in [1.2, 0.6, 0, -0.6, -1.2]:
            for j in [0.4, 1.2, 2]:
                c = Ellipse(width=0.6,height=0.25,color=RED).move_to(d_img.get_left()+i*UP+j*RIGHT)
                m = Tex(r"$-$",font_size=20).move_to(c.get_left()+0.1*RIGHT)
                p = Tex(r"$+$",font_size=20).move_to(c.get_right()+0.1*LEFT)
                img2.add(VGroup(c,p,m))

        anm3 = [Write(title),Write(img1.next_to(title,RIGHT).align_to(title,UP)),Succession(Write(steps4[0]),Write(img2.next_to(img1,RIGHT))),Write(steps4[1]),Write(steps4[2][0].set_color(GOLD)),Write(steps4[2][1]),FadeOut(steps4,title,img1,img2)]
        for item in anm3:
            self.play(item)
            self.next_slide()
        
        title = Tex(r"Polar Dielectrics in external field :",font_size=35,color=ORANGE).next_to(Intro_title,DOWN).to_edge(LEFT,buff=0.1)
        steps5 = ItemList(Item(r"In a dielectric with polar molecules, in the absence of external field, the different permanent dipoles are oriented randomly due to thermal agitation (energy). ",r"So, the total dipole moment is zero.",pw="8 cm"),
                          Item(r"But, When external field $\vec{E}_0$ is applied, each dipole molecule tend to align with the field which result in a net dipole moment in the direction of electric field.",pw="8 cm",color=YELLOW_D),
                          Item(r"The thermal energy tends to disturb the alignment and the external field tends to align the dipole. ",pw="8 cm"),
                          buff=0.55).next_to(title,DOWN).to_edge(LEFT,buff=0.3)
        for item in anm3:
            self.play(item)
            self.next_slide()
        img5 = ImageMobject("pole0.png").next_to(title,RIGHT).align_to(title,UP)
        img6 = ImageMobject("pole.png").next_to(img5,DOWN)

        anm4 = [Write(title), Succession(Write(steps5[0]),FadeIn(img5)), Succession(Write(steps5[1]),FadeIn(img6)),Write(steps5[2])]
        for item in anm4:
            self.play(item)
            self.next_slide()
