
# self.add(index_labels(text_1))


import os
import shutil
from manim import *
import copy

shutil.rmtree(os.path.join('media'))
os.mkdir('media')
# у нас есть четыре фрукта, и мы хотим их съесть поочереди. Сколько существует возможных вариантов такой трапезы?
# Если мы будем слепо перебирать варианты, то, во-первых, мы будем сталкиваться с повторами, во-вторых, рискуем случайно пропустить какие-то конкретные варианты.
# Вместо этого давайте воспользуемся логикой.
# Итак, первым мы можем съесть любой из имеющихся фруктов. Их у нас ровно четыре
# следующим фруктом может быть любой из оставшихся трех.
# после этого останется выбрать какой-то из двух оставшихся
# Ну, и, наконец, остается только один.

# У нас получилось своеобразное дерево с фрукто-овощем, где каждая ветка - это вариант трапезы.
# Эти ветки можно легко пересчитать вручную, но давайте попробуем логически. 
# Для этого повторим рассуждения
# Всего у нас четыре ветки.
# На каждой ветке по три ответвления.
# на каждом ответвлении по два отростка.
# На каждом ответвлении по одному фрукту-овощу.

# Для такого последовательного перемножения придумали компактную запись
# Такая запись может быть очень удобна, если элементов не четыре, а например 10, 100, 1000 и тд
# В следующий раз попробуем разобраться с тем, сколько вариантов трапезы у нас есть, если фрукто-овощей больше, чем мы хотим съесть за раз.
 


def make_mobs (mob_type) -> list:
    mobs = list()
    for x in np.nditer(mob_type):
        if x == 0: 
            mobs.append(SVGMobject("cucumber.svg"))
        elif x == 1:
            mobs.append(SVGMobject("plum.svg"))
        elif x == 2:
            mobs.append(SVGMobject("lemo.svg"))
        elif x == 3:
            mobs.append(SVGMobject("apple_red.svg"))
    return mobs 

def moveAlongPath(mobject_1, mobject_2, movingCameraScene, f_up_down) -> Dot:
    dot = Dot().move_to(mobject_1)
    path = Line(mobject_1.get_center(), mobject_2.get_center(),stroke_opacity=0.5).set_opacity(0)
    if f_up_down:
        path.points[1:3] += UP*2
    else:
        path.points[1:3] -= UP*2

    mobject_1.save_state()
    def update_rotate_move(mob,alpha):
        mobject_1.restore()
        mobject_1.move_to(path.point_from_proportion(alpha))
        mobject_1.rotate(2*PI*alpha)

    movingCameraScene.play(
            UpdateFromAlphaFunc(mobject_1,update_rotate_move),
            run_time = 1
        )
    return dot

def swapMobs(mobject_1, mobject_2, movingCameraScene):

    mobject_1.save_state()
    mobject_2.save_state()

    dot_1 = Dot().move_to(mobject_1)
    dot_2 = Dot().move_to(mobject_2)

    def update_rotate_move_up(mob,alpha):
        mob.restore()
        path = Line(dot_1.get_center(), dot_2.get_center(),stroke_opacity=0.5).set_opacity(0)
        path.points[1:3] += UP*2
        mob.move_to(path.point_from_proportion(alpha))
        mob.rotate(2*PI*alpha)

    def update_rotate_move_down(mob,alpha):
        mob.restore()
        path = Line(dot_2.get_center(), dot_1.get_center(),stroke_opacity=0.5).set_opacity(0)
        path.points[1:3] -= UP*2
        mob.move_to(path.point_from_proportion(alpha))
        mob.rotate(2*PI*alpha)

    movingCameraScene.play(
            AnimationGroup(
                UpdateFromAlphaFunc(mobject_1, update_rotate_move_up),
                UpdateFromAlphaFunc(mobject_2, update_rotate_move_down),
                run_time = 1
            )
        )

def placeInLine (mobs, rows, cols, x_step, y_step):
    for i, mob in enumerate(mobs):
        row = i // cols
        col = i % cols
        mob.move_to(np.array([col * x_step - (cols-1) * x_step / 2, 
                                -(row * y_step) + (rows-1) * y_step / 2, 0]))
        
def playReplaceMobs (movingCameraScene, mobs_1, mobs_2):
    for i, mob_1 in enumerate(mobs_1):
        movingCameraScene.play(Transform(mobs_1[i], mobs_2[i]))

def placeGrid(movingCameraScene):
    # Создаем сетку с настройками
    grid = NumberPlane(
        x_range=[-100, 100, 1],   # Диапазон по оси X: от -10 до 10 с шагом 1
        y_range=[-100, 100, 1],   # Диапазон по оси Y: от -10 до 10 с шагом 1
        background_line_style = {
            "stroke_color": BLUE,     # Цвет линий сетки
            "stroke_width": 1,        # Толщина линий сетки
            "stroke_opacity": 0.6     # Прозрачность линий сетки
        }
    )
    # Настроить оси
    grid.axes.set_color(BLUE).set(stroke_width = 0.5, stroke_opacity = 0.6)  # Цвет осей

    # Добавляем сетку на сцену
    movingCameraScene.add(grid)
    grid.remove(grid.x_axis, grid.y_axis)

def showEverithing(group, movingCameraScene):
    # Определение масштаба камеры по ширине и высоте
    scale_width = movingCameraScene.camera.frame_width / group.width
    scale_height = movingCameraScene.camera.frame_height / group.height

    # Выбор наименьшего масштаба для гарантии, что все объекты попадут в кадр
    optimal_scale = min(scale_width, scale_height)

    # Установка ширины и высоты кадра камеры
    movingCameraScene.play(movingCameraScene.camera.frame.animate.set(width = movingCameraScene.camera.frame_width / optimal_scale * 1.3))
    movingCameraScene.play(movingCameraScene.camera.frame.animate.move_to(group))
    

#============================================================================================================
#############################################################################################################
#############################################################################################################
#============================================================================================================
class Permutations(MovingCameraScene):
    def construct(self):
        self.camera.background_color = GREY_BROWN

        placeGrid(self)

        # Создаем несколько объектов
        mob_type = np.array([0, 1, 2, 3])
        mobs = make_mobs(mob_type)
        mobs_2 = make_mobs(mob_type)

        # Располагаем mobs по сетке вертикально
        placeInLine(mobs, 5, 1, 0, 2.1)
            
        # Располагаем mobs_2 по сетке горизонтально
        placeInLine(mobs_2, 1, 5, 1.3, 0)

        # Группируем вертикальные объекты
        grid = VGroup(*mobs).scale(0.5)
        # Группируем горизонтальные объекты
        grid_2 = VGroup(*mobs_2).next_to(grid.get_top(), UP).scale(0.5)

        # Анимация появления объектов
        self.play(self.camera.frame.animate.move_to(grid).set(height = grid.height * 1.1))
        self.play(Create(grid))
        
        group = VGroup(grid, grid_2)

        showEverithing(group, self)

        # Заменить горизонтальные на вертикальные
        playReplaceMobs(self, mobs, mobs_2)

        self.remove(grid)
        self.play(grid_2.animate.move_to(self.camera.frame.get_top()))

        self.play(self.camera.frame.animate.move_to(grid_2))
        self.play(self.camera.frame.animate.set(width = grid_2.width * 2.0))

        swapMobs(grid_2[0], grid_2[3], self)
        swapMobs(grid_2[1], grid_2[2], self)
        swapMobs(grid_2[0], grid_2[1], self)
        swapMobs(grid_2[2], grid_2[3], self)
        swapMobs(grid_2[1], grid_2[2], self)
        swapMobs(grid_2[0], grid_2[1], self)
        swapMobs(grid_2[2], grid_2[3], self)

        self.wait(2)
#============================================================================================================
#############################################################################################################
#############################################################################################################
#============================================================================================================
class Permutations_2(MovingCameraScene):
    def construct(self):
        self.camera.background_color = GREY_BROWN

        placeGrid(self)

        # Создаем несколько объектов
        list_of_grids = list() #список grids'ов 

        mob_type = np.array([0, 1, 2, 3])
        mobs_1 = make_mobs(mob_type)
        mobs_2 = make_mobs(mob_type)

        # Исходные фрукты-овощи вертикально
        placeInLine(mobs_1, 4, 1, 0, 1.5)
        grid_1 = VGroup(*mobs_1).scale(0.5)
        list_of_grids.append(grid_1)
        
        # Стартовый экран
        self.play(self.camera.frame.animate.move_to(grid_1).set(height = grid_1.height * 1.1))
        self.play(Create(grid_1))

        # Первый слой
        placeInLine(mobs_2, 4, 1, 0, 8)
        grid_2 = VGroup(*mobs_2).scale(1).next_to(grid_1, RIGHT * 5)
        list_of_grids.append(grid_2)

        showEverithing(VGroup(*list_of_grids), self)

        # Расставить первый слой
        self.play(
            AnimationGroup(
                TransformFromCopy(mobs_1[0], mobs_2[0]),
                TransformFromCopy(mobs_1[1], mobs_2[1]),
                TransformFromCopy(mobs_1[2], mobs_2[2]),
                TransformFromCopy(mobs_1[3], mobs_2[3]),
                run_time = 1
            )
        )

        self.wait(0.3)

#============================================================================================================
# Второй слой
#============================================================================================================
        mobs_3 = []
        for i in range(0,4):
            mobs_i = make_mobs(mob_type)
            inner_mob_list = []
            for n in range(0,4):
                if n != i:
                    inner_mob_list.append(mobs_i[n])
            mobs_3.append(inner_mob_list)

            placeInLine(mobs_3[i], 4, 1, 0, 3)
            list_of_grids.append(VGroup(*mobs_3[i]).scale(0.75).next_to(mobs_2[i]))

        showEverithing(VGroup(*list_of_grids), self)

        for i in range(0,4):
            c = 0
            for n in range(0,4):
                if n != i:
                    self.play(TransformFromCopy(mobs_1[n], mobs_3[i][c]), run_time = 0.5)
                    path = Line(mobs_2[i].get_center(), mobs_3[i][c].get_center(),stroke_opacity=0.5).set_opacity(0.5)
                    self.play(Create(path), run_time = 0.1)
                    c += 1
        self.wait(0.3)

#============================================================================================================
# Третий слой
#============================================================================================================
        mobs_4 = [[[]]]
        
        mob_list_1_lvl = [] #Кол-во первых уровней = 4
        c = 0
        for i in range(0,4): #заполнить элементы первого слоя
            cc = 0 # счетчик добавленных элементов во втором слое
            mob_list_2_lvl = [] #Кол-во вторых уровней = 3
            for n in range(0,4): #заполнить элементы второго слоя
                if (n != i):
                    ccc = 0 # счетчик добавленных элементов в третьем слое
                    mob_list_3_lvl = [] #Кол-во третьих уровней = 2
                    for k in range(0,4): # Перебрать каждый элемент третьего уровня
                        mobs_i = make_mobs(mob_type) #набор-донор
                        if (k != i) and (k != n):
                            mob_list_3_lvl.append(mobs_i[k])
                            ccc += 1
                    placeInLine(mob_list_3_lvl, 3, 1, 0, 2)
                    this_group = VGroup(*mob_list_3_lvl).scale(0.5)
                    this_group.next_to(mobs_3[i][cc])

                    mob_list_2_lvl.append(mob_list_3_lvl)
                    cc += 1
            mob_list_1_lvl.append(mob_list_2_lvl)
            c += 1

        c = 0
        for i in range(0,4): #заполнить элементы первого слоя
            cc = 0 # счетчик добавленных элементов во втором слое
            for n in range(0,4): #заполнить элементы второго слоя
                if (n != i):
                    ccc = 0 # счетчик добавленных элементов в третьем слое
                    for k in range(0,4): # Перебрать каждый элемент третьего уровня
                        if (k != i) and (k != n):
                            path = Line(mob_list_1_lvl[c][cc][ccc].get_center(), mobs_3[i][cc].get_center(),stroke_opacity=0.5).set_opacity(0.5)
                            self.add(path)
                            self.play(TransformFromCopy(mobs_i[k], mob_list_1_lvl[c][cc][ccc]), run_time = 0.3)
                            ccc += 1
                    cc += 1
            c += 1

#============================================================================================================
# Четвертый слой
#============================================================================================================
        mob_list_1_lvl_4 = [] #Кол-во первых уровней = 4
        c = 0
        for i in range(0,4): #заполнить элементы первого слоя
            cc = 0 # счетчик добавленных элементов во втором слое
            mob_list_2_lvl_4 = [] #Кол-во вторых уровней = 3
            for n in range(0,4): #заполнить элементы второго слоя
                if (n != i):
                    ccc = 0 # счетчик добавленных элементов в третьем слое
                    mob_list_3_lvl_4 = [] #Кол-во третьих уровней = 2
                    for k in range(0,4): # заполнить элементы третьего слоя
                        if (k != i) and (k != n):
                            cccc = 0
                            mob_list_4_lvl_4 = [] #Кол-во третьих уровней = 2
                            for p in range(0, 4):
                                mobs_i = make_mobs(mob_type) #набор-донор
                                if (p != i) and (p != n) and (p != k):
                                    mob_list_4_lvl_4.append(mobs_i[p])
                                    cccc += 1
                            placeInLine(mob_list_4_lvl_4, 2, 1, 0, 2)
                            this_group = VGroup(*mob_list_4_lvl_4).scale(0.5)
                            this_group.next_to(mob_list_1_lvl[c][cc][ccc])
                            mob_list_3_lvl_4.append(mob_list_4_lvl_4)
                            # self.add(this_group)
                            # self.wait(0.1)
                            ccc += 1
                    mob_list_2_lvl_4.append(mob_list_3_lvl_4)
                    cc += 1
            mob_list_1_lvl_4.append(mob_list_2_lvl_4)
            c += 1

        c = 0
        for i in range(0,4): #заполнить элементы первого слоя
            cc = 0 # счетчик добавленных элементов во втором слое
            for n in range(0,4): #заполнить элементы второго слоя
                if (n != i):
                    ccc = 0 # счетчик добавленных элементов в третьем слое
                    for k in range(0,4): # заполнить элементы третьего слоя
                        if (k != i) and (k != n):
                            cccc = 0
                            for p in range(0, 4):
                                if (p != i) and (p != n) and (p != k):
                                    path = Line(mob_list_1_lvl_4[c][cc][ccc][cccc].get_center(), mob_list_1_lvl[c][cc][ccc].get_center(),stroke_opacity=0.5).set_opacity(0.5)
                                    self.add(path)
                                    self.play(TransformFromCopy(mobs_1[p], mob_list_1_lvl_4[c][cc][ccc][cccc]), run_time = 0.3)
                                    self.wait(0.1)
                                    cccc += 1
                            ccc += 1
                    cc += 1
            c += 1


#============================================================================================================
#############################################################################################################
#############################################################################################################
#============================================================================================================
class Permutations_3(MovingCameraScene):
    def construct(self):
        self.camera.background_color = GREY_BROWN

        placeGrid(self)

        # Создаем несколько объектов
        list_of_grids = list() #список grids'ов 

        mob_type = np.array([0, 1, 2, 3])
        mobs_1 = make_mobs(mob_type)
        mobs_2 = make_mobs(mob_type)

        # Исходные фрукты-овощи вертикально
        placeInLine(mobs_1, 4, 1, 0, 1.5)
        grid_1 = VGroup(*mobs_1).scale(0.5)
        list_of_grids.append(grid_1)
        
        # Стартовый экран
        self.play(self.camera.frame.animate.move_to(grid_1).set(height = grid_1.height * 1.1))
        self.play(Create(grid_1))
        # self.add(grid_1)

        # Первый слой
        placeInLine(mobs_2, 4, 1, 0, 8)
        grid_2 = VGroup(*mobs_2).scale(1).next_to(grid_1, RIGHT * 5)
        list_of_grids.append(grid_2)

        showEverithing(VGroup(*list_of_grids), self)

        # Расставить первый слой
        self.play(
            AnimationGroup(
                TransformFromCopy(mobs_1[0], mobs_2[0]),
                TransformFromCopy(mobs_1[1], mobs_2[1]),
                TransformFromCopy(mobs_1[2], mobs_2[2]),
                TransformFromCopy(mobs_1[3], mobs_2[3]),
                run_time = 1
            )
        )

        self.wait(0.3)

#============================================================================================================
# Второй слой
#============================================================================================================
        mobs_3 = []
        for i in range(0,4):
            mobs_i = make_mobs(mob_type)
            inner_mob_list = []
            for n in range(0,4):
                if n != i:
                    inner_mob_list.append(mobs_i[n])
            mobs_3.append(inner_mob_list)

            placeInLine(mobs_3[i], 4, 1, 0, 3)
            list_of_grids.append(VGroup(*mobs_3[i]).scale(0.75).next_to(mobs_2[i]))

        showEverithing(VGroup(*list_of_grids), self)

        for i in range(0,4):
            c = 0
            for n in range(0,4):
                if n != i:
                    self.play(TransformFromCopy(mobs_1[n], mobs_3[i][c]), run_time = 0.5)
                    # self.add(mobs_3[i][c])
                    path = Line(mobs_2[i].get_center(), mobs_3[i][c].get_center(),stroke_opacity=0.5).set_opacity(0.5)
                    self.play(Create(path), run_time = 0.1)
                    # self.add(path)
                    c += 1
        self.wait(0.3)

#============================================================================================================
# Третий слой
#============================================================================================================
        mobs_4 = [[[]]]
        
        mob_list_1_lvl = [] #Кол-во первых уровней = 4
        c = 0
        for i in range(0,4): #заполнить элементы первого слоя
            cc = 0 # счетчик добавленных элементов во втором слое
            mob_list_2_lvl = [] #Кол-во вторых уровней = 3
            for n in range(0,4): #заполнить элементы второго слоя
                if (n != i):
                    ccc = 0 # счетчик добавленных элементов в третьем слое
                    mob_list_3_lvl = [] #Кол-во третьих уровней = 2
                    for k in range(0,4): # Перебрать каждый элемент третьего уровня
                        mobs_i = make_mobs(mob_type) #набор-донор
                        if (k != i) and (k != n):
                            mob_list_3_lvl.append(mobs_i[k])
                            ccc += 1
                    placeInLine(mob_list_3_lvl, 3, 1, 0, 2)
                    this_group = VGroup(*mob_list_3_lvl).scale(0.5)
                    this_group.next_to(mobs_3[i][cc])

                    mob_list_2_lvl.append(mob_list_3_lvl)
                    cc += 1
            mob_list_1_lvl.append(mob_list_2_lvl)
            c += 1

        c = 0
        for i in range(0,4): #заполнить элементы первого слоя
            cc = 0 # счетчик добавленных элементов во втором слое
            for n in range(0,4): #заполнить элементы второго слоя
                if (n != i):
                    ccc = 0 # счетчик добавленных элементов в третьем слое
                    for k in range(0,4): # Перебрать каждый элемент третьего уровня
                        if (k != i) and (k != n):
                            path = Line(mob_list_1_lvl[c][cc][ccc].get_center(), mobs_3[i][cc].get_center(),stroke_opacity=0.5).set_opacity(0.5)
                            self.add(path)
                            self.play(TransformFromCopy(mobs_i[k], mob_list_1_lvl[c][cc][ccc]), run_time = 0.3)
                            # self.add(mob_list_1_lvl[c][cc][ccc])
                            ccc += 1
                    cc += 1
            c += 1

#============================================================================================================
# Четвертый слой
#============================================================================================================
        mob_list_1_lvl_4 = [] #Кол-во первых уровней = 4
        c = 0
        for i in range(0,4): #заполнить элементы первого слоя
            cc = 0 # счетчик добавленных элементов во втором слое
            mob_list_2_lvl_4 = [] #Кол-во вторых уровней = 3
            for n in range(0,4): #заполнить элементы второго слоя
                if (n != i):
                    ccc = 0 # счетчик добавленных элементов в третьем слое
                    mob_list_3_lvl_4 = [] #Кол-во третьих уровней = 2
                    for k in range(0,4): # заполнить элементы третьего слоя
                        if (k != i) and (k != n):
                            cccc = 0
                            mob_list_4_lvl_4 = [] #Кол-во третьих уровней = 2
                            for p in range(0, 4):
                                mobs_i = make_mobs(mob_type) #набор-донор
                                if (p != i) and (p != n) and (p != k):
                                    mob_list_4_lvl_4.append(mobs_i[p])
                                    cccc += 1
                            placeInLine(mob_list_4_lvl_4, 2, 1, 0, 2)
                            this_group = VGroup(*mob_list_4_lvl_4).scale(0.5)
                            this_group.next_to(mob_list_1_lvl[c][cc][ccc])
                            mob_list_3_lvl_4.append(mob_list_4_lvl_4)
                            ccc += 1
                    mob_list_2_lvl_4.append(mob_list_3_lvl_4)
                    cc += 1
            mob_list_1_lvl_4.append(mob_list_2_lvl_4)
            c += 1

        c = 0
        for i in range(0,4): #заполнить элементы первого слоя
            cc = 0 # счетчик добавленных элементов во втором слое
            for n in range(0,4): #заполнить элементы второго слоя
                if (n != i):
                    ccc = 0 # счетчик добавленных элементов в третьем слое
                    for k in range(0,4): # заполнить элементы третьего слоя
                        if (k != i) and (k != n):
                            cccc = 0
                            for p in range(0, 4):
                                if (p != i) and (p != n) and (p != k):
                                    path = Line(mob_list_1_lvl_4[c][cc][ccc][cccc].get_center(), mob_list_1_lvl[c][cc][ccc].get_center(),stroke_opacity=0.5).set_opacity(0.5)
                                    self.add(path)
                                    self.play(TransformFromCopy(mobs_1[p], mob_list_1_lvl_4[c][cc][ccc][cccc]), run_time = 0.3)
                                    # self.add(mob_list_1_lvl_4[c][cc][ccc][cccc])
                                    self.wait(0.1)
                                    cccc += 1
                            ccc += 1
                    cc += 1
            c += 1

#============================================================================================================
# Фокус на одной ветке
#============================================================================================================
        mobs_to_show = []
        mobs_to_show.append(mobs_2[0])
        for i in range(0, 3):
            mobs_to_show.append(mobs_3[0][i])
            for n in range(0, 2):
                mobs_to_show.append(mob_list_1_lvl[0][i][n])
                for p in range(0, 1):
                    mobs_to_show.append(mob_list_1_lvl_4[0][i][n][p])

        focus_group = VGroup(*mobs_to_show)
        self.play(self.camera.frame.animate.move_to(focus_group).set(width = focus_group.width * 1.3))
        # self.wait(0.3)

        # Выделить фрукты на одной ветке
        framebox_1 = SurroundingRectangle(mobs_2[0], buff = .05, corner_radius=0.2)
        framebox_2 = SurroundingRectangle(mobs_3[0][0], buff = .05, corner_radius=0.2)
        framebox_3 = SurroundingRectangle(mob_list_1_lvl[0][0][0], buff = .05, corner_radius=0.2)
        framebox_4 = SurroundingRectangle(mob_list_1_lvl_4[0][0][0][0], buff = .05, corner_radius=0.2)

        self.add(framebox_1,framebox_2,framebox_3,framebox_4)
        self.wait(0.3)

#============================================================================================================
# Отдельно каждая ветка
#============================================================================================================
        mobs_to_show_by_4_all = VGroup()
        mobs_to_show_by_4 = []
        mobs_to_show_by_4_lvl_1 = mobs_to_show_by_4.copy()
        mobs_to_show_by_4_lvl_1.append((mobs_2[0]).copy())

        for i in range(0, 3):
            mobs_to_show_by_4_lvl_2 = []
            mobs_to_show_by_4_lvl_2 = copy.deepcopy(mobs_to_show_by_4_lvl_1)
            mobs_to_show_by_4_lvl_2.append(mobs_3[0][i].copy())

            for n in range(0, 2):
                mobs_to_show_by_4_lvl_3 = []
                mobs_to_show_by_4_lvl_3 = copy.deepcopy(mobs_to_show_by_4_lvl_2)
                mobs_to_show_by_4_lvl_3.append(mob_list_1_lvl[0][i][n].copy())

                for p in range(0, 1):
                    mobs_to_show_by_4_lvl_4 = []
                    mobs_to_show_by_4_lvl_4 = copy.deepcopy(mobs_to_show_by_4_lvl_3)
                    mobs_to_show_by_4_lvl_4.append(mob_list_1_lvl_4[0][i][n][p].copy())

                    placeInLine(mobs_to_show_by_4_lvl_4, 1, 4, 2, 0)
                    group_mobs_to_show_by_4 = VGroup(*(mobs_to_show_by_4_lvl_4)).scale(0.5)
                    group_mobs_to_show_by_4.next_to(mob_list_1_lvl_4[0][i][n][p], RIGHT * 2)

                    mobs_to_show_by_4_all.add(group_mobs_to_show_by_4)


        focus_group.add(mobs_to_show_by_4_all)
        self.play(self.camera.frame.animate.move_to(focus_group).set(width = focus_group.width * 1.3))
        self.wait(1)

        c = 0
        for i in range(0, 3):

            for n in range(0, 2):

                for p in range(0, 1):
                    self.play(TransformFromCopy(mobs_2[0], mobs_to_show_by_4_all[c][0]))
                    self.play(TransformFromCopy(mobs_3[0][i], mobs_to_show_by_4_all[c][1]))
                    self.play(TransformFromCopy(mob_list_1_lvl[0][i][n], mobs_to_show_by_4_all[c][2]))
                    self.play(TransformFromCopy(mob_list_1_lvl_4[0][i][n][p], mobs_to_show_by_4_all[c][3]))
                    if c == 0:
                        self.remove(framebox_1,framebox_2,framebox_3,framebox_4)
                        self.wait(0.3)
                    c += 1

#============================================================================================================
#############################################################################################################
#############################################################################################################
#============================================================================================================
class Permutations_4_Equations(MovingCameraScene):
    def construct(self):
        self.camera.background_color = GREY_BROWN

        placeGrid(self)

        text_1 = MarkupText(
            "Number of permutations – <span color = 'Yellow' font_family = 'CMU Serif' font_style='italic'>N</span>", font_size= 250, font = 'Marker Felt', color = 'White'
        )

        self.play(self.camera.frame.animate.move_to(text_1).set(width = text_1.width * 1.5))

        self.play(Create(text_1))

        # self.add(index_labels(text_1))

        self.wait(0.2)

        matex_1 = MathTex(
            r"N = 4 \times 3 \times 2 \times 1",
            font_size = 400
        ).next_to(text_1, DOWN * 10)
        matex_1[0][0].set_color(YELLOW)

        self.play(self.camera.frame.animate.move_to(matex_1).set(width = matex_1.width * 1.5))
        self.wait(0.2)

        n_copy = copy.deepcopy(text_1[24])
        
        # Transform the copy and fade out the original
        self.play(
            AnimationGroup(
                Transform(n_copy, matex_1[0][0]),
                FadeOut(text_1[22:25]),
                run_time = 0.5
            )
        )

        self.play(Create(matex_1[0][1]))
        self.wait(0.2)

        self.play(Create(matex_1[0][2:4]))
        self.wait(0.2)

        self.play(Create(matex_1[0][4:6]))
        self.wait(0.2)

        self.play(Create(matex_1[0][6:8]))
        self.wait(0.2)

        self.play(Create(matex_1[0][8:10]))
        self.wait(0.2)

        matex_2 = MathTex(
            r"N = 4!",
            font_size = 400
        )

        self.wait(0.2)

        # Нахождение точек привязки (в данном случае для символа 'a')
        point_a_formula1 = matex_1[0][1].get_center()
        point_a_formula2 = matex_2[0][1].get_center()
        
        # Смещение формулы 2 так, чтобы 'N' совпал с 'N'
        shift_vector = point_a_formula1 - point_a_formula2
        matex_2.shift(shift_vector)

        self.wait(0.2)
        self.play(Transform(matex_1[0][2:10],matex_2[0][2:4]))
        self.wait(0.2)

        self.remove(n_copy)
        self.play(matex_1.animate.shift(RIGHT * 9))
        self.wait(0.2)