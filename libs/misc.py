from math import *
from time import time

from OpenGL.GL import *
# from OpenGL.GLU import *
from OpenGL.GLUT import *
from libs.font import *
from libs.vector import *
from libs.settings import *


class ShotTrace:
    tex = loadTexture("assets/textures/ground/gnd.png", alpha=True)

    def __init__(self, normal, pos):

        # self.pos = pos + normal/1000
        self.pos = pos
        self.pos.y += 0.001
        self.opacity = 1
        self.gl_List = glGenLists(1)
        self.normal = normal
        w = 0.09

        glNewList(self.gl_List, GL_COMPILE)
        glEnable(GL_BLEND)
        glBindTexture(GL_TEXTURE_2D, self.tex)
        glBegin(GL_QUADS)
        glTexCoord2f(1, 1)
        glVertex3f(w, 0, w)
        glTexCoord2f(0, 1)
        glVertex3f(-w, 0, w)
        glTexCoord2f(0, 0)
        glVertex3f(-w, 0, -w)
        glTexCoord2f(1, 0)
        glVertex3f(w, 0, -w)
        glEnd()
        glEndList()
        glDisable(GL_BLEND)

    def draw(self):

        glPushMatrix()
        glTranslate(*self.pos.tuple())
        glRotatef(*rotationMatrix(self.normal))
        glColor4f(1, 1, 1, self.opacity)
        glCallList(self.gl_List)
        glPopMatrix()
        glColor4f(1, 1, 1, 1)


class Misc:

    def __init__(self):
        self.gl_list = glGenLists(1)
        self.Prepare()
        self.width = glutGet(GLUT_SCREEN_HEIGHT)
        self.width = glutGet(GLUT_SCREEN_WIDTH)

    def drawCursoe(self):
        glColor3d(1.0, 0.0, 0.0)
        glBegin(GL_POINTS)
        glVertex3d(0, 0, -.1)
        glEnd()

    def drawSkyBox(self):
        glColor3d(1.0, 1.0, 1.0)
        glutSolidSphere(50, 100, 100)

    def Prepare(self):
        glNewList(self.gl_list, GL_COMPILE)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glPushAttrib(GL_CURRENT_BIT)
        glLoadIdentity()
        glDisable(GL_LIGHTING)
        self.drawSkyBox()

        glPopAttrib()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glPushAttrib(GL_CURRENT_BIT)
        glLoadIdentity()

        self.drawCursoe()

        glPopAttrib()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
        glEndList()


fnt = Font("assets/font/PHANTOM.png", "assets/font/PHANTOM.fnt")
point = loadTexture("assets/textures/onscreen/crosshair_default.png", alpha=True)
bloodOnScreen = loadTexture("assets/textures/onscreen/BloodyScreen.png", alpha=True)
scoreBoard = loadTexture("assets/textures/onscreen/ammo_bg.png", alpha=True)
heart = loadTexture("assets/textures/onscreen/heart.png", alpha=True)
bloodBar = loadTexture("assets/textures/onscreen/bloodBar.jpg", alpha=True)
shoot = TexSeries("assets/textures/gun", alpha=True)


def drawRect(w=ratio, h=1.0):
    glBegin(GL_QUADS)
    glTexCoord2f(1, 1)
    glVertex2d( w / ratio,  h)
    glTexCoord2f(0, 1)
    glVertex2d(-w / ratio,  h)
    glTexCoord2f(0, 0)
    glVertex2d(-w / ratio, -h)
    glTexCoord2f(1, 0)
    glVertex2d( w / ratio, -h)
    glEnd()


def draw_health_bar(health):
    # health bar
    glEnable(GL_BLEND)
    glBindTexture(GL_TEXTURE_2D, 0)
    glColor(1, 1, 1)

    glBindTexture(GL_TEXTURE_2D, bloodBar)
    drawRectBounded(-0.5, -0.5 + health, 0.03, health)
    glBindTexture(GL_TEXTURE_2D, 0)
    glColor4f(1, 1, 1, 0.3)
    drawRect(0.5, 0.0307)
    glDisable(GL_BLEND)


def drawHorizontalRect(w=ratio, h=1.0):
    glBegin(GL_QUADS)
    glTexCoord2f(1, 1)
    glVertex3f( w / ratio, 0,  h)
    glTexCoord2f(0, 1)
    glVertex3f(-w / ratio, 0,  h)
    glTexCoord2f(0, 0)
    glVertex3f(-w / ratio, 0, -h)
    glTexCoord2f(1, 0)
    glVertex3f( w / ratio, 0, -h)
    glEnd()


def drawRectBounded(x1, x2, h, texX2):
    glBegin(GL_QUADS)
    glTexCoord2f(texX2, 1)
    glVertex2d(x2 / ratio,  h)
    glTexCoord2f(0, 1)
    glVertex2d(x1 / ratio,  h)
    glTexCoord2f(0, 0)
    glVertex2d(x1 / ratio, -h)
    glTexCoord2f(texX2, 0)
    glVertex2d(x2 / ratio, -h)
    glEnd()

def drawOnScreen(game, x, y, z):
    glDisable(GL_LIGHTING)
    glMatrixMode(GL_MODELVIEW)
    for i in game.shotTraces:
        # i.opacity -= 0.001
        # i.opacity -= 0.001 / i.opacity ** 2
        if i.opacity <= 0:
            game.shotTraces.remove(i)
            continue
        i.draw()

    if getattr(game.player, 'gameOver', False):
        return

    glPushMatrix()
    glLoadIdentity()
    # point
    if not game.player.inWater():
        # get color to revert it
        # color = glReadPixels(0, 0, 1, 1, GL_RGB, GL_FLOAT)[0][0]
        # brightness = (299 * R + 587 * G + 114 * B) / 1000
        # c = 1 - sum(color)/3

        glEnable(GL_BLEND)
        glDepthFunc(GL_ALWAYS)
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()

        # Premium Hardcore HUD Overlay (Subtle and Engaged)
        glLoadIdentity()
        
        # Dark stylized semi-transparent visor snippet
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glColor4f(0.04, 0.04, 0.05, 0.7)
        glDisable(GL_TEXTURE_2D)
        glBegin(GL_POLYGON)
        glVertex2f(-1.0, 1.0)
        glVertex2f(-0.7, 1.0)
        glVertex2f(-0.73, 0.88)
        glVertex2f(-1.0, 0.88)
        glEnd()
        
        # Modern Biological Pulse HUD (ECG Vector Icon)
        glLineWidth(3.0)
        
        # Vitality glow color check: Neon green -> orange -> crimson red
        hp_perc = game.player.health / 100.0 if hasattr(game.player, 'health') else 1.0
        if hp_perc > 0.6:
            glColor4f(0.1, 0.9, 0.7, 1.0)  # Healthy Neon Cyan-Green
        elif hp_perc > 0.3:
            glColor4f(1.0, 0.7, 0.1, 1.0)  # Warning Orange
        else:
            glColor4f(1.0, 0.1, 0.2, 1.0)  # Critical Heartrate Red
            
        # Draw Medical Pulse (ECG Monitor Graph)
        glBegin(GL_LINE_STRIP)
        glVertex2f(-0.95, 0.94)    # baseline 1
        glVertex2f(-0.89, 0.94)    # baseline 2
        glVertex2f(-0.87, 0.97)    # peak up
        glVertex2f(-0.84, 0.90)    # peak down dip
        glVertex2f(-0.81, 0.96)    # secondary up
        glVertex2f(-0.79, 0.94)    # settle to baseline
        glVertex2f(-0.75, 0.94)    # baseline end
        glEnd()
        
        # Stylized + Medical Cross for Life indicator under the pulse
        glLineWidth(2.5)
        glBegin(GL_LINES)
        # Vertical cross line
        glVertex2f(-0.93, 0.915)
        glVertex2f(-0.93, 0.895)
        # Horizontal cross line
        glVertex2f(-0.938, 0.905)
        glVertex2f(-0.922, 0.905)
        glEnd()
        
        # Restore standard draw states
        glLineWidth(1.0)
        glColor4f(1.0, 1.0, 1.0, 1.0)
        glEnable(GL_TEXTURE_2D)

        # cursor
        glLoadIdentity()
        # c = 0.7, 0.0, 0.0
        c = 1, 1, 1
        glColor(*c, 1)
        glBindTexture(GL_TEXTURE_2D, point)
        glScale(0.27, 0.27, 0.27)
        drawRect(0.1, 0.1)

        # health bar
        glLoadIdentity()
        health = game.player.health
        glTranslate(0, 0.91, 0)
        draw_health_bar(health/100)
        glPopMatrix()

        # onscreen blood
        glEnable(GL_BLEND)
        glPushMatrix()
        glLoadIdentity()

        glColor(1, 1, 1, (1-health/100)*abs(sin(glutGet(GLUT_ELAPSED_TIME)/500))+(1-health/100))
        glBindTexture(GL_TEXTURE_2D, bloodOnScreen)
        drawRect(ratio, 1)
        glDisable(GL_BLEND)
        glPopMatrix()

        # muzzle
        glMatrixMode(GL_MODELVIEW)
        if game.player.gun.muzzle.playing:
            glEnable(GL_BLEND)
            glMatrixMode(GL_PROJECTION)
            glPushMatrix()
            glLoadIdentity()
            glColor(1, 1, 1)
            glBindTexture(GL_TEXTURE_2D, game.player.gun.muzzle.getNextFrame())
            # glScale(game.p + 1.72, game.p + 1.72, game.p + 1.72)
            # glTranslate(game.x + 0.24, game.y-0.14, game.z)
            glScale(1.30999 + game.p, 1.30999 + game.p, 1.30999 + game.p)
            glTranslate(0.28 -0.035, -0.14 -0.016, 0.07999  -0.014)
            # print(0.28 + game.x, -0.14 + game.y, 0.07999 + game.z, 1.30999 + game.p)
            drawRect(0.2, 0.2)
            glPopMatrix()
            glMatrixMode(GL_MODELVIEW)
            glDisable(GL_BLEND)
    # Ammo HUD
    ammo = game.player.gun.ammo
    loaded = game.player.gun.loadedBullets
    color = (1, 0.1, 0.1, 0.8) if ammo == 0 and loaded == 0 else (0.9, 0.9, 0.9, 0.9)
    
    # Ultra-Minimalist Chamber & Reserve (using wide gaps so it won't bleed together over time)
    drawText("{}   /   {}".format(loaded, ammo), 0.82, -0.9, ratio, color, 2.0)

    # Minimalist Kills counter
    glLoadIdentity()
    glTranslate(0, 0, 0)
    drawText("TARGETS ELIMINATED // {}".format(int(game.player.kills)), 0.68, 0.86, ratio, (0.7, 0.1, 0.1, 0.8), 0.8)

    if glutGet(GLUT_ELAPSED_TIME) - game.message["start"] < 3000:
        text = game.message["message"]
        drawText(text, 0-len(text)/90, -0.95, ratio, (1, 0.2, 0.2, 1), 2, projection=True)

    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()
    glDepthFunc(GL_LESS)



def moveWithPlayer():
    gl_list = glGenLists(1)
    glNewList(gl_list, GL_COMPILE)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glPushAttrib(GL_CURRENT_BIT)
    glLoadIdentity()
    glutSolidSphere(50, 10, 10)
    glPopAttrib()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()
    glEndList()
    return gl_list


def drawText(text, x, y, wh, color=(0, 0, 0, 1), scale=1.0, projection=True):

    if projection:
        default_scale = .2 * scale
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glTranslate(x, y, 0)
        glScalef(default_scale, default_scale * wh, 1.0)

    else:
        default_scale = 0.0002 * scale
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        glScalef(default_scale, default_scale * wh, 1.0)
        glTranslate(x, y, 0)

    # glLineWidth(line)
    glColor4f(*color)
    fnt.draw(text)
    # glutStrokeString(GLUT_STROKE_MONO_ROMAN, bytes(text, 'utf-8'))
    # glColor4f(1.0, 1.0, 1.0, 1.0)
    glPopMatrix()
    glColor4f(1.0, 1.0, 1.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
