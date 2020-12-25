import pygame
import os, sys
from xml.dom.minidom import parse

def _safe_get(path:str):
    if path.startswith('std:'):
        p=os.path.join(os.path._getfullpathname('.'), path.replace('std:',''))
        p=sys.executable.replace('python.exe','')+'Lib\\pyso\\'
    else:
        p=path
    return p

class Map():
    def __init__(self, screen):
        self.screen = screen
        self._tiles = {}
        self.map = []
        self.heights = []
    
    def LoadTiles(self, arch='data/script/tiles.xml'):
        tilesArch = parse(arch)
        totTiles = tilesArch.getElementsByTagName('tile')
        for tile in totTiles:
            try:
                self._tiles[tile.childNodes[0].nodeValue] = pygame.image.load(os.path.join('data', 'images', tile.childNodes[0].nodeValue+'.png'))
            except:
                self._tiles[tile.childNodes[0].nodeValue] = pygame.image.load(_safe_get('std:')+'data\\images\\'+ tile.childNodes[0].nodeValue+'.png')
            self._tiles[tile.childNodes[0].nodeValue].convert()
    
    def makeMap(self, script):
        script=parse(script)
        for line in script.getElementsByTagName('line'):
            mapLine = []
            mapHeight = []
            for column in line.getElementsByTagName('column'):
                mapLine.append(column.childNodes[0].nodeName)
                mapHeight.append(column.childNodes[0].attributes['h'].value)
            self.map.append(mapLine)
            self.heights.append(mapHeight)
    
    def show(self, sprite=None, items=None):
        x=20
        y=10
        startX = 0
        startY = 0
        big = high = 0
        posX = posY = -1
        scrollMapX = 0
        scrollMapY = 0
        if sprite:
            scrollMapX = sprite.scrollMapX
            scrollMapY = sprite.scrollMapY
        for line in self.map[scrollMapY:]:
            posY += 1
            posX = -1
            if 380 - (posY*x)+(posX*x) < -20 :
                break
            for tile in line[scrollMapX:]:
                posX += 1
                if int(self.heights[posY+scrollMapY][posX+scrollMapX]) > 1:
                    for elevPos in range(int(self.heights[posY+scrollMapY][posX+scrollMapX])-1):
                        self.screen.blit(self._tiles['baseDirt'], (380 - (posY*x)+(posX*x), 180+(posY*y)+(posX*y)-(20*(int(elevPos)))))
                    high -= 20*int(int(self.heights[posY+scrollMapY][posX+scrollMapX])-1)
                if not 380 - (posY * x) + (posX * x) > 760 - (posY * 19):
                    self.screen.blit(self._tiles[tile.split('.')[0]], (380 - (posY * x) + (posX * x), 180 + (posY * y) + (posX * y)+high))
                    if sprite:
                        if posX + scrollMapX == sprite.pos[0] and posY + scrollMapY == sprite.pos[1]:
                            self.screen.blit(sprite.spriteActual, (380 - (posY * x) + ((posX) * x), 180 + (posY * y) + ((posX) * y) - 20 + high))
                high=0