
from krita import *

MENUTEXT = "Ten Brushes Add On"

class PREV_NEXT_BRUSH(Extension):
    def __init__(self, parent):
        super().__init__(parent)
        self.selectedPresets = []
        self.actionToIndex = {}



    def setup(self):
        self.reloadBrushes()

    
    def createActions(self, window):
    
        prevAction = window.createAction(
            "prevBrush", "Prev Brush", ""
        )
        nextAction = window.createAction(
            "nextBrush", "Next Brush", ""
        )
        
        prevAction.triggered.connect(self.prevBrush)
        nextAction.triggered.connect(self.nextBrush)
        
        menu_action = window.createAction(
            MENUTEXT,  MENUTEXT,
            "Tools/Scripts/" + MENUTEXT)
        menu = QMenu( "Ten Brushes Remove", window.qwindow())
        menu_action.setMenu(menu)
        
        
        reloadAction = window.createAction(
            "reloadBrushes", "Ten Brushes Prev && Next Reload",
            "Tools/Scripts/" + MENUTEXT
        )
        reloadAction.triggered.connect(self.reloadBrushes)
        
        for index, item in enumerate(['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']):
            action = window.createAction(
                "removeBrushes" + item,
                str(i18n("Remove Brush No.{num}")).format(num=item),
            "Tools/Scripts/" + MENUTEXT)
            action.triggered.connect(self.removeBrushes)
            self.actionToIndex[action.objectName()] = index;

        
    def reloadBrushes(self):
        self.selectedPresets = Application.readSetting("", "tenbrushes", "").split(',')
        window = Application.activeWindow()

        if (window and len(window.views()) > 0):
            window.views()[0].showFloatingMessage( "Ten Brushes reloaded for Prev & Next", Krita.instance().icon( "draw-freehand" ), 1000, 0 )
            
            
        
    def removeBrushes(self):
        # Make sure to reload presets
        self.selectedPresets = Application.readSetting("", "tenbrushes", "").split(',')
        
        presetIndex = self.actionToIndex[self.sender().objectName()]
        self.selectedPresets[presetIndex] = None
        
        presets = []
        
        realIndex = '1'

        for index, item in enumerate(['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']):
            if presetIndex == index:
                realIndex = item
            presets.append(self.selectedPresets[index])

        Application.writeSetting("", "tenbrushes", ','.join(map(str, presets)))
        
        window = Application.activeWindow()

        # Update Ten Brush plugin
        for extension in Krita.instance().extensions():
            if "tenbrushes.TenBrushesExtension" in str(extension):
                if "readSettings" in dir(extension):
                    extension.readSettings()
                    
                    if (window and len(window.views()) > 0):
                        window.views()[0].showFloatingMessage( "Ten Brushes No. " + str(realIndex) + " removed", Krita.instance().icon( "draw-freehand" ), 1000, 0 )



    def prevBrush(self):
        window = Application.activeWindow()

        if (window and len(window.views()) > 0):
            allPresets = Application.resources("preset")
            currentPreset = window.views()[0].currentBrushPreset().name()
            
            presetIndex = 10
            for i in range(10):
                if self.selectedPresets[i] == currentPreset:
                    presetIndex = i
                    break
                    
                    
            for i in range(presetIndex-1,-1,-1):
                if self.selectedPresets[i] and self.selectedPresets[i] in allPresets:
                    window.views()[0].setCurrentBrushPreset( allPresets[self.selectedPresets[i]] )
                    break

                


            
    def nextBrush(self):
        window = Application.activeWindow()

        if (window and len(window.views()) > 0):
            allPresets = Application.resources("preset")
            currentPreset = window.views()[0].currentBrushPreset().name()
            
            presetIndex = -1
            for i in range(10):
                if self.selectedPresets[i] == currentPreset:
                    presetIndex = i
                    break
                    
                    
            for i in range(presetIndex+1,10):
                if self.selectedPresets[i] and self.selectedPresets[i] in allPresets:
                    window.views()[0].setCurrentBrushPreset( allPresets[self.selectedPresets[i]] )
                    break
                




Krita.instance().addExtension(PREV_NEXT_BRUSH(Krita.instance()))

