# Copyright info-beamer.com

import json, signal
import ctypes
libc = ctypes.CDLL('libc.so.6')
from subprocess import Popen, PIPE
from itertools import count

def roundup(v, r):
    return (v + r-1) & ~(r-1)

class Detector(object):
    def __init__(self, width, height):
        self._w = roundup(width, 16)
        self._h = roundup(height, 16)
        self.start_detector()

    @property
    def width(self):
        return self._w

    @property
    def height(self):
        return self._h

    @property
    def raw_size(self):
        return self._w * self._h * 3

    def start_detector(self):
        self._detector = Popen([
            'face_detect', str(self._w), str(self._h)
        ], stdin=PIPE, stdout=PIPE, bufsize=0)

    def raw(self, raw, threshold=65):
        self._detector.stdin.write(raw)
        self._detector.stdin.flush()
        num_faces = int(self._detector.stdout.readline())
        faces = []
        for i in xrange(num_faces):
            face = json.loads(self._detector.stdout.readline())
            if face['confidence'] >= threshold:
                faces.append(face)
        return faces

    def im(self, im):
        w, h = im.size
        if w != self._w or h != self._h:
            im = im.resize((self._w, self._h))
        if im.mode != 'RGB':
            raise ValueError("invalid image mode")
        return self.raw(im.tobytes())

    def cam_loop(self,
        show_preview=False, vflip=True, threshold=65
    ):
        def set_deathsignal():
            PR_SET_PDEATHSIG = 1
            # logread will be killed if the parent process quits
            libc.prctl(PR_SET_PDEATHSIG, signal.SIGKILL, 0, 0, 0)

        cmd = [
            'raspivid',
            '-w', str(self.width),
            '-h', str(self.height),
            '-rf', 'rgb',
            '-r', '-',
            '-t', '0',
        ]

        if vflip:
            cmd.extend([
                '-vf', 
            ])

        if show_preview:
            cmd.extend([
                '-p', '0,0,%d,%d' % (self.width, self.height),
                '-op', '128',
                '--verbose',
            ])
        else:
            cmd.extend([
                '-n',
            ])

        cam = Popen(
            cmd,
            stdout=PIPE, preexec_fn=set_deathsignal, close_fds=True
        )
        for i in count():
            image = cam.stdout.read(self.raw_size)
            yield self.raw(image, threshold)

    def stop(self):
        self._detector.kill()
