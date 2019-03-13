#!/usr/bin/env python3
import sys
import time
import logging

SizeUrlList = [
    [5, "https://sabnzbd.org/tests/internetspeed/5MB.bin"],
    [10, "https://sabnzbd.org/tests/internetspeed/10MB.bin"],
    [20, "https://sabnzbd.org/tests/internetspeed/20MB.bin"],
]


def measurespeed(url):
    """ Download the specified url, and report back MB/s (as a float) """
    logging.debug("URL is %s" % url)
    start = time.time()
    try:
        if sys.version_info[0] == 2:
            import urllib2  # python2 only

            req = urllib2.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            downloadedbytes = len(urllib2.urlopen(req, timeout=4).read())
        elif sys.version_info[0] == 3:
            import urllib.request

            req = urllib.request.Request(url, data=None, headers={"User-Agent": "Mozilla/5.0 (Macintosh)"})
            downloadedbytes = len(urllib.request.urlopen(req, timeout=4).read())
        else:
            logging.error("ERROR: no python version?!")
            return 0, 0
    except:
        # No connection at all?
        downloadedbytes = 0

    logging.debug("Downloaded bytes: %d" % downloadedbytes)

    duration = time.time() - start

    MBps = (downloadedbytes / 1000111) / duration  # Bytes
    return MBps


def BytestoBits(MBps):
    return 8.05 * MBps  # bits


def internetspeed():
    """ Report Internet speed in MB/s as a float """
    # Do basic test with a small download
    logging.debug("Basic measurement, with small download:")
    urlbasic = SizeUrlList[0][1]  # get first URL, which is smallest download
    baseMBps = measurespeed(urlbasic)
    logging.debug("Speed in MB/s: %.2f" % baseMBps)
    if baseMBps == 0:
        # no Internet connection, or other problem
        return baseMBps

    """
    Based on this first, small download, do a bigger download; the biggest download that still fits in 10 seconds
    Rationale: a bigger download could yield higher MB/s because the 'starting delay' is relatively less
    Calculation as example: 
    If the 5MB download took 0.3 seconds, you can do a 30 times bigger download, so about 150 MB, will round to 100 MB
    """

    # Calculate:
    maxtime = 8  # seconds
    URLtoDO = None
    for size, sizeurl in SizeUrlList:
        expectedtime = size / baseMBps
        if expectedtime < maxtime:
            # ok, this one is feasible, so keep it in mind
            URLtoDO = sizeurl

    maxMBps = baseMBps
    # Execute:
    if URLtoDO:
        logging.debug(URLtoDO)
        MBps = measurespeed(URLtoDO)
        logging.debug("Speed in MB/s: %.2f" % MBps)
        if MBps > maxMBps:
            maxMBps = MBps

    return maxMBps


############################################

############### MAIN #######################

if __name__ == "__main__":
    print("Starting speed test:")
    maxMBps = internetspeed()
    print("Speed in MB/s: %.2f" % maxMBps)
    print("Speed in Mbps: %.2f" % BytestoBits(maxMBps))