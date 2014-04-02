----Common Settings----
red, green, blue, alpha=1,1,1,0.5
font = "Ubuntu"--"Data Control"
-----------------------
function text_cairo (cr, font_size, x, y, text, red, green, blue, alpha)
	----Text Common Settings----
	local font_slant = CAIRO_FONT_SLANT_NORMAL
	local font_face = CAIRO_FONT_WEIGHT_NORMAL
	---------------------
	cairo_select_font_face (cr, font, font_slant, font_face);
	cairo_set_font_size (cr, font_size)
	cairo_move_to (cr, x, y)
	cairo_show_text (cr, text)
	cairo_set_source_rgba (cr, red, green, blue, alpha)
	cairo_stroke (cr)
end--text_cairo

function line_cairo (cr, line_width, x, y, relx, rely, red, green, blue, alpha)
	----Line Common Settings----
	local line_cap = CAIRO_LINE_CAP_SQUARE
	---------------------
	cairo_set_line_width (cr, line_width)
	cairo_set_line_cap (cr, line_cap)
	cairo_move_to (cr, x, y)
	cairo_rel_line_to (cr, relx, rely)
	cairo_set_source_rgba (cr, red, green, blue, alpha)
	cairo_stroke (cr)
end--line_cairo


function draw_date (cr, i)
	local function add_gap (a)
					if a ~= 0 then return 80 else 
					return 0 end
				end--add_gap
  local font_size = 30
	local gap = add_gap (i)
  local x = gap + 170 + 150 * i
  local y = 50
	t = os.date ("*t")
	t.day = t.day + i
	local text = os.date ("%a %d", os.time(t))
	text_cairo (cr, font_size, x, y, text, red, green, blue, alpha)
end--draw_date

function draw_line (cr, i)
	local line_width = 1
	local x = 220 + 150 * i
	local y = 60
	local relx = 0
	local rely = 450
	line_cairo (cr, line_width, x, y, relx, rely, red, green, blue, alpha)
end--draw_line

function dyna_clock (cr)
	local curr_time = t.hour + t.min / 60
	local line_width = 1
	local line_cap = CAIRO_LINE_CAP_SQUARE
	local x = 71
	local y = 60 + (450 / 16) * (curr_time - 6)
	local relx = 298
	local rely = 0
	local red, green , blue, aplha=0.6,0,0,0.4
	line_cairo (cr, line_width, x, y, relx, rely, red, green, blue, alpha)
end--dyna_clock

function draw_hour_line (cr, i)
	function mini_hour_line (cr, line_width, x, y, rely, red, green, blue, alpha)
		local y_add = y + (450 / 16)
		local relx = -10
		line_cairo (cr, line_width, x, y_add, relx, rely, red, green, blue, alpha)
	end
	local line_width = 1
	local x = 69
	local y = 60 + (450 / 8) * i
	local relx = -20
	local rely = 0
	mini_hour_line (cr, line_width, x, y, rely, red, green, blue, alpha)
	line_cairo (cr, line_width, x, y, relx, rely, red, green, blue, alpha)
end--draw_hour_line

function draw_hour_name (cr, i)
  local font_size = 15
	local x = 10
  local y = 64 + (450 / 8) * i
	local text = ("%02d.00") :format (6 + i * 2)
	text_cairo (cr, font_size, x, y, text, red, green, blue, alpha)
end--draw_hour_name

function draw_db (cr, i)
	local function stamp_to_int(timestamp)
					time_hour = tonumber(string.sub(timestamp, -8, -7))
					time_minute = tonumber(string.sub(timestamp, -5, -4))
					time_int = time_hour + time_minute / 60
					return time_int
				end--stamp_to_int
	local loc = os.getenv("HOME")
	local db = sqlite3.open(string.format("%s/ITCKit/db/itckitdb", loc))
		for class in db:nrows("SELECT * FROM Class WHERE DATE(Class.start_timestamp) = date('now', '+"..i.." days') AND user_attends == 1") do--for
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
	local x = 74
	local y = 60 + (450 / 16) * (start_time - 6)
	local relx = 150
	local rely = 0
	line_cairo (cr, line_width, x, y, relx, rely, red, green, blue, alpha)
end--db_draw_main_startind

function db_draw_main_lengthind (cr, start_time, end_time)
	local line_width = 1
	local x = 74
	local y = 61 + (450 / 16) * (start_time - 6)
	local relx = 0
	local rely = (450/16) * (end_time - start_time) - 1
	line_cairo (cr, line_width, x, y, relx, rely, red, green, blue, alpha)
end--db_draw_main_lengthind

function db_draw_main_Name (cr, class_name, start_time)
	local font_size = 12
	local x = 75
  local y = 58 + (450 / 16) * (start_time - 6)
	local text = class_name
	text_cairo (cr, font_size, x, y, text, red, green, blue, alpha)
end--db_draw_main_Name

function db_draw_main_otherName (cr, start_time, start_stamp, end_stamp, class)
	local font_size = 15
	local x = 76
  local y = 73 + (450 / 16) * (start_time - 6)
	local text = string.format("%s - %s Room:%s", string.sub(start_stamp, -8, -4), string.sub(end_stamp, -8, -4), class)
	text_cairo (cr, font_size, x, y, text, red, green, blue, alpha)
end--db_draw_main_otherName

function db_draw_main_other2Name (cr, academician, class_type, start_time)
	local font_size = 12
	local x = 76
  local y = 84 + (450 / 16) * (start_time - 6)
	local text = string.format("%s - %s", academician, class_type)
	text_cairo (cr, font_size, x, y, text, red, green, blue, alpha)
end--db_draw_main_other2Name

function db_draw_main_other3Name (cr, groups, start_time)
	local font_size = 12
	local x = 76
  local y = 95 + (450 / 16) * (start_time - 6)
	local text = string.format("Groups: %s" ,groups)
	text_cairo (cr, font_size, x, y, text, red, green, blue, alpha)
end--db_draw_main_other3Name
----Other----
function db_draw_other_startind (cr, start_time, i)
	local line_width = 1
	local x = 374 + 150 * (i - 1)
	local y = 60 + (450 / 16) * (start_time - 6)
	local relx = 145
	local rely = 0
	line_cairo (cr, line_width, x, y, relx, rely, red, green, blue, alpha)
end--db_draw_other_startind

function db_draw_other_lengthind (cr, start_time, end_time, i)
	local line_width = 1
	local x = 374 + 150 * (i - 1)
	local y = 61 + (450 / 16) * (start_time - 6)
	local relx = 0
	local rely = (450/16) * (end_time - start_time) - 1
	line_cairo (cr, line_width, x, y, relx, rely, red, green, blue, alpha)
end--db_draw_other_lengthind

function db_draw_other_Name (cr, class_name, start_time, i)
	local function other_Name_resize (string)
					re_string = ""
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
	local x = 374 + 150 * (i - 1)
  local y = 58 + (450 / 16) * (start_time - 6)
	local text = other_Name_resize (class_name)
	text_cairo (cr, font_size, x, y, text, red, green, blue, alpha)
end--db_draw_other_Name

function db_draw_other_otherName (cr, start_stamp, end_stamp, class, start_time, i)
	local font_size = 12
	local x = 376 + 150 * (i - 1)
  local y = 72 + (450 / 16) * (start_time - 6)
	local text = string.format("%s - %s Room:%s", string.sub(start_stamp, -8, -4), string.sub(end_stamp, -8, -4), class)
	text_cairo (cr, font_size, x, y, text, red, green, blue, alpha)
end--db_draw_other_otherName

function db_draw_other_other2Name (cr, academician, class_type, start_time, i)
	local font_size = 12
	local x = 376 + 150 * (i - 1)
  local y = 84 + (450 / 16) * (start_time - 6)
	local text = string.format("%s - %s", academician, class_type)
	text_cairo (cr, font_size, x, y, text, red, green, blue, alpha)
end--db_draw_other_other2Name

function db_draw_other_other3Name (cr, groups, start_time, i)
	local font_size = 12
	local x = 376 + 150 * (i - 1)
  local y = 95 + (450 / 16) * (start_time - 6)
	local text = string.format("Groups: %s", groups)
	text_cairo (cr, font_size, x, y, text, red, green, blue, alpha)
end--db_draw_other_other3Name
------------
require 'cairo'
require 'lsqlite3'

function conky_main ()
  if conky_window == nil then return end
	local cs = cairo_xlib_surface_create(conky_window.display, conky_window.drawable, conky_window.visual, conky_window.width, conky_window.height)
  local cr = cairo_create (cs)

  local updates = conky_parse ('${updates}')
	update_num = tonumber (updates)

	if update_num > 1 then
		draw_line (cr, -1)
    for i = 0, 2, 1 do
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
		end--if
  end-- if updates>5
  cairo_destroy (cr)
  cairo_surface_destroy (cs)
  cr = nil
end-- main
