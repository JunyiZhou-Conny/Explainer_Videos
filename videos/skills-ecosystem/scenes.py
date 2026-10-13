"""Original Swiss motion design. Narration and exact budgets come from plan.json.

The Swiss visual vocabulary (palette, label/card/folder/arrow helpers) is the shared
style contract in explainer/styles/swiss.py, fed by presets/swiss.tokens.json.
"""
import json
import os
from pathlib import Path
import numpy as np
from manim import *
from explainer.scene import VoiceScene
from explainer.styles import swiss
from explainer.styles.swiss import (PAPER, INK, RED, GRAY, FAINT,
                                    label, at, left, line, card, folder, arrow)

swiss.setup_fonts()
config.background_color = PAPER

class EpisodeScene(VoiceScene):
    pad_after_clip=.18
    def setup(self):
        super().setup()
        self.camera.background_color=PAPER
        plan=json.loads(Path(os.environ["EPISODE_PLAN"]).read_text())
        self.spec=next(s for s in plan["scenes"] if s["id"].upper()==self.__class__.__name__)
        self.content=VGroup()
    def header(self, name):
        ident=self.spec['id'][1:]
        self.add(line(-6.3,3.42,6.3,3.42),left('CONNY / EXPLAINER STUDIES',-6.3,3.67,15),
                 at(f'{ident} / 12',5.85,3.67,16,RED))
        self.play(FadeIn(left(name,-6.3,2.85,47,INK,12.5,True),shift=UP*.10),run_time=.4)
        self.add(left(self.spec['title_zh'],-6.3,2.34,21,GRAY))
    def say(self,i):
        return self.voiceover(self.spec['lines'][i]['en'])
    def cue(self,vo,f,*anims,run_time=.65):
        delay=vo.duration*f-vo.elapsed
        if delay>.04:self.wait(delay)
        self.play(*anims,run_time=run_time)
    def finish(self):
        remaining=self.spec['duration']-self.renderer.time
        if remaining>.37:
            self.wait(remaining-.30)
            self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.30)
        elif remaining>.015:self.wait(remaining)

class S01(EpisodeScene):
    def construct(self):
        self.header('One sentence. A complete brief.')
        prompt=VGroup(left('Explain my Cursor skills.',-5.8,1.17,54,INK,11.6,True),
                      left('Swiss style. 5 minutes. Bilingual.',-5.8,.30,38,RED,11.6))
        underline=line(-5.8,-.26,5.8,-.26,RED,4)
        props=VGroup(*[card(a,b,x,-1.4,w=3.5,h=1.35) for a,b,x in
            [('STYLE','saved visual grammar',-4),('SPECS','saved export settings',0),('TOPIC','your next question',4)]])
        with self.say(0) as vo:
            self.cue(vo,0,FadeIn(prompt[0],shift=RIGHT*.15))
            self.cue(vo,.45,FadeIn(prompt[1],shift=RIGHT*.15),Create(underline))
        with self.say(1) as vo:
            self.cue(vo,0,LaggedStart(*[FadeIn(p,shift=UP*.2) for p in props],lag_ratio=.18),run_time=1.1)
            self.cue(vo,.50,props[0][0].animate.set_stroke(RED,3),props[1][0].animate.set_stroke(RED,3))
            self.cue(vo,.78,props[2][0].animate.set_fill(FAINT,1),prompt[0].animate.set_color(RED))
        self.finish()

class S02(EpisodeScene):
    def construct(self):
        self.header('Skill / Tool / Agent')
        blocks=[card('RECIPE','instructions',-4,0.4),card('EQUIPMENT','capability',0,.4),card('COOK','execution',4,.4)]
        foot=[at('SKILL.md',-4,-1.18,27,RED),at('Renderer · TTS',0,-1.18,26),at('Cursor · Codex\nClaude Code',4,-1.18,25)]
        with self.say(0) as vo:
            self.cue(vo,0,FadeIn(blocks[0]),FadeIn(foot[0]))
            demo=VGroup(*[line(-5.5,.2-i*.2,-3.8+i*.2,.2-i*.2,RED,3) for i in range(3)]).shift(DOWN*.5)
            self.cue(vo,.55,Create(demo))
        with self.say(1) as vo:
            self.cue(vo,0,FadeOut(demo),FadeIn(blocks[1]),FadeIn(foot[1]))
            self.cue(vo,.30,FadeIn(blocks[2]),FadeIn(foot[2]))
            rule=at('Shared instructions ≠ shared tools',0,-2.08,32,RED,11.5,True)
            self.cue(vo,.66,FadeIn(rule),Create(line(-5.8,-1.68,5.8,-1.68)))
        self.finish()

class S03(EpisodeScene):
    def construct(self):
        self.header('Three paths. Different owners.')
        rows=[]
        data=[('~/.agents/skills','83','shared user folders'),('~/.cursor/skills-cursor','25','Cursor-managed'),('~/.cursor/skills','—','absent at baseline')]
        for i,(path,note,desc) in enumerate(data):
            y=1.05-i*1.2
            rows.append(VGroup(left(path,-6,y,30,INK,8.0),at(note,3.25,y,60,RED,bold=True),left(desc,4,y,19,GRAY,2.3),line(-6,y-.5,6.2,y-.5,FAINT)))
        self.add(left('2026-10-12 BASELINE · BEFORE THIS INSTALLATION',-6,-2.37,17,GRAY))
        with self.say(0) as vo:
            self.cue(vo,0,FadeIn(rows[0],shift=UP*.1))
            self.cue(vo,.58,Indicate(rows[0][0],color=RED,scale_factor=1.025))
        with self.say(1) as vo:
            self.cue(vo,0,FadeIn(rows[1],shift=UP*.1))
            self.cue(vo,.46,FadeIn(rows[2],shift=UP*.1))
            self.cue(vo,.78,rows[0][3].animate.set_color(RED),rows[1][3].animate.set_color(RED))
        self.finish()

class S04(EpisodeScene):
    def construct(self):
        self.header('Read the folder by function.')
        items=[('extensions/','editor features'),('plugins/','agent packages'),('projects/','working state'),('skills-cursor/','managed instructions'),('mcp.json','tool connections'),('hooks.json','event commands')]
        blocks=VGroup(*[card(a,b,-4.1+(i%3)*4.1,.85-(i//3)*1.65,w=3.8,h=1.35) for i,(a,b) in enumerate(items)])
        with self.say(0) as vo:
            self.cue(vo,0,FadeIn(blocks[0]))
            self.cue(vo,.18,FadeIn(blocks[1]))
            self.cue(vo,.34,FadeIn(blocks[2]),FadeIn(blocks[3]))
            self.cue(vo,.62,FadeIn(blocks[4]),FadeIn(blocks[5]))
        note=at('CACHE COPIES ≠ ACTIVE SKILLS',0,-2.0,32,RED,bold=True)
        with self.say(1) as vo:
            versions=VGroup(*[Rectangle(width=3.8,height=1.35,stroke_color=GRAY,stroke_width=1).move_to(blocks[1]).shift(UP*.12*i+RIGHT*.1*i) for i in [2,1]])
            self.cue(vo,0,FadeIn(versions))
            self.bring_to_front(blocks[1])
            self.cue(vo,.48,FadeIn(note))
            self.cue(vo,.78,Indicate(blocks[1][1],color=RED,scale_factor=1.02))
        self.finish()

class S05(EpisodeScene):
    def construct(self):
        self.header('Open the recipe.')
        tree=VGroup(*[left(s,-6,1.25-i*.66,26,RED if i==0 else INK,6.4) for i,s in enumerate([
            'conny-explainer-video/','  SKILL.md','  defaults.json','  presets/ + references/','  scripts/','  assets/'])])
        paper=Rectangle(width=5.4,height=3.9,stroke_color=INK,stroke_width=2).move_to([3.4,-.15,0])
        contents=VGroup(left('name + description',1,.99,28,RED,4.7,True),left('WHEN TO USE',1,.49,18,GRAY),
                       left('1. Evidence\n2. Storyboard\n3. Design → render\n4. Review → deliver',1,-.72,28,INK,4.7))
        with self.say(0) as vo:
            self.cue(vo,0,FadeIn(tree[0]),FadeIn(tree[1]),Create(paper))
            self.cue(vo,.37,FadeIn(contents[0]),FadeIn(contents[1]))
            self.cue(vo,.70,FadeIn(contents[2]))
        with self.say(1) as vo:
            self.cue(vo,0,LaggedStart(*[FadeIn(t,shift=RIGHT*.1) for t in tree[2:]],lag_ratio=.2),run_time=1.1)
            self.cue(vo,.55,Create(line(-5.7,-1.75,-.3,-1.75,RED,3)))
            self.cue(vo,.79,Indicate(contents[2],color=RED,scale_factor=1.025))
        self.finish()

class S06(EpisodeScene):
    def construct(self):
        self.header('Origin needs evidence.')
        roles=VGroup(*[at(s,x,1.2,27,INK,3.7,True) for s,x in [('AUTHOR',-4),('FILE MANAGER',0),('INSTALLER',4)]])
        with self.say(0) as vo:
            self.cue(vo,0,FadeIn(roles[0]))
            self.cue(vo,.32,FadeIn(roles[1]))
            self.cue(vo,.65,FadeIn(roles[2]))
        count=at('26',-4,-.1,108,RED,bold=True)
        info=left('matching SKILL.md files',-2.3,.12,32,INK,8.5,True)
        match=left('shared folder  =  Google extension copy',-2.3,-.6,24,INK,8.5)
        evidence=VGroup(left('CONTENT MATCH',-6,-1.82,21,RED),left('verified by file hashes',-6,-2.19,21),left('INSTALLER IDENTITY',1.1,-1.82,21,GRAY),left('not established',1.1,-2.19,21))
        with self.say(1) as vo:
            self.cue(vo,0,FadeIn(count),FadeIn(info))
            self.cue(vo,.3,FadeIn(match),Create(line(-6,-1.27,6,-1.27)))
            self.cue(vo,.55,FadeIn(evidence[:2]))
            self.cue(vo,.74,FadeIn(evidence[2:]),roles[2].animate.set_color(GRAY))
        self.finish()

class S07(EpisodeScene):
    def construct(self):
        self.header('Useful for which job?')
        tasks=VGroup(*[card(a,b,x,1,w=3.6,h=1.35) for a,b,x in [('AWS','cloud projects',-4),('PYTHON','research',0),('VIDEO','explanations',4)]])
        skills=[folder('amazon-bedrock',-4,-.8,3.6),folder('python dependencies',0,-.8,3.6),folder('conny-explainer-video',4,-.8,3.6,RED)]
        with self.say(0) as vo:
            self.cue(vo,0,FadeIn(tasks[:2]))
            self.cue(vo,.2,FadeIn(skills[0]),Create(arrow([-4,-.12,0],[-4,.23,0])))
            self.cue(vo,.56,FadeIn(skills[1]),Create(arrow([0,-.12,0],[0,.23,0])))
        with self.say(1) as vo:
            self.cue(vo,0,FadeIn(tasks[2]),FadeIn(skills[2]),Create(arrow([4,-.12,0],[4,.23,0])))
            self.cue(vo,.48,FadeIn(at('Select by task, not by folder count.',0,-2.05,30,RED,12,True)))
            self.cue(vo,.8,Indicate(tasks[2],color=RED,scale_factor=1.03))
        self.finish()

class S08(EpisodeScene):
    def construct(self):
        self.header('One source. Three readers.')
        home=folder('~/.agents/skills/\nconny-explainer-video',-3.5,.08,5.2,RED)
        readers=[card(name,sub,4,y,w=3.6,h=1.2) for name,sub,y in [('Cursor','native discovery',1.35),('Codex','native discovery',-.14),('Claude Code','per-skill symlink',-1.63)]]
        joins=[arrow([-.7,.1,0],[2.1,y,0],RED if i<2 else GRAY) for i,y in enumerate([1.35,-.14,-1.63])]
        with self.say(0) as vo:
            self.cue(vo,0,FadeIn(home))
            self.cue(vo,.46,Create(joins[0]),FadeIn(readers[0]))
            self.cue(vo,.68,Create(joins[1]),FadeIn(readers[1]))
        with self.say(1) as vo:
            self.cue(vo,0,Create(joins[2]),FadeIn(readers[2]))
            self.cue(vo,.39,FadeIn(left('~/.claude/skills/\nconny-explainer-video → same files',-6,-1.63,22,GRAY,5.3)))
            self.cue(vo,.66,FadeIn(left('EDIT ONCE',-6,1.55,30,RED,bold=True)))
        self.finish()

class S09(EpisodeScene):
    def construct(self):
        self.header('Discovery is a test.')
        phases=[card(a,b,x,.7,w=3.6,h=1.75) for a,b,x in [('01 / FIND','skill appears',-4),('02 / INVOKE','brief applies defaults',0),('03 / RENDER','output inspected',4)]]
        with self.say(0) as vo:
            self.cue(vo,0,FadeIn(phases[0]))
            self.cue(vo,.42,FadeIn(phases[1]),Create(arrow([-2.1,.7,0],[-1.9,.7,0])))
        inv=VGroup(left('Codex CLI   $conny-explainer-video',-6,-1.0,24,INK,12),left('Cursor       / skill picker',-6,-1.5,24,INK,12),left('Claude Code /conny-explainer-video',-6,-2,24,INK,12))
        with self.say(1) as vo:
            self.cue(vo,0,FadeIn(phases[2]))
            self.cue(vo,.32,LaggedStart(*[FadeIn(m) for m in inv],lag_ratio=.15),run_time=1)
            self.cue(vo,.73,phases[2][0].animate.set_stroke(RED,3))
        self.finish()

def style_art(name,x,y,w=2.5,h=1.0):
    bg=Rectangle(width=w,height=h,fill_color=PAPER,fill_opacity=1,stroke_color=INK,stroke_width=1).move_to([x,y,0])
    g=VGroup(bg)
    if name=='swiss':
        g.add(left('Aa',x-w/2+.16,y,39,INK,bold=True),Square(.42,color=RED,fill_opacity=1).move_to([x+.74,y+.16,0]))
    elif name=='cassette':
        bg.set_fill('#1E2C24');g.add(left('READY_\n> 01',x-w/2+.2,y,25,'#9AD890'))
    elif name=='de-stijl':
        g.add(Rectangle(width=.9,height=.75,fill_color=RED,fill_opacity=1,stroke_width=0).move_to([x-.5,y+.12,0]),line(x+.12,y-.5,x+.12,y+.5,INK,6),line(x-w/2,y-.25,x+w/2,y-.25,INK,6))
    elif name=='bauhaus':
        g.add(Circle(.27,color='#E5BE3E',fill_opacity=1).move_to([x-.65,y,0]),Square(.45,color=RED,fill_opacity=1).move_to([x,y,0]),Triangle(color='#315897',fill_opacity=1).scale(.27).move_to([x+.65,y,0]))
    elif name=='nasa':
        g.add(left('SYS / 01',x-w/2+.18,y+.15,19,INK),line(x-w/2+.15,y-.22,x+w/2-.15,y-.22,'#A65B43',7))
    elif name=='rhine':
        g.add(Circle(.3,color='#BA9464',stroke_width=2).move_to([x-.6,y,0]),Circle(.21,color=GRAY,stroke_width=1).move_to([x-.6,y,0]),left('ARCHIVE\n01 / ACCESS',x-.1,y,17,INK))
    else:
        bg.set_fill('#343047');g.add(Square(.42,fill_color='#ECA47C',fill_opacity=1,stroke_width=0).move_to([x-.5,y,0]),Square(.42,fill_color='#79ACDD',fill_opacity=1,stroke_width=0).move_to([x+.5,y,0]))
    return g

class S10(EpisodeScene):
    def construct(self):
        self.header('Save a visual vocabulary.')
        names=[('swiss','Swiss'),('cassette','Cassette futurism'),('de-stijl','De Stijl'),('bauhaus','Bauhaus'),('nasa','NASA-punk'),('rhine','Rhine Lab'),('pixel','Pixel studio')]
        arts=VGroup()
        for i,(key,name) in enumerate(names):
            x=-4.8+(i%4)*3.2;y=.96-(i//4)*1.82
            arts.add(VGroup(style_art(key,x,y,2.8,1.1),at(name,x,y-.78,20,INK,2.9)))
        with self.say(0) as vo:
            self.cue(vo,0,FadeIn(arts[0]))
            self.cue(vo,.25,LaggedStart(*[FadeIn(g,shift=UP*.1) for g in arts[1:4]],lag_ratio=.18),run_time=1)
            self.cue(vo,.6,LaggedStart(*[FadeIn(g,shift=UP*.1) for g in arts[4:]],lag_ratio=.18),run_time=1)
        with self.say(1) as vo:
            self.cue(vo,0,arts[4][0][0].animate.set_stroke(RED,3),arts[5][0][0].animate.set_stroke(RED,3))
            self.cue(vo,.43,FadeIn(at('Palette → type → composition → motion',0,-2.2,26,RED,12,True)))
        self.finish()

class S11(EpisodeScene):
    def construct(self):
        self.header('Defaults carry the detail.')
        settings=[('STYLE','Swiss'),('DURATION','5 minutes'),('FRAME','1920 × 1080 / 30 fps'),('VOICE','English'),('CAPTIONS','中文 + English')]
        rows=VGroup(*[VGroup(left(k,-6,1.24-i*.68,22,GRAY),left(v,-2.3,1.24-i*.68,31,RED if i==1 else INK,8.4,True),line(-6,.88-i*.68,6,.88-i*.68,FAINT)) for i,(k,v) in enumerate(settings)])
        with self.say(0) as vo:
            self.cue(vo,0,LaggedStart(*[FadeIn(g,shift=RIGHT*.1) for g in rows],lag_ratio=.3),run_time=2.1)
            self.cue(vo,.65,Indicate(rows[4][1],color=RED,scale_factor=1.04))
        with self.say(1) as vo:
            self.cue(vo,.20,Transform(rows[1][1],left('2 minutes',-2.3,.56,31,RED,8.4,True)))
            self.cue(vo,.49,FadeIn(at('Current request overrides saved defaults.',0,-2.25,26,RED,12,True)))
        self.finish()

class S12(EpisodeScene):
    def construct(self):
        self.header('Make it. Review it. Reuse it.')
        prompt=VGroup(left('conny-explainer-video',-6,1.34,43,RED,12,True),left('Cursor skills / Swiss / 5 min / 中英字幕',-6,.64,30,INK,12))
        roles=VGroup(*[card(a,b,x,-.95,w=3.6,h=1.55) for a,b,x in [('DIRECTOR','facts + teaching',-4),('DESIGNER','frames + motion',0),('ENGINEER','audio + render',4)]])
        with self.say(0) as vo:
            self.cue(vo,0,FadeIn(prompt[0]))
            self.cue(vo,.42,FadeIn(prompt[1]),Create(line(-6,.13,6,.13,RED,3)))
        with self.say(1) as vo:
            self.cue(vo,0,FadeIn(roles[0]))
            self.cue(vo,.38,FadeIn(roles[1]))
            self.cue(vo,.65,FadeIn(roles[2]))
        with self.say(2) as vo:
            self.cue(vo,0,FadeIn(at('One editable library. A better next video.',0,-2.2,29,RED,12,True)))
        self.finish()
