import direct.directbase.DirectStart
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
 
from panda3d.core import TextNode
 
# Add some text
bk_text = "Login"
textObject = OnscreenText(text = bk_text, pos = (-0.525,0.1), 
scale = 0.07,fg=(1,0.5,0.5,1),align=TextNode.ACenter,mayChange=1)
 
# Callback function to set  text
def setText():
        bk_text = "Login"
        textObject.setText(bk_text)
 
def clearText():
    b.enterText("")

# Add button
#b = DirectButton(text = ("OK", "click!", "rolling over", "disabled"), scale=.05, command=setText, text_roll=90)
b = DirectButton(pos = (-0.543, 0, -0.2), text = ("Login", "Login", "Login", "disabled"), scale = 0.05, command=setText)
b = DirectButton(pos = (-0.35, 0, -0.2), text = ("Register", "Register", "Register", "disabled"), scale = 0.05, command=setText)
b.resetFrameSize()
b = DirectEntry(pos = (-0.60, 0, 0), text = "", scale = .05, command=setText, initialText="", numLines = 1, focus = 1, focusInCommand = clearText)
b = DirectEntry(pos = (-0.60, 0, -0.1), text = "", scale = .05, command=setText, initialText="", numLines = 1, focus = 1, focusInCommand = clearText, obscured = 1)
 
# Run the tutorial
run()