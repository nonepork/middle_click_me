#!/usr/bin/env python3

from flask import Flask, request, abort, send_file, redirect, make_response, render_template
from io import BytesIO
import logging
import requests
import re

app = Flask(__name__)

ua_patterns = ['discordbot', '+https://discordapp.com', 'electron', 'discord', 'firefox/38']

image_links = "https://cdn.discordapp.com/attachments/1128712115415429283/1128721762780197016/ezgif-1-95707042df.gif"

MEMES = [

    # Rick roll
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",

    # Thunder Cross Split Attack
    "https://www.reddit.com/r/YouFellForItFool/comments/cjlngm/you_fell_for_it_fool/",

    # Steamed Hams
    "https://www.youtube.com/watch?v=4jXEuIHY9ic",

    # Curb your enthusiasm
    "https://www.youtube.com/watch?v=X-KwYX2u8e4",

    # The Spanish Inquisition
    "https://www.youtube.com/watch?v=sAn7baRbhx4",

    # Jebaited
    "https://www.youtube.com/watch?v=d1YBv2mWll0",

    # Get Stickbugged
    "https://www.youtube.com/watch?v=fC7oUOUEEi4",
    
    # Guts Man's Ass
    "https://www.youtube.com/watch?v=DFtZ0SbWTrg",
]


# Crappy way to detect if we're getting indexed by the Discord web crawler for embedding
def is_embed():
    ua_string = request.user_agent.string.lower()

    logging.warn(ua_string)

    for pattern in ua_patterns:
        if pattern.lower() in ua_string.lower():
            return True

    return False


@app.route('/')
def index():
    return "Hello World"


# CDN Regex

CDN_REGEX = re.compile("""([^{}|\\^\[\]`<>#;\/?:@&=+$,]{1,50}\/)([^{}|\\^\[\]`<>#;\/?:@&=+$,]{1,50}\/)([^{}|\\^\[\]`<>#;\/?:@&=+$,]{1,50})""")

@app.route('/coolpicture.gif')
def barepath():
    return discord_image()

def discord_image():

    # We're being embedded, send normal content
    if is_embed():
        dresp = requests.get(image_links)

        if dresp.status_code == 404:
            return abort(404)


        elif dresp.status_code != 200:
            return abort(401)

        # 10 mb stream limit
        try:
            if int(dresp.headers['content-length']) >= 1e7:
                return abort(403)
        except:
            return abort(501)

        content = BytesIO(dresp.content)

        resp = make_response(send_file(content, mimetype=dresp.headers["content-type"]))

        resp.headers["connection"] = "keep-alive"

        resp.headers["vary"] = "User-Agent, Content-Encoding"

        return resp

        # resp = make_response("", 308)
        # resp.mimetype = "image/png"

        # resp.headers["Location"] = f"https://cdn.discordapp.com/attachments/{cdn_content}"

        # return resp

    # User opened in browser
    else:
        # NEVER GONNA GIVE YOU UP! NEVER GONNA LET YOU DOWN!!

        try:
            meme_url = MEMES[0]
        except:
            abort(401)

        else:
            return redirect(meme_url)
