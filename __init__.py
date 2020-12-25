import os
import sys
from xml.dom.minidom import parse

import pygame
from pygame.locals import *

from pyso.map import Map

def _safe_get(path:str):
    if path.startswith('std:'):
        p=os.path.join(os.path._getfullpathname('.'), path.replace('std:',''))
        p=sys.executable.replace('python.exe','')+'Lib\\pyso\\'
    else:
        p=path
    return p

class Game():
    def __init__(self, script=None, data_path='data', screen_size=[800,600], window_title='isometric-render'):
        if not script:
            try:
                script = parse(open(
                    os.path.join(
                        'script',
                        'map.xml'
                    )
                ))
            except:
                script = parse(open(_safe_get('std:')+'script\\map.xml'))
        pygame.init()
        self.screen = pygame.display.set_mode(screen_size) # TODO add fullscreen
        pygame.display.set_caption(window_title)
        try:
            self.background=pygame.image.load(
                os.path.join(
                    data_path,
                    'images',
                    'blueSky.png'
                )
            )
        except:
            self.background=pygame.image.load(_safe_get('std:')+'data\\images\\blueSky.png')
        font=pygame.font.SysFont('Courier New', 15)
        self.font = font.render('Press Enter to continue or Esc to exit.', 1, (255,255,255))
        self.map = Map(self.screen)
        try:
            self.map.LoadTiles(open('data/scripts/tiles.xml'))
            self.map.makeMap(open('script/map.xml'))
        except:
            self.map.LoadTiles(open(_safe_get('std:')+'data\\scripts\\tiles.xml'))
            self.map.makeMap(open(_safe_get('std:')+'script\\map.xml'))
    
    def run(self, player, items=None, *args):
        while True:
            self.screen.blit(self.background,(0,0))
            if False:
                for p in player.get_players():
                    p.action()
                for p in items[0].get_items():
                    p.anim()

            for evt in pygame.event.get():
                if evt.type == QUIT:
                    exit()
                else:
                    self.event_handler(evt)

            self.map.show()

            pygame.display.flip()
    
    def event_handler(self, key, *args):
        return key

print('thank u for using pyso! ~camillettss')
