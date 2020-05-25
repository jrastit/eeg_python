import matplotlib.pyplot as plt

from raw import Raw
from clientemulation import ClientEmulation
from server import Server

a_state = 0

raw = Raw("../react/web-media-player/db/music.sqlite3")

#ClientEmulation(raw)
Server(raw)
plt.show()
