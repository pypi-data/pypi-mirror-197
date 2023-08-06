import os

class Deserialise:

    @classmethod
    def _deserialise(cls, source, rmode, wmode, f, *arg, **kwarg):
        rn, wn = os.pipe()
        if os.fork():
            os.close(wn)
            try:
                rio = os.fdopen(rn, rmode)
                try:
                    result = f(rio, *arg, **kwarg)
                finally:
                    rio.close()
            finally:
                os.wait()
        else:
            os.close(rn)
            try:
                wio = os.fdopen(wn, wmode)
                wio.write(source)
                wio.close()
            finally:
                os._exit(0)
        return result

    @classmethod
    def _deserialise_text(cls, source, f, *arg, **kwarg):
        return cls._deserialise(source, 'r', 'w', f, *arg, **kwarg)

    @classmethod
    def _deserialise_binary(cls, source, f, *arg, **kwarg):
        return cls._deserialise(source, 'rb', 'wb', f, *arg, **kwarg)
