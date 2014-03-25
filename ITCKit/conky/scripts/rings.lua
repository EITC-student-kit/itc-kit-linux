--[[
Clock Rings by Linux Mint (2011) reEdited by despot77

This script draws percentage meters as rings, and also draws clock hands if you want! It is fully customisable; all options are described in the script. This script is based off a combination of my clock.lua script and my rings.lua script.

IMPORTANT: if you are using the 'cpu' function, it will cause a segmentation fault if it tries to draw a ring straight away. The if statement on line 145 uses a delay to make sure that this doesn't happen. It calculates the length of the delay by the number of updates since Conky started. Generally, a value of 5s is long enough, so if you update Conky every 1s, use update_num>5 in that if statement (the default). If you only update Conky every 2s, you should change it to update_num>3; conversely if you update Conky every 0.5s, you should use update_num>10. ALSO, if you change your Conky, is it best to use "killall conky; conky" to update it, otherwise the update_num will not be reset and you will get an error.

To call this script in Conky, use the following (assuming that you save this script to ~/scripts/rings.lua):
    lua_load ~/scripts/clock_rings.lua
    lua_draw_hook_pre clock_rings
    
Changelog:
+ v1.0 -- Original release (30.09.2009)
   v1.1p -- Jpope edit londonali1010 (05.10.2009)
   2011mint -- reEdit despot77 (18.02.2011)
*v StatRings -- Edit JVats (14.03.2014) 
]]

settings_table = {
    {
        -- Edit this table to customise your rings.
        -- You can create more rings simply by adding more elements to settings_table.
        -- "name" is the type of stat to display; you can choose from 'cpu', 'memperc', 'fs_used_perc', 'battery_used_perc'.
        ac_type='Productive',
        -- "max" is the maximum value of the ring. If the Conky variable outputs a percentage, use 100.
        max=100,
        -- "bg_colour" is the colour of the base ring.
        bg_colour=0x00A000,
        -- "bg_alpha" is the alpha value of the base ring.
        bg_alpha=0.1,
        -- "fg_colour" is the colour of the indicator part of the ring.
        fg_colour=0x00A000,
        -- "fg_alpha" is the alpha value of the indicator part of the ring.
        fg_alpha=0.5,
        -- "x" and "y" are the x and y coordinates of the centre of the ring, relative to the top left corner of the Conky window.
        x=60, y=75,
        -- "radius" is the radius of the ring.
        radius=50,
        -- "thickness" is the thickness of the ring, centred around the radius.
        thickness=5,
        -- "start_angle" is the starting angle of the ring, in degrees, clockwise from top. Value can be either positive or negative.
        start_angle=0,
        -- "end_angle" is the ending angle of the ring, in degrees, clockwise from top. Value can be either positive or negative, but must be larger than start_angle.
        end_angle=360
    },
    {
        ac_type='Neutral',
        max=100,
        bg_colour=0xffffff,
        bg_alpha=0.1,
        fg_colour=0xA0A0A0,
        fg_alpha=0.5,
        x=170, y=75,
        radius=50,
        thickness=5,
        start_angle=0,
        end_angle=360
    },
    {
        ac_type='Counterproductive',
        max=100,
        bg_colour=0xA00000,
        bg_alpha=0.1,
        fg_colour=0xA00000,
        fg_alpha=0.5,
        x=280, y=75,
        radius=50,
        thickness=5,
        start_angle=0,
        end_angle=360
    },
}

-- Use these settings to define the origin and extent of your clock.

require 'cairo'
require 'lsqlite3'

function rgb_to_r_g_b(colour,alpha)
    return ((colour / 0x10000) % 0x100) / 255., ((colour / 0x100) % 0x100) / 255., (colour % 0x100) / 255., alpha
end--rgb_to_r_g_b

function draw_ring(cr,t,pt)
    local w,h=conky_window.width,conky_window.height
    
    local xc,yc,ring_r,ring_w,sa,ea=pt['x'],pt['y'],pt['radius'],pt['thickness'],pt['start_angle'],pt['end_angle']
    local bgc, bga, fgc, fga=pt['bg_colour'], pt['bg_alpha'], pt['fg_colour'], pt['fg_alpha']

    local angle_0=sa*(2*math.pi/360)-math.pi/2
    local angle_f=ea*(2*math.pi/360)-math.pi/2
    local t_arc=t*(angle_f-angle_0)

    -- Draw background ring

    cairo_arc(cr,xc,yc,ring_r,angle_0,angle_f)
    cairo_set_source_rgba(cr,rgb_to_r_g_b(bgc,bga))
    cairo_set_line_width(cr,ring_w)
    cairo_stroke(cr)
    
    -- Draw indicator ring

    cairo_arc(cr,xc,yc,ring_r,angle_0,angle_0+t_arc)
    cairo_set_source_rgba(cr,rgb_to_r_g_b(fgc,fga))
    cairo_stroke(cr)        
end--draw_ring
 
function draw_precent(cr, pct, pt)
	local function round (number)
		if math.floor(number) >= 0.5 then
			number = math.ceil(number) 
		else
			number = math.floor(number)
		end
	return number
	end
	local font = "Ubuntu"
	local font_slant = CAIRO_FONT_SLANT_NORMAL
	local font_face = CAIRO_FONT_WEIGHT_NORMAL
	local font_size = 30
	local x, y = pt['x'] - 30, pt['y'] + 10
	local text = string.format("%s%%", round(pct * 100))

	cairo_select_font_face (cr, font, font_slant, font_face);
	cairo_set_font_size (cr, font_size)
	cairo_move_to (cr, x, y)
	cairo_show_text (cr, text)
	cairo_set_source_rgba (cr, rgb_to_r_g_b(pt['fg_colour'],pt['fg_alpha']))
	cairo_stroke (cr)	
end
function conky_clock_rings()
    local function setup_rings(cr,pt)
        local ac_type=''
        local value=0
        local spent_sum=0
				local total_sum=0

        ac_type=pt['ac_type']
				
        local loc = os.getenv("HOME")
				local db = sqlite3.open(string.format("%s/ITCKit/db/itckitdb", loc))
				for ac_sum in db:nrows("SELECT * FROM Activity WHERE activity_type LIKE '"..ac_type.."'") do
					spent_sum=spent_sum+ac_sum.spent_time
				end--for
				for ac_total_sum in db:nrows("SELECT * FROM Activity") do
					total_sum=total_sum+ac_total_sum.spent_time
				end--for
				pct=spent_sum/total_sum
        draw_ring(cr, pct,pt)
				draw_precent(cr, pct, pt)
    end--setup_rings
    
    -- Check that Conky has been running for at least 5s

    if conky_window==nil then return end
    local cs=cairo_xlib_surface_create(conky_window.display,conky_window.drawable,conky_window.visual, conky_window.width,conky_window.height)
    
    local cr=cairo_create(cs)    
    
    local updates=conky_parse('${updates}')
    update_num=tonumber(updates)
    
    if update_num>1 then
        for i in pairs(settings_table) do
            setup_rings(cr,settings_table[i])
        end--for
    end--if
end--conky_clock_rings
