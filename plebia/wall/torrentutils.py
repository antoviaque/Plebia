#
# Copyright (C) 2011 Xavier Antoviaque <xavier@antoviaque.org>
#
# This software's license gives you freedom; you can copy, convey,
# propagate, redistribute and/or modify this program under the terms of
# the GNU Affero General Public License (AGPL) as published by the Free
# Software Foundation (FSF), either version 3 of the License, or (at your
# option) any later version of the AGPL published by the FSF.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero
# General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program in a file in the toplevel directory called
# "AGPLv3".  If not, see <http://www.gnu.org/licenses/>.
#

# Includes ##########################################################

from plebia.wall.models import Torrent

from lxml.html import soupparser
from lxml.cssselect import CSSSelector

import re
import mechanize
from time import gmtime, strftime

# mechanize #########################################################

cookies = mechanize.CookieJar()
opener = mechanize.build_opener(mechanize.HTTPCookieProcessor(cookies))
opener.addheaders = [("User-agent", "Mozilla/5.0 (compatible; Plebia/0.1)")]
mechanize.install_opener(opener)

# Helpers - Finding torrents ########################################

def get_torrent_by_search(search_string):
    torrent = Torrent()
    html_result = submit_form("http://torrentz.com/", search_string)

    # First check if any torrent was found at all
    if(html_result is None or re.search("Could not match your exact query", html_result)):
        return None
    
    # Get the list of torrents results
    sane_text = sanitize_text(html_result)
    root = soupparser.fromstring(sane_text)
    sel = CSSSelector(".results dl")
    element = sel(root)
    if element is None:
        return None
    else:
        # Build the torrent object
        torrent.hash = element[0].cssselect("dt a")[0].get("href")[1:]
        torrent.seeds = int(element[0].cssselect("dd .u")[0].text_content().translate(None, ','))
        torrent.peers = int(element[0].cssselect("dd .d")[0].text_content().translate(None, ','))
        if torrent.hash is None or torrent.seeds is None or torrent.seeds <= 0:
            return None
        else:
            return torrent


def submit_form(url, text):
    import httplib

    try:
        br = mechanize.Browser()
        br.open(url)

        # Debug - show every request in log
        curr_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        print '%s: %s => %s' % (curr_time, url, text)

        br.select_form(nr=0)
        br["f"] = text
        response = br.submit()
        html_result = response.get_data()
    except httplib.BadStatusLine:
        html_result = None

    return html_result

def sanitize_text(text):
    '''Remove non-string characters from text'''

    sane_text = u''

    # HTML NULL entity
    text = text.replace('&#0', '')

    for c in text:
        # Make sure it's not a control character
        if ord(c) >= 32 and ord(c) <= 126:
            sane_text += c

    return sane_text

