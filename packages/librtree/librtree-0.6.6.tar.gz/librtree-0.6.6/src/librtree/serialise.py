import os

class Serialise:

    @classmethod
    def _serialise(cls, f, rmode, wmode, *arg, **kwarg):
        rn, wn = os.pipe()
        if os.fork():
            os.close(wn)
            try:
                rio = os.fdopen(rn, rmode)
                result = rio.read()
            finally:
                rio.close()
                os.wait()
        else:
            os.close(rn)
            try:
                wio = os.fdopen(wn, wmode)
                f(wio, *arg, **kwarg)
            finally:
                wio.close()
                os._exit(0)
        return result

    @classmethod
    def _serialise_text(cls, f, *arg, **kwarg):
        return cls._serialise(f, 'r', 'w', *arg, **kwarg)

    @classmethod
    def _serialise_binary(cls, f, *arg, **kwarg):
        return cls._serialise(f, 'rb', 'wb', *arg, **kwarg)
