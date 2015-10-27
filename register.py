import direct.directbase.DirectStart
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
 
from panda3d.core import TextNode
 
# Add some text
bk_text = "Register"
textObject = OnscreenText(text = bk_text, pos = (-0.48,0.1), 
scale = 0.07,fg=(1,0.5,0.5,1),align=TextNode.ACenter,mayChange=1)
 
# Callback function to set  text
def setText():
        bk_text = "Register"
        textObject.setText(bk_text)
 
def clearText():
    b.enterText("")

# Add button
#b = DirectButton(text = ("OK", "click!", "rolling over", "disabled"), scale=.05, command=setText, text_roll=90)

b = DirectButton(pos = (-0.51, 0, -0.3), text = ("Register", "Register", "Register", "disabled"), scale = 0.05, command=setText)
b.resetFrameSize()

user = OnscreenText(text="User", style=1, fg=(1,1,1,1), pos=(-0.65,0), align=TextNode.ARight, scale = .07)
password = OnscreenText(text="Password", style=1, fg=(1,1,1,1), pos=(-0.65,-0.1), align=TextNode.ARight, scale = .07)
repassword = OnscreenText(text="Re-enter Password", style=1, fg=(1,1,1,1), pos=(-0.65,-0.2), align=TextNode.ARight, scale = .07)

b = DirectEntry(pos = (-0.60, 0, 0), text = "", scale = .05, command=setText, initialText="", numLines = 1, focus = 1, focusInCommand = clearText)
b = DirectEntry(pos = (-0.60, 0, -0.1), text = "", scale = .05, command=setText, initialText="", numLines = 1, focus = 1, focusInCommand = clearText, obscured = 1)
b = DirectEntry(pos = (-0.60, 0, -0.2), text = "", scale = .05, command=setText, initialText="", numLines = 1, focus = 1, focusInCommand = clearText, obscured = 1)
 
# Run the tutorial
run()