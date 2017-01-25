#!/usr/bin/env python

#---------------------------------------
# IMPORTS
#---------------------------------------

import config
import csvdata
import features
import imp
import plot
import sys
import time
import warnings

warnings.filterwarnings("ignore")

#---------------------------------------
# FUNCTIONS
#---------------------------------------

def print_head(ds):
    print "showing first few lines of calculated features:"

    for i in range(5):
        print "    ", ds2.rows[i].raw

    print

#---------------------------------------
# ENTRY POINT
#---------------------------------------

if __name__ == "__main__":
    ds = csvdata.load("../data/EURUSD_UTC_Ticks_Bid_2015.01.01_2015.01.02.csv")
    ds2 = features.calc(ds)

    m = imp.load_source(config.MODEL, "models/" + config.MODEL + ".py")
    model = m.create_model(ds2)

    print

    it = 0
    t = 0.0
    last_t = time.time()
    update_timer = 0.0
    while it < config.TRAIN_ITERS/config.BATCH_SIZE:
        it += 1

        dt = time.time() - last_t
        last_t = time.time()

        t += dt

        model.train_once()

        mins  = int(t/60.0)
        hours = int(mins/60.0)
        mins -= hours*60
        secs  = int(t - mins*60)

        update_timer += dt
        if update_timer >= 0.1:
            sys.stdout.write("\r training [{:02d}:{:02d}:{:02d}, {}/{}] ... ".format(hours, mins, secs, it, config.TRAIN_ITERS/config.BATCH_SIZE))
            sys.stdout.flush()

            if config.TRAIN_TIME > 0 and t/60.0 > config.TRAIN_TIME:
                break

            update_timer = 0.0

        model.train_once()

    print

    if config.RESULTS == "plot":
        p = plot.Plot(ds)
        p.plot_ref()

        import features
        c = features.SMA(1)
        c.plot(p, ds2, 0, ds2.num_rows)

        p.show()
    else:
        raise Exception("unknown results method: " + config.RESULTS)
