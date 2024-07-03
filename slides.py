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
        cgroup = VGroup()
        for pt in shell.get_all_points():
            cgroup.add(Tex("$\mathbf{+}$",font_size=25,color=YELLOW).move_to(pt))
        
        img = VGroup(shell,cgroup,Q,r,R,o,P,line,q).next_to(Intro_title,DOWN).to_edge(RIGHT)

        steps1 = ItemList(Item(r"Consider a uniformly charged spherical shell of Radius (R) and having charge (Q).",pw="10 cm"),
                          Item(r"We have to find the electric potential $(V_P)$ at a point P", r" which is $r$ distance from the centre of the shell.",pw="10 cm"),
                          Item(r"Case (1) : For point(P) outside the shell $(r>R)$ ",pw="9 cm",color=GREEN),
                          Item(r"$\displaystyle V_P=\dfrac{W_{\infty P}}{q}$",r"$\displaystyle =-\int_{\infty}^{r} \dfrac{F_E}{q}\ dr$",pw="9 cm",dot=False),
                          Item(r"$\displaystyle V_{P}=-\int_{\infty}^{P} E\ dr$", r"$\displaystyle =-\int_{\infty}^{r}\dfrac{1}{4\pi\epsilon_0}\dfrac{Q}{r^2} dr$",pw="9 cm",dot=False),
                          Item(r"$ \displaystyle V_P=\dfrac{1}{4\pi\epsilon_0}\dfrac{Q}{r} \quad (r>R)$",pw="9 cm",dot=False,color=PINK),
                          buff=0.45).next_to(Intro_title,DOWN).to_edge(LEFT)
        
        sr = SurroundingRectangle(steps1[5])
        anm1 = [VGroup(steps1[0],shell,o,Q,R),VGroup(steps1[1][0],P),VGroup(steps1[1][1],r),steps1[2],VGroup(steps1[3],line,q),steps1[4],VGroup(steps1[5],sr)]

        for item in anm1:
            self.play(Write(item))
            self.next_slide()
        self.wait()
