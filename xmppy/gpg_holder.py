import logging
import gnupg
import os

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
#handler = logging.FileHandler('gpg_handler.log')
handler2 = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)
handler2.setFormatter(formatter)
# log.addHandler(handler)
log.addHandler(handler2)


class Gpg:
    def __init__(self, gnupghome=''):
        self.gnupghome = gnupghome
        log.info('New session.\n')
        if len(gnupghome) == 0:
            log.debug("Path not specified. Setting default gnupg directory.")
            log.debug('Creating gnupg instance in {}'.format(
                "default directory."))
            self.gpg = gnupg.GPG()
            return None
        else:
            log.debug("Setting {} as gnupg directory".format(gnupghome))
            if os.path.exists(gnupghome):
                log.debug('Creating gnupg instance in {}'.format(gnupghome))
                self.gpg = gnupg.GPG(gnupghome=gnupghome)
                return None
            else:
                log.warning(
                    "path {} does not exist. Trying to create...".format(gnupghome))
                try:
                    log.info("Creating dir in {}".format(gnupghome))
                    os.mkdir(gnupghome)
                    log.debug('Creating gnupg instance in {}'.format(gnupghome))
                    self.gpg = gnupg.GPG(gnupghome=gnupghome)
                    return None
                except Exception as e:
                    log.error('Cant create dir {}'.format(e))
                    return None

    def list_keys(self, **kwargs):
        #TODO: multisearch
        try:
            keys = self.gpg.list_keys()
            if len(keys) == 0:
                log.warning("gpg database is empty.")
                return [], 'Empty database'
            set1 = set(keys[1].keys())
            set2 = set(kwargs.keys())
            if set2-set1 != set():
                log.warning('Wrong keyword {}'.format(set2-set1))
                return [], "Wrong keywords {}".format(set2-set1)
            elif kwargs == {}:
                log.debug('Returning all keys.')
                return keys, None
            else:
                results = []
                log.debug('Searching {} in keys.'.format(kwargs))
                for _dict in keys:
                    for keyword in kwargs:
                        if type(_dict[keyword]) == type(list()):
                            for value in _dict[keyword]:
                                if kwargs[keyword] in value:
                                    log.debug(
                                        'Match in {}.'.format(_dict[keyword]))
                                    if not _dict in results:
                                        results.append(_dict)
                        else:
                            if kwargs[keyword] in _dict[keyword]:
                                log.debug(
                                    'Match in {}.'.format(_dict[keyword]))
                                if not _dict in results:
                                    results.append(_dict)
                log.debug("Returning {} matches.".format(len(results)))
                return results, None
        except Exception as e:
            log.error("Error in list_keys(self)", e)
            return [], 'Error in Gpg.list_keys(self, **kwargs)'

    def encrypt(self, message, sign=None, file=None, **kwargs):
        # TODO FILE ENCRYPT
        try:
            log.debug("autosearch enabled.")
            recipients = []
            encrypted = []
            errors = ''
            log.debug("Searching recipients.")
            keys, error = self.list_keys(**kwargs)
            if error != None:
                log.error(error)
                return [], error
            for key in keys:
                if key['ownertrust'] == '-':
                    log.warning(
                        "Key {} is untrusted. Forcing...".format(key['uids']))
                _encrypted = self.gpg.encrypt(
                    str(message), key['keyid'], sign=sign, always_trust=True)
                encrypted.append(_encrypted.data.decode())
                if not _encrypted.ok:
                    errors += _encrypted.stderr + '\n'
            return encrypted, errors
        except Exception as e:
            log.error("Error in self.encrypt()", e)
            return [], "Error in self.encrypt()"

    def decrypt(self):
        pass

    def sign(self):
        pass

    def symmetric_encrypt(self):
        pass

    def symmetric_decrypt(self):
        pass
