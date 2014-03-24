red,green,blue,alpha=1,1,1,0.5
font="Data Control"

function text_cairo(cr,font,font_slant,font_face,
font_size,x,y,text,red,green,blue,alpha)
	cairo_select_font_face (cr, font, font_slant, font_face);
	cairo_set_font_size (cr, font_size)
	cairo_move_to (cr,x,y)
	cairo_show_text (cr,text)
	cairo_set_source_rgba (cr,red,green,blue,alpha)
	cairo_stroke (cr)
end--text_cairo

function line_cairo(cr,line_width,line_cap,x, y,relx,rely,red,green,blue,alpha)
	cairo_set_line_width (cr,line_width)
	cairo_set_line_cap  (cr, line_cap)
	cairo_move_to (cr,x,y)
	cairo_rel_line_to (cr,relx,rely)
	cairo_set_source_rgba (cr,red,green,blue,alpha)
	cairo_stroke (cr)
end--line_cairo


function draw_date(cr, i)
	local function add_gap(a)
					if a~=0 then return 80 else 
					return 0 end
				end--add_gap
  local font_size=30
  local font_slant=CAIRO_FONT_SLANT_NORMAL
  local font_face=CAIRO_FONT_WEIGHT_NORMAL
	local gap=add_gap(i)
  local x=gap+170+150*i
  local y=50
	t = os.date("*t")
	t.day = t.day + i
	local text = os.date("%a %d",os.time(t))
	text_cairo(cr,font,font_slant,font_face,
font_size,x,y,text,red,green,blue,alpha)
end--draw_date

function draw_line(cr, i)
	local line_width=1
	local line_cap=CAIRO_LINE_CAP_SQUARE
	local x=220+150*i
	local y=60
	local relx=0
	local rely=320
	line_cairo(cr, line_width, line_cap, x, y,relx,rely,red,green,blue,alpha)
end--draw_line

function dyna_clock(cr)
	local curr_time=t.hour+(t.min/100)
	local line_width=1
	local line_cap=CAIRO_LINE_CAP_SQUARE
	local x=71
	local y=60+(320/24)*curr_time
	local relx=298
	local rely=0
	local red,green,blue,aplha=0.6,0,0,0.4
	line_cairo(cr, line_width, line_cap, x, y,relx,rely,red,green,blue,alpha)
end--dyna_clock

function draw_hour_line(cr,i)
	local line_width=1
	local line_cap=CAIRO_LINE_CAP_SQUARE
	local x=49
	local y=60+(320/6)*i
	local relx=20
	local rely=0
	line_cairo(cr, line_width, line_cap, x, y,relx,rely,red,green,blue,alpha)
end--draw_hour_line

function draw_hour_name(cr,i)
  local font_size=10
  local font_slant=CAIRO_FONT_SLANT_NORMAL
  local font_face=CAIRO_FONT_WEIGHT_NORMAL
	local x=20
  local y=63+(320/6)*i
	local text=("%02d.00"):format(0+i*4)
	text_cairo(cr,font,font_slant,font_face,
font_size,x,y,text,red,green,blue,alpha)
end--draw_hour_name

function draw_db(cr, i)
	--[[local function stamp_to_int(timestamp)
					time_int = date("%H", timestamp)
					return time_int
				end]]
	local loc = os.getenv("HOME")
	local db = sqlite3.open(string.format("%s/ITCKit/db/itckitdb", loc))
		for class in db:nrows("SELECT * FROM Class WHERE DATE(Class.start_timestamp) = date('now', '+"..i.." days')") do--for
		---draw_startind(cr, ...)
  	print(class.start_timestamp)
		--print(stamp_to_int(class.start_timestamp))
		end--for
end

function draw_startind(cr, start_time)

end
require 'cairo'
require 'lsqlite3'

function conky_main()
  if conky_window==nil then return end
	local cs=cairo_xlib_surface_create(conky_window.display,conky_window.drawable,conky_window.visual, conky_window.width,conky_window.height)
  local cr = cairo_create(cs)

  local updates=conky_parse('${updates}')
	update_num=tonumber(updates)

	if update_num>5 then
		draw_line(cr,-1)
    for i=0,4,1 do
    draw_date(cr,i)
		draw_line(cr,i+1)
		draw_db(cr,i)
    end--for
		for i=0,6,1 do
		draw_hour_line(cr,i)
		draw_hour_name(cr,i)
		end--for
		dyna_clock(cr)
  end-- if updates>5
  cairo_destroy(cr)
  cairo_surface_destroy(cs)
  cr=nil
end-- main
