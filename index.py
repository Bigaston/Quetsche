from bottle import get, run, template, response, static_file, abort
import datetime
import mimetypes

config = __import__("config")
audio = __import__("audio")

@get('/rss')
def send_rss():
  base_rss = open("./basic_rss.xml", "r", encoding="utf8").read()

  audioFiles = audio.get_all_audio()

  response.set_header("content-type", "text/xml")
  return template(base_rss, {
    "config": config,
    "build_date": datetime.datetime.today().strftime("%a, %d %b %Y %H:%M:%S +0200"),
    "episodes": audioFiles
  })

@get("/img/<slug>")
def get_episode_image(slug):
  audioInfo = audio.get_one_audio(slug + ".mp3")

  if audioInfo == None:
    abort(404, "No episode called " + slug)

  print(audioInfo["data"]["artwork"])

  # TODO : Trouver un fix propre
  response.set_header("content-type", 'image/jpeg')
  return audioInfo["data"]["artwork"].first.data

  

@get("/static/<file:path>")
def send_static(file):
  return static_file(file, "./static")

run(host='localhost', port=8080, debug=True, reloader=True)