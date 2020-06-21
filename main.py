from machine import Pin, SPI, deepsleep
import epaperdriver as epd
import connect
import urequests
import utime

sck = Pin(13)
miso = Pin(12)
mosi = Pin(14)
dc = Pin(27)
cs = Pin(15)
rst = Pin(26)
busy = Pin(25)
spi = SPI(2, baudrate=1000000, polarity=0, phase=0, sck=sck, miso=miso, mosi=mosi)

w = 400
h = 300

e = epd.EPD(spi, cs, dc, rst, busy, w, h)
e.init()

connect.wifi("SSID", "password")
print("Connecting...")
fb_b = buffer.Buffer(w, h)
fb_r = buffer.Buffer(w, h)

font12 = "./fonts/12.bin"
font17 = "./fonts/17.bin"


def icons(name):
    return "./icons/" + name + ".bmp"


def stringbuilder(device, limit):
    return "http://192.168.0.xxx:8086/query?db=weerstathome&q=SELECT%20waarde%20FROM%20%22wsex%22%20WHERE%20device=%27" + str(
        device) + "%27order%20by%20time%20desc%20LIMIT%20" + str(limit)


def get_value(device):
    return str(round(urequests.get(stringbuilder(device, 1)).json()["results"][0]["series"][0]["values"][0][1], 1))


try:
    print("Calling Api's")
    cet = urequests.get("http://api.timezonedb.com/v2.1/get-time-zone?key=OwnKey&format=json&by=position&lat=51.05&lng=3.6").json()
    datum = "-".join(cet["formatted"].split(" ")[0].split("-")[::-1])
    tijd = cet["formatted"].split(" ")[1][:5]
    epoch = 946684800
    dow = utime.localtime(int(cet["timestamp"]) - epoch)[6]
    dagen = ["Maandag", "Dinsdag", "Woensdag", "Donderdag", "Vrijdag", "Zaterdag", "Zondag"]

    result = urequests.get("http://weerlive.nl/api/json-data-10min.php?key=OwnKey&locatie=51.05,3.6").json()
    result = result["liveweer"][0]
    if result["windr"] == "Noord":
        result["windr"] = "N"

    # fixed left
    print("Fixed left")
    fb_b.display_string_at(3, 5, "Weer van", font12, 1)
    fb_b.display_string_at(3, 91, "Temp.", font12, 0)
    fb_b.display_string_at(3, 111, "gevoel", font12, 0)
    fb_r.display_string_at(68, 91, "Max", font12, 1)
    fb_r.display_string_at(68, 111, "Min", font12, 1)
    fb_b.display_string_at(3, 139, "Windricht.", font12, 1)
    fb_b.display_string_at(3, 159, "Windsnelh.", font12, 0)
    fb_r.display_string_at(42, 173, "% kans", font12, 1)
    fb_b.display_string_at(3, 187, "Vocht.", font12, 1)
    fb_b.display_string_at(3, 207, "Dauw", font12, 1)
    fb_r.display_string_at(68, 187, "Zon", font12, 1)
    fb_r.display_string_at(50, 207, "Regen", font12, 1)
    # fixed top
    print("Fixed top")
    fb_r.display_string_at(172, 5, "Vandaag", font12, 1)
    fb_b.display_string_at(245, 5, "Morgen", font12, 1)
    fb_r.display_string_at(307, 5, "Overmorgen", font12, 1)
    # fixed bottom
    print("Fixed bottom")
    fb_b.display_string_at(3, 235, "Zon Op", font12, 1)
    fb_b.display_string_at(3, 255, "Zon Onder", font12, 1)
    fb_b.display_string_at(177, 235, "Luchtdruk", font12, 1)
    fb_b.display_string_at(177, 255, "Zichtbaarheid", font12, 1)
    # fixed right
    print("Fixed right")
    fb_b.display_string_at(352, 88, "'C", font17)
    fb_b.display_string_at(352, 108, "'C", font17)
    fb_b.display_string_at(355, 156, "knt", font17)
    fb_b.display_string_at(355, 184, "%", font17)
    fb_b.display_string_at(352, 204, "'C", font17)
    fb_b.display_string_at(355, 232, "hPa", font17)
    fb_b.display_string_at(355, 252, "km", font17)
    # fixed lines
    print("Fixed lines")
    fb_b.draw_line(99, 88, 99, 227)
    fb_b.draw_line(170, 88, 170, 227)
    fb_b.draw_line(238, 88, 238, 227)
    fb_b.draw_line(306, 88, 306, 227)

    # col0
    print("Col0")
    fb_r.display_string_at(3, 23, dagen[dow], font12, 1)
    fb_b.display_string_at(3, 43, datum, font12, 1)
    fb_r.display_string_at(3, 75, result["samenv"], font12, 1)
    spaces = [i for i in range(len(result["verw"])) if result["verw"].startswith(" ", i)]
    space = [i for i in spaces if 35 < i < 45]
    if space:
        space = space[-1]
        fb_b.display_string_at(3, 272, result["verw"][:space], font12, 1)
        fb_b.display_string_at(3, 285, result["verw"][space + 1:], font12, 1)
    else:
        fb_b.display_string_at(3, 280, result["verw"], font12, 1)


    # col1
    print("Col1")
    fb_b.display_string_at(116, 5, tijd, font12, 1)
    fb_b.draw_bmp_at(105, 20, icons(result["image"]))
    fb_b.display_string_at(105, 88, get_value("Tws1"), font17, 1)
    fb_b.display_string_at(105, 108, result["gtemp"], font17, 1)
    fb_b.display_string_at(105, 136, result["windr"], font17, 1)
    fb_b.display_string_at(105, 156, result["windk"], font17, 1)
    fb_b.display_string_at(105, 184, get_value("Hws"), font17, 1)
    fb_b.display_string_at(105, 207, result["dauwp"], font17, 1)
    fb_r.display_string_at(90, 232, result["sup"], font17, 1)
    fb_r.display_string_at(90, 252, result["sunder"], font17, 1)

    # col2
    print("Col2")
    fb_r.draw_bmp_at(173, 20, icons(result["d0weer"]))
    fb_r.display_string_at(185, 88, result["d0tmax"], font17, 1)
    fb_r.display_string_at(185, 108, result["d0tmin"], font17, 1)
    fb_r.display_string_at(185, 136, result["d0windr"], font17, 1)
    fb_r.display_string_at(185, 156, result["d0windknp"], font17, 1)
    fb_r.display_string_at(185, 184, result["d0zon"], font17, 1)
    fb_r.display_string_at(185, 204, result["d0neerslag"], font17, 1)

    # col3
    print("Col3")
    fb_b.draw_bmp_at(241, 20, icons(result["d1weer"]))
    fb_b.display_string_at(253, 88, result["d1tmax"], font17, 1)
    fb_b.display_string_at(253, 108, result["d1tmin"], font17, 1)
    fb_b.display_string_at(253, 136, result["d1windr"], font17, 1)
    fb_b.display_string_at(253, 156, result["d1windknp"], font17, 1)
    fb_b.display_string_at(253, 184, result["d1zon"], font17, 1)
    fb_b.display_string_at(253, 204, result["d1neerslag"], font17, 1)

    # col4
    print("Col4")
    fb_r.draw_bmp_at(309, 20, icons(result["d2weer"]))
    fb_r.display_string_at(321, 88, result["d2tmax"], font17, 1)
    fb_r.display_string_at(321, 108, result["d2tmin"], font17, 1)
    fb_r.display_string_at(321, 136, result["d2windr"], font17, 1)
    fb_r.display_string_at(321, 156, result["d2windknp"], font17, 1)
    fb_r.display_string_at(321, 184, result["d2zon"], font17, 1)
    fb_r.display_string_at(321, 204, result["d2neerslag"], font17, 1)
    fb_r.display_string_at(264, 232, get_value("Pws"), font17, 0)
    fb_r.display_string_at(320, 252, result["zicht"], font17, 1)


    print("Drawing...")
    e.display_frame(fb_b, fb_r)
    print("Done")

    deepsleep(1000000)

except Exception as e:
    print(e)
    deepsleep(400000)
