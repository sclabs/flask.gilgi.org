import time
import tempfile
import pickle
import zlib
import os
from os.path import join, exists

import eveapi


class MyCacheHandler(object):
    def __init__(self, debug=False):
        self.debug = debug
        self.count = 0
        self.cache = {}
        self.tempdir = join(tempfile.gettempdir(), "eveapi")
        if not exists(self.tempdir):
            os.makedirs(self.tempdir)

    def log(self, what):
        if self.debug:
            print("[%d] %s" % (self.count, what))

    def retrieve(self, host, path, params):
        # eveapi asks if we have this request cached
        key = hash((host, path, frozenset(list(params.items()))))

        self.count += 1  # for logging

        # see if we have the requested page cached...
        cached = self.cache.get(key, None)
        if cached:
            cacheFile = None
            #print "'%s': retrieving from memory" % path
        else:
            # it wasn't cached in memory, but it might be on disk.
            cacheFile = join(self.tempdir, str(key) + ".cache")
            if exists(cacheFile):
                self.log("%s: retrieving from disk" % path)
                f = open(cacheFile, "rb")
                cached = self.cache[key] = pickle.loads(zlib.decompress(f.read()))
                f.close()

        if cached:
            # check if the cached doc is fresh enough
            if time.time() < cached[0]:
                self.log("%s: returning cached document" % path)
                return cached[1]  # return the cached XML doc

            # it's stale. purge it.
            self.log("%s: cache expired, purging!" % path)
            del self.cache[key]
            if cacheFile:
                os.remove(cacheFile)

        self.log("%s: not cached, fetching from server..." % path)
        # we didn't get a cache hit so return None to indicate that the data
        # should be requested from the server.
        return None

    def store(self, host, path, params, doc, obj):
        # eveapi is asking us to cache an item
        key = hash((host, path, frozenset(list(params.items()))))

        cachedFor = obj.cachedUntil - obj.currentTime
        if cachedFor:
            self.log("%s: cached (%d seconds)" % (path, cachedFor))

            cachedUntil = time.time() + cachedFor

            # store in memory
            cached = self.cache[key] = (cachedUntil, doc)

            # store in cache folder
            cacheFile = join(self.tempdir, str(key) + ".cache")
            f = open(cacheFile, "wb")
            f.write(zlib.compress(pickle.dumps(cached, -1)))
            f.close()


api = eveapi.EVEAPIConnection(cacheHandler=MyCacheHandler(debug=True))


order_state_map = {
    0: 'Open or Active',
    1: 'Closed',
    2: 'Expired or Fulfilled',
    3: 'Cancelled',
    4: 'Pending',
    5: 'Character Deleted'
}
bid_map = {
    0: 'selling',
    1: 'buying'
}


def get_first_char_ctx(keyID, vCode):
    auth = api.auth(keyID=keyID, vCode=vCode)
    result = auth.account.Characters()
    return auth.character(result.characters[0].characterID)

    
def get_balance(keyID, vCode):
    me = get_first_char_ctx(keyID, vCode)
    return "{:,.2f}".format(me.AccountBalance().accounts[0].balance)

    
def get_skill_in_training(keyID, vCode):
    me = get_first_char_ctx(keyID, vCode)
    st_result = me.SkillInTraining()
    if st_result.skillInTraining:
        tn_result = api.eve.TypeName(ids=str(st_result.trainingTypeID))
        skill_name = tn_result.types[0].typeName
        return 'currently training %s to level %s, finishes %s' % (skill_name, st_result.trainingToLevel,
                                                                   time.asctime(time.gmtime(st_result.trainingEndTime)))
    else:
        return 'no skill in training!'

        
def get_skill_queue(keyID, vCode):
    me = get_first_char_ctx(keyID, vCode)
    sq_result = me.SkillQueue()
    skill_ids = [str(skill.typeID) for skill in sq_result.skillqueue]
    tn_result = api.eve.TypeName(ids=','.join(skill_ids))
    skill_names = [type.typeName for type in tn_result.types]
    return ['%s to level %s finishes %s' % (skill_names[i], sq_result.skillqueue[i].level,
                                            time.asctime(time.gmtime(sq_result.skillqueue[i].endTime)))
            for i in range(len(skill_ids))]

            
def get_orders(keyID, vCode):
    me = get_first_char_ctx(keyID, vCode)
    mo_result = me.MarketOrders()
    item_ids = [str(order.typeID) for order in mo_result.orders]
    tn_result = api.eve.TypeName(ids=','.join(item_ids))
    item_names = [type.typeName for type in tn_result.types]
    return ['%s %s/%s %s @ %s ISK, %s' % (bid_map[mo_result.orders[i].bid], mo_result.orders[i].volRemaining,
                                            mo_result.orders[i].volEntered, item_names[i],
                                            "{:,.2f}".format(mo_result.orders[i].price),
                                            order_state_map[mo_result.orders[i].orderState])
            for i in range(len(item_ids))]
