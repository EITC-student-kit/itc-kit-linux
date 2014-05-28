----Common Settings----
font = "Ubuntu"
--loc = string.format("%s/ITCKit",os.getenv("HOME"))
loc = string.format("%s/.itc-kit",os.getenv("HOME"))
-----------------------
function text_cairo (cr, font_size, x, y, text)
	----Text Common Settings----
	local font_slant = CAIRO_FONT_SLANT_NORMAL
	local font_face = CAIRO_FONT_WEIGHT_NORMAL
	---------------------
	cairo_select_font_face (cr, font, font_slant, font_face);
	cairo_set_font_size (cr, font_size)
	cairo_move_to (cr, x, y)
	cairo_show_text (cr, text)
	cairo_set_source_rgba (cr, rgb_to_r_g_b(settings_array[5], 0.5))
	cairo_stroke (cr)
end--text_cairo

function line_cairo (cr, line_width, x, y, relx, rely)
	----Line Common Settings----
	local line_cap = CAIRO_LINE_CAP_SQUARE
	---------------------
	cairo_set_line_width (cr, line_width)
	cairo_set_line_cap (cr, line_cap)
	cairo_move_to (cr, x, y)
	cairo_rel_line_to (cr, relx, rely)
	cairo_set_source_rgba (cr, rgb_to_r_g_b(settings_array[5], 0.5))
	cairo_stroke (cr)
end--line_cairo

function rgb_to_r_g_b(colour,alpha)
    return ((colour / 0x10000) % 0x100) / 255., ((colour / 0x100) % 0x100) / 255., (colour % 0x100) / 255., alpha
end--rgb_to_r_g_b

function draw_date (cr, i)
	local function add_gap (a)
					if a ~= 0 then return 80 else 
					return 0 end
				end--add_gap
  local font_size = 30
	local gap = add_gap (i)
  local x = align() + gap + 170 + 150 * i
  local y = 50
	t = os.date ("*t")
	t.day = t.day + i
	local text = os.date ("%a %d", os.time(t))
	text_cairo (cr, font_size, x, y, text)
end--draw_date

function draw_line (cr, i)
	local line_width = 1
	local x = align() + 220 + 150 * i
	local y = 60
	local relx = 0
	local rely = 450
	line_cairo (cr, line_width, x, y, relx, rely)
end--draw_line

function dyna_clock (cr)
	local curr_time = t.hour + t.min / 60
	local line_width = 1
	local line_cap = CAIRO_LINE_CAP_SQUARE
	local x = align() + 71
	local y = 60 + (450 / 16) * (curr_time - 6)
	local relx = 298
	local rely = 0
	local red, green, blue, alpha=0.6,0,0,0.4

	cairo_set_line_width (cr, line_width)
	cairo_set_line_cap (cr, line_cap)
	cairo_move_to (cr, x, y)
	cairo_rel_line_to (cr, relx, rely)
	cairo_set_source_rgba (cr, red, green, blue, alpha)
	cairo_stroke (cr)
end--dyna_clock

function draw_hour_line (cr, i)
	function mini_hour_line (cr, line_width, x, y, rely)
		local y = y + (450 / 16)
		local relx = -10
		line_cairo (cr, line_width, x, y, relx, rely)
	end
	local line_width = 1
	local x = align() + 69
	local y = 60 + (450 / 8) * i
	local relx = -20
	local rely = 0
	mini_hour_line (cr, line_width, x, y, rely)
	line_cairo (cr, line_width, x, y, relx, rely)
end--draw_hour_line

function draw_hour_name (cr, i)
  local font_size = 15
	local x = align() + 10
  local y = 64 + (450 / 8) * i
	local text = ("%02d.00") :format (6 + i * 2)
	text_cairo (cr, font_size, x, y, text)
end--draw_hour_name

--ToDo Wrap this function in a protected call (pcall) for when the database is locked

function draw_db (cr, i)
	local function stamp_to_int(timestamp)
					local time_hour = tonumber(string.sub(timestamp, -8, -7))
					local time_minute = tonumber(string.sub(timestamp, -5, -4))
					local time_int = time_hour + time_minute / 60
					return time_int
	end--stamp_to_int

    local db = sqlite3.open(string.format("%s/itckitdb", loc))

	for class in db:nrows("SELECT * FROM Class WHERE DATE(Class.start_timestamp) = date('now', '+"..i.." days') AND user_attend == 1") do--for
		if i == 0 then
	    	----Main----
			db_draw_main_Name (cr, class.subject_name, stamp_to_int(class.start_timestamp), i)
			db_draw_main_startind (cr, stamp_to_int(class.start_timestamp))
			db_draw_main_lengthind (cr, stamp_to_int(class.start_timestamp), stamp_to_int(class.end_timestamp))
			db_draw_main_otherName (cr, stamp_to_int(class.start_timestamp), class.start_timestamp, class.end_timestamp, class.classroom)
			db_draw_main_other2Name (cr, class.academician, class.class_type, stamp_to_int(class.start_timestamp))
			db_draw_main_other3Name (cr, class.attending_groups, stamp_to_int(class.start_timestamp))
		else
		    ----Other----
			db_draw_other_startind (cr, stamp_to_int(class.start_timestamp), i)
			db_draw_other_lengthind (cr, stamp_to_int(class.start_timestamp), stamp_to_int(class.end_timestamp), i)
			db_draw_other_Name (cr, class.subject_name, stamp_to_int(class.start_timestamp), i)
			db_draw_other_otherName (cr, class.start_timestamp, class.end_timestamp, class.classroom, stamp_to_int(class.start_timestamp), i)
			db_draw_other_other2Name (cr, class.academician, class.class_type, stamp_to_int(class.start_timestamp), i)
			db_draw_other_other3Name (cr, class.attending_groups, stamp_to_int(class.start_timestamp), i)
		end--if
	end--for
end--draw_db
----Main----
function db_draw_main_startind (cr, start_time)
	local line_width = 1
	local x = align() + 74
	local y = 60 + (450 / 16) * (start_time - 6)
	local relx = 150
	local rely = 0
	line_cairo (cr, line_width, x, y, relx, rely)
end--db_draw_main_startind

function db_draw_main_lengthind (cr, start_time, end_time)
	local line_width = 1
	local x = align() + 74
	local y = 61 + (450 / 16) * (start_time - 6)
	local relx = 0
	local rely = (450/16) * (end_time - start_time) - 1
	line_cairo (cr, line_width, x, y, relx, rely)
end--db_draw_main_lengthind

function db_draw_main_Name (cr, class_name, start_time)
	local font_size = 12
	local x = align() + 75
  local y = 58 + (450 / 16) * (start_time - 6)
	local text = class_name
	text_cairo (cr, font_size, x, y, text)
end--db_draw_main_Name

function db_draw_main_otherName (cr, start_time, start_stamp, end_stamp, class)
	local font_size = 15
	local x = align() + 76
  local y = 73 + (450 / 16) * (start_time - 6)
	local text = string.format("%s - %s Room:%s", string.sub(start_stamp, -8, -4), string.sub(end_stamp, -8, -4), class)
	text_cairo (cr, font_size, x, y, text)
end--db_draw_main_otherName

function db_draw_main_other2Name (cr, academician, class_type, start_time)
	local font_size = 12
	local x = align() + 76
  local y = 84 + (450 / 16) * (start_time - 6)
	local text = string.format("%s - %s", academician, class_type)
	text_cairo (cr, font_size, x, y, text)
end--db_draw_main_other2Name

function db_draw_main_other3Name (cr, groups, start_time)
	local font_size = 12
	local x = align() + 76
  local y = 95 + (450 / 16) * (start_time - 6)
	local text = string.format("Groups: %s" ,groups)
	text_cairo (cr, font_size, x, y, text)
end--db_draw_main_other3Name
----Other----
function db_draw_other_startind (cr, start_time, i)
	local line_width = 1
	local x = align() + 374 + 150 * (i - 1)
	local y = 60 + (450 / 16) * (start_time - 6)
	local relx = 145
	local rely = 0
	line_cairo (cr, line_width, x, y, relx, rely)
end--db_draw_other_startind

function db_draw_other_lengthind (cr, start_time, end_time, i)
	local line_width = 1
	local x = align() + 374 + 150 * (i - 1)
	local y = 61 + (450 / 16) * (start_time - 6)
	local relx = 0
	local rely = (450/16) * (end_time - start_time) - 1
	line_cairo (cr, line_width, x, y, relx, rely)
end--db_draw_other_lengthind

function db_draw_other_Name (cr, class_name, start_time, i)
	local function other_Name_resize (string)
					local re_string = ""
					for word in string.gmatch (string, "%a+") do
						if string.len (re_string) < 20 then
							re_string = string.format ("%s %s" ,re_string ,word)
						else
							re_string = string.format ("%s %s." ,re_string ,string.sub (word, 0, 1))
						end--if
					end--for
					return re_string
				end--other_Name_resize
	local font_size = 10
	local x = align() + 374 + 150 * (i - 1)
  local y = 58 + (450 / 16) * (start_time - 6)
	local text = other_Name_resize (class_name)
	text_cairo (cr, font_size, x, y, text)
end--db_draw_other_Name

function db_draw_other_otherName (cr, start_stamp, end_stamp, class, start_time, i)
	local font_size = 12
	local x = align() + 376 + 150 * (i - 1)
  local y = 72 + (450 / 16) * (start_time - 6)
	local text = string.format("%s - %s Room:%s", string.sub(start_stamp, -8, -4), string.sub(end_stamp, -8, -4), class)
	text_cairo (cr, font_size, x, y, text)
end--db_draw_other_otherName

function db_draw_other_other2Name (cr, academician, class_type, start_time, i)
	local font_size = 12
	local x = align() + 376 + 150 * (i - 1)
  local y = 84 + (450 / 16) * (start_time - 6)
	local text = string.format("%s - %s", academician, class_type)
	text_cairo (cr, font_size, x, y, text)
end--db_draw_other_other2Name

function db_draw_other_other3Name (cr, groups, start_time, i)
	local font_size = 12
	local x = align() + 376 + 150 * (i - 1)
  local y = 95 + (450 / 16) * (start_time - 6)
	local text = string.format("Groups: %s", groups)
	text_cairo (cr, font_size, x, y, text)
end--db_draw_other_other3Name

function settings()
	
	local settings = io.open(string.format("%s/settings", loc), "r")
	settings_array = {}
	local settings_string = settings:read("*all")
	for word in string.gmatch(settings_string, "%w+") do
		table.insert(settings_array, word)
	end
	settings:close()
end--settings

function set_width(days)
	local width = 400 + (days - 1) * 150
end--set_width

function align()
	return 80 + (7 - settings_array[7]) * 150
end
------------
require 'cairo'
require 'lsqlite3'
------------
function conky_main ()
  if conky_window == nil then return end
	local cs = cairo_xlib_surface_create(conky_window.display, conky_window.drawable, conky_window.visual, conky_window.width, conky_window.height)
  local cr = cairo_create (cs)
	
  local updates = conky_parse ('${updates}')
	local update_num = tonumber (updates)
	
	if update_num > 1 then
		settings()
		draw_line (cr, -1)
    for i = 0, tonumber(settings_array[7])-1, 1 do
    draw_date (cr, i)
		draw_line (cr, i + 1)
		draw_db (cr, i)
    end--for
		for i = 0, 8, 1 do
		draw_hour_line (cr, i)
		draw_hour_name (cr, i)
		end--for
		if t.hour >= 6 and t.hour <= 21 then
		dyna_clock (cr)
		end--if t.hour
  end-- if update_num > 1
  cairo_destroy (cr)
  cairo_surface_destroy (cs)
  cr = nil
end-- main
