# * import block :
import tcod as libtcod


# * Main: 
def main():
# ** Initilize:
# *** varebls:
    screen_width = 80
    screen_height = 50

    xpos =1
    ypos =2
    colore =libtcod.green
    old_colore =libtcod.white

# *** console seting:
    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    libtcod.console_init_root(screen_width, screen_height, 'libtcod tutorial revised', False)

# ** main loop:
    while not libtcod.console_is_window_closed():
# *** rendrering:
        libtcod.console_set_default_foreground(0, colore)
        libtcod.console_put_char(0, xpos, ypos, '@', libtcod.BKGND_NONE)
        libtcod.console_flush()

        libtcod.console_set_default_foreground(0, old_colore)
        libtcod.console_put_char(0, xpos, ypos, '@', libtcod.BKGND_NONE)

# *** key handling:
        key = libtcod.console_check_for_keypress()

        if key.vk == libtcod.KEY_ESCAPE:
            return True
        if key.vk == libtcod.KEY_UP:
            ypos -=1
        if key.vk == libtcod.KEY_DOWN:
            ypos +=1
        if key.vk == libtcod.KEY_RIGHT:
            xpos +=1
        if key.vk == libtcod.KEY_LEFT:
            xpos -=1
        if key.vk == libtcod.KEY_SPACE:
            colore =+1

# * Main start point:
if __name__ == '__main__':
    main()
